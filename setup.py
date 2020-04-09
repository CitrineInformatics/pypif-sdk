from setuptools import setup, find_packages

setup(name='pypif-sdk',
      version='2.4.0',
      url='http://github.com/CitrineInformatics/pypif-sdk',
      description='High level support for working with Physical Information Files (PIF)',
      author='Max Hutchinson',
      author_email='maxhutch@citrine.io',
      packages=find_packages(),
      package_data={'pypif_sdk' : ['func/elements.json']},
      install_requires=[
          'pypif>=2.0.0,<4',
          'citrination_client>=3,<7',
          'toolz',
      ])
