'''
Calculate the statistics of the RMSE between all registered volumes to the
reference volume. Call with:

python rmse.py [kernel width] [reference volume number]
'''

import sys
import numpy as np
import nibabel as nib


def rmse(vol1, vol2):
    return np.sqrt(np.mean((vol1 - vol2)**2))


def main():
    try:
        k = int(sys.argv[1])
    except IndexError:
        k = 5
    try:
        ref = int(sys.argv[2])
    except IndexError:
        ref = 8
    try:
        outputfn = sys.argv[3]
    except IndexError:
        outputfn = 'output.txt'

    basefn = './k{}/registered_k{}_n'.format(k, k)
    refvol = nib.load(basefn + '{:04d}.nii.gz'.format(ref)).get_data()

    rmses = []

    for i in np.arange(0, 16):
        if i == ref:
            pass
        else:
            testvol = nib.load(basefn + '{:04d}.nii.gz'.format(i)).get_data()
            rmses.append(rmse(refvol, testvol))

    with open(outputfn, 'w') as f:
        f.write('Mean, Std\n')
        f.write('{}, {}'.format(np.mean(rmses), np.std(rmses)))


if __name__ == '__main__':
    main()
