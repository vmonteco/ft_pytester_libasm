#!/usr/bin/env python3

import pytest


@pytest.mark.parametrize(
    "method",
    [
        # Mandatory part
        "strlen",
        "strcpy",
        "strcmp",
        "write",
        "read",
        "strdup",
    ],
)
def test_presence_of_required_method_as_attribute_ref(libasm_ref, method: str):
    """
    Ensure that method is present at least as an attribute for the reference
    libasm fixture.
    """
    assert hasattr(
        libasm_ref, method
    ), f"Library doesn't have method {method} as attribute."


@pytest.mark.parametrize(
    "method",
    [
        # Mandatory part
        "ft_strlen",
        "ft_strcpy",
        "ft_strcmp",
        "ft_write",
        "ft_read",
        "ft_strdup",
        # Bonus part
        "ft_atoi_base",
        "ft_list_push_front",
        "ft_list_size",
        "ft_list_sort",
        "ft_list_remove_if",
    ],
)
def test_presence_of_required_method_as_attribute(libasm, method: str):
    """
    Ensure that method is present at least as an attribute for the
    non-reference libasm fixture.
    """
    assert hasattr(
        libasm, method
    ), f"Library doesn't have method {method} as attribute."
