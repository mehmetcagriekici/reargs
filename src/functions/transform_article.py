import os

from utils.constants import PATH_TO_TRANSFORMS
from utils.chunk_paragraphs import chunk_paragraphs
from utils.chunk_sentences import chunk_sentences
from utils.get_clusters import get_clusters
from utils.create_cluster_map import create_cluster_map
from utils.create_output_map import create_output_map

from functions.write_output import write_output


# function to transform a text file using sentence transformers
def transform_article():
    paragraph_clusters_map = {}

    # article is the only file inside the transforms folder
    article_file = open(os.path.join(PATH_TO_TRANSFORMS, os.listdir(PATH_TO_TRANSFORMS)[0]))
    article = article_file.read() 

    # chunk the current article into paragraphs
    paragraphs = chunk_paragraphs(article)

    # close the article file
    article_file.close()
       
    ### reduce/transform on paragraph level
    # iterate over each paragraph of the current article
    for i in range(len(paragraphs)):
        # create a unique id for the current paragraph using the current paragraph index and concatanate it with the current article id
        paragraph_id = f"paragraph--{i}"
        # chunk the paragraph into sentences
        sentences = chunk_sentences(paragraphs[i])
        # ignore titles
        if len(sentences) > 1:
            # get paragraph clusters - sentences inside the current paragraph - deep clusters
            paragraph_clusters = get_clusters(sentences, is_sentence_level=True)
            # if there are clusters - high similarity indexes
            if len(paragraph_clusters) > 0:
                # create a cluster map for the current paragraph
                cluster_map = create_cluster_map(sentences, paragraph_clusters, paragraph_id)
                # save the cluster
                paragraph_clusters_map[paragraph_id] = cluster_map
    
    ### reduce/transform on article level
    article_clusters = get_clusters(paragraphs)
    article_clusters_map = create_cluster_map(paragraphs, article_clusters, "cluster")
    print("File transformation successfully completed!")

    
    # create a map showing all the transformations
    # string
    output_map = create_output_map(article_clusters_map, paragraph_clusters_map)

    # write the output
    write_output(output_map)

    # inform the user that process is over.
    print("The operation completed successfully. A copy of the results has been saved in the output folder.")



            
 

