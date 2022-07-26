from __future__ import annotations


def simple_exception():
    raise ValueError("Simple Exception")


def nested_exception():
    try:
        simple_exception()
    except ValueError:
        raise RuntimeError("Nested Exception")


def recursive_exception():
    def inner():
        outer()

    def outer():
        inner()

    inner()
