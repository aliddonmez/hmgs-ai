COMPARISON_PATTERNS = [
    "arasındaki fark",
    "farkı nedir",
    "fark nedir",
    "arasındaki ayrım",
    "ayrımı nedir",
    "ayrım",
    "farkı",
    "fark",
    "karşılaştır",
]

DEFINITION_PATTERNS = [
    "nedir",
    "nelerdir",
    "ne demek",
    "unsurları",
    "şartları",
    "nedenleri",
]

REFERENCE_PATTERNS = [
    r"\bmadde\s+\d+\b",
    r"\btck\s*\d+\b",
    r"\b\d+\.\s*madde\b",
    r"\b\d+\s*madde\b",
]

STOPWORD_TOKENS = {
    "ve", "veya", "ile", "ya", "da", "de", "ki",
    "nedir", "nelerdir", "ne", "demek",
    "fark", "farkı", "ayrım", "ayrımı",
    "karşılaştır", "arasındaki", "arasında",
    "madde", "tck", "diyor",
}