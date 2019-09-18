import os
from pathlib import Path
import glob
#Rename anatomical images according to BIDS

root_path = "/nashome3/ipruotsa/afis_children/"
for folder_sub in os.listdir(root_path):
    if folder_sub.startswith("sub-"):
        folder_name = folder_sub
        new_path = root_path + folder_name + "/anat/"
        for filename in glob.glob(new_path + '*.nii.gz'):
            os.rename(filename, os.path.join(new_path, folder_name + '_T1w' + '.nii.gz'))
            for filename2 in glob.glob(new_path + '*.json'):
                os.rename(filename2, os.path.join(new_path, folder_name + '_T1w' + '.json'))

