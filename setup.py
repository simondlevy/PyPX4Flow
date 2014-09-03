#!/usr/bin/env python

'''
setup.py - Python distutils setup file for PyPX4Flow package.

Copyright (C) 2014 Simon D. Levy

This code is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as 
published by the Free Software Foundation, either version 3 of the 
License, or (at your option) any later version.

This code is distributed in the hope that it will be useful,     
but WITHOUT ANY WARRANTY without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License 
along with this code.  If not, see <http://www.gnu.org/licenses/>.
'''

from distutils.core import setup

setup (name = 'PyPX4Flow',
    version = '0.1',
    description = 'PX4Flow sensor utility',
    packages = ['px4flow'],
    author='Simon D. Levy',
    author_email='simon.d.levy@gmail.com',
    url='http://home.wlu.edu/~levys/software/pypx4flow',
    license='LGPL',
    platforms='Linux; Windows; OS X'
    )
