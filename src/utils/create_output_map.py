from utils.constants import HARD_CLUSTER_KEY, SOFT_CLUSTER_KEY, CLUSTER_BODY_SKELETON, CLUSTER_NODE_SKELETON, MAX_SENTENCE_LENGTH

# function to create a readable output map from cluster(article/paragraphs) maps
def create_output_map(article_clusters, paragraph_clusters):
    # dict to store inner cluster ids
    inner_cluster_ids = {}

    output_map = ""

    # iterate over the article clusters (cluster__index)
    for cluster_id in article_clusters:
        cluster = article_clusters[cluster_id]
        # get cluster values
        cluster_type, cluster_sentences, cluster_indexes = get_cluster_values(cluster)

        # create an article node
        article_node = None
        if cluster_type == HARD_CLUSTER_KEY:
            article_node = create_cluster_node(cluster_indexes, cluster_sentences, True, True)
        if cluster_type == SOFT_CLUSTER_KEY:
            article_node = create_cluster_node(cluster_indexes, cluster_sentences, False, True)

        # check if there are sub clusters
        
        ### create inner nodes if they exist
        inner_nodes = []
        paragraph_id = f"paragraph--{cluster_id.split("__")[1]}"
        # check if the current paragraph has inner clusters
        if  paragraph_id in paragraph_clusters:
            # save the cluster id on the memo so it will be omitted on the paragraph level iteration
            inner_cluster_ids[paragraph_id] = paragraph_id

            # iterate over the current paragraph clusters
            for inner_cluster_id in paragraph_clusters[paragraph_id]:
                inner_cluster = paragraph_clusters[paragraph_id][inner_cluster_id]
                # get cluster values
                inner_type, inner_sentences, inner_indexes = get_cluster_values(inner_cluster)

                # create a node for the inner cluster
                inner_node = None
                if inner_type == HARD_CLUSTER_KEY:
                    inner_node = create_cluster_node(inner_indexes, inner_sentences, True, False)
                if inner_type == SOFT_CLUSTER_KEY:
                    inner_node = create_cluster_node(inner_indexes, inner_sentences, False, False)

                # check if there are sub clusters

                # append the created node to the inner nodes
                if inner_node is not None:
                    inner_nodes.append(inner_node)
        
        ### join inner nodes

        ### append inner nodes to the article node

        ### append article node to the previous article node if one exsits

    # iterate over the paragraph clusters for the stand alone clusters
    # (paragraph--index)
    for cluster_id in paragraph_clusters:
        if cluster_id not in inner_cluster_ids:
            cluster = paragraph_clusters[cluster_id]
        
    return output_map

# helper function to get cluster values
def get_cluster_values(cluster):
    cluster_type = cluster["cluster_type"]
    cluster_sentences = cluster["cluster_sentences"]
    cluster_indexes = cluster["cluster_indexes"]

    return (cluster_type, cluster_sentences, cluster_indexes)

# helper function to create a cluster node for the ouput
# level -> bool : article level True, paragraph level False
# type -> bool : hard cluster True, soft cluster False
def create_cluster_node(indexes, sentences, level, c_type):
    # create the cluster title
    cluster_title = create_cluster_title(indexes, level, c_type) 
    # create cluster body
    cluster_body = create_cluster_body(indexes, sentences, level)
    # create the spaces for the node skeleton
    _s = " " * (len(cluster_title) - 1)
    # align the body
    indented_body = "\n".join(_s + line for line in cluster_body.splitlines())
    # join title and the body
    return cluster_title + CLUSTER_NODE_SKELETON(_s) + indented_body

# helper function to create cluster title
def create_cluster_title(indexes, level, type):
    # join indexes
    nums = ", and ".join(", ".join(map(str, indexes)).rsplit(", ", 1))
    # finish the title depending on the cluster type
    end = f'are {"almost duplicates" if type else "semantically similar"}.'
    # unite cluster title
    return f'{"Paragraphs" if level else "Sentences"} {nums} {end}'

# helper function to create cluster body
def create_cluster_body(indexes, sentences, level):
    new_sentences = []
    # iterate over the indexes
    for i in range(len(indexes)):
        new_sentences.append(f'{"Paragraph" if level else "Sentence"} {indexes[i]}: {sentences[i][:MAX_SENTENCE_LENGTH] + "..." if len(sentences[i]) > MAX_SENTENCE_LENGTH + 10 else sentences[i]}')
    # join the sentences and build the body
    return CLUSTER_BODY_SKELETON.join(new_sentences)

# helper function to handle the sub clusters
def handle_sub_clusters():
    pass