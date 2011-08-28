#!/usr/bin/env python2.7

from distutils.core import setup
import sys
import versioning

required_python_version = '2.7'
if sys.version < required_python_version:
    s = "I'm sorry, but %s %s requires Python %s or later."
    print(s % (name, version, required_python_version))
    sys.exit(1)

v = versioning.increment()
    
setup(name='azutils',
      version=v,
      description='Azala\'s Utilities',
      author='Azala',
      author_email='azalathemad@yahoo.com',
      packages=['azutils']
     )
