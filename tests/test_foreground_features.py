import LandscapeGenerator as LG
import LandscapeGenerator.ForegroundFeatures as LGF
import numpy as np
import numpy.testing as npt
import pytest

def test_Feature_creation():
    #Smoke tests
    LGF.TreeFeature()

def test_TreeFeature():
    M, N = 300, 200
    L = LG.LGenerator([M, N])
    L.add_feature(LGF.TreeFeature())
    rgb = L.generate()
    npt.assert_equal(len(rgb), M)
    npt.assert_equal(len(rgb[0]), N)
    npt.assert_equal(len(rgb[0][0]), 3)
    npt.assert_equal(rgb.shape, (M, N, 3))

def test_Tree_locations():
    M, N = 300, 200
    FOV = [[-10, 20], [0, 360]]
    L = LG.LGenerator([M, N], field_of_view=FOV)
    L.add_feature(LGF.TreeFeature(phi=0))
    rgb = L.generate()

if __name__ == "__main__":
    test_TreeFeature()
