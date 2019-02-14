import numpy as np
import harditools as hd

names = ['raw', 'denoised_k5', 'denoised_k7', 'denoised_k9']
datafns = ['data/raw.nii.gz'] + \
    ['data/denoised_k{}.nii.gz'.format(k) for k in [5, 7, 9]]
maskfn = 'data/mask.nii.gz'

gtab = hd.load_gtab()
mask = hd.load_mask(maskfn)

for i, datafn in enumerate(datafns):

    print(names[i])

    print('Loading data')
    img, data = hd.load_data(datafn)
    _, fod = hd.load_data('./fods/{}_fod.nii.gz'.format(names[i]))

    print('Calculating ODF')
    odf = hd.reconst.sh2odf(fod[mask])

    print('Calculating peaks')
    peaks = hd.reconst.calc_peaks(odf)

    print('Saving')
    hd.save_obj(peaks, 'peaks/{}_peaks.pkl'.format(names[i]))
