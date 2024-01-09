import logging
import os
from pathlib import Path

import pytest

logger = logging.getLogger("test-logger")
logger.setLevel(logging.INFO)
logger.propagate = False
Path("logs").mkdir(parents=True, exist_ok=True)
fh = logging.FileHandler(f"logs/test.log")
fh.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s \n\n%(message)s\n")
fh.setFormatter(formatter)
logger.addHandler(fh)

# print(logger.handlers)

if (
    "GPLATES_PROXY_TEST_MODULE" in os.environ
    and os.environ["GPLATES_PROXY_TEST_MODULE"].lower() == "true"
):
    GPLATES_PROXY_TEST_MODULE = True
else:
    GPLATES_PROXY_TEST_MODULE = False

if not GPLATES_PROXY_TEST_MODULE:
    # testing ../src
    import sys

    # Important: you need to `pip uninstall -y gplates-ws-proxy`
    sys.path.insert(0, "../src")


import gplates_ws_proxy

logger.info(
    f"GPLATES_PROXY_TEST_MODULE={GPLATES_PROXY_TEST_MODULE}; testing {gplates_ws_proxy.__file__}"
)
