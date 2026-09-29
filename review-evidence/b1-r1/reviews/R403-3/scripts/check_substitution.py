#!/usr/bin/env python3
"""Prove that a redacted file differs from its original only by one token substitution.

usage: check_substitution.py <tokens-file> <label> <placeholder> <old-file> <new-file> [...]
Arguments after the placeholder come in old/new pairs. The token is looked up by
its label in the private tokens file (label<TAB>token), which is never published.
Each pair passes when replacing the token by the placeholder in the old bytes
(case-insensitively) gives exactly the new bytes. Prints only labels, counts
and SHA-256 values, never the token. Exit 1 when any pair fails.
"""
import hashlib
import re
import sys
from pathlib import Path

toks = dict(x.split("\t", 1) for x in Path(sys.argv[1]).read_text().splitlines() if x.strip())
label, placeholder = sys.argv[2], sys.argv[3].encode()
tok = toks[label].encode()
pat = re.compile(re.escape(tok), re.I)
bad = 0
args = sys.argv[4:]
for old, new in zip(args[0::2], args[1::2]):
    ob, nb = Path(old).read_bytes(), Path(new).read_bytes()
    n = len(pat.findall(ob))
    ok = pat.sub(placeholder, ob) == nb
    left = len(pat.findall(nb))
    print(f"{Path(new).name}: [{label}] occurrences in old {n}, in new {left}; "
          f"old {hashlib.sha256(ob).hexdigest()[:16]} -> new {hashlib.sha256(nb).hexdigest()[:16]}; "
          f"substitution-only {'YES' if ok else 'NO'}")
    bad += not ok or left != 0
print("RESULT", "PASS" if not bad else "FAIL")
sys.exit(1 if bad else 0)
