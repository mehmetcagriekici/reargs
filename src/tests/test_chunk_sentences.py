# tests/test_chunk_sentences.py
import pytest
from reargs_engine.chunk_sentences import chunk_sentences


@pytest.mark.parametrize(
    "paragraph, expected",
    [
        ("", []),
        ("One sentence.", ["One sentence."]),
        ("Hello. World!", ["Hello.", "World!"]),
        ("Dr. Smith said yes. Ms. Jones said no.", ["Dr. Smith said yes.", "Ms. Jones said no."]),
        ("He said Hello! She replied.", ["He said Hello!", "She replied."]),
        ("This is sentence one? This is two! And three...", ["This is sentence one?", "This is two!", "And three..."]),
        ("A.B.C. should be one sentence.", ["A.B.C. should be one sentence."]),
        ("  Leading.  spaces.   ", ["Leading.", "spaces."]),
    ]
)
def test_chunk_sentences_basic_cases(paragraph, expected):
    result = chunk_sentences(paragraph)
    assert result == expected


def test_chunk_sentences_handles_multiple_spaces():
    text = "Hello.   World!     Test."
    assert chunk_sentences(text) == ["Hello.", "World!", "Test."]


def test_chunk_sentences_does_not_split_inside_abbreviations():
    text = "Mr. Smith Jr. went home. It was late."
    result = chunk_sentences(text)
    assert len(result) == 2
    assert "Jr." in result[0]
