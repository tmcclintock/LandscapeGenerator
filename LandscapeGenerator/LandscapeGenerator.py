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

        if "scene" not in features:
            features["scene"] = "grassy-field"
                    
        self.dimensions = dimensions
        self.field_of_view = np.asarray(field_of_view)
        self._FOV_rad = self.field_of_view * np.pi/180
        self.features = features

    def generate(self, seed = None, return_angular_coords = False):
        if seed:
            np.random.seed(seed)

        M, N = self.dimensions
        rgb = np.zeros([M, N, 3])
        
        #vertical angle goes from 30 deg to -30 deg
        #this ordering accommodates matlpotlib's imshow default configuration
        theta_min, theta_max = self._FOV_rad[0]
        theta = np.linspace(theta_max, theta_min, M)
        #azimuthal angle goes from -30 to M,N * 30 degrees
        phi_min, phi_max = self._FOV_rad[1]
        phi = np.linspace(phi_min, phi_max, N)
        THETA, PHI = np.meshgrid(theta, phi, indexing="ij")
        
        #Scene is always in features
        if self.features["scene"] == "grassy-field":
            #Split by the horizon
            M_low = len(theta[theta <= 0])
            M_hi = len(theta[theta > 0])

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

        if "has_sun" in self.features:
            t, p = self.features["has_sun"] #theta and phi
            t, p = t * np.pi/180, p * np.pi/180 #convert degree coordinates to radians
            ti = np.where(np.abs(theta - t))
            pj = np.where(np.abs(phi - p))

            #From Earth, the sun is 0.5 deg in diameter (~pi/360 radians)
            #diameter = 
            sin_t, cos_t = np.sin(t), np.cos(t)
            #Compute angular distances
            D = np.arccos(np.sin(THETA) * sin_t + np.cos(THETA) * cos_t * np.cos(PHI-p))
            for i in range(M):
                for j in range(N):
                    if D[i, j] < np.pi/180:
                        rgb[i, j, :2] = np.random.poisson(230, size=2)
                        rgb[i, j, 2] = np.random.poisson(50)

        if return_angular_coords:
            return np.clip(rgb/255., 0, 1), [THETA, PHI]
        return np.clip(rgb/255., 0, 1)
