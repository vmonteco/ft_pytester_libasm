"""
The base_wrapper module provides utilities to build wrapper
classes that will permit to build APIs on top of shared libraries
for test purpose.
"""

import ctypes
import os
from typing import Dict, Type, Tuple

from .decorators import (
    wrap_CDLL_func,
)
from .wrapper_types import FuncInfos, CDLLFunc, WrappedCDLLFunc, P


class NotImplementedCDLLFunc(CDLLFunc[None, P]):
    restype: Type[None] = type(None)
    argtypes: Tuple = ()
    errcheck: None = None
    func_name: str

    def __init__(self, func_name: str) -> None:
        self.func_name = func_name

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> None:
        raise NotImplementedError(f"{self.func_name} not implemented.")


def make_not_implemented_CDLLFunc(func_name: str) -> CDLLFunc[None, P]:

    return NotImplementedCDLLFunc("func_name")


# def NotImplementedCDLLFuncFactory(CDLLFunc):
#     def __init__(self, attr_name: str):
#         self.attr_name: str = attr_name
#         self.restype = type(None)
#         self.argtypes = ()
#         self.errcheck = None

#     def __call__(self, *args, **kwargs):
#         raise NotImplementedError(f"{self.func_name} not implemented.")


# TODO: make it explicitly an abstract class
class BaseWrapper:
    """
    This base class is intended to wrap shared libraries to build
    APIs in python over them for testing purpose.
    """

    functions: Dict[str, FuncInfos]

    def __init__(
        self,
        lib: str | ctypes.CDLL,
        /,
        *,
        system_lib: bool = False,
    ) -> None:
        """
        __init__ expects either a path to a shared library (.so), or a
        ctypes.CDLL instance.

        lib (str | ctypes.CDLL): Actual CDLL instance, library name or path to
        library.

        system_lib(bool): determines whether the provided lib path should be
        resolved as a system library by using an explicit path. Default: False.
        """
        self.system_lib: bool = system_lib

        attr_name: str

        # TODO: check path to handle possibly nonexistent file/dir...
        if isinstance(lib, str):
            # When libasm is passed as a path or system library name (str).
            if system_lib:
                # Not up to this code to handle the
                # path resolution in that case. The library
                # is passed as its name.
                # TODO: handle non-existent lib name.
                self.cdll = ctypes.CDLL(lib, use_errno=True)
            else:
                # Explicit path given expected
                # TODO: handle non-existent path.
                self.cdll = ctypes.CDLL(os.path.abspath(lib), use_errno=True)
        else:
            # When libasm is passed as a CDLL.
            self.cdll = lib

        for func_name, func_infos in self.functions.items():
            attr_name = self.get_attr_name(func_name)
            func_name = self.get_src_func_name(func_name)
            self.build_method(attr_name, func_name, func_infos)

    def get_attr_name(self, func_name: str) -> str:
        return func_name

    def get_src_func_name(self, func_name: str) -> str:
        return func_name

    def build_method(
        self, attr_name: str, func_name: str, func_infos: FuncInfos
    ) -> None:
        f_decorated: WrappedCDLLFunc
        f: CDLLFunc = getattr(
            self.cdll, func_name, make_not_implemented_CDLLFunc(func_name)
        )
        f.argtypes = func_infos.argtypes
        f.restype = func_infos.restype
        if func_infos.errcheck is not None:
            f.errcheck = func_infos.errcheck
        f_decorated = wrap_CDLL_func(f)
        setattr(self, attr_name, f_decorated)
        setattr(self, "raw_" + attr_name, f)
