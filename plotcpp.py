import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def exp_curve(n, q, arrest):
    return q * np.exp(-1 * arrest * n)


def straight_line(n, arrest, c):
    return arrest * n + c


def exp_plot(data):
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
    return popt[1]


def line_plot(data):
    nbins = int(max(data) - 1)
    plt.style.use("seaborn")

    hist = plt.hist(data, nbins, normed=True)

    x = hist[1][:-1]
    y = np.log(hist[0])

    popt, _ = curve_fit(straight_line, x, y)

    plt.plot(x, straight_line(x, *popt), c='r', label="Fitted Line")

    plt.ylabel('Probability')
    plt.xlabel('Time Survived (log no. of steps)')
    plt.legend()
    plt.show()
    return popt[1]


if __name__ == "__main__":
    data = np.loadtxt("data.dat")
    prob_arrest_curve = exp_plot(data)
    # prob_arrest_line = line_plot(data)
