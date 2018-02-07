from setuptools import setup, find_packages

setup(name='pypif-sdk',
      version='2.1.0',
      url='http://github.com/CitrineInformatics/pypif-sdk',
      description='High level support for working with Physical Information Files (PIF)',
      author='Max Hutchinson',
      author_email='maxhutch@citrine.io',
      packages=find_packages(),
      install_requires=[
          'pypif>=2.0.0,<4',
          'citrination_client>=3,<4',
          'toolz'
      ])
