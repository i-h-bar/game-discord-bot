import sys
import logging

from setuptools import setup
from Cython.Build import cythonize
import numpy as np


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
