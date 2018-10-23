from setuptools import setup, find_packages

setup(name='pypif-sdk',
      version='2.2.1',
      url='http://github.com/CitrineInformatics/pypif-sdk',
      description='High level support for working with Physical Information Files (PIF)',
      author='Max Hutchinson',
      author_email='maxhutch@citrine.io',
      packages=find_packages(),
      install_requires=[
          'pypif>=2.00,<5',
          'citrination_client>=3,<5',
          'toolz'
      ])
