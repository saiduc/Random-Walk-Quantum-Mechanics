from lattice import Lattice
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


def iterate(dimensions, catch_prob, number_iterations):
    lattice = Lattice(dimensions)

    data = []
    for i in range(number_iterations):
        caught = False
        time = 0
        while not caught:
            time += 1
            lattice.move()
            caught = lattice.caught(catch_prob)
        data.append(time)

    return data


def exp_curve(n, q, arrest):
    return q * np.exp(-1 * arrest * n)


def exp_plot(data):
    nbins = max(data) - 1
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
    nbins = max(data) - 1
    plt.style.use("seaborn")

    hist = plt.hist(data, nbins, normed=True)
    plt.clf()

    x = hist[1][:-1]
    y = hist[0]
    popt, _ = curve_fit(exp_curve, x, y)

    plt.yscale("log")
    plt.plot(x, y, marker='.', ls=' ')
    plt.plot(x, exp_curve(x, *popt), c='r', label="Fitted Curve")

    plt.ylabel('Probability')
    plt.xlabel('Time Survived (no. of steps)')
    plt.legend()
    plt.show()
    return popt[1]


if __name__ == "__main__":
    data = iterate(3, 0.1, 1000)
    prob_arrest_curve = exp_plot(data)
    prob_arrest_line = line_plot(data)
