#!/usr/bin/env python3

# NB:
# using count > len(buf) actually doesn't make sense as it relies on count
# to know how many bytes write should access, and not on the nul-termination.
# Otherwise there wouldn't be the count parameter at all.

from libasm_wrapper.tags import (
    MandatoryFunctionTag,
    CategoryTag,
    ErrorTag,
    tag_test,
)
from base_wrapper.wrapper_types import (
    FdToWriteTo,
    FdToListenOn,
    FdsToListenOnInfos,
)
from base_wrapper import Result
import errno
import ctypes
import os
import pytest
import tempfile


@tag_test(CategoryTag.MANDATORY)
@tag_test(MandatoryFunctionTag.FT_WRITE)
@pytest.mark.parametrize(
    "buf,nbytes,expected_result",
    [
        (b"", 0, 0),
        (b"foo", 0, 0),
        (b"foo", 2, 2),
        (b"foo", 3, 3),
        (b" " * 1024 * 32, 1024 * 32, 1024 * 32),
    ],
    ids=[
        "Empty str - 0 (exp: 0)",
        '"foo" - 0 (exp: 0)',
        '"foo" - 2 (exp: 2)',
        '"foo" - 3 (exp: 3)',
        "1024*32-long - 1024*64 (exp: 1024*64)",
    ],
)
def test_ft_write(
    libasm,
    buf: bytes,
    nbytes: ctypes.c_size_t,
    expected_result: ctypes.c_size_t,
) -> None:
    r, w = os.pipe()
    fd_r: FdToListenOn = FdToListenOn(r)
    fd_w: FdToWriteTo = FdToWriteTo(w)
    fds_to_listen_on_infos: FdsToListenOnInfos = {
        fd_r: (nbytes, fd_w, None),
    }

    res: Result[ctypes.c_ssize_t] = libasm.ft_write(
        fd_w,
        buf,
        nbytes,
        fds_to_listen_on_infos=fds_to_listen_on_infos,
    )
    assert res.outputs[fd_w] == (buf[: int(nbytes)], fd_r)
    assert res.return_value == expected_result


@tag_test(CategoryTag.MANDATORY)
@tag_test(MandatoryFunctionTag.FT_WRITE)
@tag_test(ErrorTag.ERRNO)
def test_ft_write_errno_bad_descriptor(
    libasm,
) -> None:
    buf: bytes = b"foo"
    nbytes: ctypes.c_size_t = ctypes.c_size_t(len(buf))
    _errno: int

    with tempfile.NamedTemporaryFile() as tmpfile:
        fd = os.open(tmpfile.name, os.O_RDONLY)
        with pytest.raises(OSError):
            try:
                libasm.ft_write(
                    fd,
                    buf,
                    nbytes,
                )
            except OSError as e:
                _errno = e.errno
                raise
            finally:
                os.close(fd)

    assert _errno == errno.EBADF


@tag_test(CategoryTag.MANDATORY)
@tag_test(MandatoryFunctionTag.FT_WRITE)
@tag_test(ErrorTag.ERRNO)
def test_ft_write_errno_no_space_left_on_device(
    libasm,
) -> None:
    buf: bytes = b"foo"
    nbytes: ctypes.c_size_t = ctypes.c_size_t(len(buf))
    _errno: int

    fd = os.open("/dev/full", os.O_WRONLY)
    with pytest.raises(OSError):
        try:
            libasm.ft_write(
                fd,
                buf,
                nbytes,
            )
        except OSError as e:
            _errno = e.errno
            raise
        finally:
            os.close(fd)

    assert _errno == errno.ENOSPC
