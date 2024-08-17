# TODO: Rewrite docstring
"""
LibASMWrapper module provides the LibASMWrapper class.
Its purpose is to build an API around a libASM shared library to
call (and test) its functions.
"""

import ctypes
import os
from typing import Dict

from .decorators import (
    wrap_CDLL_func,
)
from .wrapper_types import FuncInfos, CDLLFunc, WrappedCDLLFunc


class NotImplementedCDLLFunc(CDLLFunc):
    def __init__(self, attr_name: str):
        self.attr_name: str = attr_name
        self.restype = type(None)
        self.argtypes = ()
        self.errcheck = None

    def __call__(self):
        raise NotImplementedError(f"{self.func_name} not implemented.")


# TODO: make it explicitly an abstract class
class BaseWrapper:
    # TODO: Rewrite docstring
    """
    LibASMWrapper builds an API over the libasm.so shared library.
    """

    libasm_bonus_functions: Dict[str, FuncInfos] = {}

    functions: Dict[str, FuncInfos]

    non_ref_prefix: str = "ft_"

    def __init__(
        self,
        lib: str | ctypes.CDLL,
        /,
        *,
        ref: bool = False,
        system_lib: bool = False,
    ) -> None:
        """
        __init__ expects either a path to a shared library (.so), or a
        ctypes.CDLL instance.

        ref parameter can be set to True to provide a reference function for
        comparison during tests, then the methods embedding the foreign
        functions won't have their name prefixed with self.non_ref_prefix.
        """
        attr_name: str

        # TODO: check path.
        if isinstance(lib, str):
            # When libasm is passed as a path (str).
            if system_lib:
                # Not up to this code to handle the
                # path resolution in that case.
                self.cdll = ctypes.cdll.LoadLibrary(lib)
            else:
                # Fullpath given expected
                self.cdll = ctypes.cdll.LoadLibrary(os.path.abspath(lib))
        else:
            # When libasm is passed as a CDLL.
            self.cdll = lib

        for func_name, func_infos in self.functions.items():
            # Bonus functions will also get the prefix anyway.
            if not ref or func_name in self.libasm_bonus_functions:
                attr_name = self.non_ref_prefix + func_name
            else:
                attr_name = func_name
            self.build_method(attr_name, func_name, func_infos)

    def build_method(
        self, attr_name: str, func_name: str, func_infos: FuncInfos
    ) -> None:
        f_decorated: WrappedCDLLFunc
        f = getattr(
            self.cdll, func_name, NotImplementedCDLLFunc(attr_name=attr_name)
        )
        f.argtypes = func_infos.argtypes
        f.restype = func_infos.restype
        if func_infos.errcheck is not None:
            f.errcheck = func_infos.errcheck
        f_decorated = wrap_CDLL_func(f)
        setattr(self, attr_name, f_decorated)
