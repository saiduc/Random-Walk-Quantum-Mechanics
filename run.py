from lattice import Lattice
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

lat_3d = Lattice(3)
catch_prob = 0.1

data = []
for i in range(1000):
    caught = False
    time = 0
    while not caught:
        time += 1
        lat_3d.move()
        caught = lat_3d.caught(0.1)
    data.append(time)

nbins = max(data) - 1
hist = plt.hist(data, nbins, normed=True)


def fit(n, q, arrest):
    return q * np.exp(-1 * arrest * n)


x = hist[1][:-1]
y = hist[0]
popt, _ = curve_fit(fit, x, y)

plt.plot(x, fit(x, *popt), c='r')


plt.xlabel('Time (no. of steps)')
plt.show()
