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

IDK_TEXT = (
    "⚠️ Bu soruya, mevcut hukuki kaynaklar içinde doğrudan ve güvenli "
    "bir yanıt bulamadım. Varsayıma dayalı bir cevap üretmemek için burada duruyorum.\n\n"
    "🔎 Soruyu biraz daraltarak ya da ilgili kanun maddesini belirterek yeniden sorabilirsin."
)


def make_no_answer(reason: str):
    return {
        "type": "no_answer",
        "text": IDK_TEXT,
        "reason": reason,
    }


def make_answer(text: str, source_count: int = 0):
    return {
        "type": "answer",
        "text": text,
        "meta": {
            "source_count": source_count,
        },
    }


# =========================
# SCOPE KONTROLÜ
# =========================


def is_out_of_scope(question: str) -> bool:
    """
    Dataset dışına taşan bariz konular için erken susma.
    """
    q = question.lower()
    out_kw = [
        "ofsayt",
        "futbol",
        "kahve",
        "demleme",
        "python",
        "list",
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
    path = Path(__file__).resolve().parents[1] / "docs" / "prompt_v1.md"
    return path.read_text(encoding="utf-8")


def fill_prompt(prompt: str, question: str, context: str) -> str:
    return prompt.replace("{{question}}", question).replace("{{context}}", context)


# =========================
# CORE PIPELINE
# =========================


def run(question: str, debug: bool = True) -> dict:
    question = question.strip()
    if not question:
        return make_no_answer("empty_question")

    # (A) Scope kontrolü
    if is_out_of_scope(question):
        return make_no_answer("out_of_scope")

    # (B) Retrieval
    results = retrieve(
        question,
        top_k=5,
        fetch_k=20,
        min_score=0.60,
        use_topic_filter=True,
        debug=debug,
    )

    # ---------- DEBUG ----------
    if debug:
        print("\n--- RETRIEVAL DEBUG ---")
        for i, r in enumerate(results):
            title, content, score = r
            print(f"\n[{i+1}] SCORE: {round(score,4)}")
            print(f"TITLE: {title}")
            print("CONTENT:")
            print(content[:400])
    # ----------------------------

    # (C0) Hiç sonuç yoksa
    if not results:
        return make_no_answer("no_result")

    # (C1) Skor dağılımı kontrolü (15.2 / 15.3)
    top_scores = [r[2] for r in results]
    if len(top_scores) >= 2:
        gap = abs(top_scores[0] - top_scores[1])
        if gap < 0.005:
            return make_no_answer("ambiguous_retrieval")

    # (D) Tanım var mı kontrolü (15.4)
    # Not: Burada sadece keyword listesini genişlettik.
    definition_keywords = [
        "tanımı",
        "şudur",
        "olarak tanımlanır",
        "ifade eder",
        "alınmasıdır",
        "oluşur",
        "unsurları",
    ]

    has_definition = any(
        any(k in content.lower() for k in definition_keywords)
        for _, content, _ in results
    )

    if not has_definition:
        return make_no_answer("no_clear_definition")

    # (E) Prompt + LLM
    prompt_template = load_prompt()
    context = build_context(results)
    final_prompt = fill_prompt(prompt_template, question, context)

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return make_no_answer("missing_api_key")

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=final_prompt,
        )
        return make_answer(response.text, source_count=len(results))

    except Exception:
        return make_no_answer("llm_error")


# =========================
# CLI TEST
# =========================


def main():
    q = input("Soru: ")
    print(run(q))


if __name__ == "__main__":
    main()
