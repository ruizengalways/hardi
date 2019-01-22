import sys
import numpy as np
import nibabel as nib


def MI(im1, im2, bins):
    # Mutual information for joint histogram

    hgram, _, _ = np.histogram2d(im1.ravel(), im2.ravel(), bins=bins)

    # Convert bins counts to probability values
    pxy = hgram / hgram.sum()

    px = pxy.sum(axis=1)  # marginal for x over y
    py = pxy.sum(axis=0)  # marginal for y over x
    px_py = px[:, None] * py[None, :]  # Broadcast to multiply marginals
    # Now we can do the calculation using the pxy, px_py 2D arrays
    nzs = pxy > 0  # Only non-zero pxy values contribute to the sum
    return np.sum(pxy[nzs] * np.log(pxy[nzs] / px_py[nzs]))


def main():
    try:
        k = int(sys.argv[1])
    except IndexError:
        k = 5
    try:
        nbins = int(sys.argv[2])
    except IndexError:
        nbins = 1024
    try:
        outputfn = sys.argv[3]
    except IndexError:
        outputfn = 'output.txt'

    basefn = './k{}/registered_k{}_n'.format(k, k)
    refvol = nib.load(
        'k{}/mean_registered_k{}_b0.nii.gz'.format(k, k)).get_data()

    MIs = []

    for i in np.arange(16, 160):
        print(i)
        testvol = nib.load(basefn + '{:04d}.nii.gz'.format(i)).get_data()
        MIs.append(MI(refvol, testvol, nbins))

    with open(outputfn, 'w') as f:
        f.write('Mean, Std\n')
        f.write('{}, {}'.format(np.mean(MIs), np.std(MIs)))


if __name__ == '__main__':
    main()
