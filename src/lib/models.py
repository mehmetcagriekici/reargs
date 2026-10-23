from pydantic import BaseModel
from typing import  Literal

# Base Models
class SentenceMetaData(BaseModel):
    paragraph_index: str
    sentence_index: str
    full_paragraph_text: str

class SentenceItem(BaseModel):
    text: str
    metadata: SentenceMetaData

class Cluster(BaseModel):
    cluster_id: int
    sentences: list[SentenceItem]

class LLMCluster(BaseModel):
    cluster_id: int
    title: str
    condensed_summary: str
    keywords: list[str]
    importance: Literal["high", "medium", "low"]
    cohesion: float
    representative_sentence: str
    redundancy_notes: str

    
# reargs engine output
class ClusterResponse(BaseModel):
    id: str
    filename: str
    content_type: str
    clusters: list[list[SentenceItem]]

# reargs llm input
class LLMRequest(BaseModel):
    clusters: list[Cluster]
    
# reargs llm output
class LLMResponse(BaseModel):
    id: str
    clusters: list[LLMCluster]

# chroma db data model - for both llm and cluster responses
class ChromaData(BaseModel):
    # name of the collection
    id: str
    # no collection level metada but document level metadata
    data: list[Cluster] | list[LLMCluster]
