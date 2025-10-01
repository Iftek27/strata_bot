from utils.synonyms import SYNONYM_MAP


def expand_with_synonyms(query: str) -> str:
    """
    Expand words in the query with domain-specific synonyms.
    Example:
      "balcony repairs" -> "balcony repairs OR maintenance OR fixing damage"
    """
    words = query.split()
    expanded = []
    for w in words:
        key = w.lower().strip("?,.")
        if key in SYNONYM_MAP:
            expanded.append("(" + " OR ".join(SYNONYM_MAP[key]) + ")")
        else:
            expanded.append(w)
    return " ".join(expanded)


def rewrite_query(query: str) -> str:
    """
    Reframe a natural query into legal-style, 
    focused on the Unit Titles (Management) Act 2011 (ACT).
    """
    expanded = expand_with_synonyms(query)
    return (
        f"Under the Unit Titles (Management) Act 2011 (ACT), "
        f"what are the rules or responsibilities regarding {expanded}?"
    )


if __name__ == "__main__":
    # Quick test
    q = "Who fixes balcony leaks?"
    rewritten = rewrite_query(q)
    print("🔎 Original:", q)
    print("📝 Rewritten:", rewritten)
