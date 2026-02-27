import uuid

from fastapi import FastAPI, UploadFile, HTTPException
from typing import Annotated

from reargs_engine.reargs_engine import ReargsEngine
from reargs_llm.reargs_llm import ReargsLLM

from .models import ClusterResponse, LLMRequest, LLMResponse

from lib.markdown_processor import markdown_processor
from lib.pdf_processor import pdf_processor

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

# save into the chromadb
@app.post("/similarities/save/{similarity_id}")
async def save_similarities(similarity_id: str):
    return {"message": "will be implemented after chromadb and data persistency."}

# post
# get document, post clusters from reargs engine
# pass the document with the body
@app.post("/similarities/")
async def post_similarities(file: UploadFile) -> ClusterResponse:
    valid_types = ["text/plain", "text/markdown", "application/pdf"]

    # check if the uploaded file is .txt, .md or .pdf
    if file.content_type not in valid_types:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    # .txt
    text = ""
    if file.content_type == "text/plain":
        # plain text file content
        text = await file.read().decode("utf-8")

    # .md
    if file.content_type == "text/markdown":
        # markdown file content
        markdown_content = await file.read().decode("utf-8")
        # extract text from markdown (convert to html -> extract text)
        text = markdown_processor(markdown_content)

    if file.content_type == "application/pdf":
        content_bytes = await file.read()
        text = prf_processor(bytes)

    # build the docmap
    reargs_engine.build_docmap(text)
    # generate similarities
    reargs_engine.generate_similarities()
    # generate clusters
    reargs_engine.generate_clusters()

    # get clusters to be returned and saved to chromadb
    clusters = reargs_engine.get_clusters()

    # generate random uuid to be id
    x = uuid.uuid4()
    id = str(x)

    return {
        "id": id,
        "filename": file.filename,
        "content_type": file.content_type,
        "clusters": clusters,
    }

# get clusters, post response
# pass id with the paramaters - id of the clusters
@app.post("/similarities/llm/{id}")
async def post_similarities_llm(id: str, clusters: LLMRequest) -> LLMResponse:
    # get clusters into the ReargsLLM
    reargs_llm.get_clusters(clusters.clusters)
    # generate content
    reargs_llm.generate_content()
    # return the structured llm response
    clusters = reargs_llm.get_response()
    return {
        "id": id,
        "clusters": clusters,
    }
