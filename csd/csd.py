import numpy as np
import nibabel as nib
from dipy.core.gradients import gradient_table
from dipy.reconst.csdeconv import recursive_response, ConstrainedSphericalDeconvModel
import dipy.reconst.dti as dti
from dipy.direction import peaks_from_model
from dipy.data import get_sphere

print('Loading')
img = nib.load('../denoise/denoised_k5.nii.gz')
data = img.get_data()
gtab = gradient_table('../x_dtifit/bvals', '../x_dtifit/bvecs')
mask = nib.load('../x_dtifit/nodif_brain_mask.nii.gz').get_data()

print('Tensor model')
tenmodel = dti.TensorModel(gtab)
tenfit = tenmodel.fit(data, mask)

FA = dti.fractional_anisotropy(tenfit.evals)
MD = dti.mean_diffusivity(tenfit.evals)
wm_mask = (np.logical_or(FA >= 0.4, (np.logical_and(FA >= 0.15, MD >= 0.0011))))

print('Response')
response = recursive_response(gtab, data, mask=wm_mask, sh_order=8,
                              peak_thr=0.01, init_fa=0.08, init_trace=0.0021,
                              iter=8, convergence=0.001, parallel=True)

print('Making CSD Model')
csd_model = ConstrainedSphericalDeconvModel(gtab, response)

print('Fitting CSD Model')
csd_fit = csd_model.fit(data)

sphere = get_sphere('symmetric724')
csd_peaks = peaks_from_model(model=csd_model,
                             data=data,
                             sphere=sphere,
                             relative_peak_threshold=0.5,
                             min_separation_angle=25,
                             parallel=True)
