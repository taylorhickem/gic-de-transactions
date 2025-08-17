#!/usr/bin/env python3
"""Basic setup for convenient entry point """
# dependencies ----------------------------------------------------------------
from setuptools import setup, find_packages


# constants ----------------------------------------------------------------
APP_NAME = 'gicbank'


# setup --------------------------------------------------------------------
setup(
    name="gicbank",
    version=open('VERSION', 'r').read(),
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            f'{APP_NAME}=bank.ui:main',
        ],
    },
)
