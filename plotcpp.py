import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from subprocess import call


def run_model():
    print('compiling')
    call(['g++', 'lattice.cpp', '-o', 'lattice'])
    print('compilation successful')

    print('running model')
    call(['./lattice'])
    print('model complete')


def exp_curve(n, q, arrest):
    return q * np.exp(-1 * arrest * n)


def exp_plot(data, show=True):
    nbins = int(max(data) - 1)
    plt.style.use("seaborn")

    hist = plt.hist(data, nbins, normed=True)

    x = hist[1][:-1]
    y = hist[0]
    popt, _ = curve_fit(exp_curve, x, y)

    if show:
        plt.plot(x, exp_curve(x, *popt), c='r', label="Fitted Curve")

        plt.ylabel('Probability')
        plt.xlabel('Time Survived (no. of steps)')
        plt.legend()
        plt.show()
    return popt[1]


def line_plot(data, show=True):
    nbins = int(max(data) - 1)
    plt.style.use("seaborn")

    hist = plt.hist(data, nbins, normed=True)
    plt.clf()

    x = hist[1][:-1]
    y = hist[0]
    popt, _ = curve_fit(exp_curve, x, y)

    if show:
        plt.yscale("log")
        plt.plot(x, y, marker='.', ls=' ')
        plt.plot(x, exp_curve(x, *popt), c='r', label="Fitted Curve")

        plt.ylabel('Probability')
        plt.xlabel('Time Survived (no. of steps)')
        plt.legend()
        plt.show()
    return popt[1]


# def straight_line(n, arrest, c):
#     return arrest * n + c

# def line_plot(data):
#     """
#     This is broken since I should not be converting the data to log.
#     I should just be plotting the yscale in log
#     This is because if I convert the data to logs and do curve_fit,
#     the straight_line function has the wrong weightings
#     """
#     nbins = int(max(data) - 1)
#     plt.style.use("seaborn")

#     hist = plt.hist(data, nbins, normed=True)
#     plt.clf()

#     x = hist[1][:-1]
#     y = np.log(hist[0])

#     # Removing -inf values
#     indices = [i for i in range(len(y)) if np.isinf(y[i])]
#     x = np.delete(x, indices)
#     y = np.delete(y, indices)

#     popt, _ = curve_fit(straight_line, x, y)

#     plt.plot(x, straight_line(x, *popt), c='r', label="Fitted Line")

#     plt.plot(x,y)

#     plt.ylabel('Probability (log K)')
#     plt.xlabel('Time Survived (no. of steps)')
#     plt.legend()
#     plt.show()
#     return popt[1]


if __name__ == "__main__":
    run_model()
    data = np.loadtxt("data.dat")
    prob_arrest_curve = exp_plot(data, show=False)
    prob_arrest_line = line_plot(data, show=False)
    print(prob_arrest_curve)
