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
class ReargsEngine:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.embeddings_model = SentenceTransformer(model_name)
        # holds sentences to be embedded with metadata (paragraph id, sentence index)
        self.docmap = dict()
        # similarities map
        self.simap = dict()

    # generate embeddings from the sentences in the docmap, calculate the similarities, store them inside the similarities map with metadata 
    def generate_similarities(self):
        if len(self.docmap) == 0:
            raise ValueError("document map is empty. cannot continue with embeddings.")

        # list to store docmap texts -sentences- to be embedded
        # as of 3.7 python dicts are "ordered"
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
            # initiate a sub dictionary for each sentence with the metadata from the docmap
            self.simap[i] = {
                text: self.docmap[i]["text"],
                metadata: self.docmap[i]["metadata"],
                # initiate similarity scores - id: similarity score
                sims: {}
            }
            
            # i == j -> sentence itself
            for j in range(len(similarities)):
                if i == j:
                    continue
                # sentences accessible from the docmap
                self.simap[i]["sims"][j] = similarities[i][j]

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
                    text: s,
                    metadata: {
                        paragraph_index: p_index,
                        sentence_index: s_index,
                        full_paragraph_text: p
                    }
                }
                
                docmap_index += 1
