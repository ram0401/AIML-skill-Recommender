from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import json
import os
from typing import List, Dict, Optional
import PyPDF2
import io
from pydantic import BaseModel
import spacy
import re
from skill_extractor import SkillExtractor
from skill_matcher import SkillMatcher
from roadmap_generator import RoadmapGenerator

app = FastAPI(title="Skill Recommender API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
if os.path.exists("frontend"):
    app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Initialize components
skill_extractor = SkillExtractor()
skill_matcher = SkillMatcher()
roadmap_generator = RoadmapGenerator()

class SkillRecommendation(BaseModel):
    skill: str
    level: str
    description: str
    resources: List[Dict[str, str]]

class SkillMatchResponse(BaseModel):
    matched_skills: List[str]
    missing_skills: List[str]
    skill_gaps: List[Dict[str, str]]
    overall_match_percentage: float

@app.get("/", response_class=HTMLResponse)
async def root():
    """
    Serve the frontend application
    """
    try:
        with open("frontend/index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Skill Recommender API</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .container { max-width: 800px; margin: 0 auto; }
                .api-link { color: #667eea; text-decoration: none; }
                .api-link:hover { text-decoration: underline; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Skill Recommender API</h1>
                <p>The API is running successfully!</p>
                <ul>
                    <li><a href="/docs" class="api-link">API Documentation</a></li>
                    <li><a href="/health" class="api-link">Health Check</a></li>
                </ul>
                <p>To use the frontend, make sure the frontend files are in the <code>frontend/</code> directory.</p>
            </div>
        </body>
        </html>
        """)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    """
    Upload and extract skills from resume (PDF or text)
    """
    try:
        # Check file type
        if not file.filename.lower().endswith(('.pdf', '.txt', '.docx')):
            raise HTTPException(status_code=400, detail="Only PDF, TXT, and DOCX files are supported")
        
        # Read file content
        content = await file.read()
        
        # Extract text based on file type
        if file.filename.lower().endswith('.pdf'):
            text = extract_text_from_pdf(content)
        elif file.filename.lower().endswith('.txt'):
            text = content.decode('utf-8')
        else:  # docx
            text = extract_text_from_docx(content)
        
        # Extract skills from text
        skills = skill_extractor.extract_skills(text)
        
        return {
            "filename": file.filename,
            "extracted_skills": skills,
            "text_length": len(text)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@app.get("/job-roles")
async def get_job_roles():
    """
    Get available job roles
    """
    return skill_matcher.get_available_job_roles()

@app.post("/match-skills")
async def match_skills(
    user_skills: List[str] = Form(...),
    target_role: str = Form(...)
):
    """
    Match user skills against target job role requirements
    """
    try:
        match_result = skill_matcher.match_skills(user_skills, target_role)
        return match_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error matching skills: {str(e)}")

@app.post("/generate-roadmap")
async def generate_roadmap(skill: str = Form(...)):
    """
    Generate learning roadmap for a specific skill
    """
    try:
        roadmap = roadmap_generator.generate_roadmap(skill)
        return roadmap
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating roadmap: {str(e)}")

def extract_text_from_pdf(content: bytes) -> str:
    """Extract text from PDF content"""
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading PDF: {str(e)}")

def extract_text_from_docx(content: bytes) -> str:
    """Extract text from DOCX content"""
    try:
        from docx import Document
        doc = Document(io.BytesIO(content))
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading DOCX: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

