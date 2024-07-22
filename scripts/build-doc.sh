#!/bin/bash

source ../venvs/gplates-proxy/bin/activate

pip-compile pyproject.toml
pip3 install .
rm doc/source/gwspy.rst
rm doc/source/modules.rst
pip install -U sphinx sphinx_rtd_theme
sphinx-apidoc -o doc/source src/gwspy
cd doc
make html