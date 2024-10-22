""""""

# Note:
# Parametrization use of fixtures comes from here:
# https://stackoverflow.com/a/64348247/3156085


from ft_pytester_libasm.libasm_wrapper.tags import MandatoryFunctionTag, CategoryTag, tag_test
import ctypes
import pytest


@tag_test(CategoryTag.MANDATORY)
@tag_test(MandatoryFunctionTag.FT_STRCPY)
@pytest.mark.parametrize(
    "src,buffer_fixture_name",
    [
        (b"", "string_buffer_1"),
        (b"foo", "string_buffer_4"),
        (b"*" * 1048576, "string_buffer_1048577"),
    ],
    ids=[
        "empty str",
        "str of len 3",
        "str of len 1048576",
    ],
)
def test_ft_strcpy(
    libasm, request, src: bytes, buffer_fixture_name: str
) -> None:
    dst: ctypes.c_char_p = request.getfixturevalue(buffer_fixture_name)
    libasm.ft_strcpy(dst, src)
    assert dst.value == src
