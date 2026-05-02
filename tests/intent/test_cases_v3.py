TEST_CASES = [

# -----------------------------
# REFERENCE (15)
# -----------------------------
{"q": "TCK 82 nedir", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "TCK 91 nedir", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "madde 94 ne diyor", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "95. madde nedir", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "TCK 96 nedir", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "madde 98 nedir", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "TCK 99 nedir", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "madde 100 ne diyor", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "TCK 104 nedir", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "madde 105 nedir", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "TCK 107 nedir", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "madde 108 ne diyor", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "TCK 109 nedir", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "madde 110 nedir", "intent": "reference", "rel": "reference_lookup", "tc": 0},
{"q": "TCK 111 nedir", "intent": "reference", "rel": "reference_lookup", "tc": 0},

# -----------------------------
# COMPARISON (15)
# -----------------------------
{"q": "kasten öldürme ile ihmali davranışla öldürme farkı", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "dolaylı kast ile doğrudan kast farkı nedir", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "suç ile haksız fiil farkı", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "yağma ile gasp arasındaki fark", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "tehdit ile şantaj farkı nedir", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "dolandırıcılık ile zimmet farkı", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "kasten zarar verme ile taksirle zarar verme farkı", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "fail ile azmettiren farkı", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "iştirak ile teşebbüs farkı nedir", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "hukuka uygunluk nedeni ile kusurluluk farkı", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "icra hareketi ile hazırlık hareketi farkı", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "kasten işlenen suç ile taksirli suç farkı", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "neticesi sebebiyle ağırlaşmış suç ile basit suç farkı", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "şahsi cezasızlık sebebi ile hukuka uygunluk sebebi farkı", "intent": "comparison", "rel": "comparison", "tc": 2},
{"q": "suç ile disiplin suçu farkı nedir", "intent": "comparison", "rel": "comparison", "tc": 2},

# -----------------------------
# SINGLE_FOCUS (15)
# -----------------------------
{"q": "zimmet suçu nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "şantaj suçu nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "görevi kötüye kullanma nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "güveni kötüye kullanma nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "dolaylı kast nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "kusur ilkesi nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "kusurluluk nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "kusurun türleri nelerdir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "failin sorumluluğu nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "suçun maddi unsuru nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "suçun manevi unsuru nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "netice nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "icra hareketi nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "ihmal nedir", "intent": "single_focus", "rel": "definition", "tc": 1},
{"q": "yaptırım nedir", "intent": "single_focus", "rel": "definition", "tc": 1},

# -----------------------------
# MULTI_DEFINITION (15)
# -----------------------------
{"q": "fail ve azmettiren nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "kast ve taksir nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "hukuka uygunluk ve kusurluluk nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "suç ve yaptırım nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "tehdit ve şantaj nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "dolandırıcılık ve zimmet nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "güveni kötüye kullanma ve dolandırıcılık nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "fail ve iştirakçi nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "suç ve haksız fiil nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "icra hareketi ve hazırlık hareketi nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "netice ve nedensellik bağı nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "kusur ve sorumluluk nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "kast ve kusurluluk nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "suç ve disiplin suçu nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},
{"q": "yaptırım ve ceza nedir", "intent": "multi_definition", "rel": "definition", "tc": 2},

]