import numpy as np
from dipy.reconst import dti, csdeconv
from dipy.reconst.shm import sph_harm_ind_list
from dipy.data import get_sphere
from dipy.direction import sh_to_sf_matrix, peak_directions, gfa
from dipy.core.ndindex import ndindex
from .utils import order_to_ncoef, order_from_ncoef


class Peaks(object):
    def __init__(self, peak_dirs, peak_values, indices,
                 sphere, qa, gfa):
        self.peak_dirs = peak_dirs
        self.peak_values = peak_values
        self.indices = indices
        self.sphere = sphere
        self.qa = qa
        self.gfa = gfa

    def num_peaks(self):
        return (self.peak_values != 0).sum(axis=-1)

    def peakmask(self, thresh=1, comp='gt'):
        # Generates a spatial mask that returns true
        # if the odf has at least `numpeaks` peaks

        if comp == 'gt':
            return self.num_peaks() >= thresh
        if comp == 'lt':
            return self.num_peaks() <= thresh
        if comp == 'eq':
            return self.num_peaks() == thresh

    def unflatten_all(self, mask):
        self.peak_dirs = self._unflatten(self.peak_dirs, mask)
        self.peak_values = self._unflatten(self.peak_values, mask)
        self.indices = self._unflatten(self.indices, mask)
        self.qa = self._unflatten(self.qa, mask)
        self.gfa = self._unflatten(self.gfa, mask)

    def _unflatten(self, data, mask):

        dtype = data.dtype

        if data.ndim == 1:
            shape = mask.shape
        else:
            extra_dims = data.ndim - 1
            shape = mask.shape + data.shape[-extra_dims:]

        unflattened = np.zeros(shape, dtype=dtype)
        unflattened[mask] = data
        return unflattened


def tensor(data, gtab, mask):
    tenmodel = dti.TensorModel(gtab)
    tenfit = tenmodel.fit(data, mask=mask)
    return tenmodel, tenfit


def wm_mask_from_data(data, gtab, mask):
    tenmodel, tenfit = tensor(data, gtab, mask)
    FA = dti.fractional_anisotropy(tenfit.evals)
    MD = dti.mean_diffusivity(tenfit.evals)
    wm_mask = (np.logical_or(
        FA >= 0.4, (np.logical_and(FA >= 0.15, MD >= 0.0011))))

    return wm_mask


def csd_response(data, gtab, mask, sh_order=8):
    response = csdeconv.recursive_response(gtab, data, mask=mask, sh_order=sh_order,
                                           peak_thr=0.01, init_fa=0.08,
                                           init_trace=0.0021, iter=8, convergence=0.001,
                                           parallel=True)
    return response


def csd(response, data, gtab, mask,
        sh_order=8, reg_sphere=None, lambda_=1, tau=0.1):

    model = csdeconv.ConstrainedSphericalDeconvModel(gtab=gtab,
                                                     response=response,
                                                     reg_sphere=reg_sphere,
                                                     sh_order=sh_order,
                                                     lambda_=1,
                                                     tau=0.1)

    fit = model.fit(data, mask)

    inmaskfod = np.array(
        [fit.shm_coeff for fit in fit.fit_array.flatten()[mask.flatten()]])
    fod = np.zeros((mask.size, inmaskfod.shape[1]), dtype=inmaskfod.dtype)
    fod[mask.flatten()] = inmaskfod
    fod = fod.reshape(mask.shape + (order_to_ncoef(sh_order),))

    return model, fod


def sh2odf(sh, sphere=None):

    shape = sh.shape[:-1]

    if sphere == None:
        sphere = get_sphere('symmetric724')

    sh_order = order_from_ncoef(sh.shape[-1])

    B = sh_to_sf_matrix(sphere, sh_order, return_inv=False)

    odf = np.dot(sh, B)

    return odf


def calc_peaks(odf, mask=None, sphere=None, npeaks=5, peak_thresh=0.5, min_angle=25,
               gfa_thr=0, normalize_peaks=False):

    shape = odf.shape[:-1]

    if sphere == None:
        sphere = get_sphere('symmetric724')
    if mask is None:
        mask = np.ones(shape, dtype='bool')

    gfa_array = calc_gfa(odf)

    qa_array = np.zeros((shape + (npeaks,)))
    peak_dirs = np.zeros((shape + (npeaks, 3)))
    peak_values = np.zeros((shape + (npeaks,)))
    peak_indices = np.zeros((shape + (npeaks,)), dtype='int')
    peak_indices.fill(-1)

    global_max = -np.inf
    for idx in ndindex(shape):
        if not mask[idx]:
            continue

        if gfa_array[idx] < gfa_thr:
            global_max = max(global_max, odf[idx].max())
            continue

        direction, pk, ind = peak_directions(odf[idx], sphere,
                                             relative_peak_threshold=peak_thresh,
                                             min_separation_angle=min_angle)

        if pk.shape[0] != 0:
            global_max = max(global_max, pk[0])

            n = min(npeaks, pk.shape[0])
            qa_array[idx][:n] = pk[:n] - odf[idx].min()
            peak_dirs[idx][:n] = direction[:n]
            peak_indices[idx][:n] = ind[:n]
            peak_values[idx][:n] = pk[:n]

            if normalize_peaks:
                peak_values[idx][:n] /= pk[0]
                peak_dirs[idx] *= peak_values[idx][:, None]

    qa_array /= global_max

    peaks = Peaks(peak_dirs, peak_values, peak_indices,
                  sphere, qa_array, gfa_array)

    return peaks


def calc_gfa(odf):
    return gfa(odf.reshape(-1, odf.shape[-1])).reshape(odf.shape[:-1])


def order_to_jrange(order):
    j0 = order_to_ncoef(order - 2)
    jf = j0 + 2 * order
    return j0, jf


def sh_power(sh):
    order = order_from_ncoef(sh.shape[-1])
    bands = np.arange(0, order + 1, 2)
    sh_power = np.zeros((sh.shape[:3] + (bands.size,)))

    for i, band in enumerate(bands):
        j0, jf = order_to_jrange(band)
        sh_power[..., i] = np.sum((sh[..., j0:jf+1])**2, axis=-1)
    return sh_power
