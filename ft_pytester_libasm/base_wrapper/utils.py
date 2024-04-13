#!/usr/bin/env python3

import ctypes

_libc = ctypes.CDLL("libc.so.6")
_get_errno_loc = _libc.__errno_location
_get_errno_loc.restype = ctypes.POINTER(ctypes.c_int)


def get_errno() -> ctypes.c_int:
    return _get_errno_loc()[0]
