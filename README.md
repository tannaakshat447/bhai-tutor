# 🎒 Bhai Tutor — Your Desi AI Study Buddy

> *Doubt puch, bhai samjhayega — textbook accuracy ke saath, lekin apne andaaz mein.*

An AI-powered tutoring web app for Indian students (Classes 6–12) that answers NCERT doubts through a **3-step pipeline**: refine the question → fetch curriculum-accurate knowledge → deliver it in Hinglish like a cool older sibling.

---

## ✨ What It Does

| Step | Role | What happens |
|------|------|--------------|
| 1️⃣ | **Prompt Refiner** | Rewrites the student's vague doubt into a precise, well-formed question |
| 2️⃣ | **NCERT Knowledge Engine** | Answers the refined question strictly based on the NCERT curriculum |
| 3️⃣ | **Bhai Mode** | Rewrites the textbook answer in casual Hinglish — like a desi big bro explaining it |

---

## 🛠️ Tech Stack

- **Backend** — Python, Flask
- **AI** — OpenAI API (`gpt-4o-mini`) for all three pipeline stages
- **Frontend** — Vanilla HTML/CSS/JS with Server-Sent Events (SSE) for real-time step updates
- **Streaming** — `stream_with_context` + `EventSource`-style SSE for live pipeline progress

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/your-username/bhai-tutor.git
cd bhai-tutor
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add your OpenAI API key

Open `app.py` and replace the placeholder:

```python
client = OpenAI(api_key="YOUR_API_KEY_HERE")
```

> **Tip:** Use an environment variable instead of hardcoding it:
> ```python
> import os
> client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
> ```
> Then run: `export OPENAI_API_KEY=sk-...`

### 4. Set up the templates folder

Flask expects HTML files inside a `templates/` directory:

```
project/
├── app.py
├── requirements.txt
└── templates/
    └── index.html   ← move index.html here
```

### 5. Run the app

```bash
python app.py
```

Open your browser at **http://localhost:5000**

---

## 📁 Project Structure

```
bhai-tutor/
├── app.py              # Flask backend + 3-step AI pipeline
├── requirements.txt    # Python dependencies
└── templates/
    └── index.html      # Frontend UI
```

---

## 🌐 Deployment (Render)

1. Push your code to GitHub
2. Create a new **Web Service** on [Render](https://render.com)
3. Set the **Start Command** to: `python app.py`
4. Add `OPENAI_API_KEY` as an **Environment Variable** in Render's dashboard
5. Deploy 🚀

---

## 🔮 Planned Features

- [ ] **RAG Pipeline** — Step 2 answers drawn strictly from uploaded NCERT PDFs (via LangChain + vector DB) instead of general model knowledge
- [ ] **Multi-LLM support** — Swap OpenAI for Gemini (Step 2) and Grok (Step 3) once API keys are live
- [ ] **Supabase + pgvector** — Store and query NCERT embeddings using Google `text-embedding-004`
- [ ] **Streamlit demo UI** — Investor-facing prototype

---

## 📦 Dependencies

```
flask>=3.0.0
openai>=1.30.0
```

---

## 🙌 Built With Love

Made for desi students who learn better from a bhai than a textbook.  
*NCERT accuracy. Zero cringe. Full padhaku energy.*
