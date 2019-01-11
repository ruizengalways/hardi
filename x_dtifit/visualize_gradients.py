import numpy as np
from dipy.core.gradients import gradient_table
from dipy.viz import window, actor

gtab = gradient_table('bvals', 'bvecs')

ren = window.Renderer()
ren.add(actor.point(gtab.bvecs[1:], window.colors.red, point_radius=0.01))
ren.add(actor.point(-gtab.bvecs[1:], window.colors.green, point_radius=0.01))
window.show(ren)
