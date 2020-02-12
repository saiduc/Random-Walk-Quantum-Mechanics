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

    def move(self):
        """
        takes input directions array and adds to coordinates
        """
        direction = random.randint(0, self.dimensions-1)
        distance = random.choice([-1,1])
        
        self.coordinates[direction] += distance

    def caught(self, probability):
        dist = random.uniform(0,1)
        if dist <= probability:
            return True
