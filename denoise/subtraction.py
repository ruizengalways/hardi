import nibabel as nib

data_img = nib.load('../x_dtifit/data.nii.gz')
data = data_img.get_data()

for k in [5, 7, 9]:
    print(k)
    denoised_data = nib.load(
        './denoised_k{}.nii.gz'.format(k)).get_data()
    noise = data - denoised_data
    nib.save(nib.Nifti1Image(noise, data_img.affine),
             'noise_k{}.nii.gz'.format(k))
