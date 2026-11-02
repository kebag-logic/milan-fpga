#!/usr/bin/env python3
"""Split the previous head's hand-carried prose (note rows and paragraphs) into sentences and look for
each one, normalised, on the new page, the design notes or the descriptions. Independent of the author's tool.
Usage: survival.py <old-page> <new-page> <notes> <descriptions>"""
import re, sys
old, new, notes, desc = sys.argv[1:5]
def norm(s):
    s = s.replace("\\|", "|").replace('\\"', '"').replace("\\n"," ")
    s = re.sub(r"\]\([^)]*\)", "]", s)
    s = re.sub(r"[`*\[\]_]", "", s)
    s = re.sub(r"\s+", " ", s).strip().lower()
    return s
hay = norm(open(new, encoding="utf-8").read()) + " " + norm(open(notes, encoding="utf-8").read()) + " " + norm(open(desc, encoding="utf-8").read())
frags = []
for i, l in enumerate(open(old, encoding="utf-8"), 1):
    if l.startswith("|"):
        cs = [c.strip() for c in re.split(r"(?<!\\)\|", l)[1:-1]]
        txt = cs[-1] if cs else ""
    elif l.startswith(("#", "!", "```")): continue
    else: txt = l.strip()
    for s in re.split(r"(?<=[.;:])\s+", txt):
        s2 = norm(s)
        if len(s2.split()) >= 6: frags.append((i, s, s2))
miss = [(i, s) for i, s, n in frags if n not in hay]
print("fragments", len(frags), "missing", len(miss))
for i, s in miss: print(i, s[:300])
