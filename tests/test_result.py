#!/usr/bin/env python3

from ft_pytester_libasm.base_wrapper import Result


def test_result_integers():
    assert 1 == Result(1)
    assert not 0 == Result(1)
