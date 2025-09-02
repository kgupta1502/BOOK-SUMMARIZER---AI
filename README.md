# BookBrief - AI (AI-Powered Book Summarizer)

BookBrief - AI is an **AI-powered book summarization tool** that uses large language models to generate concise and meaningful summaries of `.txt` or `.pdf` books.
It’s built with **Streamlit** for the frontend and leverages the **OpenRouter API (OpenAI models)** for summarization.

Future updates will include **chapter-wise summarization**, smarter chunking, and advanced features like **quote extraction** and **multilingual summaries**.

---

## ✨ Features

* 📂 Upload `.txt` or `.pdf` files
* 🔎 Preview original book content inside the app
* 🤖 AI-powered summarization using GPT-based models
* 📑 Handles long texts by splitting into sections (token-aware)
* 💾 Download summaries as `.txt` files
* 🔒 Built-in caching to avoid redundant API calls

---

## 🛠️ Tech Stack

* **Frontend**: [Streamlit](https://streamlit.io/)
* **Backend**: Python (requests, PyMuPDF, dotenv)
* **AI Models**: OpenRouter API (default: `openai/gpt-3.5-turbo`)
* **Utilities**: Token handling with `tiktoken`, caching with JSON

---

## 📂 Project Structure

```
├── app.py                  # Streamlit interface
├── summarize.py            # API call + parameters
├── utilities.py            # Token handling, splitting, caching
├── book.txt / sample.pdf   # Input book file
├── summaries_cache.json    # Cached summaries
├── summary_output.txt      # Final output summary
└── requirements.txt        # Python dependencies
```

---

## ⚙️ Setup & Installation

1. **Clone the repo**

   ```bash
   git clone https://github.com/your-username/bookbrief-ai.git
   cd bookbrief-ai
   ```

2. **Create a virtual environment & install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API key**
   Add your OpenRouter API key in `.streamlit/secrets.toml`:

   ```toml
   OPENROUTER_API_KEY = "your_api_key_here"
   MODEL_NAME = "openai/gpt-3.5-turbo"
   ```

4. **Run the Streamlit app**

   ```bash
   streamlit run app.py
   ```

---

## 🖥️ Usage

* Upload a `.txt` or `.pdf` file
* Preview original content
* Click **Summarize** → chunks are processed → summary generated
* Download summary as `.txt`

---

## 📌 Roadmap

* ✅ Text + PDF support
* ✅ Token-aware chunking
* ✅ Download option
* 🔜 Chapter-wise summarization
* 🔜 Highlight key quotes & entities
* 🔜 Multilingual summarization
* 🔜 Text-to-speech summary

---

## 🤝 Contributing

Contributions are welcome!
Fork the repo, create a new branch, and submit a pull request

Do you want me to also create a **badges section** (Python, Streamlit, OpenRouter, License) for a professional GitHub look?
