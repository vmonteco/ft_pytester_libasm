"""
The result modules implements the Result class that's meant to
encapsulate the observed behaviour of a shared library function
(not only the return value).
"""

from typing import Optional, Generic, Any
from ctypes import c_int
from .wrapper_types import (
    ResTypeTypeVar,
    CapturedOutputs,
    FdToListenOn,
    FdToWriteTo,
)


class Result(Generic[ResTypeTypeVar]):
    """
    Result is meant to encapsulate the behaviour of a shared library
    function call.

    It will include the return value, captured outputs and the
    possible errno.
    """

    return_value: Any
    outputs: CapturedOutputs
    errno: Optional[c_int]

    def __init__(
        self,
        return_value,
        captured_outputs: Optional[CapturedOutputs] = None,
        errno: Optional[c_int] = None,
    ):
        """
        __init__ takes one mandatory argument (`return_value`)
        and two optional kwargs (`captured_outputs` and `errno`).
        """
        if captured_outputs is None:
            self.outputs = {}
        else:
            self.outputs = captured_outputs
        self.errno = errno
        self.return_value = return_value

    def __eq__(self, val) -> bool:
        """
        Result can be compared either to a ctypes return value,
        either to another Result object.

        If it's compared to an other Result instance, it will
        be equal to it if and only if the return_value,
        captured_outputs, and errno attributes are respectively
        equal.
        """
        if isinstance(val, Result):
            return (
                self.return_value == val.return_value
                and self.outputs == val.outputs
                and self.errno == val.errno
            )
        return self == Result(val)

    # TODO: Should it really be FDToReadFrom? Not FDToWriteTo
    #       (cf. CapturedOutputs definition)?
    def add_output(
        self, output: bytes, fd: FdToListenOn, associated_fd: FdToWriteTo
    ) -> None:
        self.outputs[fd] = output
