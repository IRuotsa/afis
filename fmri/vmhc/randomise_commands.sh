#!/bin/sh

#Randomise commands for regional homogeneity and homotopic connectivity analyses
# fsl Glm used to create contrast and matrix files 
#ReHo analysis
randomise -i reho_group_z -o reho_mvpa -d mvpa.mat -t mvpa.con -m group_mask_asym.nii.gz -n 10000 -v 6 -D -T
randomise -i reho_group_z -o reho_mvpa_motion -d mvpa_motion.mat -t mvpa_motion.con -m group_mask_asym.nii.gz -n 10000 -v 6 -D -T
randomise -i reho_group_z -o reho_fitness -d fitness.mat -t fitness.con -m group_mask_asym.nii.gz -n 10000 -v 6 -D -T
randomise -i reho_group_z -o reho_fitness_motion -d fitness_motion.mat -t fitness_motion.con -m group_mask_asym.nii.gz -n 10000 -v 6 -D -T

#VMHC analysis
randomise -i vmhc_group_z -o vmhc_fitness -d fitness.mat -t fitness.con -m group_mask_sym.nii.gz -n 10000 -v 6 -D -T
randomise -i vmhc_group_z -o vmhc_fitness_motion -d fitness_motion.mat -t fitness_motion.con -m group_mask_sym.nii.gz -n 10000 -v 6 -D -T
randomise -i vmhc_group_z -o vmhc_mvpa -d mvpa.mat -t mvpa.con -m group_mask_sym.nii.gz -n 10000 -v 6 -D -T
randomise -i vmhc_group_z -o vmhc_mvpa_motion -d mvpa_motion.mat -t mvpa_motion.con -m group_mask_sym.nii.gz -n 10000 -v 6 -D -T
