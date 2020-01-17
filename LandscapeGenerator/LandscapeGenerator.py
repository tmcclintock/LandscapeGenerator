import numpy as np

class LGenerator(object):
    """Object for generating landscapes.

    Args:
        dimensions (array): 1D list of length 2 that is
            M (number of rows) by N (number of columns)
        kind (string): 

    """
    def __init__(self, dimensions,
                 field_of_view = [[-30, 30], [-30, 30]],
                 features = {"scene": "grassy-field"}):

        #Asserts to check the input
        assert len(dimensions) == 2
        assert len(np.shape(dimensions)) == 1
        assert dimensions[0] > 0
        assert dimensions[1] > 0
        assert np.shape(field_of_view) == (2,2)
        assert field_of_view[0][0] != field_of_view[0][1]
        assert field_of_view[1][0] != field_of_view[1][1]
                    
        self.dimensions = dimensions
        self.field_of_view = np.asarray(field_of_view)
        self._FOV_rad = self.field_of_view * np.pi/180
        self.features = features

    def generate(self, seed = None, return_angular_coords = False):
        if seed:
            np.random.seed(seed)

        M, N = self.dimensions
        if self.features["scene"] == "grassy-field":
            rgb = np.zeros([M, N, 3])

            #vertical angle goes from 30 deg to -30 deg
            #this ordering accommodates matlpotlib's imshow default configuration
            theta_min, theta_max = self._FOV_rad[0]
            theta = np.linspace(np.pi/6, -np.pi/6, M)
            M_low = len(theta[theta <= 0])
            M_hi = len(theta[theta > 0])
            #azimuthal angle goes from -30 to M,N * 30 degrees
            theta_min, theta_max = self._FOV_rad[1]
            phi = np.linspace(theta_min, theta_max, N)

            #First, draw small rs
            rgb[:, :, 0] = np.random.poisson(50, size=M*N).reshape((M, N))
            #Draw greens
            rgb[theta <= 0, :, 1] = np.random.poisson(160, size = M_low*N).reshape((M_low, N))
            rgb[theta > 0, :, 1] = np.random.poisson(100, size = M_hi*N).reshape((M_hi, N))
            #Draw blues
            rgb[theta <= 0, :, 2] = np.random.poisson(70, size = M_low*N).reshape((M_low, N))
            rgb[theta > 0, :, 2] = np.random.poisson(160, size = M_hi*N).reshape((M_hi, N))

            #Add a sunset
            for i in range(0, M//2):
                rgb[M//2 - 1 - i, :, 0] += np.random.poisson(100//(i+1), size=N)

        if return_angular_coords:
            return np.clip(rgb/255., 0, 1), np.meshgrid(theta, phi, indexing="ij")
        return np.clip(rgb/255., 0, 1)
