#!/usr/bin/env python
from setuptools import setup

setup(python_requires='>=3.6',
      entry_points={'console_scripts':
                    ['gitbranch = gitbranch:main',
                     'gtps = gtps:main',
                     'ActOnChanged = ActOnChanged:main',
                     'gitemail = gitemail:main']},)
