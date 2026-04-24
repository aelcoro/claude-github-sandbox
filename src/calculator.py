"""
A small calculator module used as a sandbox for experimenting with Claude in GitHub.

Feel free to ask Claude to:
  - add new operations (power, modulo, square root, etc.)
  - refactor for better style
  - add type hints / docstrings
  - find and fix bugs (there's at least one intentional quirk below!)
  - write more tests
"""

from typing import Union

Number = Union[int, float]


def add(a: Number, b: Number) -> Number:
    """Return the sum of two numbers."""
    return a + b


def subtract(a: Number, b: Number) -> Number:
    """Return a minus b."""
    return a - b


def multiply(a: Number, b: Number) -> Number:
    """Return the product of two numbers."""
    return a * b


def divide(a: Number, b: Number) -> float:
    """Return a divided by b. Raises ValueError if b is 0."""
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b


def power(a: Number, b: Number) -> Number:
    """Return `a` raised to the power of `b`.

    Examples:
        power(2, 3)    -> 8
        power(9, 0.5)  -> 3.0
        power(2, -1)   -> 0.5
        power(0, 0)    -> 1  (follows Python's convention)
    """
    return a ** b


def average(numbers: list[Number]) -> float:
    """Return the arithmetic mean of a list of numbers.

    Raises:
        ValueError: if `numbers` is empty (the mean of zero values is undefined).
    """
    if not numbers:
        raise ValueError("Cannot take the average of an empty list.")
    return sum(numbers) / len(numbers)


if __name__ == "__main__":
    print("2 + 3 =", add(2, 3))
    print("10 / 4 =", divide(10, 4))
    print("2 ** 10 =", power(2, 10))
    print("avg([1, 2, 3, 4]) =", average([1, 2, 3, 4]))
