import os

from utils.constants import PATH_TO_TRANSFORMS
from utils.chunk_paragraphs import chunk_paragraphs
from utils.chunk_sentences import chunk_sentences
from utils.get_clusters import get_clusters


# function to transform a text file using sentence transformers
def transform_article():
    # inform the user
    print("Running Sentence Transformers...")
    # store records
    records = {}

    # store similarities inside the paragraph with unique id
    similarities_paragraphs = {}

    # article is the only file inside the transforms folder
    article = open(os.path.join(PATH_TO_TRANSFORMS, os.listdir(PATH_TO_TRANSFORMS)[0])).read() 
 
    # chunk the current article into paragraphs
    paragraphs = chunk_paragraphs(article)
       
    # iterate over each paragraph of the current article
    i = 0
    for paragraph in paragraphs:
        # create a unique id for the current paragraph using the current paragraph index and concatanate it with the current article id
        paragraph_id = f"paragraph--{i}"
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

        # re-write the reduced article into the transforms folder after each reduce
        
        # write a records file inside output after transform is complete 

    print("Transformation is complete! Your output is ready inside the outputs folder.")      

    print(similarities_paragraphs)
    

            
 

