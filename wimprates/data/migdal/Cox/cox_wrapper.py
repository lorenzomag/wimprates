"""
The paths in the code in Peter Cox's package assume the working directory to be
the root of its package. With this wrapper we change the working dir when computing
the interpolators, then returning the Migdal class instance once they've been instantiated.
The working directory is then reset.
"""

from contextlib import redirect_stdout
from functools import cache, lru_cache
import io
import os
import sys

# Cox's module prints a citation banner when imported. Capture it here (wimprates
# is re-imported by every multiprocessing worker) and print it once, the first
# time the model is actually used
with redirect_stdout(io.StringIO()) as _cox_banner:
    from .cox_submodule.Migdal import Migdal
import wimprates as wr

export, __all__ = wr.exporter()


@cache
def _print_cox_banner():
    print(_cox_banner.getvalue(), end="")


@export
@lru_cache
def cox_migdal_model(element: str, **kwargs) -> Migdal:
    """
    This function creates a Cox Migdal model for a given element.

    Parameters:
    - element (str): The element for which the Cox Migdal model is created.
    - **kwargs: Additional keyword arguments for loading probabilities and total probabilities.

    Returns:
    - material: The Cox Migdal material object.

    Example usage:
    cox_migdal_model("carbon", arg1=value1, arg2=value2)

    Note: The Cox's model assumes that the main process is running in its root directory and uses
        relative paths. Therefore, we need to switch the working directory to the root of the package
        when computing the interpolators. 
        This wrapper function changes the working directory temporarily, instantiates the Migdal class, 
        and then resets the working directory back to its original state.
    """
    _print_cox_banner()
    original_cwd = os.getcwd()

    try:
        migdal_directory = os.path.join(os.path.dirname(__file__), "cox_submodule")
        os.chdir(migdal_directory)

        material = Migdal(element)
        material.load_probabilities(**kwargs)
        material.load_total_probabilities(**kwargs)
    finally:
        os.chdir(original_cwd)

    return material
