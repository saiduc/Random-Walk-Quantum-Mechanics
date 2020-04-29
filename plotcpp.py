import matplotlib
import matplotlib.cm as cm
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from subprocess import call
import warnings
from scipy.ndimage.filters import gaussian_filter
warnings.filterwarnings("ignore")

font = {'family': 'normal',
        'weight': 'bold',
        'size': 18}

matplotlib.rc('font', **font)


def run_model(dimen, iteration, maxSteps=0, prob=0.1, potential="", boundary=3, randomise=0, energy=0):
    print('Compiling...')
    call(['g++', 'lattice.cpp', '-o', 'lattice'])
    print('Compilation successful!')

    print('Running model...')
    call([
        './lattice',
        str(dimen),
        str(iteration),
        str(maxSteps),
        str(prob),
        str(potential),
        str(boundary),
        str(randomise),
        str(energy)
    ])
    print('Model complete!')


def exp_curve(n, q, arrest):
    return q * np.exp(-1 * arrest * n)


def exp_plot(data, show=True, skip=0, start=1):
    nbins = int(int(max(data) - start)/2)

    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')

    hist = plt.hist(data, nbins, normed=True, align='mid')

    x = hist[1][skip:-1]
    y = hist[0][skip:]

    if show:
        plt.bar(x, y, width=2, aligh='center')
        plt.ylabel('Probability of Death')
        plt.xlabel('Time Survived (no. of steps)')
        plt.tight_layout()
        # plt.savefig("./Paper/images/exp_plot.pdf")
        # plt.savefig("./Paper/images/exp_plot_cutoff.pdf")
        plt.show()


def cum_exp_plot(data, show=True, skip=0, start=1):
    nbins = int(int(max(data) - start)/2)

    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')

    hist = plt.hist(data, nbins, normed=False, align='mid')
    plt.clf()

    x = hist[1][skip:-1]
    y = hist[0][skip:]

    cum_y = np.cumsum(y[::-1])[::-1]
    cum_y = cum_y/max(cum_y)

    popt, pcov = curve_fit(exp_curve, x, cum_y, p0=[1.28, 0.019])

    if show:
        plt.bar(x, cum_y, width=2, align='center')
        plt.plot(x, exp_curve(x, *popt), c='r', label="Fitted Curve")

        plt.ylabel('Probability of Survival')
        plt.xlabel('Time Survived (no. of steps)')
        plt.legend()
        plt.tight_layout()
        # plt.savefig("./Paper/images/cum_exp_plot.pdf")
        # plt.savefig("./Paper/images/cum_exp_plot_cutoff.pdf")
        plt.show()

    residuals = cum_y - exp_curve(x, *popt)
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((cum_y-np.mean(cum_y))**2)
    r_squared = 1 - (ss_res / ss_tot)
    print("R^2 value is: ", r_squared)
    print("Gradient is: ", popt[1], " ± ", pcov[1])

    return popt[1]


def line_plot(data, show=True, skip=0, start=1):
    nbins = int(int(max(data) - start)/2)

    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')

    hist = plt.hist(data, nbins, normed=True)
    plt.clf()

    x = hist[1][skip:-1]
    y = hist[0][skip:]

    if show:
        plt.yscale("log")
        plt.plot(x, y, marker='.', ls=' ')

        plt.ylabel('Probability of Death')
        plt.xlabel('Time Survived (no. of steps)')
        plt.tight_layout()
        # plt.savefig("./Paper/images/line_plot.pdf")
        plt.show()


def cum_line_plot(data, show=True, skip=0, start=1):
    nbins = int(int(max(data) - start)/2)

    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')

    hist = plt.hist(data, nbins, normed=True)
    plt.clf()

    x = hist[1][skip:-1]
    y = hist[0][skip:]

    cum_y = np.cumsum(y[::-1])[::-1]
    cum_y = cum_y/max(cum_y)

    popt, pcov = curve_fit(exp_curve, x, cum_y, p0=[1.28, 0.019])

    if show:
        plt.yscale("log")
        plt.plot(x, cum_y, marker='.', ls=' ')
        plt.plot(x, exp_curve(x, *popt), c='r', label="Fitted Curve")

        plt.ylabel('Probability of Survival')
        plt.xlabel('Time Survived (no. of steps)')
        plt.legend()
        plt.tight_layout()
        # plt.savefig("./Paper/images/cum_line_plot.pdf")
        # plt.savefig("./Paper/images/cum_line_plot_cutoff.pdf")
        plt.show()

    residuals = cum_y - exp_curve(x, *popt)
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((cum_y-np.mean(cum_y))**2)
    r_squared = 1 - (ss_res / ss_tot)
    print("R^2 value is: ", r_squared)
    print("Gradient is: ", popt[1], " ± ", pcov[1])

    return popt[1]


