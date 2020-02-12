from lattice import Lattice
import matplotlib.pyplot as plt

lat_3d = Lattice(3)
catch_prob = 0.1

data = []
for i in range(1000):
    caught = False
    time = 0
    while not caught:
        time += 1
        lat_3d.move()
        caught = lat_3d.caught(0.1)
    data.append(time)

nbins = max(data) - 1
hist = plt.hist(data, nbins)

plt.xlabel('Time (no. of steps)')
plt.show()
