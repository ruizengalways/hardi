import numpy as np
import nibabel as nib
import tifffile as tf


def save_color_rgb(path):
    FA_img = nib.load(path + 'FA.nii.gz')
    FA = FA_img.get_data()
    PDD = nib.load(path + 'V1.nii.gz').get_data()

    RGB = np.abs(PDD) * np.clip(FA, 0, 1)[..., None]
    tf.imsave(path + 'color_fa.tif',
              np.moveaxis(np.array(255 * RGB, 'uint8'), [0, 1, 2], [2, 0, 1]))


paths = ['raw/raw_'] + \
    ['denoised_k{0}/denoised_k{0}_'.format(k) for k in [5, 7, 9]]

for path in paths:
    print(path)
    save_color_rgb(path)
