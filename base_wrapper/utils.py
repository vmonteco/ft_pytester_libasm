#!/usr/bin/env python3

import ctypes
import os
from typing import Tuple, Type
from .wrapper_types import CDLLFunc, ArgType, P, PointerToChar


def integer_errcheck(
    result: ctypes.c_int,
    func: CDLLFunc[ctypes.c_int, P],
    arguments: Tuple[Type[ArgType], ...],
    /,
) -> ctypes.c_int:
    breakpoint()
    if result == -1:
        errno: int = ctypes.get_errno()
        raise OSError(errno, os.strerror(errno))
    return result


def pointer_to_char_errcheck(
    result: PointerToChar,
    func: CDLLFunc[PointerToChar, P],
    arguments: Tuple[Type[ArgType], ...],
    /,
) -> PointerToChar:
    breakpoint()
    if result is None:
        errno: int = ctypes.get_errno()
        raise OSError(errno, os.strerror(errno))
    return result
