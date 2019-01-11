# This script denoises the DWI data using the MRtrix3 software, exploiting
# data redundancy in the PCA domain [Veraart2016]

dwidenoise ../x_dtifit/data.nii.gz denoised_mrtrix3_7kernel_nomask.nii.gz -extent 7,7,7 -nthreads 2
