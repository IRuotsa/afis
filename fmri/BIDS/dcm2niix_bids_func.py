#Loop for converting dicoms to .nii.gz with dcm2niix -converter (rs-fmri images)
import os
from pathlib import Path
import subprocess

folders = '/nashome3/ipruotsa/afis_children/sourcedata/tutkittavat.txt'
path_dir = '/nashome3/ipruotsa/afis_children/sourcedata/'
path_dst = '/nashome3/ipruotsa/afis_children/'
folder_names = open(folders,'r')
for line in folder_names :
    line = line.strip()
    file_path1 = os.path.join(path_dir,line, 'func')
    file_path_dst = os.path.join(path_dst,line,'func')
    bashCommand = 'dcm2niix -o ' + file_path_dst + ' -f %f_%p_%i -b y ' + file_path1
    print(bashCommand)
    subprocess.run([bashCommand], shell=True)

