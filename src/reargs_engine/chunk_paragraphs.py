import re

# function to split a text into paragraphs
def chunk_paragraphs(article):
    raw_paras = re.split(r"\n{2,}", article)
    return [p.strip() for p in raw_paras if p.strip()]
