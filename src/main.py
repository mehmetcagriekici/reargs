import uuid

from fastapi import FastAPI, UploadFile, HTTPException
from typing import Annotated

from reargs_engine.reargs_engine import ReargsEngine
from reargs_llm.reargs_llm import ReargsLLM
from chroma_db.chroma_db import generate_collection, delete_collection, get_queries

from lib.markdown_processor import markdown_processor
from lib.pdf_processor import pdf_processor
from lib.models import ClusterResponse, LLMRequest, LLMResponse, ChromaData

# fast api server
app = FastAPI()

# API endpoints
# deployment
@app.get("/")
def health_check():
    return {
        "service": "ReArgs Similarity API",
        "status": "ok",
        "docs": "/docs"
    }
# delete
# delete a collection from chroma db
@app.delete("/similarities/delete/{collection_name}")
def delete_collection_from_chroma(collection_name: str):
    delete_collection(collection_name)
    return {"message": f"Collection {collection_name} is deleted from the chroma db cloud."}

# get
# return clusters from chroma db with query and collection name
@app.get("/similarities/{collection_name}/{query}/{limit}")
def get_similarities_from_chroma(collection_name: str, query: str, limit: int):
    docs = get_queries(collection_name, query, limit)
    return {
        "message": f"chroma db results for the query: {query} from the collection: {collection_name}",
        "collection_name": collection_name,
        "documents": docs
    }

# save into the chromadb
# post clusters into the chroma db to be queried
@app.post("/similarities/save/")
def save_similarities_to_chroma(chromaData: ChromaData):
    # generate a collection and seed the collection - chromadb database - with the data
    generate_collection(chromaData.id, chromaData.data)
    return {"message": f"A new collection created with the name: {chromaData.id} on the chromadb cloud."}

# delete an existing collection - irreversible

# post
# get document, post clusters from reargs engine
# pass the document with the body
@app.post("/similarities/")
def post_similarities(file: UploadFile) -> ClusterResponse:

    # check if the uploaded file is .txt, .md or .pdf
    filename = file.filename.lower() if file.filename else ""
    txt = filename.endswith(".txt")
    markdown = filename.endswith(".md")
    pdf = filename.endswith(".pdf")
    if not txt and not markdown and not pdf:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    # .txt
    text = ""
    if txt:
        # plain text file content
        text = (file.file.read()).decode("utf-8")

    # .md
    if markdown:
        # markdown file content
        markdown_content = (file.file.read()).decode("utf-8")
        # extract text from markdown (convert to html -> extract text)
        text = markdown_processor(markdown_content)

    if pdf:
        content_bytes = file.file.read()
        text = pdf_processor(content_bytes)

    # reargs engine
    reargs_engine = ReargsEngine()
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
def post_similarities_llm(id: str, clusters: LLMRequest) -> LLMResponse:
    # reargs llm
    reargs_llm = ReargsLLM()
    # get clusters into the ReargsLLM
    reargs_llm.get_clusters(clusters.model_dump().get("clusters"))
    # generate content
    reargs_llm.generate_content()
    # return the structured llm response
    clusters = reargs_llm.get_response()
    return {
        "id": id,
        "clusters": clusters,
    }
