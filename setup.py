"""
Setup module for install lib
"""
import os
from os import path
from typing import List

from setuptools import setup

MODULE_NAME = 'orchestrator_service'
LIB_NAME = 'orchestrator_service'
__version__ = '0.0.4'

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README_PYPI.MD'), encoding='utf-8') as f:
    long_description = f.read()


def get_packages() -> List[str]:
    """
    Help method
    :return: List[str] path to files and folders library
    """
    ignore = ['__pycache__']

    list_sub_folders_with_paths = [x[0].replace(os.sep, '.')
                                   for x in os.walk(MODULE_NAME)
                                   if x[0].split(os.sep)[-1] not in ignore]
    return list_sub_folders_with_paths


setup(name=LIB_NAME,
      version=__version__,
      description='orchestrator for microservices architecture',
      author='Denis Shchutkiy',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author_email='denisshchutskyi@gmail.com',
      url='https://github.com/Shchusia/orchestrator',
      packages=get_packages(),
      keywords=['pip', MODULE_NAME],
      )
