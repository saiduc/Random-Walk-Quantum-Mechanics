from lattice import Lattice
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


def iterate(dimensions, number_iterations, maxSteps = None, catch_prob=0.1, potential=None, boundary=None):
    lattice = Lattice(dimensions)

    data = []
    for i in range(number_iterations):
        lattice = Lattice(dimensions)
        caught = False
        time = 0
        while caught is False:
            time += 1
            lattice.move()
            caught = lattice.caught(probability=catch_prob, potential=potential, boundary=boundary, maxSteps=maxSteps)
        data.append(time)

    return data


def exp_curve(n, q, arrest):
    return q * np.exp(-1 * arrest * n)


def exp_plot(data, show=True, skip=0, start=1):
    nbins = int(max(data) - start)
    plt.style.use("seaborn")

    hist = plt.hist(data, nbins, normed=True, align='mid')

    x = hist[1][skip:-1]
    y = hist[0][skip:]

    popt, _ = curve_fit(exp_curve, x, y)

    if show:
        plt.plot(x, exp_curve(x, *popt), c='r', label="Fitted Curve")

        plt.ylabel('Probability')
        plt.xlabel('Time Survived (no. of steps)')
        plt.legend()
        plt.show()
    return popt[1]


def cum_exp_plot(data, show=True, skip=0, start=1):
    nbins = int(max(data) - start)
    plt.style.use("seaborn")

    hist = plt.hist(data, nbins, normed=True, align='mid')
    plt.clf()

    x = hist[1][skip:-1]
    y = hist[0][skip:]

    # normalising it myself since normed=True doesn't seem to work
    # y = y/np.sum(y)
    cum_y = np.cumsum(y[::-1])[::-1]

    popt, _ = curve_fit(exp_curve, x, cum_y)

    if show:
        # plt.plot(x, cum_y)
        plt.bar(x, cum_y, width=1, align='center')
        plt.plot(x, exp_curve(x, *popt), c='r', label="Fitted Curve")

        plt.ylabel('Probability')
        plt.xlabel('Time Survived (no. of steps)')
        plt.legend()
        plt.show()

    return popt[1]


def line_plot(data, show=True, skip=0, start=1):
    nbins = int(max(data) - start)
    plt.style.use("seaborn")

    hist = plt.hist(data, nbins, normed=True)
    plt.clf()

    x = hist[1][skip:-1]
    y = hist[0][skip:]

    popt, _ = curve_fit(exp_curve, x, y)

    if show:
        plt.yscale("log")
        plt.plot(x, y, marker='.', ls=' ')
        plt.plot(x, exp_curve(x, *popt), c='r', label="Fitted Curve")

        plt.ylabel('log(Probability)')
        plt.xlabel('Time Survived (no. of steps)')
        plt.legend()
        plt.show()
    return popt[1]


def cum_line_plot(data, show=True, skip=0, start=1):
    nbins = int(max(data) - start)
    plt.style.use("seaborn")

    hist = plt.hist(data, nbins, normed=True)
    plt.clf()

    x = hist[1][skip:-1]
    y = hist[0][skip:]

    cum_y = np.cumsum(y[::-1])[::-1]

    popt, _ = curve_fit(exp_curve, x, cum_y)

    if show:
        plt.yscale("log")
        plt.plot(x, cum_y, marker='.', ls=' ')
        plt.plot(x, exp_curve(x, *popt), c='r', label="Fitted Curve")

        plt.ylabel('log(Probability)')
        plt.xlabel('Time Survived (no. of steps)')
        plt.legend()
        plt.show()
    return popt[1]


if __name__ == "__main__":
    dimensions = 1
    iterations = 100000
    maxSteps = 300
    potential = "square"
    boundary = 8

    # good parameters
    # dimensions = 1
    # iterations = 100000
    # maxSteps = 300
    # potential = "square"
    # boundary = 8

    data = iterate(dimensions, iterations, maxSteps=maxSteps, potential=potential, boundary=boundary)
    # data = iterate(3, 100000, catch_prob=0.1)
    prob_arrest_curve = exp_plot(data, show=False, skip=0, start=boundary)
    prob_arrest_line = line_plot(data, show=False, skip=0, start=boundary)
    prob_arrest_curve_cum = cum_exp_plot(data, show=False, skip=10, start=boundary)
    prob_arrest_line_cum = cum_line_plot(data, show=False, skip=10, start=boundary)

    print(prob_arrest_line_cum * boundary**2)
    print(np.pi**2/8)
