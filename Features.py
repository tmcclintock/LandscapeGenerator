import numpy as np
import numpy.random as npr
from LandscapeGenerator import LGenerator

from abc import ABCMeta, abstractmethod
try:
    from six import with_metaclass
except ImportError:
    from future.utils import with_metaclass

class Feature(with_metaclass(ABCMeta, object)):
    """All actual features extend this class.

    """

    @abstractmethod
    def generate(self, LGenerator):
        pass

class SkyFeature(Feature):
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

    def generate(self, LG: LandscapeGenerator):
        M, N = LG.dimensions
        theta = LG._angles[0]
        M_hi = len(theta[theta > self.theta_boundary])
        means = self.rgb_means
        SDs = self.rgb_SDs
        #Loop over colors and draw
        for i in range(3):
            LG.rgb[theta > self.theta_boundary, :, i] = \
                means[i] + SDs[i]*npr.randn(M_hi * N).reshape((M_hi, N))
        return

class GrassFeature(Feature):
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

    def generate(self, LG: LandscapeGenerator):
        M, N = LG.dimensions
        theta = LG._angles[0]
        M_low = len(theta[theta <= self.theta_boundary])
        means = self.rgb_means
        SDs = self.rgb_SDs
        #Loop over colors and draw
        for i in range(3):
            LG.rgb[theta <= self.theta_boundary, :, i] = \
                means[i] + SDs[i]*npr.randn(M_low * N).reshape((M_low, N))
        return

class SunFeature(Feature):
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

    def generate(self, LG: LandscapeGenerator):
        M, N = LG.dimensions
        t, p = self.theta, self.phi
        t, p = t * np.pi/180, p * np.pi/180
        theta, phi = LG._angles
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
                    rgb[i, j] = means + SDs * npr.randn(3)
        return

class SkyGradientFeature(Feature):
    def __init__(self, **kwargs):
        # all those keys will be initialized as class attributes
        
        allowed_keys = ['theta_boundary', 'rgb_peak', 'decay_rates']
        default_values = [0, 2, [100, 0, 0], [1, 1, 1]]
        # initialize all allowed keys to defaults
        self.__dict__.update((key, value) for key, value in
                             zip(allowed_keys, default_values))
        # and update the given keys by their given values
        self.__dict__.update((key, value) for key, value in
                             kwargs.items() if key in allowed_keys)

    def generate(self, LG: LandscapeGenerator):
        M, N = LG.dimensions
        theta = LG._angles[0]
        M_hi = len(theta[theta > self.theta_boundary])
        peaks = self.rgb_peaks
        betas = 1./self.decay_rates
        #Loop over colors and draw
        for i in range(M_hi):
            for c in range(3):
                LG.rgb[M_hi - 1 - i, :, c] += \
                    peaks[c] * npr.exponential(scale = betas[c], N)
        return

