import numpy as np
import matplotlib.pyplot as plt
from hurst import compute_Hc, random_walk

# Use random_walk() function or generate a random walk series manually:
series = random_walk(99999, proba=500, cumprod=True)
# np.random.seed(42)
# random_changes = 1. + np.random.randn(99999) / 1000.
# series = np.cumprod(random_changes)  # create a random walk from random changes

# Evaluate Hurst equation
H, c, data = compute_Hc(series, kind='price', simplified=True)

# Plot
# f, ax = plt.subplots()
# ax.plot(data[0], c*data[0]**H, color="deepskyblue")
# ax.scatter(data[0], data[1], color="purple")
# ax.set_xscale('log')
# ax.set_yscale('log')
# ax.set_xlabel('Time interval')
# ax.set_ylabel('R/S ratio')
# ax.grid(True)
# plt.show()

print("H={:.4f}, c={:.4f}".format(H,c))