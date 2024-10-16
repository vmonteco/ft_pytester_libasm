#!/usr/bin/env python3.10

import ctypes

from typing import (
    NewType,
    Dict,
    Optional,
    Tuple,
    TypeVar,
    Protocol,
    ParamSpec,
    TYPE_CHECKING,
    Union,
    Type,
    NamedTuple,
)

from t_list import TList

# This permits to avoid circular imports.
if TYPE_CHECKING:
    from .result import Result

# TODO: improve this __all__
__all__ = [
    "ResType",
]

R = TypeVar("R", covariant=True)
P = ParamSpec("P")

# Base types:

# Pointer types:
if TYPE_CHECKING:
    PointerToChar = ctypes._Pointer[ctypes.c_char]
    PointerToFunc = ctypes._Pointer[ctypes.CFUNCTYPE]
else:
    PointerToChar = ctypes.POINTER(ctypes.c_char)
    PointerToFunc = ctypes._CFuncPtr

# Meant to represent possible ASM possible return types.
ResType = Union[
    ctypes.c_size_t,
    ctypes.c_char_p,
    ctypes.c_int,
    ctypes.c_char,
    ctypes.c_ssize_t,
    PointerToChar,
    ctypes.c_void_p,
    None,
    # TODO: remove Any
    # Any,
    # TODO: add linked lists.
]
ResTypeTypeVar = TypeVar("ResTypeTypeVar", bound=ResType, covariant=False)
ArgType = Union[
    # ctypes.c_char_p,
    ctypes.c_int,
    # TODO: add linked lists
    ctypes.c_size_t,
    ctypes.c_ssize_t,
    ctypes.c_int,
    ctypes.c_void_p,
    ctypes._Pointer,
    PointerToChar,
    PointerToFunc,
]


class ErrCheck(Protocol[ResTypeTypeVar, P]):
    def __call__(
        self,
        restype: ResTypeTypeVar,
        func: "CDLLFunc[ResTypeTypeVar, P]",
        arguments: Tuple[Type[ArgType], ...],
        /,
    ) -> ResTypeTypeVar: ...


# file descriptor related types.
FdToWriteTo = NewType("FdToWriteTo", int)
FdToListenOn = NewType("FdToListenOn", int)

# Will be used for `fdopen` calls.
Mode = NewType("Mode", str)

# Associated Fds may be useless. So could be FdsToWriteTo's int parameter.
FdToWriteToInfos = Tuple[bytes, ctypes.c_size_t, FdToListenOn, Optional[Mode]]
FdsToWriteToInfos = Dict[FdToWriteTo, FdToWriteToInfos]
FdToListenOnInfos = Tuple[ctypes.c_size_t, FdToWriteTo, Optional[Mode]]
FdsToListenOnInfos = Dict[FdToListenOn, FdToListenOnInfos]

# TODO: Those are possibly useless.
# But if used, perhaps it could be a NewType as well.
SizeToRead = int
SizeToWrite = int

CapturedOutputs = Dict[FdToWriteTo, Tuple[bytes, FdToListenOn]]


# To store infos about function (restype, argstypes, errcheck...).
# TODO: 3.10 doesn't support generic namedtuples (introduced in 3.11).
# But this could be a generic on restype.
class FuncInfos(NamedTuple):
    restype: Type[ResType]
    argtypes: Tuple[Type[ArgType], ...]
    errcheck: Optional[ErrCheck]


###############################################################################
#                               Callable types                                #
###############################################################################


class CDLLFunc(Protocol[ResTypeTypeVar, P]):
    restype: Type[ResTypeTypeVar]
    argtypes: Tuple[Type[ArgType], ...]
    errcheck: Optional[ErrCheck]

    def __call__(
        self, *args: P.args, **kwargs: P.kwargs
    ) -> ResTypeTypeVar: ...


class WrappedCDLLFunc(Protocol[ResTypeTypeVar, P]):
    def __call__(
        self,
        *args: P.args,
        # new kwargs here
        fds_to_write_to: Optional[FdsToWriteToInfos] = None,
        fds_to_listen_on: Optional[FdsToListenOnInfos] = None,
        **kwargs: P.kwargs,
    ) -> "Result[ResTypeTypeVar]": ...