def average_value(dimen, iteration, maxSteps=0, prob=0.1, potential="", boundary=3, skip=0, repeats=4):
    values = []
    for i in range(repeats):
        run_model(dimen,
                  iteration,
                  maxSteps=maxSteps,
                  potential=potential,
                  boundary=boundary)
        data = np.loadtxt("data.dat")
        prob_arrest_cum_line = cum_line_plot(
            data, show=False, skip=skip, start=boundary)
        values.append(prob_arrest_cum_line * boundary**2)

    items = np.array(values)
    items = items * boundary**2
    avg = np.average(items)
    error = np.std(items)
    print(avg, " ± ", error)
    return avg, error


def compare_boundaries(start, repeats):
    dimen = 1
    iteration = 1000000
    maxSteps = 0
    potential = "square"
    boundary = start

    alldataX = []
    alldataY = []
    labels = []
    allboundaries = []

    number = repeats
    for i in range(number):

        boundary += i

        run_model(dimen,
                  iteration,
                  maxSteps=maxSteps,
                  potential=potential,
                  boundary=boundary)

        data = np.loadtxt("data.dat")
        start = boundary
        skip = 100

        nbins = int(int(max(data) - start)/2)
        # plt.rc('text', usetex=True)
        plt.rc('font', family='serif')

        hist = plt.hist(data, nbins, normed=True)
        plt.clf()

        x = hist[1][skip:-1]
        y = hist[0][skip:]
        label = "J: " + str(boundary)

        alldataX.append(x)
        alldataY.append(y)
        labels.append(label)
        allboundaries.append(boundary)

    for i in range(number):
        cum_y = np.cumsum(alldataY[i][::-1])[::-1]

        popt, _ = curve_fit(exp_curve, alldataX[i], cum_y, p0=[1.28, 0.019])

        label = labels[i] + r", $\lambda J^2$: " + \
            str(popt[1] * allboundaries[i]**2)[:6]

        plt.yscale("log")
        plt.plot(alldataX[i], cum_y, marker='.', ls=' ', label=label)
        plt.plot(alldataX[i], exp_curve(alldataX[i], *popt), c='k')

    plt.ylabel('Probability of Survival')
    plt.xlabel('Time Survived (no. of steps)')
    plt.legend()
    plt.tight_layout()
    # plt.savefig("./Paper/images/multiplot.pdf")
    plt.show()


def spatial_plot(dimen, show=True, bins=100, sigma=16):
    nbins = bins

    positions = np.loadtxt("positions.dat")
    pos = [positions[n:n+dimen] for n in range(0, len(positions), dimen)]
    x_pos = []
    y_pos = []
    for i in pos:
        x_pos.append(i[0])
        y_pos.append(i[1])

    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')

    if show:

        heatmap, xedges, yedges = np.histogram2d(x_pos, y_pos, bins=nbins)
        heatmap = gaussian_filter(heatmap, sigma=sigma)
        extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

        img = heatmap.T
        plt.imshow(img, extent=extent, origin="lower", cmap=cm.jet)

        plt.ylabel('y Coordinate')
        plt.xlabel('x Coordinate')
        # plt.tight_layout()

        plt.show()


if __name__ == "__main__":

    dimen = 2
    iteration = 1000000
    maxSteps = 0
    potential = "circle"
    boundary = 20
    prob = 0.1
    randomise = 1
    energy = 2

    # constant potential
    if potential == "":
        run_model(dimen, iteration, prob=prob)
        data = np.loadtxt("data.dat")
        exp_plot(data, show=True, skip=0)
        line_plot(data, show=True, skip=0)

    # infinite square well
    if potential == "square":
        run_model(dimen,
                  iteration,
                  maxSteps=maxSteps,
                  potential=potential,
                  boundary=boundary)
        data = np.loadtxt("data.dat")
        exp_plot(data, show=True, skip=0, start=boundary)
        line_plot(data, show=True, skip=0, start=boundary)
        prob_arrest_cum_curve = cum_exp_plot(
            data, show=True, skip=100, start=boundary)
        prob_arrest_cum_line = cum_line_plot(
            data, show=True, skip=100, start=boundary)

        print(prob_arrest_cum_line * boundary**2)

        avg, error = average_value(
            1, 1000000, maxSteps=0, prob=0.1, potential="square", boundary=20, skip=100, repeats=10)
        print(avg, " ± ", error[1])

        compare_boundaries(14, 4)

    # circular well
    if potential == "circle":
        run_model(dimen,
                  iteration,
                  maxSteps=maxSteps,
                  potential=potential,
                  boundary=boundary,
                  randomise=randomise,
                  energy=energy)

        spatial_plot(dimen, show=True, bins=100, sigma=4)
