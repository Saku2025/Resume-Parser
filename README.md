# Resume-Parser

An AI-powered resume screener. Upload a stack of resumes (PDF or DOCX), paste a job description, and get every candidate parsed, scored and ranked against the role.

Built with **FastAPI**, **Pydantic** and LLMs on **Groq**.

## Features

- **Job description analysis**: extracts the role, required and preferred skills, minimum experience, education and responsibilities
- **Resume parsing**: pulls out name, contact details, skills, experience (including internships), education, projects and certifications, whatever the section headings are called
- **Candidate scoring**: a 0–100 match score with matching skills, missing skills, an experience check and a short verdict
- **Ranking**: candidates are sorted by score, and the top and lowest picks are highlighted
- **Web UI**: drag-and-drop uploads, live progress for each file, works on phones and in dark mode
- **CLI**: batch-process a folder of resumes from the terminal

## How it works

```
Job description ──► LLM ──► structured requirements (JobD)
                                     │
Resume PDF/DOCX ──► text ──► LLM ──► structured resume (Resume)
                                     │
                                     ▼
                        LLM compares both ──► MatchResult (score, skills, verdict)
```

Every LLM response is requested in JSON mode and validated with Pydantic models.

## Project structure

```
├── app.py              # FastAPI backend (serves the UI + API)
├── resume_parser.py    # Parsing, scoring and the CLI
├── static/index.html   # Web frontend
├── resumes/            # Put resumes here for CLI mode (git-ignored)
└── pyproject.toml
```

## Setup

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/Saku2025/Resume-Parser.git
cd Resume-Parser
uv sync
```

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_key_here
# optional, defaults to openai/gpt-oss-120b
GROQ_MODEL=openai/gpt-oss-120b
```

Get a free API key at [console.groq.com](https://console.groq.com).

## Usage

### Web app

```bash
uv run python app.py
```

Open **http://127.0.0.1:8000** and then:

1. Paste a job description (a sample Amazon SDE-I description is filled in for you)
2. Drag and drop one or more resumes
3. Click **Analyze candidates**

### Command line

Put resumes in the `resumes/` folder and run:

```bash
uv run python resume_parser.py
```

It prints each candidate's score, followed by the top and lowest candidates.

## API

| Method | Endpoint           | Description                                                        |
|--------|--------------------|--------------------------------------------------------------------|
| GET    | `/api/default-job` | The sample job description                                         |
| POST   | `/api/job`         | `{"description": "..."}` → structured job requirements             |
| POST   | `/api/analyze`     | multipart `file` + `job` (JSON from `/api/job`) → parsed resume + match result |

Interactive docs are at `/docs` while the server is running.

## Notes

- Scanned or image-only PDFs have no extractable text and are skipped.
- Scores are AI estimates. Review the candidates yourself before making decisions.
