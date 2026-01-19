import re

def chunk_text(text, chunk_size=500, overlap=100):
    sentences = re.split(r'(?<=[.!?])\s+', text)

    chunks = []
    current = ""

    for sent in sentences:
        if len(current) + len(sent) <= chunk_size:
            current += " " + sent
        else:
            chunks.append(current.strip())
            current = current[-overlap:] + " " + sent

    if current.strip():
        chunks.append(current.strip())

    return chunks
