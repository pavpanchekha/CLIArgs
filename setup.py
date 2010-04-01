from setuptools import setup

setup(
    name="CLIArgs",
    version="1.0",
    author="Pavel Panchekha",
    author_email="pavpanchekha@gmail.com",
    py_modules = ["cliargs"],
    license="LICENSE.txt",
    url="http://pypi.python.org/pypi/CLIArgs/",
    description="Absolutely trivial command line arguments",
    long_description=open("README.txt").read(),

    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python :: 2.6",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
