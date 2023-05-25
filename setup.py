from distutils.core import setup
setup(
    name = "pythoneda",
    packages = ["PythonEDA/domain", "PythonEDA/infrastructure", "PythonEDA/application"],
#    packages = find_packages(),
    version = "0.0.1.alpha.1",
    description = "Support for event-driven architectures in Python",
    author = "rydnr",
    author_email = "github@acm-sl.org",
    url = "https://github.com/rydnr/pythoneda",
    download_url = "https://github.com/rydnr/pythoneda/releases",
    keywords = ["eda", "ddd"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
    install_requires=[
        'requests>=2.28.1',
        'grpcio>=1.41.0'
    ],
    long_description = """\
PythonEDA
---------

Support for event-driven architectures in Python, promoting DDD.

This version requires Python 3 or later.
"""
)
