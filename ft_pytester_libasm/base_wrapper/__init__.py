"""
base_wrapper provides utilities to build wrappers around binary shared
libraries.
"""

from .base_wrapper import BaseWrapper
from .result import Result

__all__ = [
    "BaseWrapper",
    "Result",
]
