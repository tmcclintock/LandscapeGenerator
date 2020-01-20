import numpy as np

class LGenerator(object):
    """Object for generating landscapes.

    Args:
        dimensions (array): 1D list of length 2 that is
            M (number of rows) by N (number of columns)
        In progress

    """
    def __init__(self, dimensions,
                 field_of_view = [[-30, 30], [-30, 30]],
                 features = []):
                 
        #Asserts to check the input
        assert len(dimensions) == 2
        assert len(np.shape(dimensions)) == 1
        assert dimensions[0] > 0
        assert dimensions[1] > 0
        assert np.shape(field_of_view) == (2,2)
        assert field_of_view[0][0] != field_of_view[0][1]
        assert field_of_view[1][0] != field_of_view[1][1]
        assert type(features) == list

        self.dimensions = dimensions
        self.field_of_view = np.asarray(field_of_view)
        self._FOV_rad = self.field_of_view * np.pi/180
        self.features = features

        self.reset_canvas()
        
    def reset_canvas(self):
        M, N = self.dimensions
        self.rgb = np.zeros([M, N, 3])

        #vertical angle goes from 30 deg to -30 deg
        #this ordering accommodates matlpotlib's imshow default configuration
        theta_min, theta_max = self._FOV_rad[0]
        theta = np.linspace(theta_max, theta_min, M)
        #azimuthal angle goes from -30 to M,N * 30 degrees
        phi_min, phi_max = self._FOV_rad[1]
        phi = np.linspace(phi_min, phi_max, N)
        self._angles = [theta, phi]
        self._angles_mesh = np.meshgrid(theta, phi, indexing="ij")
        return

    def clear_features(self):
        self.features = []
        return
    
    def add_feature(self, feature):
        self.features.append(feature)
        return

    def get_angular_coordinates(self):
        return self._angles_mesh
    
    def generate(self, seed = None):
        if seed:
            np.random.seed(seed)

        for feature in self.features:
            feature.generate(self)
        return np.clip(self.rgb/255., 0, 1)
