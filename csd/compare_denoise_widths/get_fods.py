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
    response = hd.load_obj('responses/{}_response.pkl'.format(names[i]))

    print('Fitting CSD')
    model, fod = hd.reconst.csd(response, data, gtab, mask)

    print('Saving')
    hd.save_obj(model, 'models/{}_model.pkl'.format(names[i]))
    hd.niisave('fods/{}_fod.nii.gz'.format(names[i]), fod, img)
