import pytest

from lib.pdf_processor import pdf_processor

# ────────────────────────────────────────────────
# Fixtures — small real-world-like PDF byte contents
# ────────────────────────────────────────────────

@pytest.fixture
def empty_pdf_bytes():
    # Minimal valid PDF with no tex
    return (
        b"%PDF-1.4\n"
        b"1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj\n"
        b"2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj\n"
        b"3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] >> endobj\n"
        b"xref\n"
        b"0 4\n"
        b"0000000000 65535 f \n"
        b"0000000010 00000 n \n"
        b"0000000075 00000 n \n"
        b"0000000120 00000 n \n"
        b"trailer << /Size 4 /Root 1 0 R >>\n"
        b"startxref\n"
        b"180\n"
        b"%%EOF"
    )


@pytest.fixture
def simple_one_page_pdf_bytes():
    # One page with three short text blocks
    return (
        b"%PDF-1.3\n"
        b"1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n"
        b"2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n"
        b"3 0 obj<</Type/Page/MediaBox[0 0 595 842]/Parent 2 0 R/Resources<</Font<</F1 4 0 R>>>>/Contents 5 0 R>>endobj\n"
        b"4 0 obj<</Type/Font/Subtype/Type1/BaseFont/Helvetica>>endobj\n"
        b"5 0 obj<</Length 120>>stream\n"
        b"BT /F1 24 Tf 100 700 Td (Hello world) Tj\n"
        b"ET\n"
        b"BT /F1 14 Tf 100 650 Td (This is line two.) Tj\n"
        b"ET\n"
        b"BT /F1 14 Tf 100 600 Td (Third paragraph here.) Tj\n"
        b"ET\n"
        b"endstream endobj\n"
        b"xref\n0 6\n0000000000 65535 f \n0000000015 00000 n \n0000000070 00000 n \n0000000120 00000 n \n0000000220 00000 n \n0000000400 00000 n \n"
        b"trailer<</Size 6/Root 1 0 R>>\n"
        b"startxref\n520\n%%EOF"
    )


@pytest.fixture
def multi_page_minimal_pdf_bytes():
    # Two pages — first has text, second is empty
    return (
        b"%PDF-1.4\n"
        b"1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj\n"
        b"2 0 obj << /Type /Pages /Kids [3 0 R 4 0 R] /Count 2 >> endobj\n"
        b"3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Contents 5 0 R >> endobj\n"
        b"4 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] >> endobj\n"
        b"5 0 obj << /Length 60 >> stream\n"
        b"BT /F1 12 Tf 80 750 Td (Page one content only) Tj ET\n"
        b"endstream endobj\n"
        b"xref\n"
        b"0 6\n"
        b"0000000000 65535 f \n0000000010 00000 n \n0000000060 00000 n \n0000000120 00000 n \n0000000200 00000 n \n0000000280 00000 n \n"
        b"trailer << /Size 6 /Root 1 0 R >>\n"
        b"startxref\n350\n%%EOF"
    )


# ────────────────────────────────────────────────
# Tests
# ────────────────────────────────────────────────

def test_empty_pdf_returns_empty_string(empty_pdf_bytes):
    result = pdf_processor(empty_pdf_bytes)
    assert result == ""


def test_simple_pdf_extracts_all_text_blocks(simple_one_page_pdf_bytes):
    result = pdf_processor(simple_one_page_pdf_bytes)

    expected_snippets = [
        "Hello world",
        "This is line two.",
        "Third paragraph here."
    ]

    for snippet in expected_snippets:
        assert snippet in result

        # Also check that paragraphs are separated
        assert "\n\n" in result


def test_multi_page_only_extracts_text_from_pages_that_have_it(multi_page_minimal_pdf_bytes):
    result = pdf_processor(multi_page_minimal_pdf_bytes)

    assert "Page one content only" in result
    assert len(result.strip().split("\n\n")) == 1   # only one block
    assert "Page two" not in result


def test_strips_whitespace_from_each_block(simple_one_page_pdf_bytes):
    result = pdf_processor(simple_one_page_pdf_bytes)
    lines = [line.strip() for line in result.split("\n\n") if line.strip()]

    assert all(len(line) > 0 for line in lines)  # no empty paragraphs
    assert not any(line.startswith(" ") or line.endswith("  ") for line in lines)


def test_raises_error_on_invalid_pdf_bytes():
    invalid = b"This is not a PDF at all %PDF should be first but isn't"

    with pytest.raises(Exception):  # usually RuntimeError or ValueError from pymupdf
        pdf_processor(invalid)


def test_handles_pdf_with_only_newlines_and_spaces():
# Edge case: blocks exist but contain only whitespace

    pdf_bytes = (
        b"%PDF-1.3\n"
        b"1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj 2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n"
        b"3 0 obj<</Type/Page/MediaBox[0 0 595 842]/Contents 4 0 R>>endobj\n"
        b"4 0 obj<</Length 30>>stream BT /F1 12 Tf 100 700 Td (   ) Tj ET endstream endobj\n"
        b"xref\n0 5\n0000000000 65535 f \n... (shortened)\n"
        b"trailer<</Size 5/Root 1 0 R>>\nstartxref\n...\n%%EOF"
    )

    result = pdf_processor(pdf_bytes)
    assert result == ""   # after .strip() → skipped
