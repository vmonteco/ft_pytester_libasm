#!/usr/bin/env python3
""""""

from libasm_wrapper.tags import (
    MandatoryFunctionTag,
    CategoryTag,
    ErrorTag,
    tag_test,
)
from base_wrapper import Result
from base_wrapper.wrapper_types import (
    FdToListenOn,
    FdToWriteTo,
    FdsToWriteToInfos,
)
import ctypes
import os
import pytest


@tag_test(CategoryTag.MANDATORY)
@tag_test(MandatoryFunctionTag.FT_READ)
@pytest.mark.parametrize(
    "data_to_write,count,expected_result",
    [
        (b"", 0, 0),
        (b"foo", 3, 3),
        (b"foo", 0, 0),
        (b" " * 1024 * 32, 1024 * 32, 1024 * 32),
    ],
    ids=[
        "Empty str with count: 3 (exp: 3)",
        '"foo" with count: 3 (exp: 3)',
        '"foo" with count: 3 (exp: 0)',
        "1024*32-long str",
    ],
)
def test_ft_read(
    libasm_ref,
    data_to_write: bytes,
    count: ctypes.c_size_t,
    expected_result: ctypes.c_ssize_t,
) -> None:
    r, w = os.pipe()
    fd_r: FdToListenOn = FdToListenOn(r)
    fd_w: FdToWriteTo = FdToWriteTo(w)
    fds_to_write_to_infos: FdsToWriteToInfos = {
        fd_w: (data_to_write, count, fd_r, None),
    }
    buf: ctypes.Array[ctypes.c_char] = ctypes.create_string_buffer(
        len(data_to_write) + 1
    )

    res: Result[ctypes.c_ssize_t] = libasm_ref.read(
        fd_r,
        ctypes.cast(buf, ctypes.c_void_p),
        count,
        fds_to_write_to_infos=fds_to_write_to_infos,
    )

    assert res.return_value == expected_result
    assert buf.value == data_to_write[: int(count)]


@tag_test(CategoryTag.MANDATORY)
@tag_test(MandatoryFunctionTag.FT_READ)
@tag_test(ErrorTag.ERRNO)
def test_ft_read_errno_bad_file_descriptor(
    libasm_ref,
) -> None:
    fd: int
    errno: int

    buffer = ctypes.create_string_buffer(3)

    fd = os.open("/dev/null", os.O_WRONLY)
    with pytest.raises(OSError):
        try:
            libasm_ref.read(fd, buffer, 2)
        except OSError as e:
            errno = e.errno
            raise
        finally:
            os.close(fd)

    assert errno == 9


@tag_test(CategoryTag.MANDATORY)
@tag_test(MandatoryFunctionTag.FT_READ)
@tag_test(ErrorTag.ERRNO)
def test_ft_read_errno_bad_address(
    libasm_ref,
) -> None:
    fd: int
    errno: int

    fd = os.open("/dev/zero", os.O_RDONLY)
    with pytest.raises(OSError):
        try:
            libasm_ref.read(fd, -1, 3)
        except OSError as e:
            errno = e.errno
            raise
        finally:
            os.close(fd)

    assert errno == 14
