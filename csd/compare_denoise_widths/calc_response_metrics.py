import numpy as np
import matplotlib.pyplot as plt
import harditools as hd


names = ['raw'] + ['denoised_k{}'.format(k) for k in [5, 7, 9]]
raw, d5, d7, d9 = [hd.load_obj(
    'responses/{}_response.pkl'.format(name)) for name in names]

fig, axes = plt.subplots(1, 2, figsize=(12, 6))
ax1, ax2 = axes

colors = ['k'] + ['C{}'.format(i) for i in range(3)]
n_groups = 4
bwidth = 0.8 / n_groups
ind = np.arange(raw.n.size)

for i, res in enumerate([raw, d5, d7, d9]):
    ax1.bar(ind + i * bwidth, abs(res.dwi_response), bwidth,
            color=colors[i], label=names[i])

ax1.set_xlabel('SH Degree')
ax1.set_ylabel('Coefficient')
ax1.set_title('Response coefficients')
ax1.set_xticks(ind + 1.5 * bwidth)
ax1.set_xticklabels(raw.n)
ax1.legend()

n_groups = 3
bwidth = 0.8 / n_groups

for i, res in enumerate([d5, d7, d9]):
    ax2.bar(ind + i * bwidth, hd.percdiff(abs(res.dwi_response),
                                          abs(raw.dwi_response)), bwidth,
            color=colors[i+1], label=names[i+1])

ax2.set_xlabel('SH Degree')
ax2.set_ylabel('Percent difference')
ax2.set_title('Percent difference from raw')
ax2.set_xticks(ind + 1.5 * bwidth)
ax2.set_xticklabels(raw.n)

fig.tight_layout()
plt.savefig('figs/response_SH.pdf')
