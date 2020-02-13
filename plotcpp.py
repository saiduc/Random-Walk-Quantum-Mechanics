import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def func(n, q, arrest):
    return q * np.exp(-1 * arrest * n)


data = np.loadtxt("data.dat")
nbins = int(max(data) - 1)
hist = plt.hist(data, nbins, normed=True)

x = hist[1][:-1]
y = hist[0]
popt, _ = curve_fit(func, x, y)

plt.style.use("seaborn")
plt.plot(x, func(x, *popt), c='r', label="Fitted Curve")

plt.ylabel('Probability')
plt.xlabel('Time Survived (no. of steps)')
plt.legend()
plt.show()
