"""Tests for the calculator module."""

import pytest

from src.calculator import add, subtract, multiply, divide, average


def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0.1, 0.2) == pytest.approx(0.3)


def test_subtract():
    assert subtract(5, 2) == 3
    assert subtract(0, 10) == -10


def test_multiply():
    assert multiply(4, 3) == 12
    assert multiply(-2, 5) == -10
    assert multiply(0, 999) == 0


def test_divide():
    assert divide(10, 2) == 5
    assert divide(7, 2) == 3.5


def test_divide_by_zero_raises():
    with pytest.raises(ValueError):
        divide(1, 0)


def test_average():
    assert average([1, 2, 3, 4]) == 2.5
    assert average([10]) == 10
