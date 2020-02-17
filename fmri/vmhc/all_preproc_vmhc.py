# This code uses nilearn.image.clean_img to clean the rs-fmri data
# and conducts a Regional homogeneity analysis (Asym template) for each subject

# Set up Python modules
import os
from nilearn import image as img
from nilearn import plotting as plot
import pandas as pd
import glob
from subprocess import call
import subprocess


"""

The first part of the code uses nilearn.image.clean_img to 
detrend, low- and high-pass filter,remove confounds, and standardize
rs-fmri data from afis project (fmriprep has been already done)

"""

#Define path
path = sorted(glob.iglob('/nashome3/ipruotsa/afis_children/derivatives/fmriprep/**/func'))
path_vmhc = '/nashome3/ipruotsa/afis_children/derivatives/vmhc/'

for fname in path :
    path_folder = os.path.realpath(fname)
    path_name, folder_name = os.path.split(fname)
    dirname = os.path.basename(path_name) 

    if dirname.startswith('sub') : # only subject folders
        os.chdir(fname) # change current working directory
        print(os.getcwd()) #print current working directory 

        # skip the subjects who already has img.clean_img done
        path_clean_file = path_vmhc + dirname + "/" + dirname + "_task-rest_space-MNI152NLin6Sym_clean.nii.gz"
        if os.path.isfile(path_clean_file) :
            continue 
        else :    
            confound = glob.glob('*-confounds_regressors.tsv')
            func = glob.glob('*space-MNI152NLin6Sym_desc-preproc_bold.nii.gz')
            mask = glob.glob('*space-MNI152NLin6Sym_desc-brain_mask.nii.gz')
            func = ''.join(func)
            mask = ''.join(mask)

            # Read confounds -file (Delimiter is \t --> tsv is a tab-separated spreadsheet)
            confound_df = pd.read_csv(fname + '/'+ confound[0], delimiter='\t')

            # select confound variables: (Check Parkes et al. 2018)
            # first select variables that are marked as motion_outliers
            # criteria in this study FD > 0.5 and DVARS > 2
            confound_outlier = confound_df.columns.values.tolist()
            confound_outlier = [k for k in confound_outlier if 'motion_outlier' in k]

            # select other confound variables
            confound_vars = ['csf', 'csf_derivative1', 'csf_power2', 'csf_derivative1_power2', 'white_matter', 'white_matter_derivative1', 'white_matter_power2', 'white_matter_derivative1_power2', 'global_signal', 'global_signal_derivative1', 'global_signal_derivative1_power2', 'global_signal_power2', 'trans_x', 'trans_x_derivative1', 'trans_x_derivative1_power2', 'trans_x_power2', 'trans_y', 'trans_y_derivative1', 'trans_y_power2', 'trans_y_derivative1_power2', 'trans_z', 'trans_z_derivative1', 'trans_z_power2', 'trans_z_derivative1_power2', 'rot_x', 'rot_x_derivative1', 'rot_x_power2', 'rot_x_derivative1_power2', 'rot_y', 'rot_y_derivative1', 'rot_y_power2', 'rot_y_derivative1_power2', 'rot_z', 'rot_z_derivative1', 'rot_z_power2', 'rot_z_derivative1_power2']

            confound_allvars = confound_vars + confound_outlier
            confound_df = confound_df[confound_allvars]
            confound_df.fillna(0, inplace=True) #Replace Nan with value 0

            # load functional image
            func_img = img.load_img(func) 

            # Change confounds to matrix (confirm matrix with confounds_matrix.shape)
            confounds_matrix = confound_df.values

           # Define high_pass and low_pass values
            high_pass = 0.008
            low_pass = 0.08

            # Clean
            clean_img = img.clean_img(func_img, confounds=confounds_matrix, detrend=True, standardize=True, low_pass=low_pass, high_pass=high_pass, t_r=2.61, mask_img=mask, ensure_finite=True )

        #Create new subject-directory in the vmhc-directory
        new_folder = os.path.join(path_vmhc,dirname)
        os.mkdir(new_folder)
        clean_file = new_folder + '/' + dirname + '_task-rest_space-MNI152NLin6Sym_clean.nii.gz'
        # Save to nii.gz
        clean_img.to_filename(clean_file)



########################################################

"""

The second part of the code creates a group mask
from the masks produced in fmriprep 
(...MNI152NLin6Sym_desc-brain_mask.nii.gz)

"""
#Create group mask from asymmetric brain masks

