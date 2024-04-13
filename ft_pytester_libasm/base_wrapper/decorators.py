"""
This module defines decorators meant to encapsulate shared libraries
function to make them testable easily with pytest.
"""

from functools import wraps
from typing import (
    Optional,
    # ParamSpec,
    Callable,
    Type,
)

import os

from .wrapper_types import (
    CDLLFunc,
    WrappedCDLLFunc,
    P,
    ResTypeTypeVar,
    FdToWriteTo,
    FdToListenOn,
    FdsToWriteTo,
    FdsToListenOn,
    FdToWriteToInfos,
    FdToListenOnInfos,
)
from .result import Result

# from .utils import get_errno


def wrap_CDLL_func(
    f: CDLLFunc[ResTypeTypeVar, P],
) -> WrappedCDLLFunc[ResTypeTypeVar, P]:

    @wraps(f)
    def decorated_f(
        *args: P.args,
        # New kwargs here
        fds_to_write_to: Optional[FdsToWriteTo] = None,
        fds_to_listen_on: Optional[FdsToListenOn] = None,
        # Errno condition # (Perhaps use a callback instead).
        # should_get_errno: Optional[ConditionForErrno[T_inv]] = None,
        **kwargs: P.kwargs,
    ) -> Result[ResTypeTypeVar]:
        result: Result[ResTypeTypeVar]

        # Handling writing:
        if fds_to_write_to:
            current_fd_to_write_to: FdToWriteTo
            current_fd_to_write_to_infos: FdToWriteToInfos
            current_data_to_write: bytes
            current_size_to_write: int
            # current_associated_fd_to_listen_on: FdToListenOn

            current_fd_to_write_to, current_fd_to_write_to_infos = (
                fds_to_write_to.popitem()
            )
            (
                current_data_to_write,
                current_size_to_write,
                current_associated_to_listen_on,
            ) = current_fd_to_write_to_infos

            with os.fdopen(current_fd_to_write_to, "w+") as fd:

                fd.write(str(current_data_to_write, "ascii"))
                result = decorated_f(
                    *args,
                    fds_to_write_to=fds_to_write_to,
                    fds_to_listen_on=fds_to_listen_on,
                    **kwargs,
                )

        # Handling reading:
        elif fds_to_listen_on:
            current_fd_to_listen_on: FdToListenOn
            current_fd_to_listen_on_infos: FdToListenOnInfos
            current_size_to_listen: int
            current_associated_fd_to_write_to: FdToWriteTo
            retrieved_output: bytes

            current_fd_to_listen_on, current_fd_to_listen_on_infos = (
                fds_to_listen_on.popitem()
            )
            current_size_to_listen, current_associated_fd_to_write_to = (
                current_fd_to_listen_on_infos
            )

            with os.fdopen(current_fd_to_listen_on, "r") as fd:

                result = decorated_f(
                    *args,
                    fds_to_write_to=fds_to_write_to,
                    fds_to_listen_on=fds_to_listen_on,
                    **kwargs,
                )
                retrieved_output = bytes(fd.read(), encoding="ascii")
                result.add_output(
                    retrieved_output,
                    current_fd_to_listen_on,
                    current_associated_fd_to_write_to,
                )

        # Actually run the CDLL function:
        else:
            res_val = f(*args, **kwargs)
            result = Result(res_val)

        return result

    return decorated_f


def set_restype(
    restype: Type[ResTypeTypeVar],
) -> Callable[[CDLLFunc[ResTypeTypeVar, P]], CDLLFunc[ResTypeTypeVar, P]]:

    def inner(f: CDLLFunc[ResTypeTypeVar, P]) -> CDLLFunc[ResTypeTypeVar, P]:
        f.restype = restype
        return f

    return inner
