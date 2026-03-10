import re


def is_safe_sql(query: str) -> bool:
    """Return True if the query is a read-only SELECT without forbidden keywords.

    This is intentionally simple; for a production system you'd want a proper
    parser or use database permissions, but this covers the basic requirements.
    """
    if not query:
        return False

    q = query.strip().lower()
    # only allow select statements
    if not q.startswith("select"):
        return False

    # deny potentially dangerous keywords anywhere in the query
    forbidden = ["drop", "delete", "update", "insert", "alter", "truncate"]
    for kw in forbidden:
        # simple word boundary check
        if re.search(r"\b" + kw + r"\b", q):
            return False
    return True
