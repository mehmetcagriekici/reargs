from pydantic import BaseModel
from typing import List, Literal

# Base Models
class SentenceMetaData(BaseModel):
    paragraph_index: int
    sentence_index: int
    full_paragraph_text: str

class SentenceItem(BaseModel):
    text: str
    metadata: SentenceMetaData

class Cluster(BaseModel):
    cluster_id: int
    sentences: List[SentenceItem]

class LLMCluster(BaseModel):
    cluster_id: int
    title: str
    condensed_summary: str
    keywords: List[str]
    importance: Literal["high", "medium", "low"]
    cohesion: float
    representative_sentence: str
    redundancy_notes: str

    
# reargs engine output
class ClusterResponse(BaseModel):
    id: str
    filename: str
    content_type: str
    clusters: List[List[SentenceItem]]

# reargs llm input
class LLMRequest(BaseModel):
    clusters: List[Cluster]
    
# reargs llm output
class LLMResponse(BaseModel):
    id: str
    clusters: List[LLMCluster]
