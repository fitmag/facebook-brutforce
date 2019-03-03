#!/usr/bin/python

# setup.py Authors:
#   walid fitmag

import os
import os.path

from distutils.core import setup

setup(
    name="wordlist",
    author="walid fitmag",
    description="facebook wordlist generator and brute forcing",
    license="Apache",
    url="https://github.com/fitmag/facebook-brutforce",
    scripts=[
        ("wordlist.py")
    ],
)
