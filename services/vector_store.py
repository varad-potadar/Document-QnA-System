import faiss

class VectorStore:
    def __init__(self, dim):
        self.index = faiss.IndexFlatL2(dim)
        self.texts = []

    def add(self, embeddings, texts):
        self.index.add(embeddings)
        self.texts.extend(texts)

    def search(self, query_embedding, k=5):
        distances, indices = self.index.search(query_embedding, k)
        return [self.texts[i] for i in indices[0]]

    def debug_count(self):
        return self.index.ntotal