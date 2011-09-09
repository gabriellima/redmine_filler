from setuptools import setup, find_packages
from redmine_filler import __version__

README = open('README.rst').read()

setup(name='redmine_filler',
      version=__version__,
      description="Redmine Filler",
      long_description=README,
      author='Gabriel L. Oliveira',
      author_email='ciberglo@gmail.com',
      packages=find_packages(),
      include_package_data=True,
      install_requires=['splinter'],
      test_requires=['nose'],
      )

