import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def exp_curve(n, q, arrest):
    return q * np.exp(-1 * arrest * n)


def exp_plot(data=np.loadtxt("data.dat")):
    nbins = int(max(data) - 1)
    plt.style.use("seaborn")

    hist = plt.hist(data, nbins, normed=True)

    x = hist[1][:-1]
    y = hist[0]
    popt, _ = curve_fit(exp_curve, x, y)

    plt.plot(x, exp_curve(x, *popt), c='r', label="Fitted Curve")

    plt.ylabel('Probability')
    plt.xlabel('Time Survived (no. of steps)')
    plt.legend()
    plt.show()


def line_plot(data=np.loadtxt("data.dat")):
    pass


if __name__ == "__main__":
    exp_plot()
