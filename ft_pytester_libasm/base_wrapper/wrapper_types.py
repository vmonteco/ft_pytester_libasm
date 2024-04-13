#!/usr/bin/env python3.10

import ctypes

from typing import (
    NewType,
    Dict,
    Optional,
    Tuple,
    # Callable,
    TypeVar,
    # Generic,
    Protocol,
    ParamSpec,
    TYPE_CHECKING,
    Union,
    Any,
    Type,
    NamedTuple,
)

# This permits to avoid circular imports.
if TYPE_CHECKING:
    from .result import Result

# TODO: improve this __all__
__all__ = [
    "ResType",
]

R = TypeVar("R", covariant=True)
P = ParamSpec("P")

# Meant to represent possible ASM possible return types.
ResType = Union[
    ctypes.c_size_t,
    ctypes.c_char_p,
    ctypes.c_int,
    ctypes.c_ssize_t,
    None,
    # TODO: remove Any
    Any,
    # TODO: add linked lists.
]
ResTypeTypeVar = TypeVar("ResTypeTypeVar", bound=ResType, covariant=False)
ArgTypes = Union[
    ctypes.c_char_p,
    # TODO: add linked lists
]


class ErrCheck(Protocol[ResTypeTypeVar]):
    def __call__(
        self,
        restype: ResTypeTypeVar,
        func: "CDLLFunc",
        arguments: Tuple[Type[ArgTypes], ...],
        /,
    ) -> ResTypeTypeVar: ...


# file descriptor related types.
FdToWriteTo = NewType("FdToWriteTo", int)
FdToListenOn = NewType("FdToListenOn", int)

# Associated Fds may be useless. So could be FdsToWriteTo's int parameter.
FdToWriteToInfos = Tuple[bytes, int, FdToListenOn]
FdsToWriteTo = Dict[FdToWriteTo, FdToWriteToInfos]
FdToListenOnInfos = Tuple[int, FdToWriteTo]
FdsToListenOn = Dict[FdToListenOn, FdToListenOnInfos]

# TODO: Those are possibly useless.
# But if used, perhaps it could be a NewType as well.
SizeToRead = int
SizeToWrite = int

# TODO: set this
CapturedOutputs = Any


# To store infos about function (restype, argstypes, errcheck...).
# TODO: 3.10 doesn't support generic namedtuples (introduced in 3.11).
# But this could be a generic on restype.
class FuncInfos(NamedTuple):
    restype: Type[ResType]
    argtypes: Tuple[Type[ArgTypes], ...]
    errcheck: Optional[ErrCheck]


###############################################################################
#                               Callable types                                #
###############################################################################


class CDLLFunc(Protocol[ResTypeTypeVar, P]):
    restype: Type[ResTypeTypeVar]
    argtypes: Tuple[Type[ArgTypes], ...]
    errcheck: Optional[ErrCheck]

    def __call__(
        self, *args: P.args, **kwargs: P.kwargs
    ) -> ResTypeTypeVar: ...


class WrappedCDLLFunc(Protocol[ResTypeTypeVar, P]):
    def __call__(
        self,
        *args: P.args,
        # new kwargs here
        fds_to_write_to: Optional[FdsToWriteTo] = None,
        fds_to_listen_on: Optional[FdsToListenOn] = None,
        **kwargs: P.kwargs,
    ) -> "Result[ResTypeTypeVar]": ...
