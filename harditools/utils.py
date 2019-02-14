import numpy as np
import nibabel as nib
from dipy.core.gradients import gradient_table
import pickle
import pkg_resources
data_path = pkg_resources.resource_filename('harditools', 'data/')


def load_mask(fn):
    mask = nib.load(fn).get_data().astype(np.bool)
    return mask


def load_gtab(all_b0s=True, bvalfn=None, bvecfn=None):
    if np.all([bvalfn == None, bvecfn == None]):
        if all_b0s:
            bvalfn = data_path + 'bvals_with_b0s'
            bvecfn = data_path + 'bvecs_with_b0s'
        else:
            bvalfn = data_path + 'bvals'
            bvecfn = data_path + 'bvecs'

    gtab = gradient_table(bvalfn, bvecfn, atol=1)
    return gtab


def load_data(fn):
    img = nib.load(fn)
    data = img.get_data()

    return img, data


def save_data(fn, data, img):
    nib.save(nib.Nifti1Image(data, img.affine), fn)


def save_obj(obj, fn):
    with open(fn, 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(fn):
    with open(fn, 'rb') as f:
        obj = pickle.load(f)
    return obj


def order_to_ncoef(order):
    return int((order + 1) * (order + 2) / 2)


def order_from_ncoef(ncoef):
    return int((-3 + np.sqrt(9 - 8 * (1 - ncoef))) / 2)


def unmask(data, mask, dtype=np.float):
    if data.ndim == 1:
        shape = mask.shape
    else:
        extra_dims = data.ndim - 1
        shape = mask.shape + data.shape[-extra_dims:]

    unmasked = np.zeros(shape, dtype=dtype)
    unmasked[mask] = data
    return unmasked


def ang_distance(dir1, dir2):
    costheta = (dir1 * dir2).sum(axis=1) / \
        (np.linalg.norm(dir1, axis=1) * np.linalg.norm(dir2, axis=1))
    costheta = np.clip(costheta, -1, 1)
    ang = np.arccos(costheta)

    # Restricting to [0, pi] since pdd +- 180 = pdd
    ang = np.where(ang > np.pi/2, np.pi - ang, ang)

    ang *= (180/np.pi)
    return ang


def percdiff(im1, im2):
    diff = (im1 - im2) / im2 * 100
    return diff.flatten()
