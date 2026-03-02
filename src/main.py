import uuid

from fastapi import FastAPI, UploadFile, HTTPException
from typing import Annotated

from reargs_engine.reargs_engine import ReargsEngine
from reargs_llm.reargs_llm import ReargsLLM
from chroma_db.chroma_db import generate_collection

from .models import ClusterResponse, LLMRequest, LLMResponse, ChromaData

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
# return clusters from chroma db with query and collection name
@app.get("/similarities/{collection_name}/{query}")
async def get_similarities(collection_name: str, query: str):
    return {"message": "will be implemented after chromadb and data persistency."}

# save into the chromadb
# post clusters into the chroma db to be queried
@app.post("/similarities/save/")
async def save_similarities(chromaData: ChromaData):
    # generate a collection and seed the collection - chromadb database - with the data
    generate_collection(chromaData.id, chromaData.data)
    return {"message": f"A new collection created with the name: {chromaData.id} on the chromadb cloud."}

# delete an existing collection - irreversible

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
