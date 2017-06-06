#!/usr/bin/env python3

from setuptools import setup,Extension
import sys

module1 = Extension('extensions.PatchPreGlib246',
                    sources = ['PatchPreGlib246/PyDbusLowLevel.c'],
                    include_dirs = ['/usr/include/pygobject-3.0',
								'/usr/local/include',
								'/usr/include/glib-2.0',
								'/lib' + ('64' if sys.maxsize > 2**32 else '') + '/glib-2.0/include',
                                '/usr/lib' + ('x86_64' if sys.maxsize > 2**32 else 'i386')+ "-linux-gnu/glib-2.0/include"])

with open('README.rst') as f:
	readme = f.read()

setup(
	name = "pydbus",
	version = "0.8.0",
	description = "Pythonic DBus library",
	long_description = readme,
	author = "Linus Lewandowski, Harry Coin, et. al.",
	author_email = "linus@lew21.net",
	url = "https://github.com/LEW21/pydbus",
	keywords = "dbus",
	license = "LGPLv2+",
    ext_package='pydbus',
	ext_modules = [module1],

	packages = ["pydbus","pydbus.translations","pydbus.extensions"],
	package_data = {"": ["LICENSE"]},
	package_dir = {"pydbus":"pydbus"},
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
		'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
		# last v2 pydbus v0.70 'Programming Language :: Python :: 2',
		# 'Programming Language :: Python :: 2.7'
	]
)
