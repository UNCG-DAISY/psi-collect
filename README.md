# Post-Storm Imagery Collection

[![Codecov](https://img.shields.io/codecov/c/gh/UNCG-DAISY/psi-collect)](
https://codecov.io/gh/UNCG-DAISY/psi-collect)
[![PyPI](https://img.shields.io/pypi/v/psi-collect)](
https://pypi.org/project/psi-collect)
[![Travis-CI](https://travis-ci.org/UNCG-DAISY/psi-collect.svg?branch=master)](
https://travis-ci.org/UNCG-DAISY/psi-collect)

[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/UNCG-DAISY/psi-collect/graphs/commit-activity)
[![Last Commit](https://img.shields.io/github/last-commit/UNCG-DAISY/psi-collect)](
https://github.com/UNCG-DAISY/psi-collect/commits/master)

[![JOSS](https://joss.theoj.org/papers/890cc9edd3ec2aafeba9616e8c5f7813/status.svg)](
https://joss.theoj.org/papers/890cc9edd3ec2aafeba9616e8c5f7813)
[![DOI](https://zenodo.org/badge/226186823.svg)](
https://zenodo.org/badge/latestdoi/226186823)

[![ReadTheDocs](https://readthedocs.org/projects/psi-collect/badge/?version=master)](
https://psi-collect.readthedocs.io/en/master/)
[![Documentation](https://img.shields.io/badge/Documentation-Click%20Me-brightgreen)](
https://psi-collect.readthedocs.io/en/master/)

This package downloads, catalogs, and stores [NOAA emergency response imagery]( https://storms.ngs.noaa.gov)

## Quick Start

There are two ways to get started with `psi-collect` — using the version on PyPI or installing directly from this GitHub repository. The version currently on PyPI does not work with images from the two most recent Hurricanes (Hx Delta and Hx Zeta). The version here on GitHub is modified and works with these storms (but we still need to make a few more modifications before this new version is packaged for PyPI).   

### from PyPI:

0. Install Python 3.6, 3.7, or 3.8 [**(Download Here)**](https://www.python.org/downloads/)
1. Run `pip3 install psi-collect` in your favorite terminal
2. Run `pstorm collect -h` for help on collecting images or `pstorm catalog -h` for help on cataloging local archives

### from GitHub Repository

0. Install Python 3.6, 3.7, or 3.8 [**(Download Here)**](https://www.python.org/downloads/)
1. Make sure you have dependecies installed (check them out in `requirements.txt`)
2. Run `pip install git+https://github.com/UNCG-DAISY/psi-collect` in your favorite terminal
3. Run `pstorm collect -h` for help on collecting images or `pstorm catalog -h` for help on cataloging local archives

### Usage Guide

Check out the documentation for [**Collecting**](https://psi-collect.readthedocs.io/en/master/collector/) and [**Cataloging**](https://psi-collect.readthedocs.io/en/master/cataloging/) images to see usage.

### An Example Use of `psi-collect`: Labeling Imagery

We labeled storm impacts for ~300 images from Hurricane Florence using the [Coastal Image Labeler](https://github.com/UNCG-DAISY/Coastal-Image-Labeler). The labels are available on [figshare](https://doi.org/10.6084/m9.figshare.11604192.v1).

The specific NOAA imagery to link to these labels can be retrieved with `psi-collect` via:

`pstorm collect -s Florence -a 20180917a_jpgs -d`

## Contributing / Developing

### Code of Conduct

We hope to foster an inclusive and respectful environment surrounding the contribution and discussion of our project.
Make sure you understand our [**Code of Conduct**](https://psi-collect.readthedocs.io/en/master/code_of_conduct/).

### Code Conventions

Before committing to the repository **please** read the project
[**Code Conventions**](https://psi-collect.readthedocs.io/en/master/contributing/).

### Project Pre-Requisites

1. Python 3.6, 3.7, or 3.8 [**(Download Here)**](https://www.python.org/downloads/)
2. Pipenv **(Run `pip install pipenv`)**
3. You will need to add the module path `<parent dir>/psi-collect/psicollect/` to your `PYTHONPATH`
   (See [**Configuring Module**](https://psi-collect.readthedocs.io/en/master/configure_python_path/))

*If you get an error message that looks something like `Module not found: "psicollect"`,
then the `PYTHONPATH` is not configured correctly!*

***You will need this in order to run the project.***

### Installing Dependencies for Development

1. Change current directory (`cd`) to `psi-collect/` (the project root)
2. Run `pipenv install --dev` to install dependencies
3. Run `pre-commit install` to install style checking when committing

### Testing the Collect Script

1. Change current directory to the collector module (`cd collector/`)
2. Either use `pipenv run collect.py <args>` or `pipenv shell` then `collect.py <args>`
3. In addition tests can be run using `pytest` from the project root directory


*The arguments for `collect.py` are listed [**here**](https://psi-collect.readthedocs.io/en/master/collector/)*

## NOAA Data 💾

- NOAA landing page for the post-storm Emergency Response Imagery, [**here**]( https://storms.ngs.noaa.gov)

## Team Members and contributors

- [**Matthew Moretz**](https://github.com/Matmorcat)
- [**Daniel Foster**](https://github.com/dlfosterbot)
- [**John Weber**](https://github.com/JWeb56)
- [**Rinty Chowdhury**](https://github.com/rintychy)
- [**Shah Nafis Rafique**](https://github.com/ShahNafisRafique)
- [**Jamison Valentine**](https://github.com/jamisonvalentine)
- [**Evan Goldstein**](https://github.com/ebgoldstein)
- [**Somya Mohanty**](https://github.com/somyamohanty)

