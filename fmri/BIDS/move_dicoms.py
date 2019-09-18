#move anat dicoms to sourcedata

import os
from pathlib import Path
import glob
import shutil

folders = '/nashome3/ipruotsa/afis_children/sourcedata/tutkittavat.txt'
path_dir = '/nashome3/ipruotsa/MRI_freesurfer/'
path_dst = '/nashome3/ipruotsa/afis_children/sourcedata/'
folder_names = open(folders,'r')
for line in folder_names :
    line = line.strip()
    orig = '_orig'
    folder_name = line+orig
    file_path1 = os.path.join(path_dir,folder_name)
    file_path2 = os.path.join(path_dst,line,'anat')
    for filename in Path(file_path1).glob('slices/MR*') :
        print(filename)
        shutil.copy(filename,file_path2)

#move rs-fmri scans to sourcedata

folders = '/nashome3/ipruotsa/afis_children/sourcedata/tutkittavat.txt'
path_dir2 = '/nashome3/ipruotsa/Data_kaikki_lapset/'
path_dst2 = '/nashome3/ipruotsa/afis_children/sourcedata/'
folder_names2 = open(folders,'r')
for line in folder_names2 :
    line = line.strip()
    file_path1b = os.path.join(path_dir2,line)
    file_path2b = os.path.join(path_dst2,line,'func')
    for filename in Path(file_path1b).glob('*/**/func/MR*') :
        print(filename)
        shutil.copy(filename,file_path2b)
