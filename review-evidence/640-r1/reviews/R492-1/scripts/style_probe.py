#!/usr/bin/env python3
"""Apply the repository's sentence-length analyser to pages it does not list.

Usage: style_probe.py <repo> <page>...  Prints per-page sentence findings (over 10 words)
and the lines of each over-long sentence; informational, the gate does not list these pages.
"""
import importlib.util, sys
from pathlib import Path
repo = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("cds", repo / "scripts" / "check_doc_style.py")
m = importlib.util.module_from_spec(spec); sys.modules["cds"] = m; spec.loader.exec_module(m)
for page in sys.argv[2:]:
    text = (repo / page).read_text()
    f = [x for x in m.analyze(text) if x.reason.startswith("sentence")]
    print(f"{page}: {len(f)} sentence(s) over {m.MAX_SENTENCE_WORDS} words")
    for x in f:
        print(f"  {page}:{x.line}: {x.reason}: {x.text[:110]}")
