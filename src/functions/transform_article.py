import os

from utils.constants import PATH_TO_TRANSFORMS
from utils.chunk_paragraphs import chunk_paragraphs
from utils.chunk_sentences import chunk_sentences
from utils.get_clusters import get_clusters
from utils.create_cluster_map import create_cluster_map

# recursive - increase level after each reduction
# function to transform a text file using sentence transformers
def transform_article(level=0):
    # inform the user
    print("Running Sentence Transformers...")

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
                # create a cluster map for the current paragraph
                cluster_map = create_cluster_map(sentences, paragraph_clusters, paragraph_id)
                similarities_paragraphs[paragraph_id] = cluster_map

        # increase the paragraph index
        i += 1
    
    # after article level reduction
    print("Transformation is complete! Your output is ready inside the outputs folder.")      

    print(similarities_paragraphs)
    

            
 

