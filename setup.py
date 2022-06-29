from setuptools import setup
from Cython.Build import cythonize
import numpy as np

setup(
    ext_modules=cythonize(
        ["utils/string_matching.pyx"], compiler_directives={'language_level': "3"}
    ),
    include_dirs=[np.get_include()]
)
