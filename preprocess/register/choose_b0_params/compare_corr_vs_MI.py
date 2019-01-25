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


def corr(vol1, vol2):
    return np.corrcoef(vol1.flatten(), vol2.flatten())[0, 1]


calc = False
if calc:
    dofs = np.array([3, 6, 9, 12])
    volnums = np.hstack((range(8), range(9, 16)))

    # ANALYZING corratio COST FUNCTION
    corr_rs = np.zeros((4, 15))
    for i, dof in enumerate(dofs):
        print('Cost: corratio, dof: {}'.format(dof))
        basefn = './corratio_{dof}/corratio_{dof}_n'.format(dof=dof)
        ref = nib.load(basefn + '0008.nii.gz').get_data()

        for j, n in enumerate(volnums):
            vol = nib.load(basefn + '{:04d}.nii.gz'.format(n)).get_data()
            corr_rs[i, j] = corr(ref, vol)

    # ANALYZING mutualinfo COST FUNCTION
    mutualinfo_MIs = np.zeros((4, 15))
    # mutualinfo_rs = np.zeros((4, 15))
    for i, dof in enumerate(dofs):
        print('Cost: mutualinfo, dof: {}'.format(dof))
        basefn = './mutualinfo_{dof}/mutualinfo_{dof}_n'.format(dof=dof)
        ref = nib.load(basefn + '0008.nii.gz').get_data()

        for j, n in enumerate(volnums):
            vol = nib.load(basefn + '{:04d}.nii.gz'.format(n)).get_data()
            mutualinfo_MIs[i, j] = MI(ref, vol, 256)

# Getting optimal choice
choices = [np.argmax(f.mean(axis=1))
           for f in [corr_rs, mutualinfo_MIs]]
values = [f[choice].mean()
          for f, choice in zip([corr_rs, mutualinfo_MIs], choices)]

# PLOTTING corratio COST FUNCTION
fig, axes = plt.subplots(1, 2, figsize=(12, 6))
ax1, ax2 = axes

for i, dof in enumerate(dofs):
    color = 'C{}'.format(i)
    ax1.plot(volnums, corr_rs[i], '.',
             label='DOF: {}'.format(dof), c=color, ls='-')
    ax1.plot([0, 15], [corr_rs[i].mean(), corr_rs[i].mean()], c=color, ls=':')
ax1.set_title('Correlation results: corratio cost function\nBest: DOF = {}'.format(
    dofs[choices[0]]))
ax1.set_xlabel(r'$b_0$ number')
ax1.set_ylabel('Correlation coefficient')
ax1.legend()

for i, dof in enumerate(dofs):
    color = 'C{}'.format(i)
    ax2.plot(volnums, mutualinfo_MIs[i], '.',
             label='DOF: {}'.format(dof), c=color, ls='-')
    ax2.plot([0, 15], [mutualinfo_MIs[i].mean(),
                       mutualinfo_MIs[i].mean()], c=color, ls=':')
ax2.set_title('Mutual information results: mutualinfo cost function\nBest: DOF = {}'.format(
    dofs[choices[1]]))
ax2.set_xlabel(r'$b_0$ number')
ax2.set_ylabel('Mutual information')
ax2.legend()

plt.tight_layout()
plt.savefig('b0_corr_vs_MI_results.pdf')
