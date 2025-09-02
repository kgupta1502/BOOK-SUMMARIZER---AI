import streamlit as st
import fitz  # PyMuPDF for PDF reading

from summarize import call_openai_api, params
from utilities import summarization_prompt_messages, split_text_into_sections

st.set_page_config(page_title="Book Summarizer", layout="centered")

st.title("&#128218; BookBrief - AI (AI-Powered Book Summarizer)")
uploaded_file = st.file_uploader("Upload a `.txt` or `.pdf` file", type=["txt", "pdf"])

# ---------- Utility to read PDF or TXT ----------
def extract_text_from_file(uploaded_file):
    if uploaded_file.name.endswith(".txt"):
        return uploaded_file.read().decode("utf-8")
    elif uploaded_file.name.endswith(".pdf"):
        return extract_text_from_pdf(uploaded_file)
    else:
        return None

def extract_text_from_pdf(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# ---------- Main App ----------
if uploaded_file:
    text = extract_text_from_file(uploaded_file)

    st.subheader("Original Text Preview")
    st.text_area("Text", text[:-1], height=250, help="(Only first few thousand characters shown)")

    if st.button("Summarize"):
        chunks = split_text_into_sections(text, params.summary_input_size, "\n\n", "gpt-3.5-turbo")
        all_summaries = []

        with st.spinner("Summarizing..."):
            for i, chunk in enumerate(chunks):
                st.write(f"&#128270; Processing chunk {i + 1}/{len(chunks)}...")
                prompt = summarization_prompt_messages(chunk, params.target_summary_size)
                summary = call_openai_api(prompt)
                all_summaries.append(summary)

        final_summary = "\n\n".join(all_summaries)
        st.success("&#9989; Summary Completed")

        st.subheader("&#128218; Final Summary")
        st.text_area("Summary Output", final_summary, height=300)

        st.download_button(
            label="&#128190; Download Summary as TXT",
            data=final_summary,
            file_name="summary_output.txt",
            mime="text/plain"
        )
