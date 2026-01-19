from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_chunks(chunks):
    embeddings = model.encode(chunks)
    return np.array(embeddings).astype("float32")
