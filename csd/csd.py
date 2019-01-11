import numpy as np
import nibabel as nib
from dipy.core.gradients import gradient_table

img = nib.load('./data.nii.gz')
data = img.get_data()
gtab = gradient_table('./bvals', './bvecs')

from dipy.reconst.csdeconv import auto_response

response, ratio = auto_response(
    gtab, data, roi_radius=10, fa_thr=0.7)  # roi_center=(59, 61, 56),

from dipy.viz import window, actor
# ren = window.Renderer()
# evals = response[0]
# evecs = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]]).T
from dipy.data import get_sphere
sphere = get_sphere('symmetric724')
# from dipy.sims.voxel import single_tensor_odf
# response_odf = single_tensor_odf(sphere.vertices, evals, evecs)
# response_odf = response_odf[None, None, None, :]
# response_actor = actor.odf_slicer(
#     response_odf, sphere=sphere, colormap='plasma')
# ren.add(response_actor)
# window.show(ren)

# FA = nib.load('./dti_FA.nii.gz').get_data()
# MD = nib.load('./dti_MD.nii.gz').get_data()
# wm_mask = (np.logical_or(FA >= 0.4, (np.logical_and(FA >= 0.15, MD >= 0.0011))))

from dipy.reconst.csdeconv import ConstrainedSphericalDeconvModel
csd_model = ConstrainedSphericalDeconvModel(gtab, response)

data_small = data[36:67, 86:105, 21:22]
csd_fit = csd_model.fit(data_small)
csd_odf = csd_fit.odf(sphere)
# fodf_spheres = actor.odf_slicer(
#     csd_odf, sphere=sphere, scale=0.9, norm=True, colormap='plasma')

# ren.add(fodf_spheres)
# window.show(ren)

from dipy.direction import peaks_from_model

csd_peaks = peaks_from_model(model=csd_model,
                             data=data_small,
                             sphere=sphere,
                             relative_peak_threshold=0.5,
                             min_separation_angle=25,
                             parallel=25)

ren = window.Renderer()
window.clear(ren)
fodf_peaks = actor.peak_slicer(csd_peaks.peak_dirs, csd_peaks.peak_values)
ren.add(fodf_peaks)
window.show(ren)
