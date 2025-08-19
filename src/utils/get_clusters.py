from sentence_transformers import SentenceTransformer

from utils.constants import SOFT_CLUSTER_SCORE, HARD_CLUSTER_SCORE, HARD_CLUSTER_KEY, SOFT_CLUSTER_KEY

# Load a pretrained Sentence Transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

# takes an array of sentences
def get_clusters(sentences):
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
            if similarities[i][j] >= HARD_CLUSTER_SCORE:
                clusters[f"{HARD_CLUSTER_KEY}__[{i}, {j}]"] = [i, j]
                continue
            # soft cluster
            if similarities[i][j] >= SOFT_CLUSTER_SCORE:
                clusters[f"{SOFT_CLUSTER_KEY}__[{i}, {j}]"] = [i, j]
                continue
    
    return clusters
            
    