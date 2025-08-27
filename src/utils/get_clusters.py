from sentence_transformers import SentenceTransformer

from utils.constants import HARD_CLUSTER_KEY, SOFT_CLUSTER_KEY

# Load a pretrained Sentence Transformer model
model = SentenceTransformer("all-mpnet-base-v2")

# takes an array of sentences
# sentence level bool
def get_clusters(sentences, is_sentence_level=False):
    soft_cluster_score = 0.6 if is_sentence_level else 0.8
    hard_cluster_score = 0.8 if is_sentence_level else 0.9

    # store cluster indexes (hard/soft)
    clusters = {}
    
    # Calculate embeddings by calling model.encode()
    embeddings = model.encode(sentences)
    # Calculate the embedding similarities
    similarities = model.similarity(embeddings, embeddings)

    # iterate over the similarities
    for i in range(len(similarities)):
        # similarities[i][j] current sentence value 1
        # check the similarity scores on the right side
        for j in range(i + 1, len(similarities)):
            # hard cluster
            if similarities[i][j] >= hard_cluster_score:
                clusters[f"{HARD_CLUSTER_KEY}__({i}, {j})"] = (i, j)
                continue
            # soft cluster / paragraph level
            if similarities[i][j] >= soft_cluster_score:
                clusters[f"{SOFT_CLUSTER_KEY}__({i}, {j})"] = (i, j)
                continue
    
    return clusters
            
    

