import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt


def corr(vol1, vol2):
    return np.corrcoef(vol1.flatten(), vol2.flatten())[0, 1]


volnums = np.hstack((range(8), range(9, 16)))

corr_w_rs = np.zeros(15)
corr_w0_rs = np.zeros(15)
corr_nw_rs = np.zeros(15)

w_basefn = './corratio_12_weighted_n8/corratio_12_n'
w0_basefn = './corratio_12_weighted_n0/corratio_12_n'
nw_basefn = './corratio_12/corratio_12_n'

ref = nib.load(w_basefn + '0008.nii.gz').get_data()

for j, n in enumerate(volnums):
    w_vol = nib.load(w_basefn + '{:04d}.nii.gz'.format(n)).get_data()
    corr_w_rs[j] = corr(ref, w_vol)

    w0_vol = nib.load(w0_basefn + '{:04d}.nii.gz'.format(n)).get_data()
    corr_w0_rs[j] = corr(ref, w0_vol)

    nw_vol = nib.load(nw_basefn + '{:04d}.nii.gz'.format(n)).get_data()
    corr_nw_rs[j] = corr(ref, nw_vol)

fig, ax = plt.subplots()

ax.plot(volnums, corr_w_rs, '.', label='Weighted: 8', ls='-')
ax.plot(volnums, corr_w0_rs, '.', label='Weighted: 0', ls='-')
ax.plot(volnums, corr_nw_rs, '.', label='Non-weighted', ls='-')
ax.plot([0, 15], [corr_w_rs.mean(), corr_w_rs.mean()], 'C0:')
ax.plot([0, 15], [corr_w0_rs.mean(), corr_w0_rs.mean()], 'C1:')
ax.plot([0, 15], [corr_nw_rs.mean(), corr_nw_rs.mean()], 'C2:')

ax.set_title('Correlation results: weighted vs. non-weighted')
ax.set_xlabel(r'$b_0$ number')
ax.set_ylabel('Correlation coefficient')
ax.legend()
plt.tight_layout()

plt.savefig('weighted_vs_nw.pdf')
