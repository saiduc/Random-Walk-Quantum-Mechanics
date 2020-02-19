import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from subprocess import call


def run_model(dimen, iteration, prob=0.1, potential="", boundary=3):
    print('Compiling...')
    call(['g++', 'lattice.cpp', '-o', 'lattice'])
    print('Compilation successful!')

    print('Running model...')
    call([
        './lattice',
        str(dimen),
        str(iteration),
        str(prob), potential,
        str(boundary)
    ])
    print('Model complete!')


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


def cum_exp_plot(data, show=True, start=1):
    nbins = int(max(data) - start)
    plt.style.use("seaborn")

    hist = plt.hist(data, nbins, normed=True, align='mid')
    plt.clf()

    x = hist[1][:-1]
    y = hist[0]

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


def cum_line_plot(data, show=True, start=1):
    nbins = int(max(data) - start)
    plt.style.use("seaborn")

    hist = plt.hist(data, nbins, normed=True)
    plt.clf()

    x = hist[1][:-1]
    y = hist[0]

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

    dimen = 1
    iteration = 1000000

    prob = 0.1

    potential = "square"
    boundary = 11

    # Any point that has 1 item in the bin has y=1/nbins and nbins = iteration
    # So if there are 1000 iterations, the lower limit will be 1/1000

    # constant potential example
    if potential == "":
        run_model(dimen, iteration, prob=prob)
        data = np.loadtxt("data.dat")
        prob_arrest_curve = exp_plot(data, show=True, skip=0)
        prob_arrest_line = line_plot(data, show=True, skip=0)

    # infinite square well
    if potential == "square":
        run_model(dimen, iteration, potential=potential, boundary=boundary)
        data = np.loadtxt("data.dat")
        prob_arrest_curve = exp_plot(data, show=True, skip=0, start=boundary)
        prob_arrest_line = line_plot(data, show=True, skip=0, start=boundary)
        prob_arrest_cum_curve = cum_exp_plot(data, show=True, start=boundary)
        prob_arrest_cum_line = cum_line_plot(data, show=True, start=boundary)

        print(prob_arrest_cum_curve * boundary**2)
