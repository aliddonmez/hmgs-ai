# app/rag_pipeline.py
from pathlib import Path
import os

from dotenv import load_dotenv
load_dotenv()

from google import genai
from analysis.pgvector_similarity import retrieve


# =========================
# SABİT METİNLER
# =========================

IDK_TEXT = "Bu soruya, elimdeki kaynaklara dayanarak güvenilir bir cevap veremiyorum."


# =========================
# YAPISAL ÇIKTI HELPERS
# =========================

def make_no_answer(reason: str):
    return {
        "type": "no_answer",
        "text": IDK_TEXT,
        "reason": reason,
    }


def make_answer(text: str):
    return {
        "type": "answer",
        "text": text,
    }


# =========================
# SCOPE KONTROLÜ
# =========================

def is_out_of_scope(question: str) -> bool:
    """
    Dataset dışına taşan bariz konuları direkt sustur.
    (Bunu LLM'e bırakmıyoruz.)
    """
    q = question.lower()

    out_kw = [
        "ofsayt", "futbol",
        "kahve", "filtre kahve", "demleme",
        "kasten öldürme", "yağma",
    ]
    return any(k in q for k in out_kw)


# =========================
# PROMPT & CONTEXT
# =========================

def build_context(results):
    parts = []
    for title, content, score in results:
        parts.append(f"### {title}\n{content}")
    return "\n\n---\n\n".join(parts)


def load_prompt():
    prompt_path = Path(__file__).resolve().parents[1] / "docs" / "prompt_v1.md"
    return prompt_path.read_text(encoding="utf-8")


def fill_prompt(prompt_template: str, question: str, context: str) -> str:
    prompt = prompt_template.replace("{{question}}", question)
    prompt = prompt.replace("{{context}}", context)
    return prompt


# =========================
# CORE PIPELINE (UI + API İÇİN)
# =========================

def run(question: str, debug: bool = False) -> dict:
    question = question.strip()
    if not question:
        return make_no_answer("empty_question")

    # (A) Out-of-scope
    if is_out_of_scope(question):
        return make_no_answer("out_of_scope_keyword")

    # (B) Retrieval
    results = retrieve(
        question,
        top_k=5,
        fetch_k=20,
        min_score=0.60,
        use_topic_filter=True,
        debug=debug,
    )

    # (C) Context yoksa
    if not results:
        return make_no_answer("no_result_after_min_score")

    # (D) Prompt
    context = build_context(results)
    prompt_template = load_prompt()
    final_prompt = fill_prompt(prompt_template, question, context)

    # (E) LLM
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return make_no_answer("missing_api_key")

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=final_prompt
        )
        return make_answer(response.text)

    except Exception:
        return make_no_answer("llm_error")


# =========================
# CLI ENTRY (TEST AMAÇLI)
# =========================

def main():
    question = input("Lütfen sorunuzu girin: ")
    result = run(question)
    print(result)


if __name__ == "__main__":
    main()
