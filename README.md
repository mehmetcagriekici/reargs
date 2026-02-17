# ReArgs

**ReArgs** is a cloud-native semantic analysis engine that leverages Large Language Models (LLMs) and vector embeddings to detect patterns, redundancies, and thematic clusters in written content. 

Originally built as a local CLI tool to help writers identify unintentional repetitions, ReArgs has evolved into a containerized REST API powered by a Retrieval-Augmented Generation (RAG) architecture.

## 🚀 The Mission

Writing complex technical articles often leads to fragmented drafts and semantic "bloat." ReArgs automates the identification of these patterns, providing a data-driven map of a document's logical flow. By integrating Google's Gemini LLM and Sentence-Transformers, the system doesn't just find duplicates—it understands the context and intent of your writing.

## 🛠️ Technology Stack

- **Language:** Python 3.10+
- **API Framework:** FastAPI / Uvicorn
- **AI/ML Layer:** Google Gemini (LLM), Sentence-Transformers (Embeddings)
- **Data Persistence:** ChromaDB (Vector Database for RAG)
- **Containerization:** Docker & Docker Compose
- **Orchestration:** Kubernetes (K8s)
- **CI/CD:** GitHub Actions

## 🏗️ System Architecture

ReArgs is designed with a modern, decoupled architecture:

1.  **Client Layer:** Users interact with the system via a RESTful API.
2.  **Processing Engine:** Text is ingested, cleaned, and split into semantic chunks.
3.  **Embedding & Vectorization:** Chunks are converted into high-dimensional vectors using Sentence-Transformers and stored in a local vector database.
4.  **Intelligence Layer (RAG):** When a query is made or a document is analyzed, the system retrieves relevant context from the vector store and passes it to the Gemini LLM for high-level semantic insights.
5.  **Deployment:** The entire stack is containerized, ensuring consistent environments from development to production.

## 📦 Installation & Setup

### Prerequisites
- Docker & Docker Compose
- Google Gemini API Key

### Local Development
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/reargs.git
   cd reargs
   ```
2. Create a `.env` file and add your Gemini API Key:
    ```
    GEMINI_API_KEY=your_api_key_here
    ```
3. Build and run the containers:
   ```bash
   docker-compose up --build
   ```
4. Your API will be available at `http://localhost:8000`
