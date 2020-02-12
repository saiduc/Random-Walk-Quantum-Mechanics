from lattice import Lattice
import matplotlib.pyplot as plt

lat_3d = Lattice(3)

data = []
for i in range(1000):
    caught = False
    time = 0
    while not caught:
        time += 1
        lat_3d.move()
        caught = lat_3d.caught(0.7)
    data.append(time)

plt.hist(data, 30)
plt.show()
