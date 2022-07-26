from __future__ import annotations

import inspect

from crashtest.frame import Frame
from tests.helpers import nested_exception
from tests.helpers import simple_exception


def test_frame():
    try:
        simple_exception()
    except ValueError as e:
        frame_info = inspect.getinnerframes(e.__traceback__)[0]
        frame = Frame(frame_info)
        same_frame = Frame(frame_info)
        assert frame_info.frame == frame.frame

    assert 11 == frame.lineno
    assert __file__ == frame.filename
    assert "test_frame" == frame.function
    assert "        simple_exception()\n" == frame.line

    with open(__file__) as f:
        assert f.read() == frame.file_content

    assert f"<Frame {__file__}, test_frame, 11>" == repr(frame)

    try:
        nested_exception()
    except Exception as e:
        frame_info = inspect.getinnerframes(e.__traceback__)[0]
        other_frame = Frame(frame_info)

    assert same_frame == frame
    assert other_frame != frame
    assert hash(same_frame) == hash(frame)
    assert hash(other_frame) != hash(frame)


def test_frame_with_no_context_should_return_empty_line():
    frame = Frame(inspect.FrameInfo(None, "filename.py", 123, "function", None, 3))

    assert "" == frame.line