# Define mask, path to directory and subject labels 
mask_sym = '_task-rest_space-MNI152NLin6Sym_desc-brain_mask.nii.gz' # maskname after sub-label
path_fmriprep='/nashome3/ipruotsa/afis_children/derivatives/fmriprep/'
subjects = '/nashome3/ipruotsa/afis_children/sourcedata/tutkittavat_fmri.txt' #subject labels
subject_names = open(subjects,'r')

fsl_command = ""
for index, subject_tag  in enumerate(subject_names) :
    subject_tag = subject_tag.strip()
    mask_dest = "/nashome3/ipruotsa/afis_children/derivatives/vmhc/group_mask_sym.nii.gz" #group file name and destination
    if not index:
        mask_command = "fslmaths " + path_fmriprep + subject_tag + "/func/" + subject_tag + mask_sym + " "
        fsl_command += mask_command # for the first iteration -mul not included
    else :
        mask_command = "-mul " + path_fmriprep + subject_tag + "/func/" + subject_tag + mask_sym + " "
        fsl_command += mask_command
final_command = fsl_command + mask_dest
call(final_command, shell=True)
print('Groupmask created')



#######################################################
"""

The third part of the code conducts the 
1)Smoothing (fslmaths)
2)L/R swap (fslswapdim)
3)Calculation of the pearson correlation (3dTcorrelate from afni)
4)Fisher Z Transform the correlation (3dcalc from afni)
5)Compute the Z statistic map (3dcalc from afni)

"""
#Preprocessing steps following img.clean_img function (ReHo analysis)

# Define mask, path to directory and subject labels 
cleaned_img = '_task-rest_space-MNI152NLin6Sym_clean.nii.gz'
subjects = '/nashome3/ipruotsa/afis_children/sourcedata/tutkittavat_fmri.txt' #subject labels
subject_names = open(subjects,'r')

for subject in subject_names :
    subject = subject.strip()

    # change current working directory
    path_wdc = path_vmhc + "/" + subject
    os.chdir(path_wdc)
    # skip the subjects who already has VMHC done
    path_vmhc_last = path_wdc + "/" + subject + "_space-MNI152NLin6Sym_vmhc_peacorr_z_stat.nii.gz"
    if os.path.isfile(path_vmhc_last) :
        continue 
    else :  
        print("Working ..." + subject)

        #Smoothing 6mm, (Gauss FHWM/sqrt(8*ln(2))
        smooth_command = "fslmaths " + path_vmhc + subject + "/" + subject + "_task-rest_space-MNI152NLin6Sym_clean.nii.gz -kernel gauss 2.5 -fmean -mas " + path_fmriprep + subject + "/func/" + subject + mask_sym + " " + path_vmhc + subject + "/" + subject + "_vmhc_space-MNI152NLin6Sym_smooth.nii.gz" 
        call(smooth_command, shell=True)

        #Copy and L/R swap the output  
        fslswap_command = "fslswapdim " + path_vmhc + subject + "/" + subject + "_vmhc_space-MNI152NLin6Sym_smooth.nii.gz -x y z " + path_vmhc + subject + "/" + subject +"_task-rest_space-MNI152NLin6Sym_LRflipped.nii.gz" 
        call(fslswap_command, shell=True)

        #Calculate pearson correlation between sub-001_preproc_bold_smooth.nii.gz and flipped tmp_LRflipped.nii.gz (AFNI) 
        corr_command = "3dTcorrelate -pearson -polort -1 -prefix " + path_vmhc + subject + "/" + subject + "_space-MNI152NLin6Sym_vmhc_peacorr.nii.gz " + path_vmhc + subject + "/" + subject + "_vmhc_space-MNI152NLin6Sym_smooth.nii.gz " + path_vmhc + subject + "/" + subject + "_task-rest_space-MNI152NLin6Sym_LRflipped.nii.gz" 
        call(corr_command, shell=True)

        #Fisher Z Transform the correlation 
        fisher_z = "3dcalc -a " + path_vmhc + subject + "/" + subject + "_space-MNI152NLin6Sym_vmhc_peacorr.nii.gz -expr 'log((a+1)/(1-a))/2' -prefix " + path_vmhc + subject + "/" + subject + "_space-MNI152NLin6Sym_vmhc_peacorr_Z.nii.gz" 
        call(fisher_z, shell=True)

        #Compute the Z statistic map (nvol = 160)!! Make sure that it's right if you change data!
        z_map = "3dcalc -a " + path_vmhc + subject + "/" + subject + "_space-MNI152NLin6Sym_vmhc_peacorr_Z.nii.gz -expr 'a*sqrt(160-3)' -prefix " + path_vmhc + subject + "/" + subject + "_space-MNI152NLin6Sym_vmhc_peacorr_z_stat.nii.gz"  
        call(z_map, shell=True)


