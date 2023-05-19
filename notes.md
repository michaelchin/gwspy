#### activate/deactivate the python virtual env

- `source geoserver-pyadm-venv/bin/activate`

- `deactivate`

#### build and install the package

- `pip3 install pip-tools`
- `pip-compile pyproject.toml`
- `pip3 install .`

#### test

- The file .env must be in current working directory. Alternatively you can set the env variables instead.

#### doc

- `pip-compile pyproject.toml`
- `pip3 install .`
- `sphinx-apidoc -o doc/source src/geoserver_pyadm/`
- `make html`

⚠️You need to re-install the geoserver_pyadm, otherwise the sphinx will keep using the installed stable version(old code).

#### Publish to PyPI

- `pip install build twine`
- `python -m build`
- `twine check dist/*`
- `twine upload -r testpypi dist/*`
- `twine upload dist/*`