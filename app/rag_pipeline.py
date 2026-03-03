# app/rag_pipeline.py
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

from app.repositories.retrieval_repo import search_chunks

IDK_TEXT = (
    "⚠️ Bu soruya, mevcut hukuki kaynaklar içinde doğrudan ve güvenli "
    "bir yanıt bulamadım. Varsayıma dayalı bir cevap üretmemek için burada duruyorum.\n\n"
    "🔎 Soruyu biraz daraltarak ya da ilgili kanun maddesini belirterek yeniden sorabilirsin."
)


def make_no_answer(reason: str):
    return {"type": "no_answer", "text": IDK_TEXT, "reason": reason}


def quick_answer_from_context(question: str, results):
    """
    LLM yokken / hata verince: en iyi chunk(lar)dan kısa, güvenli cevap üret.
    Bu fonksiyon HALÜSİNASYON yapmaz: sadece kaynak metni döndürür.
    """
    if not results:
        return None

    # En iyi 1-2 kaynağı birleştir
    top = results[:2]
    parts = []
    for r in top:
        c = (r.get("content") or "").strip()
        if c:
            parts.append(c)

    if not parts:
        return None

    return "(LLM devre dışı) Kaynaktan bulunan bilgi:\n\n" + "\n\n".join(parts)


def is_out_of_scope(question: str) -> bool:
    """
    Basit kapsam dışı kontrolü.
    (Bu listeyi büyütmek istersen sonra konuşuruz.)
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


def build_context(results):
    parts = []
    for r in results:
        parts.append(
            f"[{r.get('document_id')} | {r.get('title')} | score={float(r.get('score',0.0)):.3f}]\n{r.get('content')}"
        )
    return "\n\n---\n\n".join(parts)


def load_prompt():
    path = Path(__file__).resolve().parents[1] / "docs" / "prompt_v1.md"
    return path.read_text(encoding="utf-8")


def fill_prompt(prompt: str, question: str, context: str) -> str:
    return prompt.replace("{{question}}", question).replace("{{context}}", context)


def run(question: str, debug: bool = True) -> dict:
    question = question.strip()
    if not question:
        return make_no_answer("empty_question")

    # (A) Scope
    if is_out_of_scope(question):
        return make_no_answer("out_of_scope")

    # (B) Retrieval
    results = search_chunks(question, top_k=5)

    # (B1) Anayasa sorusu geldiyse ama anayasa kaynağın yoksa cevap verme
    q_lower = question.lower()
    if "anayasa" in q_lower or "anayasası" in q_lower or "2709" in q_lower:
        has_constitution_source = any(
            ("anayasa" in (r.get("title") or "").lower())
            or ("mevzuatno=2709" in (r.get("content") or "").lower())
            or ("2709" in (r.get("content") or "").lower())
            for r in results
        )
        if not has_constitution_source:
            return make_no_answer("out_of_scope")

    if not results:
        return make_no_answer("no_result")

    # Debug
    if debug:
        print("\n--- RETRIEVAL DEBUG ---")
        for i, r in enumerate(results):
            title = r.get("title")
            content = (r.get("content") or "")
            score = float(r.get("score", 0.0))
            print(f"\n[{i+1}] SCORE: {round(score,4)}")
            print(f"TITLE: {title}")
            print("CONTENT:")
            print(content[:400])

    # (C) Belirsizlik kontrolü (çok yakın skorlar)
    top_scores = [float(r.get("score", 0.0)) for r in results]
    if len(top_scores) >= 2:
        gap = abs(top_scores[0] - top_scores[1])
        if gap < 0.0005:
            return make_no_answer("ambiguous_retrieval")

    # (D) Güvenli fallback (LLM kullanmadan)
    fallback = quick_answer_from_context(question, results)
    if fallback:
        return {"type": "answer", "text": fallback, "sources": results[:3]}

    return make_no_answer("no_clear_context")


def main():
    q = input("Soru: ")
    print(run(q, debug=True))


if __name__ == "__main__":
    main()
