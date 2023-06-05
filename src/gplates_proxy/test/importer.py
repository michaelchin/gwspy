import os

GPLATES_PROXY_TEST_MODULE = False
if (
    "GPLATES_PROXY_TEST_MODULE" in os.environ
    and os.environ["GPLATES_PROXY_TEST_MODULE"].lower() == "true"
):
    GPLATES_PROXY_TEST_MODULE = True

if GPLATES_PROXY_TEST_MODULE:
    import gplates_proxy as gplates

    print("GPLATES_PROXY_TEST_MODULE=true; testing gplates_proxy module")
else:
    # if you are testing the local python files, use the code below
    import sys

    # Important: you need to `pip uninstall -y gplates-ws-proxy`
    sys.path.append("../..")
    from gplates_proxy import gplates

    print("GPLATES_PROXY_TEST_MODULE=false; testing gplates.py")
