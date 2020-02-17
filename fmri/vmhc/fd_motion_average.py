"""

Average motion (FD) per subject 

"""

# Set up Python modules
import os
import pandas as pd
import glob


#Define path to fmriprep folder
path = sorted(glob.iglob('/nashome3/ipruotsa/afis_children/derivatives/fmriprep/**/func'))
averages = []

for fname in path :
    path_folder = os.path.realpath(fname)
    path_name, folder_name = os.path.split(fname)
    dirname = os.path.basename(path_name) 
    

    if dirname.startswith('sub') : # only subject folders
        os.chdir(fname) # change current working directory
        
        confound = glob.glob('*-confounds_regressors.tsv')

        # Read confounds -file (Delimiter is \t --> tsv is a tab-separated spreadsheet)
        confound_df = pd.read_csv(fname + '/'+ confound[0], delimiter='\t')

        # select other confound variables
        confound_vars = ['framewise_displacement']
        confound_df = confound_df[confound_vars]
        confound_df.fillna(0, inplace=True) #Replace Nan with value 0
        average_fd = float(confound_df.mean())
        averages.append((dirname, average_fd))

cols = ['id_sub','fd_val']  
result = pd.DataFrame(averages, columns=cols)  
result.to_csv('/nashome3/ipruotsa/afis_children/fmriprep_movement_averages.csv', header=True )


