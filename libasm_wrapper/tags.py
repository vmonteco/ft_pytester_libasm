#!/usr/bin/env python3

"""
This modules sets informations about the libasm 42 project structure.

The structure is as follow:

 - Mandatory part:
   - ft_strlen (man 3 strlen)
   - ft_strcpy (man 3 strcpy)
   - ft_strcmp (man 3 strcmp)
   - ft_write (man 2 write)
   - ft_read (man 2 read)
   - ft_strdup (man 3 strdup)
 - Bonus part:
   - ft_atoi_base
   - ft_list_push_front
   - ft_list_size
   - ft_list_sort
   - ft_list_remove_if
"""

from enum import Enum
from typing import Union, Sequence
from pytest import mark

__all__ = [
    "MandatoryFunctionTag",
    "BonusFunctionTag",
    "CategoryTag",
    "FunctionTag",
    "LibASMTag",
    "ErrorTag",
    "tag_test",
]


class StrEnum(str, Enum):
    pass


class MandatoryFunctionTag(StrEnum):
    FT_STRLEN = "ft_strlen"
    FT_STRCPY = "ft_strcpy"
    FT_STRCMP = "ft_strcmp"
    FT_WRITE = "ft_write"
    FT_READ = "ft_read"
    FT_STRDUP = "ft_strdup"


class BonusFunctionTag(StrEnum):
    FT_ATOI_BASE = "ft_atoi_base"
    FT_LIST_PUSH_FRONT = "ft_list_push_front"
    FT_LIST_SIZE = "ft_list_size"
    FT_LIST_SORT = "ft_list_sort"
    FT_LIST_REMOVE_IF = "ft_list_remove_if"


class ToolFunctionTag(StrEnum):
    FT_STRCHR = "ft_strchr"


class CategoryTag(StrEnum):
    MANDATORY = "mandatory"
    BONUS = "bonus"
    TOOL = "tool"


class ErrorTag(StrEnum):
    ERRNO = "errno"


FunctionTag = Union[MandatoryFunctionTag, BonusFunctionTag, ToolFunctionTag]
LibASMTag = Union[CategoryTag, FunctionTag, ErrorTag]

all_tags: Sequence[LibASMTag] = (
    list(MandatoryFunctionTag)
    + list(BonusFunctionTag)
    + list(CategoryTag)
    + list(ErrorTag)
)


def tag_test(tag: LibASMTag):
    return mark.__getattr__(tag)
