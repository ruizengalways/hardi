# This script forms a brain mask using median otsu thresholding

import numpy as np
import nibabel as nib
from dipy.segment.mask import median_otsu
from dipy.core.gradients import gradient_table

print('Loading data')
img = nib.load('../x_dtifit/data.nii.gz')
data = img.get_data()[..., 0]

print('Masking')
b0_mask, mask = median_otsu(data, 1, 1, dilate=2)

print('Saving')
nib.save(nib.Nifti1Image(b0_mask, img.affine), 'data_masked.nii.gz')
nib.save(nib.Nifti1Image(mask.astype('float'), img.affine), 'mask.nii.gz')
