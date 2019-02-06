import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
import tifffile as tf

load = True
plotfa = False
plotpdd = True


class tensorfit(object):
    def __init__(self, path):
        self.fa = nib.load(path + 'FA.nii.gz').get_data()
        self.pdd = nib.load(path + 'V1.nii.gz').get_data()


def ang_distance(dir1, dir2):
    ang = np.arccos((dir1 * dir2).sum(axis=1) /
                    (np.linalg.norm(dir1, axis=1) * np.linalg.norm(dir2, axis=1)))

    # Restricting to [0, pi] since pdd +- 180 = pdd
    ang = np.where(ang > np.pi/2, np.pi - ang, ang)

    ang *= (180/np.pi)
    return ang


if load:
    paths = ['raw/raw_'] + \
        ['denoised_k{0}/denoised_k{0}_'.format(k) for k in [5, 7, 9]]
    mask = nib.load(
        '../../preprocess/mask/denoised_k7_mask.nii.gz').get_data().astype('bool')
    raw, d5, d7, d9 = [tensorfit(path) for path in paths]

fns = ['d5', 'd7', 'd9']
if plotfa:
    # FA
    fig, axes = plt.subplots(3, 1, sharex=True, figsize=(12, 12))
    bins = 512
    names = ['FA: {0} x {0} x {0}'.format(i) for i in [5, 7, 9]]
    colors = ['C{}'.format(i) for i in range(3)]

    for i, (ax, d) in enumerate(zip(axes.flatten(), [d5, d7, d9])):
        diff = (d.fa - raw.fa) / raw.fa * 100
        diff[~mask] = 0
        counts, fas, _ = ax.hist(diff[mask],
                                 bins=bins, color=colors[i])
        ylow, yhigh = ax.get_ylim()
        ml_fa = (fas[np.argmax(counts)] + fas[np.argmax(counts) + 1]) / 2
        ax.plot([ml_fa, ml_fa], [ylow, yhigh],
                'k-', label='Peak: {:.2f}%\nStd: {:.1f}%'.format(ml_fa, diff[mask].std()))
        ax.set_title(names[i])
        ax.set_xlabel('Percent difference')
        ax.set_ylabel('Counts')
        ax.set_ylim([ylow, yhigh])
        ax.legend()

        tf.imsave('diff_volumes/' +
                  fns[i] + '_fa_absdif.tif', np.moveaxis(np.abs(diff).astype(np.float32), [0, 1, 2], [2, 0, 1]))

    plt.tight_layout()
    plt.savefig('figs/noreg_fa.pdf')

# PDD
if plotpdd:
    fig, axes = plt.subplots(3, 1, sharex=True, figsize=(12, 12))
    bins = 512
    names = ['PDD: {0} x {0} x {0}'.format(i) for i in [5, 7, 9]]
    colors = ['C{}'.format(i) for i in range(3)]

    for i, (ax, d) in enumerate(zip(axes.flatten(), [d5, d7, d9])):
        ang = ang_distance(raw.pdd.reshape(-1, 3), d.pdd.reshape(-1, 3))
        ang = ang.reshape((110, 74, 150))
        ang[np.isnan(ang)] = 0
        ang[~mask] = 0
        counts, angs, _ = ax.hist(ang[mask],
                                  bins=bins, color=colors[i])
        ml_ang = (angs[np.argmax(counts)] + angs[np.argmax(counts) + 1])/2
        ylow, yhigh = ax.get_ylim()
        xlow, xhigh = ax.get_xlim()
        ax.plot([ml_ang, ml_ang], [ylow, yhigh], 'k-',
                label='Peak: {:.1f}$\degree$'.format(ml_ang))
        ax.plot([ang[mask].mean(), ang[mask].mean()], [ylow, yhigh], 'k:',
                label='Mean: {:.1f}$\degree$'.format(ang[mask].mean()))
        ax.set_title(names[i])
        ax.set_xlabel('Angular difference ($\degree$)')
        ax.set_ylabel('Counts')
        ax.set_ylim([ylow, yhigh])
        ax.legend()
        ax.set_xticks(range(0, 91, 5))

        tf.imsave('diff_volumes/' +
                  fns[i] + '_pdd_dif.tif', np.moveaxis(ang.astype(np.float32),
                                                       [0, 1, 2], [2, 0, 1]))

    plt.tight_layout()
    plt.savefig('figs/noreg_pdd.pdf')

fig, axes = plt.subplots(3, 1, sharex=True, figsize=(12, 12))
bins = 512
names = ['PDD (FA > 0.7): {0} x {0} x {0}'.format(i) for i in [5, 7, 9]]
colors = ['C{}'.format(i) for i in range(3)]

for i, (ax, d) in enumerate(zip(axes.flatten(), [d5, d7, d9])):
    mask = d.fa > 0.7
    ang = ang_distance(raw.pdd.reshape(-1, 3), d.pdd.reshape(-1, 3))
    ang = ang.reshape((110, 74, 150))
    ang[np.isnan(ang)] = 0
    ang[~mask] = 0
    counts, angs, _ = ax.hist(ang[mask],
                              bins=bins, color=colors[i])
    ml_ang = (angs[np.argmax(counts)] + angs[np.argmax(counts) + 1])/2
    ylow, yhigh = ax.get_ylim()
    ax.plot([ml_ang, ml_ang], [ylow, yhigh], 'k-',
            label='Peak: {:.1f}$\degree$'.format(ml_ang))
    ax.plot([ang[mask].mean(), ang[mask].mean()], [ylow, yhigh], 'k:',
            label='Mean: {:.1f}$\degree$'.format(ang[mask].mean()))
    ax.set_title(names[i])
    ax.set_xlabel('Angular difference ($\degree$)')
    ax.set_ylabel('Counts')
    ax.set_ylim([ylow, yhigh])
    ax.set_xlim([xlow, xhigh])
    ax.legend()
    ax.set_xticks(range(0, 91, 5))

plt.tight_layout()
plt.savefig('figs/noreg_pdd_famask.pdf')
