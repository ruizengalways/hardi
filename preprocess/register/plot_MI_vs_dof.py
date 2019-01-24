import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt


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


load = True
if load:
    print('Loading b0s')
    d3b0 = nib.load(
        './k5_MI_sinc_dof3_noweight/mean_registered_k5_b0.nii.gz').get_data()
    d6b0 = nib.load(
        './k5_MI_sinc_dof6_noweight/mean_registered_k5_b0.nii.gz').get_data()
    d9b0 = nib.load(
        './k5_MI_sinc_dof9_noweight/mean_registered_k5_b0.nii.gz').get_data()
    d12b0 = nib.load(
        './k5_MI_sinc_dof12_noweight/mean_registered_k5_b0.nii.gz').get_data()

    print('Loading diffs')
    d3full = nib.load(
        './k5_MI_sinc_dof3_noweight/registered_k5_full.nii.gz').get_data()
    d6full = nib.load(
        './k5_MI_sinc_dof6_noweight/registered_k5_full.nii.gz').get_data()
    d9full = nib.load(
        './k5_MI_sinc_dof9_noweight/registered_k5_full.nii.gz').get_data()
    d12full = nib.load(
        './k5_MI_sinc_dof12_noweight/registered_k5_full.nii.gz').get_data()

calc = True
if calc:
    nbins = 1024
    MI3 = []
    MI6 = []
    MI9 = []
    MI12 = []
    MI6w = []
    for i in range(16, 160):
        print(i)
        MI3.append(MI(d3b0, d3full[..., i], nbins))
        MI6.append(MI(d6b0, d6full[..., i], nbins))
        MI9.append(MI(d9b0, d9full[..., i], nbins))
        MI12.append(MI(d12b0, d12full[..., i], nbins))

plot = True
if plot:
    fig, ax = plt.subplots()
    ax.plot(MI3, label='DOF: 3')
    ax.plot(MI6, label='DOF: 6')
    ax.plot(MI9, label='DOF: 9')
    ax.plot(MI12, label='DOF: 12')
    ax.plot([0, 144], [np.mean(MI3), np.mean(MI3)], 'C0:')
    ax.plot([0, 144], [np.mean(MI6), np.mean(MI6)], 'C1:')
    ax.plot([0, 144], [np.mean(MI9), np.mean(MI9)], 'C2:')
    ax.plot([0, 144], [np.mean(MI12), np.mean(MI12)], 'C3:')
    ax.set_title('Mutual Information')
    ax.set_xlabel('Diffusion Direction Number')
    ax.set_ylabel('Mutual Information')
    plt.legend()
    plt.tight_layout()
    plt.savefig('./comparison_stats/MI_lineprofiles.pdf')

    fig2, axes = plt.subplots(4, 1, sharex=True)
    ax1, ax2, ax3, ax4 = axes

    nbins = 30

    ax1.hist(MI3, bins=nbins, color='C0')
    ax1.set_title('DOF: 3')

    ax2.hist(MI6, bins=nbins, color='C1')
    ax2.set_title('DOF: 6')

    ax3.hist(MI9, bins=nbins, color='C2')
    ax3.set_title('DOF: 9')

    ax4.hist(MI12, bins=nbins, color='C3')
    ax4.set_title('DOF: 12')
    ax4.set_xlabel('Mutual Information')

    plt.tight_layout()
    plt.savefig('./comparison_stats/MI_histograms.pdf')
