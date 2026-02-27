# Fact_Check_System.py
"""
Fact‑check system prototype for OpenClaw‑driven reporting.

Features:
- `keyword_flags` – map of suspicious keyword patterns to a red‑flag label.
- `source_trust` – dictionary of known domains with a base trust score (0‑100).
- `compute_trust_score(text, source_url)` – returns a composite trust score for a
  piece of content.
- `is_red_flagged(text)` – quick check whether the content contains any
  high‑risk keyword combination (e.g., "quantum" + "Fibonacci" + "time manipulation").

The implementation is a lightweight placeholder; actual production code would
populate the dictionaries from a persistent DB and use more sophisticated NLP
(embeddings, similarity search, LLM verification) to refine the score.
"""
import re
from urllib.parse import urlparse

# ---------------------------------------------------------------------------
# Configuration – these would normally be loaded from a DB or config file.
# ---------------------------------------------------------------------------
# Keywords that raise suspicion. The value is the weight (0‑100) added to the
# final score when the pattern is found.
keyword_flags = {
    r"quantum\s*comput(?:er|ing)": 30,
    r"fibonacci": 20,
    r"time\s*manipulation|time\s*travel|time\s*warp": 30,
    # Add more patterns as needed.
}

# Source trust scores – higher is more trustworthy. Domains not listed default
# to a neutral baseline (50).
source_trust = {
    "arxiv.org": 90,
    "nature.com": 85,
    "ieee.org": 80,
    "github.com": 75,
    "medium.com": 60,
    "clickbaitnews.example": 10,  # example of low‑trust source
    # … extend with real values.
}

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------
def _normalize_text(text: str) -> str:
    """Lower‑case and collapse whitespace for simple matching."""
    return " ".join(text.lower().split())

def _extract_domain(url: str) -> str:
    """Return the hostname part of a URL, without sub‑domains.
    e.g. ``https://sub.example.com/path`` -> ``example.com``.
    """
    try:
        hostname = urlparse(url).hostname or ""
        # Strip sub‑domains (keep last two labels)
        parts = hostname.split('.')
        return ".".join(parts[-2:]) if len(parts) >= 2 else hostname
    except Exception:
        return ""

# ---------------------------------------------------------------------------
# Core scoring logic
# ---------------------------------------------------------------------------
def compute_trust_score(text: str, source_url: str = "") -> int:
    """Calculate a trust score (0‑100) for the given content.

    The algorithm is a simple weighted sum:
    1. Start from the base source trust (default 50).
    2. Add keyword penalties (higher weight = less trustworthy).
    3. Clamp the final value to the 0‑100 range.
    """
    norm = _normalize_text(text)
    # Base trust from source
    domain = _extract_domain(source_url)
    base = source_trust.get(domain, 50)
    penalty = 0
    for pattern, weight in keyword_flags.items():
        if re.search(pattern, norm):
            penalty += weight
    # The higher the penalty, the lower the trust.
    score = max(0, min(100, base - penalty))
    return score

def is_red_flagged(text: str) -> bool:
    """Return ``True`` if the text contains a high‑risk keyword combination.
    Currently we flag content that mentions *all* of the following groups:
      - quantum computing related term
      - fibonacci (or a variant)
      - time manipulation / travel term
    """
    norm = _normalize_text(text)
    has_quantum = any(re.search(r"quantum\s*comput(?:er|ing)", norm) for _ in [1])
    has_fibo = any(re.search(r"fibonacci", norm) for _ in [1])
    has_time = any(re.search(r"time\s*manipulation|time\s*travel|time\s*warp", norm) for _ in [1])
    return has_quantum and has_fibo and has_time

# ---------------------------------------------------------------------------
# Example usage (would be removed or placed under a ``if __name__ == '__main__'``
# guard in production).
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    sample = "Quantum computers using Fibonacci sequences could enable time manipulation."
    print("Red flag?", is_red_flagged(sample))
    print("Trust score", compute_trust_score(sample, "https://clickbaitnews.example/article"))
"""
