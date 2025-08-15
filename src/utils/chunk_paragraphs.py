import re

# function to split a text into paragraphs
def chunk_paragraphs(article):
    # split the article into paragraphs
    return re.split(r"\n{2,}", article)