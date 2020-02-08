#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""The setup script."""
from setuptools import setup, find_packages

REPO_URL = 'https://github.com/UNCG-DAISY/psi-collect/'
DOCS_URL = 'https://psi-collect.readthedocs.io/en/latest/'

with open('README.md', 'r', encoding='utf8') as fh:
    long_description = fh.read()

setup(
    name='psi-collect',
    version='1.0.1',
    author='PSI Team',
    description='Collection, aggregation, and cataloging of NOAA post-storm emergency response imagery.',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Atmospheric Science',
    ],
    keywords='python',
    license='MIT license',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['requests', 'tqdm', 'pandas', 'Pillow', 'imageio'],
    # package_data={'': ['*.csv']},
    include_package_data=True,
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    project_urls={
        'Documentation': DOCS_URL,
        'Source': REPO_URL,
        'Tracker': REPO_URL + 'issues',
    },
    python_requires='>=3.6',
    entry_points={  # Executable scripts as command-line
        'console_scripts': [
            'pstorm=psicollect.common.pstorm:main',
        ],
    },
    url=REPO_URL,
    zip_safe=False,
)
