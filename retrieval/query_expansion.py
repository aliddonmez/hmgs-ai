# retrieval/query_expansion.py

EXPANSIONS = {
    "hırsızlık": ["taşınır mal", "zilyet", "rızasız alma"],
    "dolandırıcılık": ["hile", "aldatma", "menfaat"],
    "taksir": ["dikkat", "özen yükümlülüğü"],
}


def expand_query(question: str):

    q = question.lower()
    expanded = question

    for keyword, words in EXPANSIONS.items():

        if keyword in q:
            expanded += " " + " ".join(words)

    return expanded
