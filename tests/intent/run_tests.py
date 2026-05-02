import sys

from retrieval.intent.classifier import classify_intent

if len(sys.argv) < 2:
    print("Kullanım: python -m tests.intent.run_tests v1|v2|v3")
    raise SystemExit(1)

version = sys.argv[1]

if version == "v1":
    from tests.intent.test_cases import TEST_CASES
elif version == "v2":
    from tests.intent.test_cases_v2 import TEST_CASES
elif version == "v3":
    from tests.intent.test_cases_v3 import TEST_CASES
elif version == "v4":
    from tests.intent.test_cases_v2 import TEST_CASES
elif version == "v5":
    from tests.intent.test_cases_v3 import TEST_CASES
else:
    print("Geçersiz test seti. v1, v2, v3, v4 veya v5 yaz.")
    raise SystemExit(1)



correct = 0
total = len(TEST_CASES)

wrong_cases = []

for case in TEST_CASES:
    result = classify_intent(case["q"])

    ok = (
        result["intent_type"] == case["intent"]
        and result["relation_type"] == case["rel"]
        and result["target_count"] == case["tc"]
    )

    if ok:
        correct += 1
    else:
        wrong_cases.append({
            "question": case["q"],
            "expected": case,
            "actual": result,
        })

print("\n====================")
print(f"TOTAL: {total}")
print(f"CORRECT: {correct}")
print(f"ACCURACY: {correct/total:.2%}")

print("\n--- WRONG CASES ---")
for w in wrong_cases:
    print("\nQ:", w["question"])
    print("EXPECTED:", w["expected"])
    print("ACTUAL:", {
        "intent": w["actual"]["intent_type"],
        "rel": w["actual"]["relation_type"],
        "tc": w["actual"]["target_count"],
    })