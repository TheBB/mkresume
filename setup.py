#!/usr/bin/env python

from setuptools import setup

setup(
    name='mkresume',
    version='0.1.0',
    description='Resume generator from template',
    maintainer='Eivind Fonn',
    maintainer_email='eivind.fonn@sintef.no',
    packages=['resume'],
    package_data={
        'resume': [
            'templates/*',
            'extra/awesome-cv.cls',
            'extra/fontawesome.sty',
            'extra/fonts/*.ttf',
        ],
    },
    install_requires=[
        'click',
        'click-pathlib',
        'goldpy>=2',
        'jinja2',
        'pydantic',
        'pybtex',
        'rich',
    ],
    entry_points={
        'console_scripts': [
            'mkresume=resume.__main__:main',
        ],
    },
)
