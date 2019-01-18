import numpy as np
import nibabel as nib

img = nib.load('../x_raw_data/x3D_DWSE_100um_TR1000_b0_rep01.nii.gz')
hdr = img.header
hdr.set_data_dtype('<f4')

for k in [5, 7, 9]:
    print(k)
    base = 'split_k{}/denoised_k{}_x3D_DWSE_100um_TR1000_'.format(k, k)
    fns = [base + 'b0_rep{:02d}.nii.gz'.format(i) for i in range(1, 17)] + [
        base + 'dir{:03d}.nii.gz'.format(i) for i in range(1, 145)]

    denoised_img = nib.load('denoised_k{}.nii.gz'.format(k))
    data = denoised_img.get_data()
    for i in range(data.shape[-1]):
        nib.save(nib.Nifti1Image(data[..., i], img.affine, hdr), fns[i])
