import numpy as np
import nibabel as nib
import dipy.reconst.dti as dti
from dipy.core.gradients import gradient_table

load = True
fit = True
metrics = True
view = False
save = True
compare = False

if load:
    print('Loading')
    img = nib.load('../denoise/denoised_mrtrix3_7kernel_nomask.nii.gz')
    data = img.get_data()
    gtab = gradient_table('../x_dtifit/bvals', '../x_dtifit/bvecs')
    mask = nib.load('../x_dtifit/nodif_brain_mask.nii.gz').get_data()

if fit:
    print('Creating tensor model')
    tenmodel = dti.TensorModel(gtab)
    print('Fitting tensor')
    tenfit = tenmodel.fit(data, mask)

if metrics:
    FA = dti.fractional_anisotropy(tenfit.evals)
    FA[np.isnan(FA)] = 0
    RGB = dti.color_fa(FA, tenfit.evecs)

if save:
    def nibsave(data, fn, f32=True, aff=img.affine):
        if f32:
            data = data.astype(np.float32)

        nib.save(nib.Nifti1Image(data, aff), fn)

    nibsave(FA, 'tensor_fa.nii.gz')
    nibsave(tenfit.md, 'tensor_md.nii.gz')
    nibsave(np.array(255 * RGB, 'uint8'), 'tensor_rgb.nii.gz')
    # nibsave(tenfit.evals[..., 0], 'tensor_L1.nii.gz')
    # nibsave(tenfit.evals[..., 1], 'tensor_L2.nii.gz')
    # nibsave(tenfit.evals[..., 2], 'tensor_L3.nii.gz')
    # nibsave(tenfit.evecs[..., 0, 0], 'tensor_V1.nii.gz')
    # nibsave(tenfit.evecs[..., 0, 1], 'tensor_V2.nii.gz')
    # nibsave(tenfit.evecs[..., 0, 2], 'tensor_V3.nii.gz')

if compare:
    print("Loading Sean's")
    sL1 = nib.load('../dti_L1.nii.gz').get_data()
    sL2 = nib.load('../dti_L2.nii.gz').get_data()
    sL3 = nib.load('../dti_L3.nii.gz').get_data()
    sV1 = nib.load('../dti_V1.nii.gz').get_data()
    sV2 = nib.load('../dti_V2.nii.gz').get_data()
    sV3 = nib.load('../dti_V3.nii.gz').get_data()
    sFA = nib.load('../dti_FA.nii.gz').get_data()
    sMD = nib.load('../dti_MD.nii.gz').get_data()

    def compare(metric, mine, sean, vec=False):
        rmse = np.sqrt(np.mean((sean - mine)**2)) / sean.mean() * 100
        print(metric + ': {}'.format(rmse))

    compare('FA', FA, sFA)
    compare('MD', tenfit.md, sMD)
    compare('L1', tenfit.evals[..., 0], sL1)
    compare('L2', tenfit.evals[..., 1], sL2)
    compare('L3', tenfit.evals[..., 2], sL3)
    compare('V1', tenfit.evecs[..., 0, :], sV1)
    compare('V2', tenfit.evecs[..., 1, :], sV2)
    compare('V3', tenfit.evecs[..., 2, :], sV3)


if view:
    from dipy.data import get_sphere
    sphere = get_sphere('symmetric724')
    from dipy.viz import window, actor
    ren = window.Renderer()
    evals = tenfit.evals[36:67, 86:105, 21:22]
    evecs = tenfit.evecs[36:67, 86:105, 21:22]

    cfa = RGB[36:67, 86:105, 21:22]
    cfa /= cfa.max()

    ren.add(actor.tensor_slicer(evals, evecs,
                                scalar_colors=cfa, sphere=sphere, scale=0.3))
    window.show(ren)
