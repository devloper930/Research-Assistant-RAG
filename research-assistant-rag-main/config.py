# config.py (Updated)
import os
from dataclasses import dataclass

# Get the absolute path of the project's root directory
# This makes all other paths relative to the project folder itself
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

@dataclass(frozen=True)
class Config:
    # Paths are now relative to the project root
    PDF_GLOB       = os.path.join(ROOT_DIR, "docs", "*.pdf")
    MODEL_PATH     = os.path.join(ROOT_DIR, "models", "gemma-2-2b-it-Q4_K_M.gguf")
    INDEX_DIR      = os.path.join(ROOT_DIR, "faiss_index")
    
    # Model and RAG parameters
    CHUNK_SIZE     = 2048
    CHUNK_OVERLAP  = 512
    EMBEDDING_MODEL= "sentence-transformers/all-MiniLM-L6-v2"
    LLM_THREADS    = 8
    LLM_CTX        = 4096