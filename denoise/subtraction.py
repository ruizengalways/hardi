import nibabel as nib

data_img = nib.load('../x_raw_data/raw_data.nii.gz')
data = data_img.get_data()

for k in [5, 7, 9]:
    print(k)
    denoised_data_img = nib.load(
        './denoised_k{}.nii.gz'.format(k))
    denoised_data = denoised_data_img.get_data()
    noise = data.astype(denoised_data.dtype) - denoised_data
    nib.save(nib.Nifti1Image(noise, denoised_data_img.affine,
                             denoised_data_img.header),
             'noise_k{}.nii.gz'.format(k))
