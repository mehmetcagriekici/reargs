<<<<<<< HEAD
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
# reargs engine
reargs_engine = ReargsEngine()
# reargs llm
reargs_llm = ReargsLLM()

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
async def delete_collection(collection_name: str):
    delete_collection(collection_name)
    return {"message": f"Collection {collection_name} is deleted from the chroma db cloud."}

# get
# return clusters from chroma db with query and collection name
@app.get("/similarities/{collection_name}/{query}/{limit}")
async def get_similarities(collection_name: str, query: str, limit: int):
    docs = get_queries(collection_name, query, limit)
    return {
        "message": f"chroma db results for the query: {query} from the collection: {collection_name}",
        "collection_name": collection_name,
        "documents": docs
    }

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
        text = (await file.read()).decode("utf-8")

    # .md
    if file.content_type == "text/markdown":
        # markdown file content
        markdown_content = (await file.read()).decode("utf-8")
        # extract text from markdown (convert to html -> extract text)
        text = markdown_processor(markdown_content)

    if file.content_type == "application/pdf":
        content_bytes = await file.read()
        text = pdf_processor(content_bytes)

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
=======
import sys

from functions.get_article import get_article
from functions.transform_article import transform_article
from functions.write_article import write_article

def main():    
    # get the article file
    get_article(sys.argv)
    # transform the file contents
    transform_article()
    # write the new file into the output folder
    write_article()
    
main()
>>>>>>> efeec18 (get files changes before transformer implementation, app now works with 1 single txt file)
