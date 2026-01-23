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

## prompt doldurma 
def load_prompt():
    prompt_path = Path(__file__).resolve().parents[1] / "docs" / "prompt_v1.md"
    return prompt_path.read_text(encoding="utf-8")

##{context doldurma}
def fill_prompt(prompt_template: str, context: str) -> str:
    return prompt_template.replace("{{context}}", context)


def main():
    # 1️⃣ Soru
    question = "Hırsızlık suçu nedir?"

    # 2️⃣ Retrieval + Context
    results = retrieve(question, top_k=5)
    context = build_context(results)

    # 3️⃣ Prompt
    prompt_template = load_prompt()
    final_prompt = fill_prompt(prompt_template, context)

    print("=== FINAL PROMPT ===\n")
    print(final_prompt)

    # 4️⃣ LLM (Gemini)
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

    response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=final_prompt
    )

    print("\n=== LLM ANSWER (GEMINI) ===\n")
    print(response.text)
    
    


if __name__ == "__main__":
    main()
