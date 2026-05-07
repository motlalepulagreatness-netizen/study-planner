from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from StudyPlanner.core.models_services import Student
from StudyPlanner.core.service_provider import CourseManagement

app = FastAPI()
FILE_PATH = "StudyPlanner/data/student.json"

app.mount("/static", StaticFiles(directory="StudyPlanner/frontend"), name="static")

@app.get("/")
def serve_frontend():
    return FileResponse("StudyPlanner/frontend/index.html")

# Allow your frontend to talk to this backend
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

student = Student(FILE_PATH)
manager = CourseManagement(student)

# --- Input models (replaces your stdio inputs) ---
class CourseIn(BaseModel):
    name: str
    weekly_hours: int
    difficulty_level: int

class SessionIn(BaseModel):
    course: str
    duration: float
    focus_level: int

# --- Routes ---
@app.get("/courses")
def get_courses():
    return student._courses

@app.post("/courses")
def add_course(data: CourseIn):
    student.add_course(data.name, data.weekly_hours, data.difficulty_level)
    student._save()
    return {"message": f"{data.name} added"}

@app.put("/courses/{name}")
def modify_course(name: str, data: CourseIn):
    student.modify_course(name, data.weekly_hours, data.difficulty_level)
    student._save()
    return {"message": f"{name} updated"}

@app.delete("/courses/{name}")
def delete_course(name: str):
    student.delete_course(name)
    student._save()
    return {"message": f"{name} deleted"}

@app.post("/sessions")
def add_session(data: SessionIn):
    from datetime import date
    student.add_sessions(data.course, str(date.today()), data.duration, data.focus_level)
    student._save()
    return {"message": "Session logged"}

@app.get("/summary")
def get_summary():
    manager.summaryCourse()
    return student._summary