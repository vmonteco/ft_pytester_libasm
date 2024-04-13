from ctypes import create_string_buffer as csb
import ctypes
import pytest
from typing import Tuple  # , Callable

# from libasm_wrapper import LibASMWrapper
from base_wrapper import Result
from base_wrapper.wrapper_types import FdToWriteTo, FdToWriteToInfos


# TODO: get result values in a variable systematically?


# ft_strlen;
# NB: NULL (None) as an input is undefined behavior.
# @pytest.mark.parametrize("s", [b"", b"foo", b" " * 1048576])
@pytest.mark.parametrize("s", [b"", b"foo"])
def test_ft_strlen(libasm, s: bytes) -> None:
    assert libasm.ft_strlen(s) == len(s)


# ft_strcpy
# Possible other version :
# @pytest.mark.parametrize("src", [b"", b"foo"])  # , b" " * 1048576])
# def test_ft_strcpy(libasm, src: bytes) -> None:
#     dst = ctypes.create_string_buffer(len(src))
#     assert dst is not None, "Allocation failed during strcpy test"
#     libasm.ft_strcpy(dst, src)
#     # TODO: Ensure good practices (to access the value).
#     assert dst.raw == src


@pytest.mark.parametrize(
    "src,dst",
    [
        (src := b"", csb(len(src))),
        (src := b"foo", csb(len(src))),
    ],
)  # , b" " * 1048576])
def test_ft_strcpy(libasm, src: bytes, dst: ctypes.c_char_p) -> None:
    assert dst is not None, "Allocation failed during strcpy test"
    libasm.ft_strcpy(dst, src)
    # TODO: Ensure good practices (to access the value).
    # https://docs.python.org/3/library/ctypes.html#fundamental-data-types
    assert dst.value == src


# ft_strcmp
@pytest.mark.parametrize(
    "s1,s2,expected_result",
    [
        (b"", b"", "equal"),
        (b"", b"foo", "neg"),
        (b"foo", b"", "pos"),
        (b"bar", b"foo", "equal"),
    ],
)
def test_ft_strcmp(
    libasm,
    s1: bytes,
    s2: bytes,
    expected_result: str,
):
    if expected_result == "neg":
        assert libasm.ft_strcmp(s1, s2).return_value < 0
    elif expected_result == "pos":
        assert libasm.ft_strcmp(s1, s2).return_value > 0
    elif expected_result == "equal":
        assert libasm.ft_strcmp(s1, s2).return_value == 0


# ft_write:
# TODO: should NULL as buf be considered?
# TODO: ft_write could modify ERRNO
# @pytest.mark.parametrize("buf", [b"", b"foo", b"bar", b"\x42" * 1048576])
@pytest.mark.parametrize("buf", [b"", b"foo", b"bar"])
# @pytest.mark.parametrize("nbyte", [-1, 0, 1, 1048576])
@pytest.mark.parametrize("nbyte", [-1, 0, 1, 2, 3])
# TODO: CF: https://stackoverflow.com/q/42014484/3156085
@pytest.mark.parametrize("fd_infos", [])
def test_ft_write(
    libasm,
    libasm_ref,
    # TODO: Maybe this should replace buf and nbyte?
    fd_infos: Tuple[FdToWriteTo, FdToWriteToInfos],
    buf: bytes,
    nbyte: ctypes.c_size_t,
) -> None:
    fd: FdToWriteTo = fd_infos[0]
    res: Result[ctypes.c_ssize_t] = libasm.ft_write(fd, buf, nbyte)
    # TODO Perhaps using a new fd is necessary?
    res_ref: Result[ctypes.c_ssize_t] = libasm_ref.write(fd, buf, nbyte)
    # TODO: Maybe make this a bit more explicit.
    assert res_ref.return_value == res.return_value, (
        f"[test_ft_write]: write returned {res_ref.return_value}"
        " and ft_write returned {res.return_value}"
    )
    assert res_ref.errno == res.errno
    assert res_ref.outputs == res.outputs


# ft_read:


# ft_strdup:
