import numpy as np
from dipy.core.gradients import gradient_table

bvalfn = 'bvals'
bvecfn = 'bvecs'

gtab = gradient_table(bvalfn, bvecfn)

bvals = 3000 * np.ones(160, dtype=np.int)
bvals[::10] = 0

bvecs = np.insert(gtab.bvecs[1:], np.arange(
    0, gtab.bvecs[1:].shape[0], 9), [0, 0, 0], axis=0)


with open('./bvals_with_b0s', 'w') as f:
    for bval in bvals:
        f.write('{} '.format(bval))

with open('./bvecs_with_b0s', 'w') as f:
    for i in range(3):
        for val in bvecs[:, i]:
            f.write('{} '.format(val))
        f.write('\n')
