import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from retrieval.pipeline import retrieve_chunks
from evaluation.test_questions import TEST_QUESTIONS


def extract_top_madde(results):
    if not results:
        return None

    top = results[0]
    meta = top.get("meta", {}) or {}
    return meta.get("madde_no")


def main():
    total = len(TEST_QUESTIONS)
    correct = 0

    print("\n=== RETRIEVAL EVALUATION START ===\n")

    for i, item in enumerate(TEST_QUESTIONS, start=1):
        question = item["question"]
        expected_madde = item["expected_madde"]
        expected_type = item["expected_type"]
        group = item.get("group", "unknown")

        results = retrieve_chunks(question)

        if not results:
            top_madde = None
        else:
            sorted_results = sorted(
                results,
                key=lambda x: float(x.get("final_score", 0.0)),
                reverse=True,
            )
            top_madde = extract_top_madde(sorted_results)

        is_correct = False

        if expected_type == "answer":
            is_correct = top_madde == expected_madde
        elif expected_type == "uncertain":
            is_correct = top_madde is None

        if is_correct:
            correct += 1

        print(f"{i}. SORU: {question}")
        print(f"   Grup          : {group}")
        print(f"   Beklenen madde: {expected_madde}")
        print(f"   Gelen madde   : {top_madde}")
        print(f"   Beklenen tip  : {expected_type}")
        print(f"   SONUÇ         : {'✔️ DOĞRU' if is_correct else '❌ YANLIŞ'}")
        print("-" * 60)

    accuracy = (correct / total) * 100 if total else 0.0

    print("\n=== RETRIEVAL EVALUATION END ===")
    print(f"Toplam soru : {total}")
    print(f"Doğru       : {correct}")
    print(f"Accuracy    : %{accuracy:.2f}")


if __name__ == "__main__":
    main()