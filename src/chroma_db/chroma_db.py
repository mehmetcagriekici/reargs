import chromadb

import os
from dotenv import load_dotenv

# load the api key from .env file
load_dotenv()

api_key = os.environ.get("CHROMA_API_KEY")
chroma_tenant = os.environ.get("CHROMA_TENANT")
chroma_db = os.environ.get("CHROMA_DATABASE")

client = chromadb.CloudClient(
      api_key=api_key,
      tenant=chroma_tenant,
      database=chroma_db
)

# LLM data structure
    # cluster_id: int
    # title: str
    # condensed_summary: str # document
    # keywords: List[str]
    # importance: Literal["high", "medium", "low"]
    # cohesion: float
    # representative_sentence: str
    # redundancy_notes: str

# Cluster data structure
    # cluster_id: int
    # sentences: List[SentenceItem]

# Sentence Item
    # text: str # document
    # metadata: SentenceMetaData # document level metadata

# Sentence Item Metadata
    # paragraph_index: int
    # sentence_index: int
    # full_paragraph_text: str

# collection names are uuids of the reargs response models
# it's practically zero to get same collection name
def generate_collection(collection_name, chromaData):
    # create a collection on the cloud
    collection = client.create_collection(name=collection_name)

    # extract ids and the documents from the data - models described above -
    # cluster already has metadata - document level -
    ids = list()
    documets = list()

    # iterate over the chroma data
    for data in chromaData:
        ids.append(data.cluster_id) # exist in both

        # stringify rest of the data to be appended to documents
        doc = ""
        for key in data:
            if key != "cluster_id":
                # check if list
                pass
        
        # append doc to the documents
        documets.append(doc)
        
    # add documents and ids to the collection
    collection.add(ids=ids,
                   documents=documets,
                   )
