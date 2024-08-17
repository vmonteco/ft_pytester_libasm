#!/usr/bin/env python3

import pytest
from libasm_wrapper import LibASMWrapper


@pytest.fixture(scope="session")
def libasm_ref() -> LibASMWrapper:
    """
    Reference libasm implementation that should pass any test for mandatory
    part (Wrapping libc functions).
    """
    lib = LibASMWrapper("libc.so.6", ref=True, system_lib=True)
    return lib


@pytest.fixture(scope="session")
def libasm() -> LibASMWrapper:
    """
    A LibASMWrapper instance using the system libc.
    """
    lib = LibASMWrapper("libc.so.6", ref=False, system_lib=True)
    return lib
