# Resume-Parser

Parses resumes (PDF/DOCX) with an LLM on Groq and scores them against a job description.

## Setup

Create a `.env` file with your key:

```
GROQ_API_KEY=your_key_here
# optional, defaults to openai/gpt-oss-120b
GROQ_MODEL=openai/gpt-oss-120b
```

## Web app

```
uv run python app.py
```

Open http://127.0.0.1:8000, paste a job description, drop in resumes and click **Analyze candidates**.

## Command line

Put resumes in `resumes/` and run:

```
uv run python resume_parser.py
```
