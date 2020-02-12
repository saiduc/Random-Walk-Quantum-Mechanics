from lattice import Lattice

lat_3d = Lattice(3)

caught = False
time = 0

while not caught:
    time += 1
    lat_3d.move()
    caught = lat_3d.caught(0.9)

print(time)
