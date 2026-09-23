#!/usr/bin/env python3
"""List public comment IDs whose text carries an identity token (labels only).

Usage: comment_token_scan.py TOKENS.tsv COMMENTS.json [...]
Raw, case-insensitive (or case-sensitive per token mode) substring search of
each comment body; prints comment id, author role prefix and token labels.
"""
import ast, json, re, sys

toks = []
for ln in open(sys.argv[1], encoding="utf-8"):
    if ln.strip():
        l, c, m, lit = ln.rstrip("\n").split("\t", 3)
        t = ast.literal_eval(lit).decode("latin-1")
        toks.append((l, c, re.compile(re.escape(t), re.I if m == "ci" else 0)))
for f in sys.argv[2:]:
    for c in json.load(open(f)):
        b = c["body"]
        hit = sorted({f"{l}({cls})" for l, cls, p in toks if p.search(b)})
        if hit:
            role = re.match(r"\[?([A-Z]\d+[^\]\s]*)", b.strip())
            print(f"COMMENT {c['id']} {c['created_at']} {role.group(1) if role else '?'} :: {', '.join(hit)}")
