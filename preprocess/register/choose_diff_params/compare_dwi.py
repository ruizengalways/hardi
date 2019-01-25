import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt


def MI(im1, im2, bins=256):
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


calc = False
if calc:
    dofs = np.array([3, 6, 9, 12])
    volnums = np.arange(16, 160)
    weightstrs = ['w', 'nw']
    ref = nib.load('../registered_b0/mean_registered_b0.nii.gz').get_data()

    # shape = (weighting, dof, volume)
    MIs = np.zeros((2, dofs.size, volnums.size))

    for i, weighting in enumerate(weightstrs):
        for j, dof in enumerate(dofs):
            basefn = 'dof{}_{}'.format(dof, weighting)
            print(basefn)
            for k, n in enumerate(volnums):
                print(n)
                vol = nib.load(
                    basefn + '/{}_n{:04d}.nii.gz'.format(basefn, n)).get_data()
                MIs[i, j, k] = MI(ref, vol)

# Getting optimal choice
choices = MIs.mean(axis=2).argmax(axis=1)  # DOF index for w and nw
values = MIs.mean(axis=2).max(axis=1)

# PLOTTING corratio COST FUNCTION
fig, ax = plt.subplots(1, 2, figsize=(12, 6))
title = ['Weighted', 'Non-weighted']

for i, weighting in enumerate(weightstrs):
    for j, dof in enumerate(dofs):
        color = 'C{}'.format(j)
        ax[i].plot(1+np.arange(144), MIs[i, j], '.', label='DOF: {}'.format(dof),
                   c=color, ls='-')
        ax[i].plot([1, 144], [MIs[i, j].mean(),
                              MIs[i, j].mean()], c=color, ls=':')
        ax[i].set_title('Mutual information results: {}\nBest: DOF = {}, MI={}'.format(
            title[i], dofs[choices[i]], values[i].round(4)))
        ax[i].set_xlabel('DWI number')
        ax[i].set_ylabel('Mutual Information')
        ax[i].legend()

ax[0].set_ylim(ax[1].get_ylim())

plt.tight_layout()
plt.savefig('dwi_MI_results.pdf')
