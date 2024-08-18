"""
This module contains some necessary fixtures necessary for the test
suite to run.
Those fixtures are libasm_shared_library_path and libasm, necessary
to wrap the libasm.so file to test and make it accessible to the
different tests to run.
"""

from libasm_wrapper import LibASMWrapper
from linked_lists import IntLinkedList
import ctypes
import pytest
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# Add --libasm parameter to pytest:
def pytest_addoption(parser):
    parser.addoption(
        "--libasm",
        action="store",
        default="./libasm.so",
        help="Path to shared library (libasm.so) to test.",
        # type=path_checker
    )


# Shared libraries:
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


@pytest.fixture(scope="session")
def libc() -> ctypes.CDLL:
    libc = ctypes.CDLL("libc.so.6", use_errno=True)

    # set strlen:
    libc.strlen.restype = ctypes.c_size_t
    libc.strlen.argtypes = (ctypes.c_char_p,)

    return libc


# String buffers:
@pytest.fixture
def string_buffer_1() -> ctypes.Array[ctypes.c_char]:
    return ctypes.create_string_buffer(1)


@pytest.fixture
def string_buffer_4() -> ctypes.Array[ctypes.c_char]:
    return ctypes.create_string_buffer(4)


@pytest.fixture
def string_buffer_1048577() -> ctypes.Array[ctypes.c_char]:
    return ctypes.create_string_buffer(1048577)


# strdup-specific
@pytest.fixture
def test_suite_base_directory() -> str:
    return BASE_DIR

# Bonus part:
@pytest.fixture
def int_linked_list_1_2_3() -> IntLinkedList:
    node_3 = IntLinkedList(ctypes.c_int(3), None)
    node_2 = IntLinkedList(ctypes.c_int(2), ctypes.pointer(node_3))
    node_1 = IntLinkedList(ctypes.c_int(1), ctypes.pointer(node_2))
    return node_1
