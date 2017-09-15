#!/usr/bin/python
# docutils GLEP support
# Copyright (c) 2017 Gentoo Foundation
# Placed in public domain

from distutils.core import setup

setup(
    name='docutils_glep',
    version='0.5',
    author='Gentoo Foundation',
    author_email='glep@gentoo.org',
    url='http://github.com/gentoo/docutils-glep',

    packages=['docutils_glep', 'docutils_glep.html_writer'],
    package_data={'docutils_glep.html_writer': ['*.css', '*.txt']},
    scripts=['glep'],

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Other Audience',
        'License :: Public Domain',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Documentation'
    ]
)
