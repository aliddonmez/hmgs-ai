# app/rag_pipeline.py

from analysis.pgvector_similarity import retrieve
from pathlib import Path
import os
from google import genai


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
    question = input("Lütfen sorunuzu girin: ")

    results = retrieve(question, top_k=5)
    context = build_context(results)

    prompt_template = load_prompt()
    final_prompt = fill_prompt(prompt_template, question, context)

    print("=== FINAL PROMPT ===\n")
    print(final_prompt)

    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=final_prompt
    )

    print("\n=== LLM ANSWER (GEMINI) ===\n")
    print(response.text)


if __name__ == "__main__":
    main()
