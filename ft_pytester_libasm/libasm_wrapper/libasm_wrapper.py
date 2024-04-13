import ctypes
from typing import (
    Dict,
)

from base_wrapper import BaseWrapper
from base_wrapper.wrapper_types import FuncInfos


class LibASMWrapper(BaseWrapper):
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
            argtypes=(ctypes.c_char_p,),
            restype=ctypes.c_size_t,
            errcheck=None,
        ),
        "strcpy": FuncInfos(
            argtypes=(
                ctypes.c_char_p,
                ctypes.c_char_p,
            ),
            restype=ctypes.c_size_t,
            errcheck=None,
        ),
        "strcmp": FuncInfos(
            argtypes=(
                ctypes.c_char_p,
                ctypes.c_char_p,
            ),
            restype=int,
            errcheck=None,
        ),
        "write": FuncInfos(
            argtypes=(),
            restype=type(None),
            errcheck=None,  # TODO: write can set errno.
        ),
        "read": FuncInfos(
            argtypes=(),
            restype=type(None),
            errcheck=None,  # TODO: read can set errno.
        ),
        "strdup": FuncInfos(
            argtypes=(),
            restype=type(None),
            errcheck=None,  # TODO: write can set errno.
        ),
    }

    # TODO: complete infos on bonus functions.
    libasm_bonus_functions: Dict[str, FuncInfos] = {
        "atoi_base": FuncInfos(
            argtypes=(),
            restype=type(None),
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

    functions: Dict[str, FuncInfos] = dict(
        **libasm_mandatory_functions,
        **libasm_bonus_functions,
    )

    non_ref_prefix: str = "ft_"
