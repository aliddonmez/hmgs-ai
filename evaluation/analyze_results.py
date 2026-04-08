import re
from collections import defaultdict


def analyze(log_text: str):
    results = []

    pattern = re.compile(
        r"(\d+)\.\s+SORU:\s+(.*?)\n"
        r".*?Grup\s+:\s+(.*?)\n"
        r".*?Beklenen madde:\s+(.*?)\n"
        r".*?Gelen madde\s+:\s+(.*?)\n"
        r".*?Beklenen tip\s+:\s+(.*?)\n"
        r".*?SONUÇ\s+:\s+(✔️ DOĞRU|❌ YANLIŞ)",
        re.DOTALL,
    )

    matches = pattern.findall(log_text)

    for q_no, question, group, expected_madde, gelen_madde, expected_type, result in matches:
        results.append(
            {
                "q_no": int(q_no),
                "question": question.strip(),
                "group": group.strip(),
                "expected_madde": expected_madde.strip(),
                "gelen_madde": gelen_madde.strip(),
                "expected_type": expected_type.strip(),
                "correct": "✔️" in result,
            }
        )

    stats = defaultdict(lambda: {"total": 0, "correct": 0})

    for r in results:
        stats[r["group"]]["total"] += 1
        if r["correct"]:
            stats[r["group"]]["correct"] += 1

    print("\n=== GROUP ANALYSIS ===\n")

    total_all = 0
    correct_all = 0

    for group in ["single_article", "comparison", "concept", "other"]:
        if group not in stats:
            continue

        total = stats[group]["total"]
        correct = stats[group]["correct"]
        acc = (correct / total) * 100 if total else 0.0

        total_all += total
        correct_all += correct

        print(f"{group.upper():<15} | total={total:<3} correct={correct:<3} acc={acc:.2f}%")

    print("\n--- OVERALL ---")
    overall_acc = (correct_all / total_all) * 100 if total_all else 0.0
    print(f"TOTAL={total_all} CORRECT={correct_all} ACC={overall_acc:.2f}%")

    print("\n=== WRONG QUESTIONS ===\n")
    for r in results:
        if not r["correct"]:
            print(f"[{r['q_no']}] {r['question']}")
            print(f"  group         : {r['group']}")
            print(f"  expected_madde: {r['expected_madde']}")
            print(f"  gelen_madde   : {r['gelen_madde']}")
            print(f"  expected_type : {r['expected_type']}")
            print("-" * 60)


if __name__ == "__main__":
    print("Evaluation çıktısı dosyadan veya terminalden verilecek.\n")

    import sys

    log_text = sys.stdin.read()
    analyze(log_text)