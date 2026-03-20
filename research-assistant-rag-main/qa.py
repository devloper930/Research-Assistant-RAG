# qa.py
from functools import lru_cache
from langchain.chains import RetrievalQA
from langchain.llms import LlamaCpp
from langchain.prompts import PromptTemplate

from config import Config

PROMPT = PromptTemplate(
    template="""
You are a research assistant. Answer concisely based on context.

Context:
{context}

Question:
{question}

Answer:
""",
    input_variables=["context", "question"]
)

@lru_cache(maxsize=1)
def _load_llm():
    return LlamaCpp(
        model_path=Config.MODEL_PATH,
        n_threads=Config.LLM_THREADS,
        #n_ctx=Config.LLM_CTX,
        temperature=0.2,        # Ensure factual consistency
        max_tokens=1024,         # Enough for concise responses
        n_ctx=2048,             # Defines context + response limit
                   # Optimize for CPU performance
        n_batch=1024,            # Improve inference speed
        top_k=40,               # Keeps answers relevant
        top_p=0.9,              # Allows controlled diversity
        use_mlock=True,         # Prevent swapping out of memory
        verbose=False,
        stop=["\n##", "Sources:"],
        model_kwargs={"n_gqa":8, "offload_kqv":True}
    )



@lru_cache(maxsize=1)
def get_qa_chain(vector_store):
    llm       = _load_llm()
    retriever = vector_store.as_retriever(search_kwargs={"k":3})
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
        chain_type="stuff",
        chain_type_kwargs={"prompt": PROMPT}
    )
