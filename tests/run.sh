#!/bin/bash

source ~/.init_mamba

micromamba activate gplates-ws-example

export GWS_URL=http://localhost:18000/
export GPLATES_PROXY_TEST_MODULE=false

pytest -vv