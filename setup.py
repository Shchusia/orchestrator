import os

from setuptools import setup

module_name = 'orchestrator'
__version__ = '0.0.1'


def get_packages():
    ignore = ['__pycache__']

    list_sub_folders_with_paths = [x[0].replace(os.sep, '.')
                                   for x in os.walk("L3IMTPackages")
                                   if x[0].split(os.sep)[-1] not in ignore]
    return list_sub_folders_with_paths


setup(name=module_name,
      version=__version__,
      description='orchestrator for microservices architecture',
      author='Denis Shchutkiy',
      author_email='denisshchutskyi@gmail.com',
      url='https://github.com/Shchusia/orchestrator',
      packages=get_packages(),
      keywords=['pip', module_name],
      )
