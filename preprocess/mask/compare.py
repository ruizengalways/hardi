import numpy as np
import nibabel as nib

raw = nib.load('./raw_mask.nii.gz').get_data()
d5 = nib.load('./denoised_k5_mask.nii.gz').get_data()
d7 = nib.load('./denoised_k7_mask.nii.gz').get_data()
d9 = nib.load('./denoised_k9_mask.nii.gz').get_data()

names = ['raw', 'd5', 'd7', 'd9']

# Raw
for i, d in enumerate([d5, d7, d9]):
    neq = np.sum(raw != d)
    print('Raw / {}: {}'.format(names[i + 1], neq))

# d5
for i, d in enumerate([d7, d9]):
    neq = np.sum(d5 != d)
    print('d5 / {}: {}'.format(names[i + 2], neq))

# d7/9
neq = np.sum(d7 != d9)
print('d7 / d9: {}'.format(neq))
