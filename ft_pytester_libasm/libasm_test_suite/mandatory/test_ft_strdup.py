#!/usr/bin/env python3
""""""

from ft_pytester_libasm.libasm_wrapper.tags import (
    MandatoryFunctionTag,
    CategoryTag,
    ErrorTag,
    tag_test,
)
from ft_pytester_libasm.base_wrapper.result import Result
from ft_pytester_libasm.base_wrapper.wrapper_types import PointerToChar
import ctypes
import pytest
import subprocess
import os


@tag_test(CategoryTag.MANDATORY)
@tag_test(MandatoryFunctionTag.FT_STRDUP)
@pytest.mark.parametrize(
    "src",
    [
        ctypes.create_string_buffer(b""),
        ctypes.create_string_buffer(b"foo"),
        ctypes.create_string_buffer(b"*" * 1048575),
        ctypes.create_string_buffer(b"*" * 10485750),
    ],
    ids=[
        "Empty str",
        '"foo"',
        "1048576-long str",
        "10485751-long str",
    ],
)
def test_ft_strdup(libasm, libc, src: PointerToChar) -> None:
    result: Result = libasm.ft_strdup(src)
    dst = result.return_value

    src_addr = ctypes.addressof(src)
    src_content = src[: libc.strlen(src)]

    dst_addr = ctypes.addressof(dst.contents)
    dst_content = dst[: libc.strlen(dst)]

    assert src_content == dst_content
    assert src_addr != dst_addr


@tag_test(CategoryTag.MANDATORY)
@tag_test(MandatoryFunctionTag.FT_STRDUP)
@tag_test(ErrorTag.ERRNO)
def test_ft_strdup_insufficient_memory(test_suite_base_directory) -> None:
    """
    Warning: this test can only confirm that ENOMEM is correctly hanlded
    when it occurs. Not that the implementation is broken.
    """
    p = os.path.join(test_suite_base_directory, "bin_tools")
    subprocess.run("./run_ft_strdup", check=True, cwd=p)
