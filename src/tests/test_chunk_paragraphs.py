# tests/test_chunk_paragraphs.py
import pytest
from reargs_engine.chunk_paragraphs import chunk_paragraphs


@pytest.mark.parametrize(
    "text, expected",
    [
        ("", []),
        ("\n\n", []),
        ("single line", ["single line"]),
        ("para1\npara2", ["para1\npara2"]),
        ("para1\n\npara2\n\n\npara3", ["para1", "para2", "para3"]),
        ("  \n\n  \ntext  \n\n\nmore", ["text", "more"]),
        ("line1\nline2\n\nline3\nline4", ["line1\nline2", "line3\nline4"]),
    ]
)

def test_chunk_paragraphs_various_inputs(text, expected):
    result = chunk_paragraphs(text)
    assert result == expected


def test_chunk_paragraphs_keeps_internal_newlines():
    text = "First paragraph with\nmultiple\nlines\n\nSecond para"
    result = chunk_paragraphs(text)
    assert len(result) == 2
    assert "multiple\nlines" in result[0]
