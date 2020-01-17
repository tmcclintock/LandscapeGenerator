import LandscapeGenerator as LG
import numpy as np
import numpy.testing as npt
import pytest

def test_LGenerator():
    #Smoke test
    L = LG.LGenerator([300, 200])

def test_assertions_in_LGenerator():
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
