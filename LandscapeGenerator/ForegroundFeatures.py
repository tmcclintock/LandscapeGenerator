import numpy as np
import numpy.random as npr

class TreeFeature(object):
    def __init__(self, **kwargs):
        # all those keys will be initialized as class attributes
        allowed_keys = ['height', 'branch_radius', 'phi', 'distance',
                        'leaf_rgb_means', 'leaf_rgb_SDs',
                        'trunk_rgb_means', 'trunk_rgb_SDs']
        default_values = [3, 1.5, 30, 10,
                          [80, 160, 100], [2, 2, 2],
                          [105, 75, 50], [2, 2, 2]]
        # initialize all allowed keys to defaults
        self.__dict__.update((key, value) for key, value in
                             zip(allowed_keys, default_values))
        # and update the given keys by their given values
        self.__dict__.update((key, value) for key, value in
                             kwargs.items() if key in allowed_keys)
        self._phi_RAD = self.phi * np.pi/180
    
    def generate(self, LG):
        M, N = LG.dimensions
        theta, phi = LG._angles
        p = self._phi_RAD

        x, ht, rt = float(self.distance), float(self.height), \
            float(self.branch_radius)
        #Compute angles for all points
        theta_bottom = np.arctan2(-1, x)
        theta_leaves = np.arctan2(ht - LG.height - rt, x)
        theta_top = np.arctan2(ht - LG.height + rt, x)
        #Draw the trunk and assume that the width of the trunk is 0.5 m
        dphi_trunk = np.arctan(1./(4 * x)) #half width of trunk
        N_trunk = len(phi[(phi > p - dphi_trunk) * \
                       (phi < p + dphi_trunk)])
        for m in range(M):
            if (theta[m] > theta_bottom) and (theta[m] < theta_leaves):
                LG.rgb[m, (phi > p - dphi_trunk) * \
                       (phi < p + dphi_trunk), :]\
                       = self.trunk_rgb_means + self.trunk_rgb_SDs * \
                       npr.randn(N_trunk, 3)
                if N_trunk == 0:
                    LG.rgb[m, np.argmin(np.fabs(phi - p)), :]\
                        = self.trunk_rgb_means + self.trunk_rgb_SDs * \
                        npr.randn(1, 3)
            elif (theta[m] > theta_leaves) * (theta[m] < theta_top):
                yprime = x * np.tan(theta[m])
                dy = np.fabs(ht - LG.height - yprime) #distances from center of tree leaves
                dw = np.sqrt(rt**2 - dy**2) #half of chord length
                dphi = np.arctan(dw / x)
                N_leaves = len(phi[(phi > p - dphi) * \
                       (phi < p + dphi)])
                LG.rgb[m, (phi > p - dphi) * \
                       (phi < p + dphi), :]\
                       = self.leaf_rgb_means + self.leaf_rgb_SDs * \
                       npr.randn(N_leaves, 3)
        return
