
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from Rag_graph.configs.settings import settings

def load_project_documents(state, data_root="data"):
    """
    Node สำหรับโหลดไฟล์ .txt และ .md ในทุกโปรเจค
    คืนค่า state พร้อม docs และ vectorstore (Gemini embedding)
    """
    docs = {}
    # Walk the directory recursively to find .md and .txt files
    for root, _, files in os.walk(data_root):
        rel_dir = os.path.relpath(root, data_root)
        for fname in files:
            if fname.lower().endswith(".txt") or fname.lower().endswith(".md"):
                fpath = os.path.join(root, fname)
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        key = f"{rel_dir}/{fname}" if rel_dir not in (".", ".\\") else fname
                        # Normalize path separators to forward slash for consistency
                        key = key.replace('\\', '/')
                        docs[key] = f.read()
                except Exception:
                    # skip problematic files but continue scanning
                    continue
    # สร้าง embedding และ vector index ด้วย Gemini
    texts = list(docs.values())
    metadatas = [{"source": fname} for fname in docs.keys()]
    google_api_key = getattr(settings, "GOOGLE_API_KEY", None)
    # Check for Application Default Credentials path as an alternative
    adc_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not google_api_key and not adc_path:
        # No Google credentials available in this environment (e.g., tests).
        # Skip creating embeddings/vectorstore so tests don't require external auth.
        state["docs"] = docs
        state["vectorstore"] = None
        return state

    embeddings = GoogleGenerativeAIEmbeddings(
        google_api_key=google_api_key,
        model=getattr(settings, "EMBEDDING_MODEL_NAME", "models/embedding-001")
    )
    # Use Chroma vectorstore for embeddings
    vectorstore = Chroma.from_texts(texts, embeddings, metadatas=metadatas)
    state["docs"] = docs
    state["vectorstore"] = vectorstore
    return state

# ตัวอย่างการใช้งาน
if __name__ == "__main__":
    # Example: create an input state dict and call the node
    state = {}
    state = load_project_documents(state, data_root="data")
    docs = state.get("docs", {})
    for fname, content in docs.items():
        print(f"--- {fname} ---\n{content}\n")
