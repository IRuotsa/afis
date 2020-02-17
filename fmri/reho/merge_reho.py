# Merge ReHo maps to one file
import os
from subprocess import call

# Define ReHo folder & file
path_reho='/nashome3/ipruotsa/afis_children/derivatives/reho/'
folders = '/nashome3/ipruotsa/afis_children/sourcedata/tutkittavat_fmri.txt' #subject labels
reho_file = "_ReHo_norm_smooth.nii.gz " #space at the end
folder_names = open(folders,'r')

# Merge maps
merge_reho_maps = ""
for index, line in enumerate(folder_names) :
    line = line.strip()     
    if not index:
        merge_command = "fslmerge -t " + path_reho + "reho_group_z " + path_reho + line + "/" + line + reho_file
        merge_reho_maps += merge_command # first iteration
    else :
        merge_command = path_reho + line + "/" + line + reho_file
        merge_reho_maps += merge_command 
call(merge_reho_maps, shell=True)
