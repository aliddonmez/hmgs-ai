# app/rag_pipeline.py
from pathlib import Path
import os

from dotenv import load_dotenv
load_dotenv()

from google import genai
from analysis.pgvector_similarity import retrieve


IDK_TEXT = "Bu soruya, elimdeki kaynaklara dayanarak güvenilir bir cevap veremiyorum."


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


def build_context(results):
    parts = []
    for title, content, score in results:
        parts.append(f"### {title}\n{content}")
    return "\n\n---\n\n".join(parts)


def load_prompt():
    prompt_path = Path(__file__).resolve().parents[1] / "docs" / "prompt_v1.md"
    print("PROMPT PATH:", prompt_path)
    return prompt_path.read_text(encoding="utf-8")


def fill_prompt(prompt_template: str, question: str, context: str) -> str:
    prompt = prompt_template.replace("{{question}}", question)
    prompt = prompt.replace("{{context}}", context)
    return prompt


def main():
    debug = os.environ.get("DEBUG") == "1"

    question = input("Lütfen sorunuzu girin: ").strip()
    if not question:
        print("⚠️ Boş soru girdin.")
        return

    # (A) Out-of-scope => direkt IDK
    if is_out_of_scope(question):
        if debug:
            print("\n=== FINAL ANSWER ===\n")
            print(IDK_TEXT)
            print("\n[DEBUG] reason=out_of_scope_keyword")
        else:
            print(IDK_TEXT)
        return

    # (B) Retrieval (confidence + topic filter içeride)
    results = retrieve(
        question,
        top_k=5,
        fetch_k=20,
        min_score=0.60,
        use_topic_filter=True,
        debug=debug,
    )

    # (C) Confidence check: sonuç yoksa LLM yok
    if not results:
        if debug:
            print("\n=== FINAL ANSWER ===\n")
            print(IDK_TEXT)
            print("\n[DEBUG] reason=no_result_after_min_score")
        else:
            print(IDK_TEXT)
        return

    # (D) Prompt + LLM
    context = build_context(results)
    prompt_template = load_prompt()
    final_prompt = fill_prompt(prompt_template, question, context)

    if debug:
        print("\n=== FINAL PROMPT ===\n")
        print(final_prompt)

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY bulunamadı.")
        return

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=final_prompt
        )
        print("\n=== LLM ANSWER (GEMINI) ===\n")
        print(response.text)

    except Exception as e:
        print("\n❌ LLM çağrısı başarısız oldu.")
        print("Hata:", str(e))


if __name__ == "__main__":
    main()