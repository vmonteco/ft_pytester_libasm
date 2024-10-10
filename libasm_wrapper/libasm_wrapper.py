import ctypes
from typing import (
    Dict,
)

from base_wrapper import BaseWrapper
from base_wrapper.wrapper_types import FuncInfos, PointerToChar
from base_wrapper.utils import pointer_to_char_errcheck, integer_errcheck


class LibASMWrapper(BaseWrapper):
    # TODO: Check this docstring.
    """
    LibASMWrapper are instanciated by providing a shared library path/name
    (.so) or ctypes.CDLL instance to it that should contain the libasm foreign
    functions as defined in the subject.

    Alternatively, it can also be instanciated with a shared library that
    will have to provide the reference functions to reproduce (libc for
    instance), cf. LibASMWrapper.__init__ documentation for more, in that
    case, the functions will be embedded in methods named without the prefix
    "ft_" (please note that then the bonus part won't exist with the standard
    libc).

    It embeds the behavior (return value, errno, input and outputs) in
    wrapper.Result instances.
    """

    libasm_mandatory_functions: Dict[str, FuncInfos] = {
        "strlen": FuncInfos(
            argtypes=(PointerToChar,),
            restype=ctypes.c_size_t,
            errcheck=None,
        ),
        "strcpy": FuncInfos(
            argtypes=(
                PointerToChar,
                PointerToChar,
            ),
            restype=ctypes.POINTER(ctypes.c_char),
            errcheck=None,
        ),
        "strcmp": FuncInfos(
            argtypes=(
                PointerToChar,
                PointerToChar,
            ),
            restype=ctypes.c_int,
            errcheck=None,
        ),
        "write": FuncInfos(
            argtypes=(ctypes.c_int, ctypes.c_void_p, ctypes.c_size_t),
            restype=ctypes.c_ssize_t,
            errcheck=integer_errcheck,  # TODO: write can set errno.
        ),
        "read": FuncInfos(
            argtypes=(ctypes.c_int, ctypes.c_void_p, ctypes.c_size_t),
            restype=ctypes.c_ssize_t,
            errcheck=integer_errcheck,  # TODO: read can set errno.
        ),
        "strdup": FuncInfos(
            argtypes=(ctypes.POINTER(ctypes.c_char),),
            restype=ctypes.POINTER(ctypes.c_char),
            errcheck=pointer_to_char_errcheck,  # TODO: write can set errno.
        ),
    }

    # TODO: complete infos on bonus functions.
    libasm_bonus_functions: Dict[str, FuncInfos] = {
        "atoi_base": FuncInfos(
            argtypes=(
                ctypes.POINTER(ctypes.c_char),
                ctypes.POINTER(ctypes.c_char),
            ),
            restype=ctypes.c_int,
            errcheck=None,
        ),
        "list_push_front": FuncInfos(
            argtypes=(),
            restype=type(None),
            errcheck=None,
        ),
        "list_size": FuncInfos(
            argtypes=(),
            restype=type(None),
            errcheck=None,
        ),
        "list_sort": FuncInfos(
            argtypes=(),
            restype=type(None),
            errcheck=None,
        ),
        "list_remove_if": FuncInfos(
            argtypes=(),
            restype=type(None),
            errcheck=None,
        ),
    }

    libasm_tool_functions: Dict[str, FuncInfos] = {
        "strchr": FuncInfos(
            argtypes=(ctypes.c_void_p, ctypes.c_int),
            restype=ctypes.c_void_p,
            errcheck=None,
        ),
    }

    functions: Dict[str, FuncInfos] = dict(
        **libasm_mandatory_functions,
        **libasm_bonus_functions,
        **libasm_tool_functions,
    )

    non_ref_prefix: str = "ft_"

    def __init__(self, *args, ref: bool = False, **kwargs):
        self.ref = ref
        super().__init__(*args, **kwargs)

    def get_attr_name(self, func_name: str) -> str:
        """
        get_attr_name converts func_name in a string that will be returned as
        a valid attribute name to store wrapping methods.
        """
        if not self.ref or func_name in self.libasm_bonus_functions:
            return self.non_ref_prefix + func_name
        return func_name

    def get_src_func_name(self, func_name: str) -> str:
        """
        get_src_func_name behaves similarly as get_attr_name.

        It provides the attribute name of the foreign function to retrieve.
        """
        if not self.ref or func_name in self.libasm_bonus_functions:
            return self.non_ref_prefix + func_name
        return func_name
