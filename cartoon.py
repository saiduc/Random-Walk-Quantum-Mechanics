import matplotlib.pyplot as plt
import numpy as np
import random

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
plt.savefig("./Paper/images/cartoon.pdf")
plt.show()
