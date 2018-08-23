#!/usr/bin/env python3

from distutils.core import setup

setup(name='Picker',
      version='1.0',
      description='Pick and open various handy links',
      author='Jeppe Petersen',
      author_email='jeppejp@gmail.com',
      url='',
      packages=['Picker',],
      entry_points = {
                      'console_scripts': [
                                          'picker = Picker.picker:main',
                                         ],              
                     },
     )
