import os
import json
import requests
import fitz  # PyMuPDF for PDF reading
from dotenv import load_dotenv
from utilities import (
    summarization_prompt_messages,
    num_tokens_from_messages,
    split_text_into_sections,
    summarization_token_parameters,
    SummarizationParameters,
    memoize_to_file,
)

import streamlit as st

api_key = st.secrets["OPENROUTER_API_KEY"]
model_name = st.secrets.get("MODEL_NAME", "openai/gpt-3.5-turbo")


book_path = "book.txt"  # Can be .txt or .pdf
context_size = 16000
size = 1000

params = summarization_token_parameters(
    target_summary_size=size,
    model_context_size=context_size
)

@memoize_to_file("summaries_cache.json")
def call_openai_api(prompt_messages):
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "HTTP-Referer": "https://localhost",  # or your actual site
            "X-Title": "Book Summarizer",
            "Content-Type": "application/json",
        },
        json={
            "model": model_name,
            "messages": prompt_messages,
            "temperature": 0.7,
        },
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

def extract_text_from_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    elif ext == ".pdf":
        return extract_text_from_pdf(file_path)
    else:
        raise ValueError("Unsupported file format. Use .txt or .pdf")

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

def main():
    book_text = extract_text_from_file(book_path)

    chunks = split_text_into_sections(book_text, params.summary_input_size, "\n\n", model_name)
    all_summaries = []

    for i, chunk in enumerate(chunks):
        print(f" Summarizing chunk {i+1}/{len(chunks)}...")
        prompt = summarization_prompt_messages(chunk, params.target_summary_size)
        summary = call_openai_api(prompt)
        all_summaries.append(summary)

    with open("summary_output.txt", "w", encoding="utf-8") as f:
        for i, summary in enumerate(all_summaries):
            f.write(f"[[[ {summary} ]]]\n\n")

    print(" Summary written to summary_output.txt")

if __name__ == "__main__":
    main()
