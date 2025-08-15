import os

from utils.constants import PATH_TO_TRANSFORMS
from utils.chunk_paragraphs import chunk_paragraphs
from utils.chunk_sentences import chunk_sentences

# function to transform a text file using sentence transformers
def transform_articles():
    # store the paragraphs and sentences
    
    # get the articles from the transforms
    articles = os.listdir(PATH_TO_TRANSFORMS)

    # iterate over the articles - we already know they exist from the get_articles
    for article in articles:
        # chunk the article into paragraphs
        article_paragraphs = chunk_paragraphs(article)
        # add the article paragraph
        # iterate over each paragraph
        for paragraph in article_paragraphs:
            # chunk the paragraph into sentences
            article_sentences = chunk_sentences(paragraph)
            # add the article sentence
