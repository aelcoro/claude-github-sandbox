"""Tests for string_utils."""

from src.string_utils import reverse, is_palindrome, word_count


def test_reverse():
    assert reverse("hello") == "olleh"
    assert reverse("") == ""
    assert reverse("a") == "a"


def test_is_palindrome_basic():
    assert is_palindrome("racecar")
    assert is_palindrome("level")
    assert not is_palindrome("python")


def test_is_palindrome_ignores_case_and_punctuation():
    assert is_palindrome("A man, a plan, a canal: Panama")
    assert is_palindrome("No 'x' in Nixon")


def test_word_count():
    assert word_count("hello world") == 2
    assert word_count("one") == 1
    assert word_count("") == 0
    assert word_count("  multiple   spaces   here  ") == 3
