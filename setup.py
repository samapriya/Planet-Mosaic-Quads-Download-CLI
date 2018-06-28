import sys
import os
import sys
import setuptools
from setuptools import find_packages
from setuptools.command.test import test as TestCommand
from distutils.version import StrictVersion
from setuptools import __version__ as setuptools_version

if StrictVersion(setuptools_version) < StrictVersion('38.3.0'):
    raise SystemExit(
        'Your `setuptools` version is old. '
        'Please upgrade setuptools by running `pip install -U setuptools` '
        'and try again.'
    )
def readme():
    with open('README.md') as f:
        return f.read()
setuptools.setup(
    name='mosaic',
    version='0.0.1',
    packages=find_packages(),
    package_data={'mosaic': ['ids.csv','idmetadata.csv']},
    url='https://github.com/samapriya/Planet-Mosaic-Quads-Download-CLI',
    install_requires=['requests>=2.18.4','hurry.filesize>=0.9','planet>=1.1.0','psutil>=5.4.5','pyshp>=1.2.12',
                      'pytest>=3.5.1','requests-toolbelt>=0.8.0','retrying>=1.3.3',
                      'pypiwin32; platform_system == "Windows"','pywin32; platform_system == "Windows"'],
    license='Apache 2.0',
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: GIS',
    ),
    author='Samapriya Roy',
    author_email='samapriya.roy@gmail.com',
    description='Tool to download Planet Monthly Mosaic Quads',
    entry_points={
        'console_scripts': [
            'mosaic=mosaic.mosaic:main',
        ],
    },
)
