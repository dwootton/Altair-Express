#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()
    
install_requires=['altair @ https://github.com/dwootton/altair/releases/download/v4.3.1/altair-4.3.0.dev0.tar.gz']

requirements = ['Click>=7.0', 'pandas','altair','numpy']

test_requirements = [ ]

setup(
    author="Dylan Wootton",
    author_email='dwootton@mit.edu',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Create interactive data visualizations in one line of code.",
    entry_points={
        'console_scripts': [
            'altair_express=altair_express.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='altair_express',
    name='altair_express',
    packages=find_packages(include=['altair_express', 'altair_express.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/dwootton/altair_express',
    version='0.1.27',
    zip_safe=False,
)
