#!/usr/bin/env python3
"""Derive, without printing them, the tokens a published mask removed.

usage: derive_mask_tokens.py BEFORE_FILE AFTER_FILE OUT_TOKENS_FILE
BEFORE/AFTER are the published grade_b8.py at 5bad6a43 and at 36ee6d8a.
Writes the removed-only tokens to OUT_TOKENS_FILE (keep it unpublished) and
prints only their count and shape.
"""
import difflib, re, sys
a = open(sys.argv[1]).read().splitlines(); b = open(sys.argv[2]).read().splitlines()
d = list(difflib.unified_diff(a, b, lineterm="", n=0))
rem = [l for l in d if l.startswith("-") and not l.startswith("---")]
add = [l for l in d if l.startswith("+") and not l.startswith("+++")]
tok = sorted(set(re.findall(r"[A-Za-z0-9_]+", " ".join(rem))) - set(re.findall(r"[A-Za-z0-9_]+", " ".join(add))))
open(sys.argv[3], "w").write("\n".join(tok))
print("removed lines %d, added %d, tokens %d, shapes %s"
      % (len(rem), len(add), len(tok), [("digits" if t.isdigit() else "word", len(t)) for t in tok]))
