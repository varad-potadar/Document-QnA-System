from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import os

from services.pdf_extractor import extract_text_from_pdf
from services.chunker import chunk_text
from services.embedder import embed_chunks
from services.vector_store import VectorStore
from services.qa_engine import answer_question

app = FastAPI()

class Question(BaseModel):
    question: str

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# FAISS vector store (MiniLM = 384 dims)
vector_store = VectorStore(384)


def is_useful_chunk(text: str) -> bool:
    t = text.lower()

    if t.startswith("references"):
        return False
    if "terms and conditions" in t:
        return False
    if "creative commons" in t:
        return False
    if "doi.org" in t:
        return False
    if len(text.split()) < 30:
        return False

    return True


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # 1. Save PDF
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # 2. Extract clean linear text (PyMuPDF)
    text = extract_text_from_pdf(file_path)

    # 3. Chunk text
    chunks = chunk_text(text)

    # 4. Filter low-signal chunks
    chunks = [c for c in chunks if is_useful_chunk(c)]

    print("DEBUG: Stored chunks:", len(chunks))

    # 5. Embed
    embeddings = embed_chunks(chunks)

    # 6. Store in FAISS
    vector_store.add(embeddings, chunks)
    print("DEBUG: FAISS vectors:", vector_store.index.ntotal)

    return {
        "filename": file.filename,
        "num_chunks": len(chunks),
        "status": "Document indexed successfully"
    }


@app.post("/ask")
def ask_question(payload: Question):
    print("DEBUG: /ask endpoint hit")
    answer = answer_question(payload.question, vector_store)
    return {"answer": answer}
