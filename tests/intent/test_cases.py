TEST_CASES = [

# -----------------------------
# REFERENCE (15)
# -----------------------------
{"q": "TCK 141 nedir", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "TCK 142 nedir", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "TCK 21 nedir", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "TCK 22 nedir", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "madde 141 nedir", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "madde 22 ne diyor", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "22. madde ne diyor", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "141. madde ne diyor", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "TCK 141 hırsızlık nedir", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "TCK 22 taksir nedir", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "madde 86 kasten yaralama nedir", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "tck 149 ne diyor", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "madde 157 nedir", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "TCK 35 teşebbüs nedir", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "madde 267 iftira nedir", "intent": "reference", "rel": "reference_lookup", "tc": 0},

# -----------------------------
# COMPARISON (15)
# -----------------------------
{"q": "kast ile taksir farkı nedir", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "olası kast ile bilinçli taksir farkı", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "yağma ile hırsızlık farkı nedir", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "dolandırıcılık ile hırsızlık farkı nedir", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "kasten yaralama ile taksirle yaralama farkı nedir", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "hırsızlık ve yağma arasındaki fark", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "kast ve taksir arasındaki ayrım", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "olası kast bilinçli taksir farkı", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "yağma hırsızlık farkı", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "dolandırıcılık hırsızlık ayrımı", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "kast taksir karşılaştır", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "ceza sorumluluğu ile kusur farkı", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "suç ve kabahat farkı nedir", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "teşebbüs ile hazırlık hareketleri farkı", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "doğrudan kast ile olası kast farkı", "intent": "comparison", "rel": "comparison", "tc": 2},

# -----------------------------
# SINGLE (20)
# -----------------------------
{"q": "hırsızlık nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "yağma nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "dolandırıcılık nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "iftira suçu nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "kasten yaralama nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "taksirle öldürme nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "nitelikli hırsızlık nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "suç nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "kusur nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "ceza hukuku nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "ceza sorumluluğu nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "hukuka uygunluk nedenleri nelerdir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "suçun unsurları nelerdir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "teşebbüs nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "iştirak nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "içtima nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "meşru savunma nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "zorunluluk hali nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "kanunilik ilkesi nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "kastın unsurları nelerdir", "intent": "single_focus", "rel": "definition", "tc": 1},

# -----------------------------
# MULTI / AMBIGUOUS (10)
# -----------------------------
{"q": "hırsızlık ve nitelikli hırsızlık nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "kast ve taksir nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "yağma ve hırsızlık nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "suç ve ceza sorumluluğu nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "meşru savunma ve zorunluluk hali nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "olası kast ve bilinçli taksir nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "teşebbüs ve iştirak nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "ceza hukuku ve ceza sorumluluğu nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "suç kusur", "intent": "unknown", "rel": None, "tc": 2},
{"q": "kast taksir", "intent": "unknown", "rel": None, "tc": 2},

]