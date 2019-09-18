import os

#Rename sourcedata
path_folder = "/nashome3/ipruotsa/afis_children/sourcedata/"
for folder in os.listdir(path_folder):
    if folder.startswith("AFIS_C"):
        os.rename(path_folder + folder, path_folder + folder.replace("AFIS_C", "sub-"))

#Rename subject files

path_subjects = "/nashome3/ipruotsa/afis_children/"
for folder_sub in os.listdir(path_subjects):
    if folder_sub.startswith("AFIS_C"):
        os.rename(path_subjects + folder_sub, path_subjects + folder_sub.replace("AFIS_C", "sub-"))
