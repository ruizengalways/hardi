import numpy as np
import matplotlib.pyplot as plt
from dipy.viz import window, actor
from dipy.data import get_sphere
from .reconst import Peaks


def quick_vis(obj, _slice=None, sphere=None):
    if sphere == None:
        sphere = get_sphere('symmetric724')

    ren = window.Renderer()

    if type(obj) == Peaks:
        if _slice is not None:
            ren.add(actor.peak_slicer(
                obj.peak_dirs[_slice], obj.peak_values[_slice]))
        else:
            ren.add(actor.peak_slicer(
                obj.peak_dirs, obj.peak_values))

    if type(obj) == np.ndarray:
        if _slice is not None:
            ren.add(actor.odf_slicer(obj[_slice], sphere=sphere, scale=0.9,
                                     norm=False))
        else:
            ren.add(actor.odf_slicer(obj, sphere=sphere, scale=0.9,
                                     norm=False))

    window.show(ren)


def plot_diff_hists(raw_data, denoised_data_list, metricfunc,
                    title, xlabel, ylabel='Counts',
                    show=True, save=False,
                    fn='diff_hists.pdf',
                    nbins=512, figsize=(12, 12),
                    xticks=None, plotmax=True,
                    sharex=True):

    fig, axes = plt.subplots(3, 1, sharex=sharex, figsize=figsize)
    names = ['{0} x {0} x {0}'.format(i) for i in [5, 7, 9]]
    colors = ['C{}'.format(i) for i in range(3)]

    for i, (ax, d) in enumerate(zip(axes.flatten(), denoised_data_list)):
        diff = metricfunc(d, raw_data)
        counts, bins, _ = ax.hist(diff, bins=nbins, color=colors[i])
        ylow, yhigh = ax.get_ylim()
        if plotmax:
            maxbin = (bins[np.argmax(counts)] +
                      bins[np.argmax(counts) + 1]) / 2
            ax.plot([maxbin, maxbin], [ylow, yhigh],
                    'k-', label='Max: {:.2f}\nStd: {:.1f}'.format(maxbin, diff.std()))
            ax.legend()
        ax.set_title(names[i])
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_ylim([ylow, yhigh])
        if xticks is not None:
            ax.set_xticks(xticks)

    plt.tight_layout()
    fig.subplots_adjust(top=0.92)
    fig.suptitle(title, fontweight='bold')

    if show:
        plt.show()
    if save:
        plt.savefig(fn)
    plt.close('all')


def boxprep(obj, mask):
    return obj.power[mask].reshape(-1, obj.power.shape[-1])
