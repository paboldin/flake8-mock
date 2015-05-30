# -*- coding: utf-8 -*-
from __future__ import with_statement

from setuptools import setup


def get_version(fname='mock_check.py'):
    with open(fname) as f:
        for line in f:
            if line.startswith('__version__'):
                return eval(line.split('=')[-1])


setup(
    name='mock_check',
    version=get_version(),
    description="Mock naming checker",
    keywords='flake8 mock check',
    author='Pavel Boldin',
    author_email='boldin.pavel@gmail.com',
    url='https://github.com/paboldin/mock-check',
    license='Expat license',
    py_modules=['mock_check'],
    zip_safe=False,
    test_suite='test_mock_check',
    entry_points={
        'flake8.extension': [
            'C100 = mock_check:MockChecker',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Quality Assurance',
    ],
)
