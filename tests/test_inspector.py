from __future__ import annotations

from crashtest.inspector import Inspector

from .helpers import nested_exception
from .helpers import recursive_exception
from .helpers import simple_exception


def test_inspector_with_simple_exception():
    try:
        simple_exception()
    except ValueError as e:
        inspector = Inspector(e)

        assert e == inspector.exception
        assert not inspector.has_previous_exception()
        assert inspector.previous_exception is None
        assert "ValueError" == inspector.exception_name
        assert "Simple Exception" == inspector.exception_message
        assert len(inspector.frames) > 0


def test_inspector_with_nested_exception():
    try:
        nested_exception()
    except RuntimeError as e:
        inspector = Inspector(e)

        assert e == inspector.exception
        assert inspector.has_previous_exception()
        assert inspector.previous_exception is not None
        assert "RuntimeError" == inspector.exception_name
        assert "Nested Exception" == inspector.exception_message
        assert len(inspector.frames) > 0
        assert 1 == len(inspector.frames.compact())


def test_inspector_with_recursive_exception():
    try:
        recursive_exception()
    except RuntimeError as e:
        inspector = Inspector(e)

        assert e == inspector.exception
        assert not inspector.has_previous_exception()
        assert inspector.previous_exception is None
        assert "RecursionError" == inspector.exception_name
        assert "maximum recursion depth exceeded" == inspector.exception_message
        assert len(inspector.frames) > 0
        assert len(inspector.frames) > len(inspector.frames.compact())
