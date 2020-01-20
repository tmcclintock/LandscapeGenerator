import numpy as np
import numpy.random as npr

class SkyFeature(object):
    def __init__(self, **kwargs):
        # all those keys will be initialized as class attributes
        allowed_keys = ['theta_boundary', 'rgb_means', 'rgb_SDs']
        default_values = [0, [50, 100, 160], [7, 10, 12]]
        # initialize all allowed keys to defaults
        self.__dict__.update((key, value) for key, value in
                             zip(allowed_keys, default_values))
        # and update the given keys by their given values
        self.__dict__.update((key, value) for key, value in
                             kwargs.items() if key in allowed_keys)

    def generate(self, LG):
        M, N = LG.dimensions
        theta = LG._angles[0]
        M_hi = len(theta[theta > self.theta_boundary*np.pi/180])
        means = self.rgb_means
        SDs = self.rgb_SDs
        #Loop over colors and draw
        if M_hi == 0:
            return
        for i in range(3):
            LG.rgb[theta > self.theta_boundary * np.pi/180, :, i] = \
                means[i] + SDs[i]*npr.randn(M_hi * N).reshape((M_hi, N))
        return

class GrassFeature(object):
    def __init__(self, **kwargs):
        # all those keys will be initialized as class attributes
        allowed_keys = ['theta_boundary', 'rgb_means', 'rgb_SDs']
        default_values = [0, [50, 160, 70], [7, 12, 8]]
        # initialize all allowed keys to defaults
        self.__dict__.update((key, value) for key, value in
                             zip(allowed_keys, default_values))
        # and update the given keys by their given values
        self.__dict__.update((key, value) for key, value in
                             kwargs.items() if key in allowed_keys)

    def generate(self, LG):
        M, N = LG.dimensions
        theta = LG._angles[0]
        M_low = len(theta[theta <= self.theta_boundary])
        if M_low == 0:
            return
        means = self.rgb_means
        SDs = self.rgb_SDs
        #Loop over colors and draw
        for i in range(3):
            LG.rgb[theta <= self.theta_boundary*np.pi/180, :, i] = \
                means[i] + SDs[i]*npr.randn(M_low * N).reshape((M_low, N))
        return

class SunFeature(object):
    def __init__(self, **kwargs):
        # all those keys will be initialized as class attributes
        allowed_keys = ['theta', 'phi', 'angular_diameter',
                        'rgb_means', 'rgb_SDs']
        default_values = [15, 0, 2, [230, 230, 50], [15, 15, 7]]
        # initialize all allowed keys to defaults
        self.__dict__.update((key, value) for key, value in
                             zip(allowed_keys, default_values))
        # and update the given keys by their given values
        self.__dict__.update((key, value) for key, value in
                             kwargs.items() if key in allowed_keys)

    def generate(self, LG):
        M, N = LG.dimensions
        t, p = self.theta, self.phi
        t, p = t * np.pi/180, p * np.pi/180
        theta, phi = LG._angles
        THETA, PHI = LG._angles_mesh
        ti = np.where(np.abs(theta - t))
        pj = np.where(np.abs(phi - p))
        sin_t, cos_t = np.sin(t), np.cos(t)
        D = np.arccos(np.sin(THETA) * sin_t +\
                      np.cos(THETA) * cos_t * np.cos(PHI-p))
        diameter = self.angular_diameter * np.pi/180.
        means = self.rgb_means
        SDs = self.rgb_SDs
        for i in range(M):
            for j in range(N):
                if D[i, j] < diameter:
                    LG.rgb[i, j] = means + SDs * npr.randn(3)
        return

class SkyGradientFeature(object):
    def __init__(self, **kwargs):
        # all those keys will be initialized as class attributes
        allowed_keys = ['theta_boundary', 'rgb_peaks', 'decay_rates']
        default_values = [0, [100, 0, 0], [1, 1, 1]]
        # initialize all allowed keys to defaults
        self.__dict__.update((key, value) for key, value in
                             zip(allowed_keys, default_values))
        # and update the given keys by their given values
        self.__dict__.update((key, value) for key, value in
                             kwargs.items() if key in allowed_keys)
    
    def generate(self, LG):
        M, N = LG.dimensions
        theta = LG._angles[0]
        M_hi = len(theta[theta > self.theta_boundary*np.pi/180])
        peaks = self.rgb_peaks
        betas = 1./np.asarray(self.decay_rates)
        #Loop over colors and draw
        for i in range(M_hi):
            for c in range(3):
                LG.rgb[M_hi - 1 - i, :, c] += \
                    peaks[c] * npr.exponential(scale = betas[c] / (i + 1),
                                               size = N)
        return

