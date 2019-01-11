import nibabel as nib

# data_img = nib.load('../mask/data_masked.nii.gz')
# data = data_img.get_data()
# denoised_data = nib.load('./denoised_mrtrix3_7kernel.nii.gz').get_data()
# noise = data - denoised_data
# nib.save(nib.Nifti1Image(noise, data_img.affine), 'mrtrix_noise.nii.gz')

data_img = nib.load('../x_dtifit/data.nii.gz')
data = data_img.get_data()
denoised_data = nib.load('./denoised_mrtrix3_7kernel_nomask.nii.gz').get_data()
noise = data - denoised_data
nib.save(nib.Nifti1Image(noise, data_img.affine), 'mrtrix_noise_nomask.nii.gz')
