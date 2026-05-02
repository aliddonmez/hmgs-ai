TEST_CASES = [

# -----------------------------
# REFERENCE (15)
# -----------------------------
{"q": "TCK 301 nedir", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "TCK 302 nedir", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "madde 303 ne diyor", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "304. madde nedir", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "TCK 305 nedir", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "madde 306 nedir", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "TCK 307 nedir", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "madde 308 ne diyor", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "TCK 309 nedir", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "madde 310 nedir", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "TCK 311 nedir", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "madde 312 ne diyor", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "TCK 313 nedir", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "madde 314 nedir", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "TCK 315 nedir", "intent": "reference", "rel": "reference_lookup", "tc": 0},

# -----------------------------
# COMPARISON (15)
# -----------------------------
{"q": "kast taksir farkı nedir", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "suç kusur farkı nedir", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "fail mağdur farkı", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "suç ceza farkı", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "teşebbüs icra farkı", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "icra ihmal farkı", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "netice nedensellik farkı", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "fail iştirakçi farkı", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "hukuka uygunluk kusurluluk farkı", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "suç tipi suç unsuru farkı", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "kasten öldürme taksirle öldürme farkı", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "yağma gasp farkı", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "dolandırıcılık hırsızlık farkı", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "ceza yaptırım farkı", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "suç kabahat farkı", "intent": "comparison", "rel": "comparison", "tc": 2},

# -----------------------------
# SINGLE_FOCUS (15)
# -----------------------------
{"q": "kast nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "taksir nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "suç nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "kusur nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "ceza nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "yaptırım nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "fail nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "mağdur nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "teşebbüs nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "icra nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "ihmal nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "netice nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "nedensellik nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "suç unsuru nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "suç tipi nedir", "intent": "single_focus", "rel": "definition", "tc": 1},

# -----------------------------
# MULTI_DEFINITION (15)
# -----------------------------
{"q": "kast taksir nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "suç kusur nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "fail mağdur nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "ceza yaptırım nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "teşebbüs icra nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "icra ihmal nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "netice nedensellik nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "suç tipi suç unsuru nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "hukuka uygunluk kusurluluk nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "fail iştirakçi nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "yağma gasp nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "dolandırıcılık hırsızlık nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "suç kabahat nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "kast kusur nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "ceza sorumluluk nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},

]