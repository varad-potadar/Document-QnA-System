import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Research Assistant",
    page_icon="📑",
    layout="centered"
)

# -------------------------------
# Minimal CSS (very important)
# -------------------------------
st.markdown("""
<style>
.main {
    max-width: 720px;
    padding-top: 2rem;
}

h1 {
    font-weight: 600;
    letter-spacing: -0.5px;
}

.stTextInput > div > div > input {
    font-size: 16px;
    padding: 0.75rem;
}

.stButton > button {
    padding: 0.6rem 1.2rem;
    font-size: 15px;
}

.answer-box {
    background-color: #f8f9fa;
    padding: 1.2rem;
    border-radius: 8px;
    line-height: 1.6;
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# App State
# -------------------------------
if "pdf_uploaded" not in st.session_state:
    st.session_state.pdf_uploaded = False

# -------------------------------
# Header
# -------------------------------
st.markdown("## Research Paper Assistant")
st.markdown(
    "<span style='color: #6c757d;'>Ask questions grounded strictly in the uploaded paper.</span>",
    unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)

# -------------------------------
# Upload Section
# -------------------------------
uploaded_file = st.file_uploader(
    "Upload a research paper (PDF)",
    type=["pdf"],
    label_visibility="collapsed"
)

if uploaded_file is not None and not st.session_state.pdf_uploaded:
    if st.button("Process paper"):
        with st.spinner("Reading and indexing document..."):
            files = {
                "file": (uploaded_file.name, uploaded_file, "application/pdf")
            }
            response = requests.post(f"{BACKEND_URL}/upload", files=files)

            if response.status_code == 200:
                st.session_state.pdf_uploaded = True
                st.success("Paper ready for querying.")
            else:
                st.error("Failed to process the paper.")
                st.code(response.text)

# -------------------------------
# Divider
# -------------------------------
if st.session_state.pdf_uploaded:
    st.markdown("<hr style='margin: 2rem 0;'>", unsafe_allow_html=True)

# -------------------------------
# Question Section
# -------------------------------
question = st.text_input(
    "Ask a question about the paper",
    disabled=not st.session_state.pdf_uploaded,
    placeholder="e.g. What methods are discussed for pose estimation?"
)

if st.session_state.pdf_uploaded and st.button("Get answer"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Analyzing content..."):
            response = requests.post(
                f"{BACKEND_URL}/ask",
                json={"question": question},
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                }
            )

            if response.status_code == 200:
                answer = response.json()["answer"]

                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("### Answer")
                st.markdown("### Answer")
                st.markdown(answer)

            else:
                st.error("Could not retrieve answer.")
                st.code(response.text)
