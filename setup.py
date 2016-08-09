from setuptools import setup, find_packages

requirements = ['nltk', 'bs4', 'unicodecsv']

setup(name='fbcanalyzer',
      version='1.0',
      description='Facebook chat analyzer',
      author='William Hammond',
      packages=find_packages(),
      include_package_data=True,
      install_requires=requirements)
