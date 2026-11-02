#!/usr/bin/env python3
"""usage: classify.py <out dir> ... Scratch only: count each tree's runs by what its log shows, and print each CLEANUP FAILED message."""
import re, sys, collections
from pathlib import Path
for out in map(Path, sys.argv[1:]):
    for tree in sorted(p for p in out.iterdir() if p.is_dir()):
        c = collections.Counter(); msgs = []
        for rcf in sorted(tree.glob("*.rc")):
            text = rcf.with_suffix(".log").read_text(errors="replace")
            rc = rcf.read_text().strip()
            # Judge the exception that ended the run, never a message a control printed on purpose.
            ends = re.findall(r"^(?:AssertionError|RuntimeError|subprocess\.TimeoutExpired)[^\n]*", text, re.M)
            last = ends[-1] if ends else ""
            if rc == "0": k = "pass"
            elif "CLEANUP FAILED" in last or (last.startswith("AssertionError") and "REFUSED: process ownership: CLEANUP FAILED" in text):
                k = "CLEANUP FAILED"; msgs.append((rcf.stem, re.findall(r"CLEANUP FAILED[^\n]*", text)[-1][:520]))
            elif "TimeoutExpired" in last: k = "fixture 12 s bound (TimeoutExpired)"
            elif "missing boundary" in last: k = "fixture handshake bound (missing boundary)"
            elif "TIMEOUT  omega" in text or "TIMEOUT  alpha" in text: k = "fixture 0.5 s SUITE_TIMEOUT in ordinary(timeout)"
            elif last: k = "assertion: " + last[:110]
            else: k = "other rc " + rc
            c[k] += 1
        print(f"{out.name}/{tree.name}: runs {sum(c.values())} {dict(c)}")
        for stem, msg in msgs: print("   ", stem, msg)
