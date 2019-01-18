import numpy as np
import nibabel as nib

ref_img = nib.load('./registered_k5/denoised_k5_registered_b0_rep08.nii.gz')
ref_hdr = ref_img.header

img = nib.load('./registered_k5/denoised_k5_registered_b0s.nii.gz')
data = img.get_data()

avg = data.mean(axis=-1)

nib.save(nib.Nifti1Image(avg, ref_img.affine, header=ref_hdr),
         './registered_k5/denoised_k5_averaged_registered_b0.nii.gz')
