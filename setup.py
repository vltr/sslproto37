"""This file is mostly useless since I do not plan on releasing this package
on PyPI.
"""

from glob import glob
from os.path import basename, splitext

from setuptools import find_packages, setup


setup(
    name="sslproto37",
    version="0.0.1",
    license="Unlicense",
    description="",
    long_description="",
    author="Richard Kuesters",
    author_email="rkuesters@gmail.com",
    url="https://github.com/vltr/sslproto37",
    packages=find_packages("sslproto37"),
    package_dir={"": "sslproto37"},
    py_modules=[splitext(basename(path))[0] for path in glob("sslproto37/*.py")],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Intended Audience :: Developers",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Utilities",
    ],
    keywords=[],
    install_requires=[],
    extras_require={},
)
