#!/usr/bin/env python3
"""
    Auxiliary Tools
    ===============

    For all those things which you need a bit everywhere, but are otherwise part
    of nothing.

"""

import sys
import copy
import logging
import matplotlib.pyplot as pltlib


DEFAULT_MAIN_OPTS = {
    "WarBot.run": {"verbose": False}
}

DEFAULT_MATPLOTLIB_OPTIONS = {
    "figsize": (16, 9),
}


def setup_logging(file__name__: str, local_level: int = logging.INFO) -> "logger":
    """Sets up logging module.

    The firs argument to be passed is __name__, the second is the local logging
    level, i.e. the desired logging level for the file this function is called
    in, when said file is run as standalone.
    """

    logging.basicConfig(format = "%(asctime)s :: %(name)s :: %(levelname)s :: %(message)s")
    logger = logging.getLogger(file__name__)
    logger.setLevel(logging.INFO if file__name__ == "__main__" else logging.ERROR)

    return logger



def parse_args() -> dict:
    """Parse command-line arguments for detection options."""

    options = copy.deepcopy(DEFAULT_MAIN_OPTS)

    VALID_OPTIONS = ("-v", )
    if len(sys.argv) > 1:
        argvs = sys.argv[1:]
        for arg in argvs:
            if arg == "-v":
                options["WarBot.run"]["verbose"] = True

    return options



def setup_matplotlib_options(**kwargs):
    """Setup matplotlib options."""

    if "figsize" in kwargs.keys():
        pltlib.rc("figure", figsize = kwargs["figsize"])



if __name__ == "__main__":
    print(__doc__)

    logger = setup_logging(__name__, local_level = logging.INFO)
    logger.info("This message will be printed if local_level was set to or below logging.INFO")
