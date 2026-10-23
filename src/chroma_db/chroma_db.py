import chromadb

import os
from dotenv import load_dotenv
from lib.models import  Cluster, LLMCluster

# load the api key from .env file
load_dotenv()

api_key = os.environ.get("CHROMA_API_KEY")
chroma_tenant = os.environ.get("CHROMA_TENANT")
chroma_db = os.environ.get("CHROMA_DATABASE")

client = chromadb.CloudClient(
    tenant=chroma_tenant,
    database=chroma_db,
    api_key=api_key
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
    # paragraph_index: str
    # sentence_index: str
    # full_paragraph_text: str

# collection names are uuids of the reargs response models
# it's practically zero to get same collection name
def generate_collection(collection_name: str, chromaData: list[Cluster] | list[LLMCluster]):
    # create a collection on the cloud
    collection = client.create_collection(name=collection_name)

    # extract ids and the documents from the data - models described above -
    # cluster already has metadata - document level -
    ids = []
    documets = []

    # iterate over the chroma data
    for data in chromaData:
        ids.append(str(data.cluster_id)) # exist in both

        # stringify rest of the data to be appended to documents
        doc = ""
        if isinstance(data, Cluster):
            # only sentence text goes into chroma db
            doc += "\n".join([sentence_item.text for sentence_item in data.sentences])

        if isinstance(data, LLMCluster):
            # strings that go to chroma db
            doc += f"{data.title} {data.condensed_summary}"
            doc += "\n"
            # list that goes to chroma db
            doc += " ".join(data.keywords)
        
        # append doc to the documents
        documets.append(doc)
        
    # add documents and ids to the collection
    collection.add(ids=ids,
                   documents=documets,
                   )

# query collection and get data
def get_queries(collection_name, query, limit):
    collection = client.get_collection(name=collection_name)
    
    res = collection.query(query_texts=[query],
                           n_results=limit
                           )
    # query result is a dict, not an object -> index by key
    return res["documents"]
    

# delete collection
def delete_collection(collection_name):
    client.delete_collection(name=collection_name)
