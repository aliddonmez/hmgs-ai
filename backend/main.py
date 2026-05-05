import sys
import os

# Project root'u path'e ekle
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from dotenv import load_dotenv
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uuid

from backend.scenarios import router as scenario_router

app = FastAPI(title="HMGS API", version="1.0.0")

# React dev server'ına izin ver
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router'ları ekle
app.include_router(scenario_router)

# ─── In-memory quiz session store ───────────────────────────────────────────
quiz_sessions: dict = {}


# ─── Request / Response modelleri ───────────────────────────────────────────

class ChatRequest(BaseModel):
    question: str

class QuizStartRequest(BaseModel):
    user_id: str
    mode: str = "random"          # random | balanced | weak_focus
    n_questions: int = 20
    weak_topic: Optional[str] = None

class QuizAnswerRequest(BaseModel):
    session_id: str
    selected_index: int

class ProfileRequest(BaseModel):
    user_id: str
    display_name: str


# ─── CHAT ────────────────────────────────────────────────────────────────────

@app.post("/api/chat")
def chat(req: ChatRequest):
    from app.rag_pipeline import run
    result = run(req.question)
    return result


# ─── PROFILES ────────────────────────────────────────────────────────────────

@app.get("/api/profiles")
def profiles_list():
    from app.sqlstorage import list_profiles
    return {"profiles": list_profiles()}


@app.get("/api/profiles/{user_id}")
def profile_get(user_id: str):
    from app.sqlstorage import get_profile

    profile = get_profile(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profil bulunamadı.")
    return profile


@app.post("/api/profiles")
def profile_upsert(req: ProfileRequest):
    from app.sqlstorage import upsert_profile

    try:
        return upsert_profile(req.user_id, req.display_name)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


# ─── QUIZ ────────────────────────────────────────────────────────────────────

@app.post("/api/quiz/start")
def quiz_start(req: QuizStartRequest):
    from app.repositories.questions_repo import get_questions
    from app.question_select import select_questions
    from app.quiz_engine import start_quiz
    from app.sqlstorage import get_profile
    from analysis.user_report import get_user_report

    if not get_profile(req.user_id):
        raise HTTPException(status_code=404, detail="Quiz başlatmak için önce profil oluşturun.")

    questions = get_questions()
    if not questions:
        raise HTTPException(status_code=404, detail="Veritabanında soru bulunamadı.")

    weak_topic_names = []
    if req.mode == "weak_focus":
        report = get_user_report(req.user_id)
        weak_topic_names = [
            t.get("konu") for t in report.get("weak_topics", []) if t.get("konu")
        ]
        if req.weak_topic:
            weak_topic_names = [req.weak_topic] + weak_topic_names

    selected = select_questions(
        question_pool=questions,
        n_questions=req.n_questions,
        mode=req.mode,
        weak_topics=weak_topic_names,
    )

    if not selected:
        raise HTTPException(status_code=422, detail="Bu ayarlara göre soru seçilemedi.")

    state = start_quiz(selected)
    session_id = str(uuid.uuid4())
    quiz_sessions[session_id] = {"state": state, "user_id": req.user_id, "saved": False}

    first_q = selected[0]
    return {
        "session_id": session_id,
        "total": len(selected),
        "current_index": 0,
        "question": {
            "question_id": first_q.get("question_id"),
            "question": first_q.get("question"),
            "options": first_q.get("options"),
            "ders": first_q.get("ders"),
            "konu": first_q.get("konu"),
        },
    }


@app.post("/api/quiz/answer")
def quiz_answer(req: QuizAnswerRequest):
    from app.quiz_engine import submit_answer, is_finished, get_score, get_current_question, export_attempt_rows
    from app.sqlstorage import save_attempt_rows

    session = quiz_sessions.get(req.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Geçersiz session_id.")

    state = session["state"]
    result = submit_answer(state, req.selected_index)

    if is_finished(state):
        # Quiz bitti — kaydet
        if not session["saved"]:
            rows = export_attempt_rows(state, user_id=session["user_id"])
            save_attempt_rows(rows)
            session["saved"] = True

        score = get_score(state)
        return {
            "finished": True,
            "result": result,
            "score": score,
        }

    # Sonraki soruyu gönder
    next_q = get_current_question(state)
    return {
        "finished": False,
        "result": result,
        "current_index": state["current_index"],
        "question": {
            "question_id": next_q.get("question_id"),
            "question": next_q.get("question"),
            "options": next_q.get("options"),
            "ders": next_q.get("ders"),
            "konu": next_q.get("konu"),
        },
    }


@app.get("/api/quiz/session/{session_id}")
def quiz_session_status(session_id: str):
    from app.quiz_engine import get_current_question, get_score, is_finished

    session = quiz_sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session bulunamadı.")

    state = session["state"]
    if is_finished(state):
        return {"finished": True, "score": get_score(state)}

    q = get_current_question(state)
    return {
        "finished": False,
        "current_index": state["current_index"],
        "total": len(state["questions"]),
        "question": {
            "question_id": q.get("question_id"),
            "question": q.get("question"),
            "options": q.get("options"),
            "ders": q.get("ders"),
            "konu": q.get("konu"),
        },
    }


# ─── DASHBOARD ───────────────────────────────────────────────────────────────

@app.get("/api/dashboard/{user_id}")
def dashboard(user_id: str):
    from app.sqlstorage import get_profile
    from analysis.user_report import get_user_report

    if not get_profile(user_id):
        raise HTTPException(status_code=404, detail="Dashboard için önce profil oluşturun.")

    report = get_user_report(user_id)
    return report


# ─── HEALTH ──────────────────────────────────────────────────────────────────

@app.get("/api/health")
def health():
    return {"status": "ok"}
