#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(name='cpcdemotools',
      version='0.2',
      description='Python tools for Amstrad CPC demoscene projects',
      author='Romain Giot',
      author_email='giot.romain@gmail.com',
      url='http://www.python.org/sigs/distutils-sig/',
      packages=[
          'cpcdemotools', 
          'cpcdemotools.source_checker',
          'cpcdemotools.sound',
          'cpcdemotools.curves',
          'cpcdemotools.graph',

      ],
      scripts=[
          'cpcdemotools/source_checker/z80_syntax_checker.py',
          'cpcdemotools/source_checker/vasm_symbols.py',
          'cpcdemotools/sound/ymreader.py',
          'cpcdemotools/curves/curves256.py',
 #         'cpcdemotools/graph/extract_pal.py',
          'cpcdemotools/crtc/crtc_transitions_helper.py',
          'cpcdemotools/graph/memorydraw.py'
    
      ]
     )



# metadata
__author__ = 'Romain Giot'
__copyright__ = 'Copyright 2012, Romain Giot'
__credits__ = ['Romain Giot']
__licence__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Romain Giot'
__email__ = 'giot.romain@gmail.com'
__status__ = 'Prototype'

