import LandscapeGenerator as LG
import numpy as np
import numpy.testing as npt
import pytest

def test_LGenerator():
    #Smoke tests
    L = LG.LGenerator([300, 200])
    L = LG.LGenerator([300, 200],
                      field_of_view = [[-20, 20], [-30, 30]])
    
def test_assertions():
    #Test pixel dimensions
    with npt.assert_raises(AssertionError):
        LG.LGenerator([0])
    with npt.assert_raises(AssertionError):
        LG.LGenerator([[0]])
    with npt.assert_raises(AssertionError):
        LG.LGenerator([100, 200, 300])
    with npt.assert_raises(AssertionError):
        LG.LGenerator([-100, 200])
    with npt.assert_raises(AssertionError):
        LG.LGenerator([100, -200])
    #Test fields of view
    with npt.assert_raises(AssertionError):
        LG.LGenerator([100, 200], [[0, 10, 20], [10, 20]])
    with npt.assert_raises(AssertionError):
        LG.LGenerator([100, 200], [[0, 10], [0, 10, 20]])
    with npt.assert_raises(AssertionError):
        LG.LGenerator([100, 200], [[10, 20], [10, 20], [10, 20]])
    with npt.assert_raises(AssertionError):
        LG.LGenerator([100, 200], [[0, 0], [0, 10]])
    with npt.assert_raises(AssertionError):
        LG.LGenerator([100, 200], [[0, 10], [0, 0]])

def test_generate():
    M, N = 300, 200
    L = LG.LGenerator([M, N])
    rgb = L.generate()
    npt.assert_equal(len(rgb), M)
    npt.assert_equal(len(rgb[0]), N)
    npt.assert_equal(len(rgb[0][0]), 3)
    npt.assert_equal(rgb.shape, (M, N, 3))

    t, p = L.get_angular_coordinates()
    npt.assert_equal(np.shape(rgb[:, :, 0]), t.shape)
    npt.assert_equal(t.shape, p.shape)
    npt.assert_equal(t.shape, [M, N])

    rgb1 = L.generate(seed = 123)
    rgb2 = L.generate(seed = 123)
    npt.assert_equal(rgb1, rgb2)

def test_reset_features():
    M, N = 300, 200
    L = LG.LGenerator([M, N])
    rgb1 = L.generate(seed=1)
    L.reset_canvas()
    rgb2 = L.generate(seed=1)
    npt.assert_equal(rgb1, rgb2)

def test_clear_features():
    import LandscapeGenerator.BackgroundFeatures as LGF

    M, N = 300, 200
    L = LG.LGenerator([M, N])
    L.add_feature(LGF.SkyFeature())
    L.clear_features()
    L.reset_canvas()
    rgb3 = L.generate(seed=1)
    npt.assert_equal(rgb3, np.zeros_like(rgb3))
#if __name__ == "__main__":
#    test_generate()
