#!/usr/bin/env python

from distutils.core import setup

setup(name='html_doc',
      version='0.1',
      description='An extremely terse document generation library that uses html',
      author='Giles Barton-Owen',
      author_email='giles.bartonowen@gmail.com',
      url='',
      packages=['html_doc'],
      package_dir={'html_doc': 'html_doc'},
      package_data={'html_doc':['static/default.css']}
     )