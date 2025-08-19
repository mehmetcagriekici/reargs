import re

# function to split a paragraph into sentences
def chunk_sentences(paragraph):
    # split the paragraph into sentences - filter out the empty sentences
    return list(filter(lambda s: s, re.split(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<!\b[A-Z]\.)(?<=\.|\?|!)\s", paragraph)))