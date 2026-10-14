"""Scan the visible copy of an HTML page for AI writing tells. Exit code 1 if anything is found.
Usage: python3 copy_check.py page.html"""
import re, sys, html

ALLOWED_HYPHENS = {"Full-Funnel"}  # product names only
AUDIENCE = r"\b(you|your|yours|yourself|board|boards|CEO|CEOs|leaders should|executives should)\b"
PHRASES = [
    "the proof is", "proof gate", "game changer", "game-changer", "unlock", "leverage", "landscape", "seamless",
    "robust", "journey", "empower", "in today's", "it's not about", "isn't about", "the reality is", "worth noting",
    "the question is", "the answer is", "here's the thing", "make no mistake", "at its core", "the bottom line",
    "not just", "more than ever", "the future of", "delve", "navigate", "holistic", "synergy", "cutting edge",
    "paradigm", "transformative", "revolutionis", "supercharge", "elevate", "harness", "ever-evolving",
    "fast-paced", "what remains open", "which is how", "and that matters", "this piece", "this paper",
    "in this article", "let's", "imagine a world", "simply put", "put simply", "in short", "the stakes",
]
PATTERNS = [
    (r"[—–]", "em or en dash"),
    (r"\bnot (only )?\w+(?: \w+){0,4}, but\b", "not X, but Y"),
    (r"\b\w+ isn't \w+\. It's\b", "isn't X. It's Y"),
    (r"(?:^|\. )[A-Z][^.?!]{0,18}\.(?= |$)", "short fragment sentence"),
    (r":\s+[a-z][^.]{0,40}\.\s", "possible colon reveal"),
]


def visible_text(path):
    t = open(path, encoding="utf-8").read()
    t = re.sub(r"<(script|style|title|desc)\b.*?</\1>", " ", t, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", html.unescape(t))


def check(path):
    txt = visible_text(path)
    issues = []
    for m in re.finditer(r"\b[A-Za-z]+-[A-Za-z]+\b", txt):
        if m.group() not in ALLOWED_HYPHENS:
            issues.append(("hyphenated compound", m.group()))
    for m in re.finditer(AUDIENCE, txt, flags=re.I):
        issues.append(("addresses the reader", txt[max(0, m.start() - 40):m.end() + 40]))
    low = txt.lower()
    for p in PHRASES:
        for m in re.finditer(re.escape(p), low):
            issues.append(("stock phrase", txt[max(0, m.start() - 30):m.end() + 30]))
    for rx, name in PATTERNS:
        for m in re.finditer(rx, txt):
            issues.append((name, txt[max(0, m.start() - 30):m.end() + 30]))
    return issues


if __name__ == "__main__":
    found = check(sys.argv[1])
    for kind, ctx in found:
        print(f"{kind}: ...{ctx.strip()}...")
    print(f"{len(found)} issues")
    sys.exit(1 if found else 0)
