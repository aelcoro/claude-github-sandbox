"""Simple string helpers for experimenting with Claude refactors and tests."""


def reverse(text: str) -> str:
    """Return the reversed version of a string."""
    return text[::-1]


def is_palindrome(text: str) -> bool:
    """Return True if the input reads the same forwards and backwards.

    Casing and non-alphanumeric characters are ignored.
    """
    cleaned = "".join(ch.lower() for ch in text if ch.isalnum())
    return cleaned == cleaned[::-1]


def word_count(text: str) -> int:
    """Return the number of whitespace-separated words in `text`."""
    return len(text.split())
