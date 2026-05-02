# app/rag_pipeline.py

import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from pathlib import Path
from dotenv import load_dotenv

from retrieval.pipeline import retrieve_chunks
from app.llm.gemini_client import ask_gemini
from retrieval.config import (
    AMBIGUITY_MARGIN,
    DEBUG_RAG,
    MIN_TOP_SCORE,
    MIN_SECOND_SCORE,
    MIN_AVG_TOP3_SCORE,
)

IDK_TEXT = (
    "⚠️ Bu soruya, mevcut hukuki kaynaklar içinde doğrudan ve güvenli "
    "bir yanıt bulamadım. Varsayıma dayalı bir cevap üretmemek için burada duruyorum.\n\n"
    "🔎 Soruyu biraz daraltarak ya da ilgili kanun maddesini belirterek yeniden sorabilirsin."
)


def make_no_answer(reason: str):
    return {"type": "no_answer", "text": IDK_TEXT, "reason": reason}


def quick_answer_from_context(results):
    if not results:
        return None

    top = results[:2]
    parts = []

    for r in top:
        c = (r.get("content") or "").strip()
        if c:
            parts.append(c)

    if not parts:
        return None

    return "(LLM devre dışı) Kaynaktan bulunan bilgi:\n\n" + "\n\n".join(parts)


def is_out_of_scope(question: str):
    q = question.lower()
    out_kw = ["ofsayt", "futbol", "kahve", "demleme", "python", "list"]
    return any(k in q for k in out_kw)


def build_context(results):
    parts = []

    for r in results:
        parts.append(f"[{r.get('doc_id')} | {r.get('title')}]\n{r.get('content')}")

    return "\n\n---\n\n".join(parts)


def load_prompt():
    path = Path(__file__).resolve().parents[1] / "docs" / "prompt_v1.md"
    return path.read_text(encoding="utf-8")


def fill_prompt(prompt: str, question: str, context: str):
    return prompt.replace("{{question}}", question).replace("{{context}}", context)


def run(question: str, debug: bool = False) -> dict:
    question = question.strip()

    if not question:
        return make_no_answer("empty_question")

    # (A) Scope kontrolü
    if is_out_of_scope(question):
        return make_no_answer("out_of_scope")

    # (B) Retrieval
    results = retrieve_chunks(question)

    if not results:
        return make_no_answer("no_result")

    sorted_results = sorted(
        results,
        key=lambda x: float(x.get("final_score", 0.0)),
        reverse=True,
    )

    # Debug
    if DEBUG_RAG or debug:
        print("\n--- RETRIEVAL DEBUG ---")

        for i, r in enumerate(sorted_results):
            print(f"\n[{i+1}] FINAL_SCORE: {round(float(r.get('final_score', 0.0)), 4)}")
            print("VECTOR_SCORE:", round(float(r.get("vector_score", 0.0)), 4))
            print("TITLE:", r.get("title"))
            print("CONTENT:", (r.get("content") or "")[:300])

    # (C) Retrieval kalite kontrolü
    scores = [float(r.get("final_score", 0.0)) for r in sorted_results]

    top_score = scores[0] if len(scores) >= 1 else 0.0
    second_score = scores[1] if len(scores) >= 2 else 0.0
    avg_top3 = sum(scores[:3]) / min(len(scores), 3) if scores else 0.0

    if DEBUG_RAG or debug:
        print("\n=== RETRIEVAL QUALITY DEBUG ===")
        print("top_score:", round(top_score, 4))
        print("second_score:", round(second_score, 4))
        print("avg_top3:", round(avg_top3, 4))
        print("ambiguity_gap:", round(abs(top_score - second_score), 4))

    # 1) Top sonuç çok zayıfsa dur
    if top_score < MIN_TOP_SCORE:
        return make_no_answer("weak_top_result")

    # 2) İlk birkaç sonuç genel olarak zayıfsa dur
    if avg_top3 < MIN_AVG_TOP3_SCORE:
        return make_no_answer("weak_retrieval")

    # 3) İlk iki sonuç birbirine çok yakınsa ve ikinci sonuç da güçlü ise kararsız say
    if len(scores) >= 2:
        if abs(top_score - second_score) < AMBIGUITY_MARGIN and second_score >= MIN_SECOND_SCORE:
            return make_no_answer("ambiguous_retrieval")

    # (D) Context oluştur
    context = build_context(sorted_results)

    prompt_template = load_prompt()
    final_prompt = fill_prompt(prompt_template, question, context)

    if DEBUG_RAG or debug:
        print("\n=== CONTEXT DEBUG ===")
        print(context)
        print("=====================\n")

    # (E) LLM çağrısı
    try:
        answer = ask_gemini(final_prompt)

        if not answer or len(answer.strip()) < 10:
            raise ValueError("Empty LLM response")

        return {
            "type": "answer",
            "text": answer,
            "sources": sorted_results[:3],
        }

    except Exception as e:
        print("LLM ERROR:", e)

        fallback = quick_answer_from_context(sorted_results)

        if fallback:
            return {
                "type": "answer",
                "text": fallback,
                "sources": sorted_results[:3],
            }

        return make_no_answer("llm_failed")


def main():
    q = input("Soru: ")
    print(run(q, debug=True))


if __name__ == "__main__":
    main()