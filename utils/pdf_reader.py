"""
PDF Text Extraction

This file only does one job: take an uploaded PDF and return clean text.
Keeping this separate from app.py so the extraction logic can be explained
and tested on its own.
"""

import re
from pypdf import PdfReader


def extract_text_from_pdf(uploaded_file):
    """
    Reads a PDF (resume or job description) and returns raw extracted text.

    uploaded_file: a file-like object from Streamlit's file_uploader
    """
    reader = PdfReader(uploaded_file)

    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text


def clean_text(text):
    """
    Basic text cleaning before sending to the LLM.

    - removes extra blank lines
    - removes extra spaces
    - strips leading/trailing whitespace
    """
    text = re.sub(r"\n+", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = text.strip()
    return text


def read_and_clean_pdf(uploaded_file):
    """
    Combined helper: extract + clean in one call.
    This is the function app.py will actually use.
    """
    raw_text = extract_text_from_pdf(uploaded_file)
    return clean_text(raw_text)
