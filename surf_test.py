import numpy as np
from mayavi import mlab

x, y = np.linspace(-2.5, 2.5, 250), np.linspace(-2.5, 2.5, 250)
x, y = np.meshgrid(x, y)
x, y = x.T, y.T


f = np.sin(x ** 2 + y ** 2)

mlab.figure(bgcolor=(1, 1, 1))

s = mlab.surf(x, y, f)
s.module_manager.scalar_lut_manager.lut_mode = 'viridis'

mlab.savefig('surf_test.pov', )
mlab.show()
