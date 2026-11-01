#!/usr/bin/env python3
"""Independent survival check: old-page sentences (soft wraps joined, Contents block and
the regenerated feature block removed) that are absent from the new page after normalising
whitespace, dashes, link prefixes and markup. Usage: old_sentences.py <old> <new>"""
import re, sys
def norm(s):
    s = s.replace("—", "--").replace("–", "-")
    s = re.sub(r"\]\((\.\./)+", "](", s)
    s = re.sub(r"\]\([^)]*\)", "]", s)
    s = re.sub(r"[`*\\|>]", "", s)
    s = re.sub(r"\s*-{1,2}\s*", " - ", s)
    return " ".join(s.split()).lower()
old = open(sys.argv[1], encoding="utf-8").read()
new = norm(open(sys.argv[2], encoding="utf-8").read())
start = old.find("## Contents")
end = old.find("\n## ", start + 5)
old = old[:start] + old[end:]
old = re.sub(r"<!-- milan-feature-status:start -->.*?<!-- milan-feature-status:end -->", "", old, flags=re.S)
paras, cur = [], []
for line in old.splitlines():
    t = line.strip()
    if t.startswith("|"):
        if cur: paras.append(" ".join(cur)); cur = []
        for c in re.split(r"(?<!\\)\|", t.strip("|")):
            c = c.strip()
            if not re.fullmatch(r"[-: ]*", c):
                paras.append(c)
    elif not t or t.startswith("#") or t.startswith("```"):
        if cur: paras.append(" ".join(cur)); cur = []
    else:
        cur.append(re.sub(r"^(>\s*|[*-]\s+|\d+\.\s+)", "", t))
if cur: paras.append(" ".join(cur))
sents = []
for p in paras:
    sents += [s.strip() for s in re.split(r"(?<=[.;:])\s+(?=[A-Z`*\[(])", p) if len(s.strip()) > 18]
missing = [s for s in sents if norm(s) not in new]
print("sentences", len(sents), "absent", len(missing))
for s in missing:
    print("-", s[:300])
