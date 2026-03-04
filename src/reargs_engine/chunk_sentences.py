import re

# function to split a paragraph into sentences
def chunk_sentences(paragraph):
    if not paragraph.strip():
        return []

    pattern = r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<!\b[A-Z]\.)(?<!\.\.)(?<=[.!?])(?!\.)['\"]?\s+"
    
    raw_sentences = re.split(pattern, paragraph)

    sentences = [s.strip() for s in raw_sentences if s.strip()]
    return sentences
