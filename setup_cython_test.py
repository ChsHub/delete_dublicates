from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("delete_duplicates.py")
)
 # python setup_cython_test.py build_ext --inplace