# This script denoises the DWI data using the MRtrix3 software, exploiting
# data redundancy in the PCA domain [Veraart2016]

data=../x_raw_data/raw_data.nii.gz

dwidenoise $data denoised_k5.nii.gz -extent 5,5,5 -nthreads 4
dwidenoise $data denoised_k7.nii.gz -extent 7,7,7 -nthreads 4
dwidenoise $data denoised_k9.nii.gz -extent 9,9,9 -nthreads 4
