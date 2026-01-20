import streamlit as st
import os
import tempfile

from services.pdf_extractor import extract_text_from_pdf
from services.chunker import chunk_text
from services.embedder import embed_chunks
from services.vector_store import VectorStore
from services.qa_engine import answer_question

# -------------------------------
# App Config
# -------------------------------
st.set_page_config(
    page_title="DocQuery",
    page_icon="🧬",
    layout="centered"
)

# -------------------------------
# State
# -------------------------------
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

# -------------------------------
# UI
# -------------------------------
st.title("📑 DocQuery - Ask Anything")
st.caption("Ask questions grounded strictly in the uploaded research paper.")

uploaded_file = st.file_uploader(
    "Upload a research paper (PDF)",
    type=["pdf"]
)

# -------------------------------
# PDF Processing
# -------------------------------
if uploaded_file is not None and st.session_state.vector_store is None:
    if st.button("Process paper"):
        with st.spinner("Reading and indexing document..."):
            # Save PDF temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.read())
                pdf_path = tmp.name

            # Extract text
            text = extract_text_from_pdf(pdf_path)

            # Chunk
            chunks = chunk_text(text)

            # Embed
            embeddings = embed_chunks(chunks)

            # Store
            vector_store = VectorStore(embeddings.shape[1])
            vector_store.add(embeddings, chunks)

            st.session_state.vector_store = vector_store

            st.success("Paper indexed successfully.")

# -------------------------------
# Question Section
# -------------------------------
if st.session_state.vector_store is not None:
    question = st.text_input(
        "Ask a question about the paper",
        placeholder="e.g. What methods are discussed?"
    )

    if st.button("Get answer"):
        with st.spinner("Analyzing paper..."):
            answer = answer_question(
                question,
                st.session_state.vector_store
            )

            st.markdown("### Answer")
            st.markdown(answer)





