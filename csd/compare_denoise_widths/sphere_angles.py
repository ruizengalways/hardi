import numpy as np
import harditools as hd
import matplotlib.pyplot as plt
from dipy.data import get_sphere


def get_min_angle(sph, ind):
    angs = hd.ang_distance(sph.vertices[ind][None, :], sph.vertices)
    angs.sort()
    angs = angs[angs >= 1e-3]
    return angs.min()


sph = get_sphere('symmetric724')
min_angs = np.array([get_min_angle(sph, i)
                     for i in range(sph.vertices.shape[0])])

plt.hist(min_angs, bins=512)
plt.xlabel('Separation angle ($\degree$)')
plt.ylabel('Counts')
plt.title('Angular separation between neighboring sample points')
plt.savefig('figs/spheredist.pdf')
