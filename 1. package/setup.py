#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 16:01:07 2025

@author: wang
"""
from setuptools import setup, find_packages

setup(
    name='team_10',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',  
        'pandas',    
        'python-dotenv',  
        'google-cloud-bigquery', 
        'matplotlib',  
        'seaborn',  
        'scikit-learn',  
        'numpy',  
    ],
)
