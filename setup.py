from distutils.core import setup
setup(
    name = "pythoneda",
    packages = ["."],
#    packages = find_packages(),
    version = "0.0.1a4",
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
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
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

This package provides support for event-driven architectures in Python, following the hexagonal architecture layout, and encouraging domain-driven design.

In summary, this package helps you to focus on your domain, and assume all interaction with the outside is through events. Let PythonEDA provide you the infrastructure (grpc, d-bus, https, relational databases) and resolve the ports (in DDD jargon) for you.

This is what PythonEDA provides:
- domain support: Port and PrimaryPort interfaces, ValueObject and Entity classes.
- infrastructure: Implementations of the primary ports (grpc, https, etc.).
- application: A bootstrap mechanism that resolves the ports, listens to incoming events, and route them to your domain.

Some examples can be found on the "ecosystem" repositories:
- [Python packages](https://github.com/rydnr/ecosystem-python-packages "Python packages' github repository"): Domain of Python packages.
- [Git repositories](https://github.com/rydnr/ecosystem-git-repositories "Git repositories' github repository"): Domain of Git repositories.
- [Nix-shared](https://github.com/rydnr/ecosystem-nix-shared "Shared kernel for Nix-related domains"): Shared kernel of Nix-related domains.
- [Nix flakes' github repository](https://github.com/rydnr/ecosystem-nix-flakes "Nix flakes' github repository"): Domain of Nix flakes.
""",
    tests_require=['pytest']
)
