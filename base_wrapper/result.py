"""
The result modules implements the Result class that's meant to
encapsulate the observed behaviour of a shared library function
(not only the return value).
"""

from typing import Optional, Generic
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

    It will include the return value and the captured outputs.
    """

    return_value: ResTypeTypeVar
    outputs: CapturedOutputs

    def __init__(
        self,
        return_value,
        captured_outputs: Optional[CapturedOutputs] = None,
    ):
        """
        __init__ takes one mandatory argument (`return_value`)
        and two optional kwargs (`captured_outputs` and `errno`).
        """
        if captured_outputs is None:
            self.outputs = {}
        else:
            self.outputs = captured_outputs
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
            )
        return self == Result(val)

    def add_output(
        self,
        output: bytes,
        fd_output_was_read_on: FdToListenOn,
        fd_output_was_written_to: FdToWriteTo,
    ) -> None:
        self.outputs[fd_output_was_written_to] = (
            output,
            fd_output_was_read_on,
        )
