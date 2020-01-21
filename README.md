# LandscapeGenerator [![Build Status](https://travis-ci.com/tmcclintock/LandscapeGenerator.svg?branch=master)](https://travis-ci.com/tmcclintock/LandscapeGenerator)

Generate synthetic landscape images at low resolution. For use in diagnosing ML systems.

## Installation

To install use

```bash
pip install -r requirements.txt
python setup.py install
```

The requirements are:

* `numpy`
* `scipy`
* `pytest` (for testing)
* `notebook` (for notebooks)
* `matplotlib` (for notebooks)

## Usage

See the example notebook in `notebooks/Example.ipynb`. Landscapes are constructed by adding features to the scene and then calling the `generate()` function. This function uses an RNG to assign pixel colors following the rules of the features in the landscape. The result are things like:

![alt text][example]

[example]: https://github.com/tmcclintock/LandscapeGenerator/blob/master/notebooks/images/example_landscape.png "Example landscape with trees"

This example landscape contains some sky features, a gradient in the sky to invoke a sunset, the sun, and a few dozen trees. The objects in the scene follow heuristics, but the pixel values themselves are the result of an RNG. Hence, landscape scenes like this can be used to double check that an ML algorithm is learning the image correctly.