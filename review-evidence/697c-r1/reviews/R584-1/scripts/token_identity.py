#!/usr/bin/env python3
"""Compare C token streams (comments dropped) of file pairs with clang's raw lexer.
usage: token_identity.py OLD_ROOT NEW_ROOT old_rel:new_rel ...
Prints per pair: token counts, IDENTICAL/DIFFERENT, and whether line numbers match."""
import subprocess, sys, re
def toks(path):
    out = subprocess.run(["clang", "-cc1", "-x", "c", "-std=c11", "-dump-raw-tokens", path],
                         capture_output=True, text=True).stderr
    res = []
    for line in out.splitlines():
        kind = line.split(" ", 1)[0]
        i = line.find("'"); mm = list(re.finditer(r"'\s+Loc=<", line)); j = mm[-1].start() if mm else -1
        if i < 0 or j < 0:
            raise SystemExit(f"unparsed: {line!r}")
        spell = line[i + 1:j]
        m = re.search(r"Loc=<.*:(\d+):(\d+)>", line)
        ln = int(m.group(1))
        if kind in ("comment", "eof", "eod"):
            continue
        if kind == "unknown" and spell.replace("\\n", "").replace("\\t", "").strip() == "":
            continue
        res.append((kind, spell, ln))
    return res
old_root, new_root = sys.argv[1], sys.argv[2]
rc = 0
for pair in sys.argv[3:]:
    o, n = pair.split(":")
    a, b = toks(f"{old_root}/{o}"), toks(f"{new_root}/{n}")
    same = [(k, s) for k, s, _ in a] == [(k, s) for k, s, _ in b]
    lines = [l for *_, l in a] == [l for *_, l in b]
    print(f"{o} -> {n}: tokens {len(a)} vs {len(b)}: {'IDENTICAL' if same else 'DIFFERENT'}; same lines: {lines}")
    if not same or not a:
        rc = 1
sys.exit(rc)
