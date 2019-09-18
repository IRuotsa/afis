#create folders from tutkittavat.txt -file
import os
#Create folders under sourcedata folder
#root_path = '/nashome3/ipruotsa/afis_children/sourcedata/'
folders = '/nashome3/ipruotsa/afis_children/sourcedata/tutkittavat.txt'
folder_names = open(folders,'r')
for line in folder_names :
    line = line.strip()
    subfolder_names = ['anat','func','dwi']
    for subfolder_name in subfolder_names :
        os.makedirs(os.path.join(line, subfolder_name))


