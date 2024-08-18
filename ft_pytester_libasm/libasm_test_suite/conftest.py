"""
This module contains some necessary fixtures necessary for the test
suite to run.
Those fixtures are libasm_shared_library_path and libasm, necessary
to wrap the libasm.so file to test and make it accessible to the
different tests to run.
"""

from libasm_wrapper import LibASMWrapper
from typing import List, Optional
from linked_lists import IntLinkedList
import ctypes
import pytest
import os

# def path_checker(path):
#     # TODO: complete this.
#     return path


def pytest_addoption(parser):
    parser.addoption(
        "--libasm",
        action="store",
        default="./libasm.so",
        help="Path to shared library (libasm.so) to test.",
        # type=path_checker
    )


@pytest.fixture(scope="session")
def libasm_shared_library_path(request: pytest.FixtureRequest) -> str:
    """
    The libasm_shared_library_path fixture gives access to and
    returns the provided libasm.so path through the pytest --libasm
    option.
    It also checks if such file exist and raises a FileNotFoundError
    if it's not the case.
    """
    path = request.config.getoption("--libasm")
    path = os.path.abspath(path)
    if not os.path.isfile(path):
        raise FileNotFoundError(path)
    return path


@pytest.fixture(scope="session")
def libasm(libasm_shared_library_path: str) -> LibASMWrapper:
    """
    The libasm fixture gives access to the wrapped libasm.so shared
    library built from the libASM project to test.
    It uses the libasm_shared_library_path to determine where to find
    it.
    """
    return LibASMWrapper(libasm_shared_library_path, ref=False)


@pytest.fixture(scope="session")
def libasm_ref() -> LibASMWrapper:
    return LibASMWrapper("libc.so.6", ref=True, system_lib=True)


# Arguments related fixtures:
# Types to handle:

bytes_vals: List[bytes] = [
    b"",
    b"foo",
    b"bar",
    b" " * 1048576,
]


@pytest.fixture
@pytest.mark.parametrize("s", bytes_vals)
def bytes_1(s: Optional[bytes]) -> Optional[bytes]:
    return s


@pytest.fixture
@pytest.mark.parametrize("s", bytes_vals)
def bytes_2(s: Optional[bytes]) -> Optional[bytes]:
    return s


optional_bytes_vals: List[Optional[bytes]] = [
    None,
]
# + c_char_p_vals


@pytest.fixture
@pytest.mark.parametrize("s", optional_bytes_vals)
def optionnal_bytes_1(s: Optional[bytes]) -> Optional[bytes]:
    return s


@pytest.fixture
@pytest.mark.parametrize("s", optional_bytes_vals)
def optionnal_bytes_2(s: Optional[bytes]) -> Optional[bytes]:
    return s


@pytest.fixture
@pytest.mark.parametrize("size", list(set(len(b) + 1 for b in bytes_vals)))
def bytes_buffer(size: int):
    return ctypes.create_string_buffer(size + 1)


# Mandatory part:
# - c_char_p (with NULL included).
# - c_char_p (without NULL)
# - c_int
# - File descriptor
# - c_void_p
# - c_size_t


# Bonus part:
@pytest.fixture
def int_linked_list_1_2_3() -> IntLinkedList:
    node_3 = IntLinkedList(ctypes.c_int(3), None)
    node_2 = IntLinkedList(ctypes.c_int(2), ctypes.pointer(node_3))
    node_1 = IntLinkedList(ctypes.c_int(1), ctypes.pointer(node_2))
    return node_1
