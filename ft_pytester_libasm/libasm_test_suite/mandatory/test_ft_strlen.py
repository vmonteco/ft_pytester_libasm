"""
NB:
NULL (None) as an input is an undefined behavior and therefore doesn't
have to be tested.
C standard : 7.1.4.1
https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1256.pdf
"""

from ft_pytester_libasm.libasm_wrapper.tags import MandatoryFunctionTag, CategoryTag, tag_test
import pytest


@tag_test(CategoryTag.MANDATORY)
@tag_test(MandatoryFunctionTag.FT_STRLEN)
@pytest.mark.parametrize(
    "string,expected_length",
    [
        (b"", 0),
        (b"foo", 3),
        (b"*" * 1048576, 1048576),
        (b"*" * (1024**3), 1024**3),
    ],
    ids=[
        "empty string",
        "foo",
        "104576-long str",
        f"{1024**3}-long str",
    ],
)
def test_ft_strlen(libasm, string: bytes, expected_length: int) -> None:
    assert libasm.ft_strlen(string) == expected_length
