#! /usr/bin/env python

from setuptools import setup, find_packages
import versioneer

setup (
    name = "retryp",
    version = versioneer.get_version (),
    description = "Well-featured retry decorator",
    long_description = file ("README.rst").read (),
    cmdclass = versioneer.get_cmdclass (),
    classifiers = [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: "
        + "GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Topic :: Utilities",
    ],
    keywords = "decorator exception retry retrying",
    author = "J C Lawrence",
    author_email = "claw@kanga.nu",
    url = "https://github.com/clearclaw/retryp",
    license = "LGPL v3.0",
    packages = find_packages (exclude = ["tests",]),
    test_suite = "tests",
    package_data = {
    },
    zip_safe = True,
    install_requires = [line.strip ()
        for line in file ("requirements.txt").readlines ()],
    entry_points = {
        "console_scripts": [
        ],
    },
)
