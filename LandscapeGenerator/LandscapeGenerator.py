import numpy as np

class Landscape(object):
    def __init__(self, dimensions, kind="grassy-field"):
        self.dimensions = dimensions
        self.kind = kind

    def generate(self, seed = None):
        if seed:
            np.random.set_seed(seed)
        pass
