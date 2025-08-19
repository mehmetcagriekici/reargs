import os
from sentence_transformers import SentenceTransformer

from utils.constants import PATH_TO_TRANSFORMS
from utils.chunk_paragraphs import chunk_paragraphs
from utils.chunk_sentences import chunk_sentences
from utils.get_clusters import get_clusters

# Load a pretrained Sentence Transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

# function to transform a text file using sentence transformers
def transform_articles():
    # store the similarities inside the article with unique id
    similarities_articles = {}
    # store similarities inside the paragraph with unique id
    similarities_paragraphs = {}

    # get the articles from the transforms
    articles = os.listdir(PATH_TO_TRANSFORMS)

    # store sentences before transforming
    # iterate over the articles - we already know they exist from the get_articles
    for article_path in articles:
        # create a unique id for the current article using the article path
        article_id = os.path.join(PATH_TO_TRANSFORMS, article_path)
        # read the file content using the article_id / in this case also the article address
        article = open(article_id).read() 
 
        # chunk the current article into paragraphs
        paragraphs = chunk_paragraphs(article)
       
        # iterate over each paragraph of the current article
        i = 0
        for paragraph in paragraphs:
            # create a unique id for the current paragraph using the current paragraph index and concatanate it with the current article id
            paragraph_id = article_id + f"--{i}"
            # chunk the paragraph into sentences
            sentences = chunk_sentences(paragraph)
            # ignore titles
            if len(sentences) > 1:
                # get paragraph clusters - sentences inside the current paragraph - deep clusters
                paragraph_clusters = get_clusters(sentences)
                # if there are clusters - high similarity indexes
                if len(paragraph_clusters) > 0:
                    # iterate over the clusters
                    similarities_paragraphs[paragraph_id] = paragraph_clusters

            # increase the paragraph index
            i += 1
        
        # re-write the article inside the transforms folder

    print(similarities_articles)
    print("---------------------")
    print(similarities_paragraphs)
    

            
 

