
from BatCurvInterp import BatCurvInterp
import numpy as np
import matplotlib.pylab as plt

vals = np.linspace(3.339999914, 4.199, 100)


# BEST IDENTIFIED POLYNOMIAL IS 8
bcinterp = BatCurvInterp(8)
print(bcinterp.interp_val([4, 4.1], False))

