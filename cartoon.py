import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import random

font = {'family': 'normal',
        'weight': 'bold',
        'size': 18}

matplotlib.rc('font', **font)

length = 20
x = np.linspace(0, length, length+1)
y = [0]

for i in range(length):
    y.append(y[i] + random.choice([-1, 1]))

plt.rc("text", usetex=True)
plt.rc("font", family="Serif")
plt.plot(x, y, marker='o', markersize=20)
plt.xlabel("Step Number")
plt.ylabel("Position")
plt.tight_layout()
plt.savefig("./Paper/images/cartoon.pdf")
plt.show()
