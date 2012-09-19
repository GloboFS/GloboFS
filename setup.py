#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

from globofs import __version__

setup(
    name='GloboFS',
    version=__version__,
    author='Shane R. Spencer',
    author_email='shane@bogomip.com',
    packages=['globofs'],
    url='https://github.com/whardier/GloboFS',
    license='MIT',
    description='Global Area Filesystem',
    long_description=open('README.md').read(),
    install_requires=[
        'fusepy >= 2.0.1',
    ],
    classifiers=[
        'Topic :: Communications :: File Sharing',
        'Topic :: Internet :: File Transfer Protocol (FTP)',
        'Topic :: System :: Distributed Computing',
        'Topic :: System :: Archiving',
        'Topic :: System :: Archiving :: Backup',
        'Topic :: System :: Archiving :: Compression',
        'Topic :: System :: Archiving :: Mirroring',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Development Status :: 1 - Planning',
        'Environment :: No Input/Output (Daemon)',
        'Environment :: Console',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
    ],
    entry_points={
        'console_scripts': [
            'globofs = globofs.console:run',
        ],
    }

)


