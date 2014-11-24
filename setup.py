#! /usr/bin/env python

from setuptools import setup, find_packages

import pyver
__version__, __version_info__ = pyver.get_version (pkg = "retryp",
                                                   public = True)

setup (
    name = "retryp",
    version = __version__,
    description = "Well-featured retry decorator",
    long_description = file ("README.rst").read (),
    classifiers = [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: "
        + "GNU General Public License v3 or later (GPLv3+)",
        "Topic :: Utilities",
    ],
    keywords = "decorator exception retry retrying",
    author = "J C Lawrence",
    author_email = "claw@kanga.nu",
    url = "https://github.com/clearclaw/retryp",
    download_url = ("https://github.com/clearclaw/retryp/Tarball/%s.%s"
                    % (__version_info__[0], __version_info__[1])),
    license = "GPL v3.0",
    packages = find_packages (exclude = ["tests",]),
    package_data = {
    },
    zip_safe = True,
    install_requires = [
        "wrapt",
        "logtool",
        "pyver",
    ],
    entry_points = {
        "console_scripts": [
        ],
    },
)
