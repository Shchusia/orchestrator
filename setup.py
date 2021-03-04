"""
Setup module for install lib
"""
import os
from typing import List

from setuptools import setup

MODULE_NAME = 'orchestrator'
__version__ = '0.0.1'


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

setup(name=MODULE_NAME,
      version=__version__,
      description='orchestrator for microservices architecture',
      author='Denis Shchutkiy',
      author_email='denisshchutskyi@gmail.com',
      url='https://github.com/Shchusia/orchestrator',
      packages=get_packages(),
      keywords=['pip', MODULE_NAME],
      )
