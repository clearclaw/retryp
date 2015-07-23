#! /usr/bin/env python

try:
  import pyver # pylint: disable=W0611
except ImportError:
  import os, subprocess
  try:
    environment = os.environ.copy()
    cmd = "pip install pyver".split (" ")
    subprocess.check_call (cmd, env = environment)
  except subprocess.CalledProcessError:
    import sys
    print >> sys.stderr, "Problem installing 'pyver' dependency."
    print >> sys.stderr, "Please install pyver manually."
    sys.exit (1)
  import pyver # pylint: disable=W0611

from setuptools import setup, find_packages

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
