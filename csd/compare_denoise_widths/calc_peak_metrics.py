import numpy as np
import harditools as hd
import matplotlib.pyplot as plt

load = True
plotgfa = True
plotnpeaks = True
plotgreatestpeak = True
plotpower = True
plotangdiff = True


class csdfit(object):
    def __init__(self, name, mask):
        self.peaks = hd.load_obj('peaks/{}_peaks.pkl'.format(name))
        self.img, fod = hd.load_data('fods/{}_fod.nii.gz'.format(name))
        self.peaks.unflatten_all(mask)
        self.power = hd.reconst.sh_power(fod)


if load:
    print('Loading')
    names = ['raw', 'denoised_k5', 'denoised_k7', 'denoised_k9']
    mask = hd.load_mask('./data/mask.nii.gz')
    raw, d5, d7, d9 = [csdfit(name, mask) for name in names]


# 1) per-voxel GFA
if plotgfa:
    print('Plotting GFA')
    hd.vis.plot_diff_hists(raw.peaks.gfa[mask],
                           [d.peaks.gfa[mask] for d in [d5, d7, d9]],
                           metricfunc=hd.percdiff,
                           sharex=True,
                           title='GFA',
                           xlabel='Percent Difference',
                           show=False,
                           save=True,
                           fn='figs/gfa.pdf')

# 2) number of peaks
if plotnpeaks:
    print('Plotting Number of peaks')
    hd.vis.plot_diff_hists(raw.peaks.num_peaks()[mask],
                           [d.peaks.num_peaks()[mask]
                            for d in [d5, d7, d9]],
                           metricfunc=np.subtract,
                           nbins=np.arange(-4.5, 5.5),
                           title='Number of peaks',
                           xlabel='$N_{dn} - N_{raw}$',
                           show=False,
                           save=True,
                           fn='figs/numpeaks.pdf')


# 3) size of greatest peak
if plotgreatestpeak:
    print('Plotting height of greatest peak')
    hd.vis.plot_diff_hists(raw.peaks.peak_values[mask].max(axis=-1),
                           [d.peaks.peak_values[mask].max(
                               axis=-1) for d in [d5, d7, d9]],
                           metricfunc=hd.percdiff,
                           nbins=512,
                           title='Height of greatest peak',
                           xlabel='Percent difference',
                           show=False,
                           save=True,
                           fn='figs/greatestpeak.pdf')

# 4) Angular distance between first two peaks
if plotangdiff:
    print('Plotting angular distance between peaks')

    npeaks = 2

    # Intersection of all (x,y,z) where all 4 datasets have exactly
    # 2 peaks
    fullmask = np.logical_and.reduce((raw.peaks.peakmask(npeaks, comp='eq'),
                                      d5.peaks.peakmask(npeaks, comp='eq'),
                                      d7.peaks.peakmask(npeaks, comp='eq'),
                                      d9.peaks.peakmask(npeaks, comp='eq')))

    hd.vis.plot_diff_hists(raw.peaks.peak_dirs[fullmask][:, :2].reshape(-1, 3),
                           [d.peaks.peak_dirs[fullmask][:, :2].reshape(-1, 3)
                            for d in [d5, d7, d9]],
                           metricfunc=hd.ang_distance,
                           nbins=256,
                           xticks=np.arange(0, 91, 10),
                           plotmax=False,
                           sharex=False,
                           title='Angular separation',
                           xlabel='Angular separation ($\degree$)',
                           show=False,
                           save=True,
                           fn='figs/angdifference_firsttwo.pdf')


# 5) band power
if plotpower:
    print('Plotting SH power')

    # GFA >= 0
    gfa_thr = 0.0
    gfamask = d7.peaks.gfa >= gfa_thr
    fullmask = gfamask & mask

    figsize = (12, 12)
    metricfunc = hd.percdiff
    title = 'SH Power'
    show = False
    save = True
    fn = 'figs/shpower_gfa0.pdf'
    xlabel = 'Percent Difference'

    fig, axes = plt.subplots(3, 1, sharex=True, figsize=figsize)
    names = ['{0} x {0} x {0}'.format(i) for i in [5, 7, 9]]
    colors = ['C{}'.format(i) for i in range(3)]

    for i, (ax, d) in enumerate(zip(axes.flatten(), [hd.vis.boxprep(d, fullmask) for d in [d5, d7, d9]])):
        diff = (d - hd.vis.boxprep(raw, fullmask)) / \
            hd.vis.boxprep(raw, fullmask) * 100
        ax.boxplot(diff, 0, '', 0)
        ax.plot([0, 0], [0.5, d.shape[-1] + 0.5], 'k:')
        ax.set_title(names[i])
        ax.set_xlabel(xlabel)
        ax.set_ylabel('L$_{max}$')
        ax.set_yticklabels(np.arange(0, 2 * d.shape[-1], 2))

    xticks = ax.get_xticks()
    xticklabels = ax.get_xticklabels()

    plt.tight_layout()
    fig.subplots_adjust(top=0.92)
    fig.suptitle(title, fontweight='bold')

    if show:
        plt.show()
    if save:
        plt.savefig(fn)

    # GFA >= 0.85
    gfa_thr = 0.85
    gfamask = d7.peaks.gfa >= gfa_thr
    fullmask = gfamask & mask

    figsize = (12, 12)
    metricfunc = hd.percdiff
    title = 'SH Power (GFA > {})'.format(gfa_thr)
    show = False
    save = True
    fn = 'figs/shpower_gfa85.pdf'
    xlabel = 'Percent Difference'

    fig, axes = plt.subplots(3, 1, sharex=False, figsize=figsize)
    names = ['{0} x {0} x {0}'.format(i) for i in [5, 7, 9]]
    colors = ['C{}'.format(i) for i in range(3)]

    for i, (ax, d) in enumerate(zip(axes.flatten(), [hd.vis.boxprep(d, fullmask) for d in [d5, d7, d9]])):
        diff = (d - hd.vis.boxprep(raw, fullmask)) / \
            hd.vis.boxprep(raw, fullmask) * 100
        ax.boxplot(diff, 0, '', 0)
        ax.plot([0, 0], [0.5, d.shape[-1] + 0.5], 'k:')
        ax.set_title(names[i])
        ax.set_xlabel(xlabel)
        ax.set_ylabel('L$_{max}$')
        ax.set_yticklabels(np.arange(0, 2 * d.shape[-1], 2))
        ax.set_xticks(np.arange(-100, 301, 50))

    plt.tight_layout()
    fig.subplots_adjust(top=0.92)
    fig.suptitle(title, fontweight='bold')

    if show:
        plt.show()
    if save:
        plt.savefig(fn)
    plt.close('all')
