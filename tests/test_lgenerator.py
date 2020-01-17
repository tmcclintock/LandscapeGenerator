import LandscapeGenerator as LG
import numpy as np
import numpy.testing as npt
import pytest

def test_LGenerator():
    #Smoke tests
    L = LG.LGenerator([300, 200])
    L = LG.LGenerator([300, 200],
                      fields_of_view = [[-20, 20], [-30, 30]])


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

    rgb, [t, p] = L.generate(return_angular_coords = True)
    npt.assert_equal(np.shape(rgb[:, :, 0]), t.shape)
    npt.assert_equal(t.shape, p.shape)
    npt.assert_equal(t.shape, [M, N])

#if __name__ == "__main__":
#    test_generate()
