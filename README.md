# Reargs Similarity API

ReArgs is a semantic document analysis API that helps writers identify patterns and redundancies in their writing using AI.

## Features

- File upload and processing (.txt, .md, .pdf)
- Automatic document mapping, similarity calculation and clustering
- Persistent storage of clusters in Chroma vector database
- Natural language query of similar clusters
- LLM-powered content generation from selected clusters
- Collection management (create / delete)

## Tech Stack

- Python 3.11+
- FastAPI
- ChromaDB
- Custom Reargs Engine & Reargs LLM modules
- PDF and Markdown processing utilities
- Uvicorn (ASGI server)
- Docker + multi-stage build

## API Endpoints

| Method | Endpoint                                              | Description                                                  | Request                                      | Response                          |
|--------|-------------------------------------------------------|--------------------------------------------------------------|----------------------------------------------|-----------------------------------|
| POST   | /similarities/                                        | Upload document and return clusters                          | UploadFile (txt/md/pdf)                      | ClusterResponse (id + clusters)   |
| POST   | /similarities/save/                                   | Save clusters to a new Chroma collection                     | JSON: ChromaData (id, data)                  | Success message                   |
| GET    | /similarities/{collection_name}/{query}/{limit}       | Search similar items in a collection                         | Path: collection_name, query, limit          | Documents + metadata              |
| DELETE | /similarities/delete/{collection_name}                | Delete a Chroma collection                                   | Path: collection_name                        | Success message                   |
| POST   | /similarities/llm/{id}                                | Generate LLM content/response from selected clusters         | Path: id<br>Body: LLMRequest (clusters)      | LLMResponse (processed clusters)  |

## Installation & Running

The project uses pyproject.toml for dependency management (no requirements.txt file).

### Local Development

1. Create and activate virtual environment 
   python -m venv .venv 
   source .venv/bin/activate          # Linux/macOS 
		 
2. Install dependencies and project 
   pip install --upgrade pip 
   pip install -e .
			   
3. Run the API (development mode with auto-reload) 
   uvicorn src.main:app --reload --port 8000
				  
   For production-like run: 
   uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
						
### Running with Docker (recommended)
						
The repository includes a Dockerfile and docker-compose.yml.
						
1. Prepare environment variables (create .env file if needed) 
   Example .env content: 
   CHROMA_HOST=your-chroma-host-url 
   CHROMA_API_KEY=your-chroma-key
   CHROMA_DATABASE=your-chroma-database-name
   GEMINI_API_KEY=your-gemini-api-key
   
2. Build and start 
   docker compose up --build
										  
3. Access the API 
   http://localhost:8000 
   http://localhost:8000/docs  (interactive Swagger UI)
													  
4. Stop services 
   docker compose down
															   
## Docker Notes

- Multi-stage build → smaller final image 
- Uses CPU-only PyTorch 
- Runs as non-root user (appuser) 
- Single worker by default (can be adjusted in Dockerfile CMD) 
- Port 8000 exposed
															   
## Usage Examples

Upload document and get clusters
curl -X POST "http://localhost:8000/similarities/" -F "file=@report.md"
															   
Save clusters to Chroma  
curl -X POST "http://localhost:8000/similarities/save/" -H "Content-Type: application/json" -d '{"id": "doc-abc123", "data": [...]}'
															   
Query similar content 
curl "http://localhost:8000/similarities/doc-abc123/what%20is%20the%20main%20goal/5"
															   
Generate LLM response 
curl -X POST "http://localhost:8000/similarities/llm/doc-abc123" -H "Content-Type: application/json" -d '{"clusters": [...]}'
															   
Delete collection 
curl -X DELETE "http://localhost:8000/similarities/delete/doc-abc123"
