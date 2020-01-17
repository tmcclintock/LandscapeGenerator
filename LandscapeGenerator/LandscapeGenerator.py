import numpy as np

class Landscape(object):
    def __init__(self, dimensions, kind="grassy-field"):
        assert len(dimensions) == 2
        assert len(np.shape(dimensions)) == 1
        self.dimensions = dimensions
        self.kind = kind

    def generate(self, seed = None):
        if seed:
            np.random.set_seed(seed)
        pass
