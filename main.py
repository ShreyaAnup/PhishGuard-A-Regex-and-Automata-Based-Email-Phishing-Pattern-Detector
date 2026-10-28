from pathlib import Path
import sys
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from detector import analyze_input
from automata import trace_contains_digit

app = FastAPI(title="PhishGuard API", version="1.0.0")
app.mount("/static", StaticFiles(directory=ROOT / "frontend"), name="static")

class AnalyzeRequest(BaseModel):
    text: str = Field(min_length=1, max_length=10000)
    mode: str = "message"

@app.get("/")
def home():
    return FileResponse(ROOT / "frontend" / "index.html")

@app.post("/api/analyze")
def analyze(payload: AnalyzeRequest):
    return analyze_input(payload.text, payload.mode)

@app.post("/api/automata/trace")
def automata_trace(payload: AnalyzeRequest):
    return trace_contains_digit(payload.text)

@app.get("/api/health")
def health():
    return {"status": "ok", "app": "PhishGuard"}
