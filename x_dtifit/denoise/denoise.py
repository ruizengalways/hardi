import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
from dipy.denoise.localpca import localpca
from dipy.denoise.pca_noise_estimate import pca_noise_estimate
from dipy.core.gradients import gradient_table

# Loading data
print('Loading data')
img = nib.load('../x_dtifit/data.nii.gz')
data = img.get_data()
gtab = gradient_table('../x_dtifit/bvals', '../x_dtifit/bvecs')

# Estimating sigma to be used in local PCA algorithm
print('Estimating sigma')
sigma = pca_noise_estimate(data, gtab, correct_bias=True, smooth=3)

# Denoising
print('Denoising')
denoised_arr = localpca(data, sigma=sigma, patch_radius=2)

# Saving
print('Saving')
nib.save(nib.Nifti1Image(denoised_arr, img.affine), 'denoised_localpca.nii.gz')
