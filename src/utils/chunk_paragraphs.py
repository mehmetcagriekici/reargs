import re

# function to split a text into paragraphs
def chunk_paragraphs(article):
    # split the article into paragraphs - filter out the empty paragraphs
    
    return list(filter(lambda a: a, re.split(r"\n{2,}", article)))