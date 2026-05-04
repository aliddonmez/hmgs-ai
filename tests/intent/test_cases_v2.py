TEST_CASES = [

# -----------------------------
# REFERENCE (15)
# -----------------------------
{"q": "TCK 125 nedir", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "TCK 106 nedir", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "madde 81 nedir", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "madde 86 ne diyor", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "87. madde nedir", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "tck 29 nedir", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "tck 30 nedir", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "madde 43 nedir", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "tck 102 ne diyor", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "madde 103 nedir", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "tck 188 nedir", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "madde 191 nedir", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "tck 204 nedir", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "madde 267 ne diyor", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "tck 272 nedir", "intent": "reference", "rel": "reference_lookup", "tc": 0},

# -----------------------------
# COMPARISON (15)
# -----------------------------
{"q": "kasten yaralama ile taksirle yaralama farkı", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "yağma ile gasp farkı nedir", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "hırsızlık dolandırıcılık farkı nedir", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "olası kast bilinçli taksir farkı nedir", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "doğrudan kast olası kast farkı", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "suç kabahat farkı", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "kasten öldürme taksirle öldürme farkı", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "teşebbüs hazırlık hareketleri farkı nedir", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "fail iştirakçi farkı nedir", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "dolandırıcılık güveni kötüye kullanma farkı", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "kast taksir farkı", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "yağma hırsızlık farkı nedir", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "suç ceza sorumluluğu farkı", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "meşru savunma zorunluluk hali farkı", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "hırsızlık nitelikli hırsızlık farkı", "intent": "comparison", "rel": "comparison", "tc": 2},

# -----------------------------
# SINGLE_FOCUS (15)
# -----------------------------
{"q": "hakaret suçu nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "tehdit suçu nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "kasten öldürme nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "taksir nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "olası kast nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "bilinçli taksir nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "hukuka aykırılık nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "kusurluluk nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "fail nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "iştirak nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "içtima nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "ceza nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "suçun unsurları nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "kastın türleri nelerdir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "taksirin unsurları nelerdir", "intent": "single_focus", "rel": "definition", "tc": 1},

# -----------------------------
# MULTI_DEFINITION (15)
# -----------------------------
{"q": "kast ve taksir nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "olası kast ve bilinçli taksir nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "hırsızlık ve yağma nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "suç ve ceza nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "fail ve mağdur nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "kusur ve sorumluluk nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "meşru savunma ve zorunluluk hali nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "teşebbüs ve iştirak nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "ceza ve yaptırım nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "hukuka aykırılık ve kusur nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "kast ve kusur nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "fail ve iştirakçi nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "suç ve kabahat nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "hırsızlık ve nitelikli hırsızlık nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "kasten öldürme ve taksirle öldürme nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},

]