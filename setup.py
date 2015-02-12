#!/usr/bin/env python3

from setuptools import setup, find_packages

with open('README.rst') as f:
	readme = f.read()

setup(
	name = "pydbus",
	version = "0.2",
	description = "Pythonic DBus library",
	long_description = readme,
	author = "Janusz Lewandowski",
	author_email = "lew21@xtreeme.org",
	url = "https://github.com/LEW21/pydbus",
	keywords = "dbus",
	license = "LGPLv2+",

	packages = find_packages(),
	package_data = {
		'': ['LICENSE, *.rd'],
	},
	zip_safe = True,
	classifiers = [
		'Development Status :: 5 - Production/Stable',
		'Intended Audience :: Developers',
		'Natural Language :: English',
		'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
		'Programming Language :: Python',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.3',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 2.7'
	]
)
