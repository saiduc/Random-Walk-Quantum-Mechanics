import numpy as np
import random


class Lattice:
    """
    Class of lattice.
    Takes init parameter: number of dimensions
    """
    def __init__(self, dimensions):
        self.dimensions = dimensions
        self.coordinates = np.zeros(dimensions, dtype='int')
        self.numberSteps = 0

    def move(self):
        """
        takes input directions array and adds to coordinates
        """
        direction = random.randint(0, self.dimensions-1)
        distance = random.choice([-1, 1])
        self.coordinates[direction] += distance
        self.numberSteps += 1

    def caught(self, probability=0.1, potential=None, boundary=None, maxSteps=None):

        if (maxSteps is None) or (self.numberSteps < maxSteps):
            if potential is None:
                dist = random.uniform(0, 1)
                if dist <= probability:
                    return True
                else:
                    return False

            elif potential == "square":
                for coordinate in self.coordinates:
                    if not (-1*boundary < coordinate < boundary):
                        return True
                return False

        else:
            return True
