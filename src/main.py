from fastapi import FastAPI

from reargs_engine.reargs_engine import ReargsEngine
from reargs_llm.reargs_llm import ReargsLLM

from .models import ClusterResponse, LLMRequest, LLMResponse

# fast api server
app = FastAPI()
# reargs engine
reargs_engine = ReargsEngine()
# reargs llm
reargs_llm = ReargsLLM()

# API endpoints

# get
# return all clusters
# later with chroma db
@app.get("/similarities/")
async def get_similarities():
    return {"message": "will be implemented after chromadb and data persistency."}

# return all responses
# later with chroma db
@app.get("/similarities/llm/")
async def get_similarities():
    return {"message": "will be implemented after chromadb and data persistency."}

# post
# get document, post clusters from reargs engine
@app.post("/similarities/")
async def post_similarities():
    return {"message": "takes a document as req body, and returns clusters as a json object."}

# get clusters, post response 
@app.post("/similarities/llm/")
async def post_similarities_llm(clusters: LLMRequest):
    return {"message": "takes clusters as a list of cluster objects, returns an llm response as a json object"}
