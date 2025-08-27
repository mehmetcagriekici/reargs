from utils.constants import HARD_CLUSTER_KEY, SOFT_CLUSTER_KEY, PARAGRAPH_LEVEL, ARTICLE_LEVEL
from utils.separators import MAP_SEPARATOR, NODE_SEPARATOR, INNER_SEPARATOR, SUBS_SEPARATOR

# function to create a readable output map from cluster(article/paragraphs) maps
def create_output_map(article_clusters, paragraph_clusters):
    # dict to store inner cluster ids
    inner_cluster_ids = {}

    output_map = "###\n"

    # iterate over the article clusters (cluster__index)
    paragraphs = []
    for cluster_id in article_clusters:
        cluster = article_clusters[cluster_id]
        # get cluster values
        cluster_type, cluster_sentences, cluster_indexes, cluster_subs = get_cluster_values(cluster)

        # create an article string
        article_string = assign_cluster_string(cluster_indexes, cluster_sentences, cluster_type, ARTICLE_LEVEL)

        # check if there are sub clusters
        if len(cluster_subs) > 0:
            sub_string = handle_sub_clusters(cluster_subs, ARTICLE_LEVEL)
            # update article string
            article_string = join_clusters([article_string, sub_string], separator=SUBS_SEPARATOR)
        
        ### create inner strings if they exist
        paragraph_id = f"paragraph--{cluster_id.split("__")[1]}"
        # check if the current paragraph has inner clusters
        if  paragraph_id in paragraph_clusters:
            # save the cluster id on the memo so it will be omitted on the paragraph level iteration
            inner_cluster_ids[paragraph_id] = paragraph_id
            # get the current paragraph cluster
            paragraph_cluster = paragraph_clusters[paragraph_id]
            # get the paragraph string
            paragraph_string = handle_paragraph_clusters(paragraph_cluster)
            # add paragraph string to its parent article string
            article_string = join_clusters([article_string, paragraph_string], separator=INNER_SEPARATOR)

        paragraphs.append(article_string)
    # join paragraphs
    article = join_clusters(paragraphs, separator=NODE_SEPARATOR)
        
    sentences = []
    # iterate over the paragraph clusters for the stand alone clusters
    # (paragraph--index)
    for cluster_id in paragraph_clusters:
        if cluster_id not in inner_cluster_ids: 
            sentence_clusters = paragraph_clusters[cluster_id]
            paragraph_string = handle_paragraph_clusters(sentence_clusters)
            sentences.append(paragraph_string)
    # join sentences
    paragraph = join_clusters(sentences, separator=NODE_SEPARATOR)
    
    # separation between main and rest -
    if len(article) == 0:
        article = "No Article Level Clusters..."
    output_map += join_clusters([article, paragraph], separator=MAP_SEPARATOR)
        
    return output_map.strip() + "\n###\n"

# helper function to join clusters
def join_clusters(strings, separator="\n"):
    return separator.join(strings)

# helper function to get cluster values
def get_cluster_values(cluster):
    cluster_type = cluster["cluster_type"]
    cluster_sentences = cluster["cluster_sentences"]
    cluster_indexes = cluster["cluster_indexes"]
    sub_clusters = cluster["sub_clusters"]

    return (cluster_type, cluster_sentences, cluster_indexes, sub_clusters)

# helper fucntion to assign a cluster string depending on the level and the type
def assign_cluster_string(indexes, sentences, c_type, level):
    string = None
    if c_type == HARD_CLUSTER_KEY:
        string = create_cluster_string(indexes, sentences, True, level)
    if c_type == SOFT_CLUSTER_KEY:
        string = create_cluster_string(indexes, sentences, False, level)   
    return string 

# helper function to create a cluster string for the ouput
# level -> bool : article level True, paragraph level False
# type -> bool : hard cluster True, soft cluster False
def create_cluster_string(indexes, sentences, c_type, level):
    # create the cluster title
    cluster_title = create_cluster_title(indexes, c_type, level) 
    # create cluster body
    cluster_body = create_cluster_body(indexes, sentences, level)
    # join title and the body
    return cluster_title + "\n\n" + cluster_body

# helper function to create cluster title
def create_cluster_title(indexes, c_type, level):
    # join indexes
    nums = ", and ".join(", ".join(map(str, indexes)).rsplit(", ", 1))
    # finish the title depending on the cluster type
    end = f'are {"almost duplicates" if c_type else "semantically similar"}.'
    # unite cluster title
    return f'{"Paragraphs" if level else "Sentences"} {nums} {end}'

# helper function to create cluster body
def create_cluster_body(indexes, sentences, level):
    new_sentences = []
    # iterate over the indexes
    for i in range(len(indexes)):
        new_sentences.append(f'{"Paragraph" if level else "Sentence"} {indexes[i]}: { sentences[i]}')
    # join the sentences and build the body
    return "\n".join(new_sentences)

# helper function to handle the sub clusters
def handle_sub_clusters(clusters, level):
    strings = []
    # iterate over the sub clusters
    for cluster in clusters:
        # sub clusters do not have other sub classes - empty array
        c_type, sentences, indexes, _ = get_cluster_values(cluster)
        string = assign_cluster_string(indexes, sentences, c_type, level)
        strings.append(string)
    return join_clusters(strings)
    
# helper function to handle paragraph level clusters
# clusters inside a paragraph
def handle_paragraph_clusters(paragprah_cluster):
    strings = []
    # iterate over the clusters
    for cluster_id in paragprah_cluster:
        cluster = paragprah_cluster[cluster_id]
        # get cluster values
        _type, sentences, indexes, subs = get_cluster_values(cluster)
        # create a string for the cluster
        string = assign_cluster_string(indexes, sentences, _type, PARAGRAPH_LEVEL)
        # check if there are sub clusters
        if len(subs) > 0:
            sub_string = handle_sub_clusters(subs, PARAGRAPH_LEVEL)
            # join sub string with the current string
            string = join_clusters([string, sub_string], separator=SUBS_SEPARATOR) 
        strings.append(string)
    return join_clusters(strings) 