import random
from collections import defaultdict


def select_questions(
    question_pool, n_questions, mode="balanced", weak_topics=None, seed=None
):
    rnd = random.Random(seed)

    if mode == "random":
        return qrandom(question_pool, n_questions, rnd)

    if mode == "balanced":
        return qbalanced(question_pool, n_questions, rnd)

    if mode == "weak_focus":
        return qweak_focus(question_pool, n_questions, weak_topics, rnd)

    raise ValueError("Geçersiz Mod")


## random secimi
def qrandom(pool, n, rnd):
    return rnd.sample(pool, min(n, len(pool)))


## balanced secimi
import random
from collections import defaultdict

def _lesson_name(q: dict) -> str:
    return q.get("ders") or q.get("dersadi") or "Bilinmiyor"

def qbalanced(question_pool, n, rnd: random.Random):
    # Havuz boşsa direkt boş dön
    if not question_pool:
        return []

    by_lesson = defaultdict(list)
    for q in question_pool:
        by_lesson[_lesson_name(q)].append(q)

    lessons = list(by_lesson.keys())

    # ✅ KRİTİK FIX: ders yoksa patlama -> random fallback
    if not lessons:
        k = min(n, len(question_pool))
        return rnd.sample(question_pool, k)

    base = n // len(lessons)
    extra = n % len(lessons)

    selected = []
    rnd.shuffle(lessons)

    for i, lesson in enumerate(lessons):
        k = base + (1 if i < extra else 0)
        candidates = by_lesson[lesson]
        if not candidates:
            continue
        take = min(k, len(candidates))
        selected.extend(rnd.sample(candidates, take))

    # Eğer derslerden yeterince toplayamadıysak random ile tamamla
    if len(selected) < n:
        remaining = [q for q in question_pool if q not in selected]
        need = min(n - len(selected), len(remaining))
        if need > 0:
            selected.extend(rnd.sample(remaining, need))

    return selected[:n]


def qweak_focus(pool, n, weak_topics, rnd):

    if not weak_topics:
        return qbalanced(pool, n, rnd)

    weak3 = weak_topics[:3]

    ## örneğin 20 soru varsa 8 tanesi eksik oldugun konudan
    weak_quota = int(n * 0.4)
    general_quota = n - weak_quota
    ## kalanı genel havuzdan

    weak_pool = [q for q in pool if q.get("konu") in weak3]

    selected = []

    if weak_pool:
        weak_picks = rnd.sample(weak_pool, min(weak_quota, len(weak_pool)))
        selected.extend(weak_picks)

    ## örneğin zayıf konuda 8 tane soru yok 5 tane var hata vermez o 5 i alır .

    remaining_pool = [q for q in pool if q not in selected]
    ## secilenler dışarı atılır tekrar secilmemesi icin

    general_picks = rnd.sample(remaining_pool, min(general_quota, len(remaining_pool)))
    ## geri kalanlar havuzdan doldurulur.

    selected.extend(general_picks)

    ## eğer weak soru az olduğu için toplam n'e ulaşmadıysa tekrar tamamla
    if len(selected) < n:
        remaining_pool2 = [q for q in pool if q not in selected]
        fill = rnd.sample(remaining_pool2, min(n - len(selected), len(remaining_pool2)))
        selected.extend(fill)

    return selected[:n]
