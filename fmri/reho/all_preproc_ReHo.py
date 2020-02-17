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


#Define path for cleaning
path = sorted(glob.iglob('/nashome3/ipruotsa/afis_children/derivatives/fmriprep/**/func'))
path_reho = '/nashome3/ipruotsa/afis_children/derivatives/reho/'

for fname in path :
    path_folder = os.path.realpath(fname)
    path_name, folder_name = os.path.split(fname)
    dirname = os.path.basename(path_name) 

    if dirname.startswith('sub') : # only subject folders
        os.chdir(fname) # change current working directory
        print(os.getcwd()) #print current working directory    

        # skip the subjects who already has img.clean_img done
        path_clean_file = path_reho + dirname + "/" + dirname + "_task-rest_space-MNI152NLin6Asym_clean.nii.gz"
        if os.path.isfile(path_clean_file) :
            continue 

        else :      
            confound = glob.glob('*-confounds_regressors.tsv')
            func = glob.glob('*space-MNI152NLin6Asym_desc-preproc_bold.nii.gz')
            mask = glob.glob('*space-MNI152NLin6Asym_desc-brain_mask.nii.gz')
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

            # Change confounds to matrix (confirm matrix size with confounds_matrix.shape)
            confounds_matrix = confound_df.values

            # Define high_pass and low_pass values
            high_pass = 0.008
            low_pass = 0.08

            # Clean
            clean_img = img.clean_img(func_img, confounds=confounds_matrix, detrend=True, standardize=True, low_pass=low_pass, high_pass=high_pass, t_r=2.61, mask_img=mask, ensure_finite=True )

            #Create new subject-directory in the reho-directory
            new_folder = os.path.join(path_reho,dirname)
            os.mkdir(new_folder)
            clean_file = new_folder + '/' + dirname + '_task-rest_space-MNI152NLin6Asym_clean.nii.gz'
            # Save to nii.gz
            clean_img.to_filename(clean_file)

########################################################

"""

The second part of the code creates a group mask
from the masks produced in fmriprep 
(...MNI152NLin6Asym_desc-brain_mask.nii.gz)

"""

#Create group mask from asymmetric brain masks

# Define mask, path to directory and subject labels 
mask_asym = '_task-rest_space-MNI152NLin6Asym_desc-brain_mask.nii.gz' # maskname after sub-label
path_fmriprep='/nashome3/ipruotsa/afis_children/derivatives/fmriprep/'
subjects = '/nashome3/ipruotsa/afis_children/sourcedata/tutkittavat_fmri.txt' #subject labels
subject_names = open(subjects,'r')

fsl_command = ""
for index, subject_tag  in enumerate(subject_names) :
    subject_tag = subject_tag.strip()
    mask_dest = "/nashome3/ipruotsa/afis_children/derivatives/reho/group_mask_asym.nii.gz" #file name and destination
    if not index:
        mask_command = "fslmaths " + path_fmriprep + subject_tag + "/func/" + subject_tag + mask_asym + " "
        fsl_command += mask_command # for the first iteration -mul not included
    else :
        mask_command = "-mul " + path_fmriprep + subject_tag + "/func/" + subject_tag + mask_asym + " "
        fsl_command += mask_command
final_command = fsl_command + mask_dest
call(final_command, shell=True)
print('Group mask created')

#######################################################
"""

The third part of the code conducts the 
1)ReHo analysis (3dReHo from afni)
2)Smoothing (fslmaths)
3)Normalization (fslstats + fslmaths

"""
#Preprocessing steps following image cleaning (ReHo analysis)
# Define mask, path to directory and subject labels 
cleaned_img = '_task-rest_space-MNI152NLin6Asym_clean.nii.gz'
subjects = '/nashome3/ipruotsa/afis_children/sourcedata/tutkittavat_fmri.txt' #subject labels
subject_names = open(subjects,'r')

for subject in subject_names :
    subject = subject.strip()

    # change current working directory
    path_wdc = path_reho + "/" + subject
    os.chdir(path_wdc) 
    # skip the subjects who already has ReHo done
    path_reho_smooth = path_reho + subject + "/" + subject + "_ReHo_norm_smooth.nii.gz"
    if os.path.isfile(path_reho_smooth) :
        continue 
    else :  
        print("Working ..." + subject)
        #ReHo analysis
        reho_command = "3dReHo -prefix " + subject + "_ReHo_result.nii.gz -inset " + path_reho + subject + "/" + subject + cleaned_img + " -mask " + path_fmriprep + subject + "/func/" + subject + mask_asym + " -nneigh 27"
        call(reho_command, shell=True)

        #Normalization
        mean_command = "fslstats " + path_reho + subject + "/" + subject + "_ReHo_result.nii.gz -M"
        meanReHo = call(mean_command, shell=True)
        std_command = "fslstats " + path_reho + subject + "/" + subject + "_ReHo_result.nii.gz -S"
        stdReHo = call(std_command, shell=True)
        normalization = "fslmaths " + path_reho + subject + "/" + subject + "_ReHo_result.nii.gz -sub " + str(meanReHo) + " -div " + str(stdReHo) + " -mul " + path_reho + "group_mask_asym.nii.gz " + path_reho + subject + "/" + subject + "_norm_ReHo.nii.gz"
        call(normalization, shell=True)

        #Smoothing using fslmaths
        smooth_command = "fslmaths " + path_reho + subject + "/" + subject + "_norm_ReHo.nii.gz -kernel gauss 2.5 -fmean -mas " + path_fmriprep + subject + "/func/" + subject + mask_asym + " " + path_reho + subject + "/" + subject + "_ReHo_norm_smooth.nii.gz"
        call(smooth_command, shell=True)


