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
    name='pbasemap',
    version='0.0.6',
    packages=find_packages(),
    package_data={'mosaic': ['ids.csv','idmetadata.csv']},
    url='https://github.com/samapriya/Planet-Mosaic-Quads-Download-CLI',
    install_requires=['requests>=2.19.1',
    'DateTimeRange>=0.5.5',
    'planet>=1.2.1',
    'psutil>=5.4.5',
    'pyshp>=1.2.12',
    'retrying>=1.3.3',
    'pySmartDL==1.2.5;python_version<"3.4"',
    'pySmartDL>=1.3.1;python_version>"3.4"',
    'geopandas>=0.4.0',
    'pypiwin32; platform_system == "Windows"','pywin32; platform_system == "Windows"'],
    license='Apache 2.0',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: GIS',
    ),
    author='Samapriya Roy',
    author_email='samapriya.roy@gmail.com',
    description='Tool to download Planet Monthly Mosaic Quads',
    entry_points={
        'console_scripts': [
            'pbasemap=pbasemap.pbasemap:main',
        ],
    },
)
