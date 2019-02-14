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
    _, data = hd.load_data(datafn)

    print('Making wm_mask')
    wm_mask = hd.reconst.wm_mask_from_data(data, gtab, mask)

    print('Getting response')
    response = hd.reconst.csd_response(data, gtab, wm_mask, sh_order=8)

    print('Saving')
    hd.save_obj(response, 'responses/{}_response.pkl'.format(names[i]))
