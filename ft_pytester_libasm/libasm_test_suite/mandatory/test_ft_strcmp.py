#!/usr/bin/env python3
""""""

from ft_pytester_libasm.libasm_wrapper.tags import MandatoryFunctionTag, CategoryTag, tag_test
import pytest


@tag_test(CategoryTag.MANDATORY)
@tag_test(MandatoryFunctionTag.FT_STRCMP)
@pytest.mark.parametrize(
    "s1,s2,expected_result",
    [
        (b"", b"", "zero"),
        (b"", b"foo", "neg"),
        (b"foo", b"", "pos"),
        (b"foo", b"foo", "zero"),
        (b"foo", b"bar", "pos"),
        (b"bar", b"foo", "neg"),
        (b"\x80", b"\x7f", "pos"),
        (b"\x7f", b"\x80", "neg"),
        (b"\x80", b"\x80", "zero"),
        (b"\x7f", b"\x7f", "zero"),
        (b"foo" * 1024**3 + b"a", b"foo" * 1024**3 + b"b", "neg"),
    ],
    ids=[
        "comparing two empty strs",
        'empty str vs "foo"',
        '"foo" vs empty str',
        '"foo" vs "foo"',
        '"foo" vs "bar"',
        '"bar" vs "foo"',
        '"\x80" vs "\x7f" (char limit values)',
        '"\x7f" vs "\x80" (char limit values)',
        '"\x80" vs "\x80" (char limit values)',
        '"\x7f" vs "\x7f" (char limit values)',
        "long strs (1024**3+1) different at the end",
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
    elif expected_result == "zero":
        assert libasm.ft_strcmp(s1, s2).return_value == 0
