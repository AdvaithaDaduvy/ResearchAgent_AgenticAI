# app.py

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import os, time
from fastapi import UploadFile, File, Form
from fastapi.responses import StreamingResponse
from anothercrew import run_research_bot_with_progress 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with frontend origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/analyze/")
async def analyze_pdfs_stream(question: str = Form(...), files: list[UploadFile] = File(...)):
    # Save uploaded files first before starting generator
    pdf_paths = []

    for file in files:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            content = await file.read()  # Read content while file is open
            f.write(content)
        pdf_paths.append(file_path)

    def generate():
        for update in run_research_bot_with_progress(pdf_paths, question):
            yield f"data: {update}\n\n" 
            time.sleep(0.1)

    return StreamingResponse(generate(), media_type="text/event-stream")