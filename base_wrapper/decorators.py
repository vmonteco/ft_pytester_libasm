"""
This module defines decorators meant to encapsulate shared libraries
function to make them testable easily with pytest.
"""

from functools import wraps
from typing import (
    Optional,
    Callable,
    Type,
)

import ctypes
import os

from .wrapper_types import (
    CDLLFunc,
    WrappedCDLLFunc,
    P,
    ResTypeTypeVar,
    FdToWriteTo,
    FdToListenOn,
    FdsToWriteToInfos,
    FdsToListenOnInfos,
    FdToWriteToInfos,
    FdToListenOnInfos,
    Mode,
)
from .result import Result


def wrap_CDLL_func(
    f: CDLLFunc[ResTypeTypeVar, P],
) -> WrappedCDLLFunc[ResTypeTypeVar, P]:
    """Current wrapper."""

    @wraps(f)
    def decorated_f(
        *args: P.args,
        fds_to_write_to_infos: Optional[FdsToWriteToInfos] = None,
        fds_to_listen_on_infos: Optional[FdsToListenOnInfos] = None,
        # Errno condition # (Perhaps use a callback instead).
        # should_get_errno: Optional[ConditionForErrno[T_inv]] = None,
        **kwargs: P.kwargs,
    ) -> Result[ResTypeTypeVar]:
        result: Result[ResTypeTypeVar]
        mode: Optional[Mode]

        # Handling writing:
        if fds_to_write_to_infos:
            current_fd_to_write_to: FdToWriteTo
            current_fd_to_write_to_infos: FdToWriteToInfos
            current_data_to_write: bytes
            current_size_to_write: ctypes.c_size_t
            current_associated_fd_to_listen_on: FdToListenOn

            current_fd_to_write_to, current_fd_to_write_to_infos = (
                fds_to_write_to_infos.popitem()
            )
            (
                current_data_to_write,
                current_size_to_write,
                current_associated_fd_to_listen_on,
                mode,
            ) = current_fd_to_write_to_infos

            # fds should be assumed to be already opened
            with os.fdopen(current_associated_fd_to_listen_on, "rb") as fd_r:
                if mode is None:
                    mode = Mode("bw")
                with os.fdopen(current_fd_to_write_to, mode) as fd_w:
                    fd_w.write(current_data_to_write)

                result = decorated_f(
                    *args,
                    fds_to_write_to_infos=fds_to_write_to_infos,
                    fds_to_listen_on_infos=fds_to_listen_on_infos,
                    **kwargs,
                )

        # Handling reading:
        elif fds_to_listen_on_infos:
            current_fd_to_listen_on: FdToListenOn
            current_fd_to_listen_on_infos: FdToListenOnInfos
            current_size_to_listen: ctypes.c_size_t
            current_associated_fd_to_write_to: FdToWriteTo
            retrieved_output: bytes

            current_fd_to_listen_on, current_fd_to_listen_on_infos = (
                fds_to_listen_on_infos.popitem()
            )
            current_size_to_listen, current_associated_fd_to_write_to, mode = (
                current_fd_to_listen_on_infos
            )

            if mode is None:
                mode = Mode("rb")
            with os.fdopen(current_fd_to_listen_on, mode) as fd_r:
                with os.fdopen(
                    current_associated_fd_to_write_to, "wb"
                ) as fd_w:
                    result = decorated_f(
                        *args,
                        fds_to_write_to_infos=fds_to_write_to_infos,
                        fds_to_listen_on_infos=fds_to_listen_on_infos,
                        **kwargs,
                    )
                retrieved_output = fd_r.read()
                result.add_output(
                    retrieved_output,
                    current_fd_to_listen_on,
                    current_associated_fd_to_write_to,
                )

        # Actually run the CDLL function:
        else:
            try:
                res_val = f(*args, **kwargs)
            except OSError:
                raise
            result = Result(res_val)

        return result

    return decorated_f


# TODO: Ensure this is still useful. Delete it if not.
def set_restype(
    restype: Type[ResTypeTypeVar],
) -> Callable[[CDLLFunc[ResTypeTypeVar, P]], CDLLFunc[ResTypeTypeVar, P]]:

    def inner(f: CDLLFunc[ResTypeTypeVar, P]) -> CDLLFunc[ResTypeTypeVar, P]:
        f.restype = restype
        return f

    return inner
