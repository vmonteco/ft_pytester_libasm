#!/usr/bin/env python3

from libasm_wrapper.tags import (
    BonusFunctionTag,
    ToolFunctionTag,
    CategoryTag,
    tag_test,
)
from typing import Optional
import ctypes
import pytest

BASE1: bytes = b"1"  # This is an error case
BASE2: bytes = b"01"
BASE10: bytes = b"0123456789"
BASE16_up: bytes = b"0123456789ABCDEF"
BASE16_low: bytes = b"0123456789abcdef"


@tag_test(CategoryTag.TOOL)
@tag_test(ToolFunctionTag.FT_STRCHR)
@pytest.mark.parametrize(
    "s,c,exp",
    [
        (b"", 0x2A, None),
        (b"\x2a", 0x2A, 0),
        (b"\x15\x2a", 0x2A, 1),
        (b"\x15\x15", 0x2A, None),
        (b" " * 255 + b"\x2a", 0x2A, 255),
    ],
    ids=[
        "In empty str (exp: NULL)",
        "char contained at index 0",
        "char contained at index 1",
        "char not contained",
        "char contained at index 255",
    ],
)
def test_ft_strchr(libasm, s: bytes, c: ctypes.c_int, exp: Optional[int]):
    """
    This function wasn't demanded in the subject but I implemented
    it because I found it practical to do the ft_atoi_base function.
    """
    sb = ctypes.create_string_buffer(s)
    res = libasm.ft_strchr(sb, c)
    if exp is None:
        assert res.return_value is None
    else:
        assert res.return_value is not None, "Unexpected NULL return value."
        assert (res.return_value - ctypes.addressof(sb)) == exp


@tag_test(CategoryTag.BONUS)
@tag_test(BonusFunctionTag.FT_ATOI_BASE)
@pytest.mark.parametrize(
    "_str,base,exp",
    [
        # Error cases
        (b"0", b"", 0),  # Empty
        (b"11", BASE1, 0),  # base of size 1.
        (b"", BASE2, 0),  # check that this is indeed an error case.
        (b"xyz", BASE2, 0),  # str that doesn't contain any char from base.
        (b"1", b"11", 0),  # Base with duplicate char.
        (b"1", b"-1", 0),  # Base with '-' character.
        (b"1", b"+1", 0),  # Base with '+' character.
        (b"1", b" 1", 0),  # Base with ' ' character.
        (b"+a", BASE2, 0),  # Bad str.
        (b"-b", BASE2, 0),  # Bad str
        (b"+ 0", BASE2, 0),  # Bad str
        # TODO: add cases which are out of range (> INT_MAX or < INT_MIN)
        # TODO: ^^^ (ensure this isn't undefined behavior).
        # Normal behavior
        # - Base 2:
        (b"0", BASE2, 0),
        (b"     0000000000", BASE2, 0),
        (b"-0", BASE2, 0),
        (b"---0", BASE2, 0),
        (b"1", BASE2, 1),
        (b"10", BASE2, 2),
        (b"01", BASE2, 1),
        (b"-1", BASE2, -1),
        (b"--1", BASE2, 1),
        (b"-+-1", BASE2, 1),
        (b"---1", BASE2, -1),
        (b"11111111", BASE2, 255),
        (b"10", BASE2, 2),
        # BASE 10:
        (b"0", BASE10, 0),
        (b"1", BASE10, 1),
        (b"10", BASE10, 10),
        (
            b"  ---+--+1234ab567",
            BASE10,
            -1234,
        ),  # The example from the subject.
        (b"42", BASE10, 42),
        (b"-42", BASE10, -42),
        (b"2A", BASE10, 2),
        (b"-2A", BASE10, -2),
        # BASE 16:
        (b"2A", BASE16_up, 42),
        (b"-2A", BASE16_up, -42),
        (b"2A", BASE16_low, 2),
        (b"-2A", BASE16_low, -2),
        (b"10", BASE16_low, 16),
    ],
)
def test_ft_atoi_base(libasm, _str: bytes, base: bytes, exp: int) -> None:
    assert libasm.ft_atoi_base(_str, base).return_value == exp
