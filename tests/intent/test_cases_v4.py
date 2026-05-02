TEST_CASES = [

# -----------------------------
# REFERENCE (15)
# -----------------------------
{"q": "TCK 212 nedir", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "TCK 213 nedir", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "madde 214 ne diyor", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "215. madde nedir", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "TCK 216 nedir", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "madde 217 nedir", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "TCK 218 nedir", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "madde 219 ne diyor", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "TCK 220 nedir", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "madde 221 nedir", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "TCK 222 nedir", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "madde 223 ne diyor", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "TCK 224 nedir", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "madde 225 nedir", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "TCK 226 nedir", "intent": "reference", "rel": "reference_lookup", "tc": 0},

# -----------------------------
# COMPARISON (15)
# -----------------------------
{"q": "kasten yaralama ile neticesi sebebiyle ağırlaşmış yaralama farkı", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "dolandırıcılık ile hileli davranış farkı nedir", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "suç ile ceza farkı", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "kasten zarar verme ile mala zarar verme farkı", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "fail ile mağdur farkı nedir", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "hukuka uygunluk sebebi ile hukuka aykırılık farkı", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "doğrudan kast ile bilinçli taksir farkı", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "suç unsuru ile suç tipi farkı", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "ihmal ile icra farkı", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "teşebbüs ile tamamlanmış suç farkı nedir", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "kast taksir ayrımı", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "yağma dolandırıcılık farkı", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "suç kusur farkı", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "fail iştirakçi ayrımı", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "hırsızlık yağma ayrımı", "intent": "comparison", "rel": "comparison", "tc": 2},

# -----------------------------
# SINGLE_FOCUS (15)
# -----------------------------
{"q": "teşebbüs nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "icra hareketi nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "hazırlık hareketi nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "netice nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "nedensellik bağı nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "kusurluluk nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "ceza sorumluluğu nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "hukuka uygunluk sebebi nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "fail nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "mağdur nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "suç tipi nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "suç unsurları nelerdir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "kastın türleri nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "taksirin türleri nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "ceza nedir", "intent": "single_focus", "rel": "definition", "tc": 1},

# -----------------------------
# MULTI_DEFINITION (15)
# -----------------------------
{"q": "kast ve taksir nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "fail ve mağdur nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "suç ve ceza nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "hukuka uygunluk ve kusurluluk nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "teşebbüs ve icra nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "icra ve ihmal nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "suç ve kusur nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "ceza ve yaptırım nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "netice ve nedensellik nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "fail ve iştirakçi nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "suç ve suç tipi nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "kast ve kusurluluk nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "teşebbüs ve tamamlanmış suç nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "hukuka uygunluk ve hukuka aykırılık nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "suç ve haksız fiil nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},

]