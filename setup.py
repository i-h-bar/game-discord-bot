import logging
import sys

import numpy as np
from Cython.Build import cythonize
from setuptools import setup


def build():
    # Build Cython modules
    sys.argv.append("build_ext")
    sys.argv.append("-i")

    setup(
        ext_modules=cythonize(
            ["utils/string_matching.pyx"], compiler_directives={'language_level': "3"}
        ),
        include_dirs=[np.get_include()]
    )

    # Set logging level
    logging.getLogger().setLevel(logging.WARNING)


if __name__ == "__main__":
    build()
