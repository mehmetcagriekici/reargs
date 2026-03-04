import pymupdf

def pdf_processor(bytes: bytes):
    # createish a pdf document from the file content bytes
    doc = pymupdf.open(stream=bytes, filetype="pdf")

    text_parts = []
    # iterate over the doc parts
    for page in doc:
        # get the blocks from the page
        # (x0, y0, x1, y1, "lines in block", block_no, block_type) ->index 4
        blocks = page.get_text("blocks")

        # add texts (lines) into the text parts - skip empty
        texts = blocks[4].strip()
        if texts:
            text_parts.append(texts)

    doc.close()

    # mimic paragraphs
    full_text = "\n\n".join(text_parts)

    # return the full text
    return full_text
