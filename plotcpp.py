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


def line_plot(data, show=True, skip=False):
    nbins = int(max(data) - 1)
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


if __name__ == "__main__":
    dimen = 3
    iteration = 1000000
    prob = 0.1
    potential = "square"
    boundary = 3

    # Any point that has 1 item in the bin has y=1/nbins and nbins = iteration
    # So if there are 1000 iterations, the lower limit will be 1/1000

    run_model(dimen, iteration, prob=prob)
    run_model(dimen, iteration, potential=potential, boundary=boundary)

    data = np.loadtxt("data.dat")
    prob_arrest_curve = exp_plot(data, show=True, skip=7)
    prob_arrest_line = line_plot(data, show=True, skip=7)

    print(prob_arrest_curve)
