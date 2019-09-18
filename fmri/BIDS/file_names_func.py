import os
from pathlib import Path
import glob
#Rename functional images according to BIDS

root_path = "/nashome3/ipruotsa/afis_children/"
for folder_sub in os.listdir(root_path):
    if folder_sub.startswith("sub-"):
        folder_name = folder_sub
        new_path = root_path + folder_name + "/func/"
        for filename in glob.glob(new_path + '*.nii.gz'):
            os.rename(filename, os.path.join(new_path, folder_name + '_task-rest_bold' + '.nii.gz'))
            for filename2 in glob.glob(new_path + '*.json'):
                os.rename(filename2, os.path.join(new_path, folder_name + '_task-rest_bold' + '.json'))
