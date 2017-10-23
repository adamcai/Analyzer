from distutils.core import setup
from setuptools import find_packages

setup(
    name='analyzer',
    version='0.1dev',
    license='GNU',
    packages=['pyanalyzer', 'pyanalyzer.stats'],
    package_dir={'pyanalyzer': 'src/pyanalyzer'},
    long_description=open('README.md').read(),
)