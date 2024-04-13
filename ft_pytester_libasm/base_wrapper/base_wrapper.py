# TODO: Rewrite docstring
"""
LibASMWrapper module provides the LibASMWrapper class.
Its purpose is to build an API around a libASM shared library to
call (and test) its functions.
"""

import ctypes
import os
from typing import Dict  # , Callable, Type

# from wrapper.result import Result
from .decorators import (
    wrap_CDLL_func,
)  # , set_restype
from .wrapper_types import FuncInfos  # , Restype


# TODO: make it explicitly an abstract class
class BaseWrapper:
    # TODO: Rewrite docstring
    """
    LibASMWrapper builds an API over the libasm.so shared library.
    """

    # <<<<<<< HEAD
    #     libasm_mandatory_functions: Dict[str, Type[ResType]] = {
    #         "ft_strlen": int,
    #     }
    #
    #     libasm_bonus_functions: Dict[str, Type[ResType]] = {}
    #
    #     libasm_functions: Dict[str, Type[ResType]] = dict(
    # =======
    libasm_mandatory_functions: Dict[str, FuncInfos] = {
        "strlen": FuncInfos(
            argtypes=(ctypes.c_char_p,),
            restype=ctypes.c_size_t,
            errcheck=None,
        ),
        "strcpy": FuncInfos(
            argtypes=(
                ctypes.c_char_p,
                ctypes.c_char_p,
            ),
            restype=type(None),
            errcheck=None,
        ),
    }

    libasm_bonus_functions: Dict[str, FuncInfos] = {}

    libasm_functions: Dict[str, FuncInfos] = dict(
        **libasm_mandatory_functions,
        **libasm_bonus_functions,
    )

    non_ref_prefix: str = "ft_"

    def __init__(
        self, lib: str | ctypes.CDLL, /, *, ref: bool = False
    ) -> None:
        """
        __init__ expects either a path to a shared library (.so), or a
        ctypes.CDLL instance.

        ref parameter can be set to True to provide a reference function for
        comparison during tests, then the methods embedding the foreign
        functions won't have their name prefixed with self.non_ref_prefix.
        """
        # TODO: check path.
        if isinstance(lib, str):
            # When libasm is passed as a path (str).
            self.cdll = ctypes.cdll.LoadLibrary(os.path.abspath(lib))
        else:
            # When libasm is passed as a CDLL.
            self.cdll = lib

        # Let's locally declare a function that will be used it as a
        # placeholder for not implemented (not found) functions in
        # the shared library to test.
        def not_implemented_generator(name):
            def f():
                raise NotImplementedError

        # Set restypes:
        for func_name, func_infos in self.libasm_functions.items():
            if hasattr(self.cdll, func_name):
                f = getattr(self.cdll, func_name)
                f.argtypes = func_infos.argtypes
                f.restype = func_infos.restype
                if func_infos.errcheck is not None:
                    f.errcheck = func_infos.errcheck
                setattr(
                    self,
                    func_name if ref else self.non_ref_prefix + func_name,
                    # func_name,  # There also was this :
                    #             ```
                    #             func_name if ref else (
                    #                 self.non_ref_prefix + func_name
                    #             ),
                    #             ```
                    # wrap_CDLL_func(
                    #     set_restype(restype)(getattr(self.cdll, func_name))
                    # ),
                    wrap_CDLL_func(f),
                )
            else:
                # If a function isn't found, then let's put a
                # placeholder that actually raises a
                # NotImplementedError.
                setattr(
                    self.cdll, func_name, not_implemented_generator(func_name)
                )

    # @wrap_CDLL_func
    # def ft_strlen(self, s: ctypes.c_char_p) -> ctypes.c_size_t:
    #     """
    #     ft_strlen is meant to reproduce the C stdlib's strlen
    #     function, which is prototyped this way:
    #     size_t strlen(const char *s);
    #     """
    #     import pdb; pdb.set_trace()
    #     return self.cdll.ft_strlen(s)

    # @wrap_CDLL_func
    # def ft_write(
    #     self, fd: int, buf: ctypes.c_void_p, count: int
    # ) -> ctypes.c_ssize_t:
    #     """
    #     ft_write is meant to reproduce the C stdlib's write
    #     function, which is prototyped this way:
    #     ssize_t write(int fd, const void buf[.count], size_t count)
    #     """
    #     return self.cdll.ft_write(fd, buf, count)
