# Merge vmhc maps to one file
import os
from subprocess import call

# Define vmhc folder & file
path_vmhc='/nashome3/ipruotsa/afis_children/derivatives/vmhc/'
folders = '/nashome3/ipruotsa/afis_children/sourcedata/tutkittavat_fmri.txt' #subject labels
vmhc_file = "_space-MNI152NLin6Sym_vmhc_peacorr_z_stat.nii.gz "
folder_names = open(folders,'r')

# Merge maps
merge_vmhc_maps = ""
for index, line in enumerate(folder_names) :
    line = line.strip()     
    if not index:
        merge_command = "fslmerge -t " + path_vmhc + "vmhc_group_z " + path_vmhc + line + "/" + line + vmhc_file
        merge_vmhc_maps += merge_command # first iteration
    else :
        merge_command = path_vmhc + line + "/" + line + vmhc_file
        merge_vmhc_maps += merge_command 
call(merge_vmhc_maps, shell=True)
