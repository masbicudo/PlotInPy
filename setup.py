# ref: https://setuptools.readthedocs.io/en/latest/setuptools.html#development-mode
# ref: https://dzone.com/articles/executable-package-pip-install
# ref: https://stackoverflow.com/questions/47362271/python-upgrade-my-own-package

# install for develop:
#   python setup.py develop

import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name='plotinpy',
    version='0.1.0',
    author="MASBicudo",
    author_email="masbicudo@gmail.com",
    description="PlotInPy is a collection of plotting functions made on top of MatPlotLib.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/masbicudo/PlotInPy",
    license="apache-2.0",

    # include all packages under src, except for tests
    packages=setuptools.find_packages("src", exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),

    # tell distutils packages are under src
    package_dir={"": "src"},

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "matplotlib",
        "numpy"
    ],
    extras_require={
        "Use-Pandas-DataFrame": ["pandas"]
    }
)