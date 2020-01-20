import LandscapeGenerator as LG
import LandscapeGenerator.BackgroundFeatures as LGF
import numpy as np
import numpy.testing as npt
import pytest

def test_Feature_creation():
    #Smoke tests
    LGF.SkyFeature()
    LGF.GrassFeature()
    LGF.SunFeature()
    LGF.SkyGradientFeature()

def test_SkyFeature():
    M, N = 300, 200
    L = LG.LGenerator([M, N])
    L.add_feature(LGF.SkyFeature())
    rgb = L.generate()
    npt.assert_equal(len(rgb), M)
    npt.assert_equal(len(rgb[0]), N)
    npt.assert_equal(len(rgb[0][0]), 3)
    npt.assert_equal(rgb.shape, (M, N, 3))

def test_GrassFeature():
    M, N = 100, 50
    L = LG.LGenerator([M, N])
    L.add_feature(LGF.GrassFeature())
    rgb = L.generate()
    npt.assert_equal(len(rgb), M)
    npt.assert_equal(len(rgb[0]), N)
    npt.assert_equal(len(rgb[0][0]), 3)
    npt.assert_equal(rgb.shape, (M, N, 3))

def test_SunFeature():
    M, N = 150, 250
    L = LG.LGenerator([M, N])
    L.add_feature(LGF.SunFeature())
    rgb = L.generate()
    npt.assert_equal(len(rgb), M)
    npt.assert_equal(len(rgb[0]), N)
    npt.assert_equal(len(rgb[0][0]), 3)
    npt.assert_equal(rgb.shape, (M, N, 3))

def test_SkyGradientFeature():
    M, N = 120, 120
    L = LG.LGenerator([M, N])
    L.add_feature(LGF.SkyGradientFeature())
    rgb = L.generate()
    npt.assert_equal(len(rgb), M)
    npt.assert_equal(len(rgb[0]), N)
    npt.assert_equal(len(rgb[0][0]), 3)
    npt.assert_equal(rgb.shape, (M, N, 3))
