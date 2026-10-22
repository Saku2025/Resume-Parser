import io
from pathlib import Path
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel, ValidationError

from resume_parser import JobD, final_score, job_description, parse_job, parse_resume, read_resume

app = FastAPI(title="Resume Matcher")
static_dir = Path(__file__).parent / "static"


class JobRequest(BaseModel):
    description: str


@app.get("/")
def index():
    return FileResponse(static_dir / "index.html")


@app.get("/api/default-job")
def default_job():
    return {"description": job_description.strip()}


# endpoints are plain `def` so FastAPI runs the blocking groq calls in a thread pool
@app.post("/api/job")
def analyze_job(request: JobRequest):
    if not request.description.strip():
        raise HTTPException(400, "Job description is empty")
    try:
        return parse_job(request.description)
    except Exception as error:
        raise HTTPException(502, f"Could not analyze job description: {error}")


@app.post("/api/analyze")
def analyze_resume(file: UploadFile = File(...), job: str = Form(...)):
    try:
        job_data = JobD.model_validate_json(job)
    except ValidationError:
        raise HTTPException(400, "Invalid job data")

    try:
        resume_text = read_resume(io.BytesIO(file.file.read()), file.filename)
    except ValueError as error:
        raise HTTPException(400, str(error))
    except Exception:
        raise HTTPException(400, "Could not read this file")

    try:
        resume = parse_resume(resume_text)
        match = final_score(job_data, resume)
    except Exception as error:
        raise HTTPException(502, f"AI analysis failed: {error}")

    return {"filename": file.filename, "resume": resume, "match": match}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
