#Plotting of the images

#source activate mne-dev # environment with Python 3.x
#ipython --matplotlib #to open ipython
from nilearn import plotting

#ReHo images
reho_fitness1 = "/nashome3/ipruotsa/afis_children/derivatives/reho/reho_fitness_tfce_corrp_tstat1.nii.gz"
reho_fitness2 = "/nashome3/ipruotsa/afis_children/derivatives/reho/reho_fitness_tfce_corrp_tstat2.nii.gz"
reho_mvpa1 = "/nashome3/ipruotsa/afis_children/derivatives/reho/reho_mvpa_tfce_corrp_tstat1.nii.gz"
reho_mvpa2 = "/nashome3/ipruotsa/afis_children/derivatives/reho/reho_mvpa_tfce_corrp_tstat2.nii.gz"

#VMHC images
vmhc_fitness1 = "/nashome3/ipruotsa/afis_children/derivatives/vmhc/vmhc_fitness_tfce_corrp_tstat1.nii.gz"
vmhc_fitness2 = "/nashome3/ipruotsa/afis_children/derivatives/vmhc/vmhc_fitness_tfce_corrp_tstat2.nii.gz"
vmhc_mvpa1 = "/nashome3/ipruotsa/afis_children/derivatives/vmhc/vmhc_mvpa_tfce_corrp_tstat1.nii.gz"
vmhc_mvpa2 = "/nashome3/ipruotsa/afis_children/derivatives/vmhc/vmhc_mvpa_tfce_corrp_tstat2.nii.gz"

# Plot images (No thresholds)
reho_fit_plot1 = plotting.plot_glass_brain(reho_fitness1, display_mode='lyrz', threshold=0, colorbar=True, cmap='cold_white_hot', output_file='/nashome3/ipruotsa/afis_children/derivatives/reho/reho_fit_plot1.png') 
reho_fit_plot2 = plotting.plot_glass_brain(reho_fitness2, display_mode='lyrz', threshold=0, colorbar=True, cmap='cold_white_hot', output_file='/nashome3/ipruotsa/afis_children/derivatives/reho/reho_fit_plot2.png')
reho_mvpa_plot1 = plotting.plot_glass_brain(reho_mvpa1, display_mode='lyrz', threshold=0, colorbar=True, cmap='cold_white_hot', output_file='/nashome3/ipruotsa/afis_children/derivatives/reho/reho_mvpa_plot1.png')
reho_mvpa_plot2 = plotting.plot_glass_brain(reho_mvpa2, display_mode='lyrz', threshold=0, colorbar=True, cmap='cold_white_hot', output_file='/nashome3/ipruotsa/afis_children/derivatives/reho/reho_mvpa_plot2.png')

vmhc_fit_plot1 = plotting.plot_glass_brain(vmhc_fitness1, display_mode='lyrz', threshold=0, colorbar=True, cmap='cold_white_hot', output_file='/nashome3/ipruotsa/afis_children/derivatives/vmhc/vmhc_fit_plot1.png') 
vmhc_fit_plot2 = plotting.plot_glass_brain(vmhc_fitness2, display_mode='lyrz', threshold=0, colorbar=True, cmap='cold_white_hot', output_file='/nashome3/ipruotsa/afis_children/derivatives/vmhc/vmhc_fit_plot2.png')
vmhc_mvpa_plot1 = plotting.plot_glass_brain(vmhc_mvpa1, display_mode='lyrz', threshold=0, colorbar=True, cmap='cold_white_hot', output_file='/nashome3/ipruotsa/afis_children/derivatives/vmhc/vmhc_mvpa_plot1.png')
vmhc_mvpa_plot2 = plotting.plot_glass_brain(vmhc_mvpa2, display_mode='lyrz', threshold=0, colorbar=True, cmap='cold_white_hot', output_file='/nashome3/ipruotsa/afis_children/derivatives/vmhc/vmhc_mvpa_plot2.png')

# Plot images with clusters p<0.05
reho_mvpa_plot1_thr = plotting.plot_glass_brain(reho_mvpa1, threshold=0.95, colorbar=True, cmap='cold_white_hot', output_file='reho_mvpa_thr_plot1.png')
