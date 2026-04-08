# Candidate retrieval
FETCH_K = 50

# Reranking
RERANK_K = 15

# Final selection
TOP_K = 10
PER_DOC_LIMIT = 2

# Filtering / boosting
MIN_SCORE = 0.35
TOPIC_BOOST = 0.05

# Answer interpretation
AMBIGUITY_MARGIN = 0.0005

# Weak retrieval kontrolü
MIN_TOP_SCORE = 0.65
MIN_SECOND_SCORE = 0.45
MIN_AVG_TOP3_SCORE = 0.55

# Debug flags
DEBUG_RETRIEVAL = True
DEBUG_RAG = False
DEBUG_LLM = False
DEBUG_META = False  # metadata debug aç/kapat

# Topic classifier ayarları
TOPIC_CONFIDENCE_THRESHOLD = 0.4   # minimum güven
TOPIC_MARGIN_THRESHOLD = 0.1       # ilk iki skor farkı