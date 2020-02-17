#!/bin/sh

#Get cluster statistics and location (only one significant cluster here)
cluster -i reho_mvpa_tfce_corrp_tstat1.nii.gz -t 0.95 --oindex=output_index > output_results.txt
# Cluster statistics
cluster -i reho_mvpa_tfce_corrp_tstat1.nii.gz -t 0.95 -c reho_mvpa_tstat1 --scalarname='1-p' >cluster_corrp.txt
# Resample to MNI152_T1_2mm space
fnirt --ref=MNI152_T1_2mm --in=output_index.nii.gz --iout=output_index_MNI152_2mm.nii.gz
# Binarize mask
fslmaths -dt int output_index_MNI152_2mm.nii.gz -thr 1 -uthr 1 -bin cluster_mask_MNI152_2mm
# Atlasquery
autoaq -i cluster_mask_MNI152_2mm.nii.gz -a "Harvard-Oxford Cortical Structural Atlas" -t 0.95 -u -o autoaq_cluster1_MNI152_2mm
