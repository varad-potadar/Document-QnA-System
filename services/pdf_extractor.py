import fitz  # PyMuPDF
import re

def extract_text_from_pdf(path: str) -> str:
    doc = fitz.open(path)
    text = ""

    for page in doc:
        text += page.get_text("text") + "\n"

    # Light cleanup only
    text = re.sub(r"\n{2,}", "\n", text)
    text = re.sub(r"\s{2,}", " ", text)

    return text.strip()
