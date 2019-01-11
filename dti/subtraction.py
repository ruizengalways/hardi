import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt

my_fa_img = nib.load('./tensor_fa.nii.gz')
my_fa = my_fa_img.get_data()
seans_fa = nib.load('../x_dtifit/dti_FA.nii.gz').get_data()
mask = nib.load(
    '../x_dtifit/nodif_brain_mask.nii.gz').get_data().astype(np.bool)

diff = my_fa - seans_fa
nib.save(nib.Nifti1Image(diff, my_fa_img.affine), 'FA_subtraction.nii.gz')

inbrain_diff = diff[mask]

plt.hist(inbrain_diff, bins=256, log=True)
plt.title('Denoised - Raw \n Mean: {:.4f}, Max: {:.2f}, Min: {:.2f}'.format(inbrain_diff.mean(),
                                                                            inbrain_diff.max(),
                                                                            inbrain_diff.min()))
plt.show()
plt.savefig('diff_hist.png')
