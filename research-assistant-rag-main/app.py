# app.py (Corrected)
import os
import time
import psutil
import gradio as gr

from config import Config
from processing import load_or_create_index
from qa import get_qa_chain

# Initialize index & QA chain
vector_store = load_or_create_index()
qa_chain     = get_qa_chain(vector_store)

def respond(message: str, history: list):
    """
    Gradio ChatInterface function.

    Args:
        message: The new message from the user.
        history: The past conversation history (managed by Gradio).

    Returns:
        A string with the assistant's new response.
    """
    # 1. Run the QA chain on the new message. The history is not needed for this simple RAG.
    start = time.time()
    result = qa_chain({"query": message})
    elapsed = time.time() - start

    # 2. Format the answer with sources and performance stats
    answer = result.get("result", "❗️ No answer generated.")
    sources = result.get("source_documents", [])
    
    if sources:
        # Create a unique, sorted list of sources to avoid duplicates
        unique_sources = sorted(list(set(
            f"- {os.path.basename(d.metadata.get('source', ''))} (p.{d.metadata.get('page', '?')})"
            for d in sources
        )))
        answer += "\n\n**Sources:**\n" + "\n".join(unique_sources)

    mem_mb = psutil.Process(os.getpid()).memory_info().rss / 1e6
    answer += f"\n\n_Time: {elapsed:.2f}s · Mem: {mem_mb:.1f} MB_"

    # 3. Return ONLY the new, formatted answer string
    return answer

if __name__ == "__main__":
    demo = gr.ChatInterface(
        fn=respond,
        # The 'type' parameter is deprecated and should be removed.
        examples=[["What is attention mechanism?"], ["Explain fine-tuning."]],
        title="🔬 Research Assistant",
        description="Ask questions about your PDF docs.",
        theme="soft",
        cache_examples=False # Recommended to set for dynamic backends
    )
    demo.launch()