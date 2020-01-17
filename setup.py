from setuptools import setup

dist = setup(name="LandscapeGenerator",
             author="Tom McClintock",
             author_email="thmsmcclintock@gmail.com",
             version="0.1.0",
             description="Create synthetic landscape pictures for use in diagnosing ML algorithms.",
             url="https://github.com/tmcclintock/LandscapeGenerator",
             packages=['LandscapeGenerator'],
             install_requires=['numpy']
)
