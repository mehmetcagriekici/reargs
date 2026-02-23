# imports
# external
import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from google import genai

# internal
from chunk_paragraphs import chunk_paragraphs
from chunk_sentences import chunk_sentences

load_dotenv()
gemini_api_key = os.environ.get("GEMINI_API_KEY")

# main
# usage order:
# 1) build a docmap with an input text
# 2) create embeddings from the document and generate similarities
# 3) create chunks from similarities to be sent to the LLM
class ReargsEngine:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.embeddings_model = SentenceTransformer(model_name)
        # holds sentences to be embedded with metadata (paragraph id, sentence index)
        self.docmap = dict()
        # similarities map text_id: sims (dict) (similarity scores between the current text and the rest)
        self.simap = dict()
        # article grouped by similarities using simap and docmap -> final product before LLM
        self.clusters = list()

    # creates clusters from similarities - optimizing and organizing the data before sending it to the LLM and make it more structured for better results.
    def generate_clusters(self):
        # track the sentences already visited
        visited = set()

        # iterate over the docmap
        for i in self.docmap:
            if i not in visited:
                # initiate a new cluster
                cluster = []
                # queue to control the loop -> stores so far visited sentences and pops them -> initiated with the current sentence if not in visited
                queue = [i]

                while queue:
                    curr_idx = queue[0]
                    cluster.append(curr_idx)

                    # get all the neighbours -> first check everything curr_index points to
                    neighbors = list(self.simap.get(curr_idx, {}).keys())

                    # check everything that points to curr_idx -> to not create duplicate clusters
                    for prev_idx, matches in self.simap.items():
                        if curr_idx in matches:
                            neighbors.append(prev_idx)

                    # add neighbors to visited and the queue
                    for neighbor in neighbors:
                        if neighbor not in visited:
                            visited.add(neighbor)
                            queue.append(neighbor)

                    # only keep clusters with more than one sentence
                    if len(cluster) > 1:
                        # hydrate a cluster with the actual data from the docmap
                        hydrated_cluster = [self.docmap[idx] for idx in cluster]
                        self.clusters.append(hydrated_cluster)

    # generate embeddings from the sentences in the docmap, calculate the similarities, store them inside the similarities map with metadata
    # threshold -> min similarity score to be stored - default -> 0.75
    def generate_similarities(self, threshold=0.6):
        if len(self.docmap) == 0:
            raise ValueError("document map is empty. cannot continue with embeddings.")

        # list to store docmap texts -sentences- to be embedded
        # as of 3.7 python dicts are "insertion ordered"
        texts = [] # sentences
        # iterate over the docmap push texts ito the list to be embedded
        for k in self.docmap:
            texts.append(self.docmap[k]["text"])

        # create embeddings from the texts
        embeddings = self.embeddings_model.encode(texts)

        # calculate similarities from the embeddings nxn -> matrix
        similarities = self.embeddings_model.similarity(embeddings, embeddings)

        # iterate over the similarities to store them in the simap (similarities[i][j] where i == j -> sentence itself, metada is stored at self.docmap[i])
        for i in range(len(similarities)):
            # initiate a sub dictionary for each sentence matching the insert order in docmap
            self.simap[i] = dict()
            
            # i == j -> sentence itself -> store only the right side to not to make duplications
            for j in range(i + 1, len(similarities)):
                # sentences accessible from the docmap
                # if similarity score is above the threshold push it to the similarities map to be clustered
                if similarities[i][j] >= threshold:
                    self.simap[i][j] = similarities[i][j]

    # text -> entire document
    def build_docmap(self, text):
        # chunk the text into paragraphs
        paragraphs = chunk_paragraphs(text)

        # sentence index document wise
        docmap_index = 0
        for i in range(len(paragraphs)):
            p_index = f"paragraph_index_{i}"
            p = paragraphs[i]

            # chunk the paragraph into sentences
            sentences = chunk_sentences(p)
            for j in range(len(sentences)):
                # skip empty sentences
                if sentences[j].strip() == "":
                    continue
                
                # sentence index inside the paragraph
                s_index = f"sentence_index_{j}"
                s = sentences[j]

                # will be used for embeddings
                self.docmap[docmap_index] = {
                    "text": s,
                    "metadata": {
                        "paragraph_index": p_index,
                        "sentence_index": s_index,
                        "full_paragraph_text": p
                    }
                }
                
                docmap_index += 1
