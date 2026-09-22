#!/usr/bin/env python3
"""R226-2: materialize closer-only mutant copies of a tree's scripts/ for e2e.

Usage: python3 -B make_mutant_dirs.py <tree-root> <outroot> <tag>
Writes <outroot>/<tag>-<id>/scripts for R15 (div), R16 (title), X04 (xmp):
the single edit at the `_type_1_end` closer site used by R226-1, applied to a
copy; each edit must match exactly once. Prints the SHA-256 of each mutated
gen_toc.py and of the unmodified input.
"""
import hashlib
import shutil
import sys
from pathlib import Path

src = Path(sys.argv[1]).resolve() / "scripts"
root = Path(sys.argv[2]).resolve()
tag = sys.argv[3]
CLOSE = 'return bool(re.search(r"</(?:%s)>" % "|".join(RAW_HTML_TAGS), line, ASCII_FOLD))'
print("input gen_toc.py sha256", hashlib.sha256((src / "gen_toc.py").read_bytes()).hexdigest())
for mid, name in (("R15", "div"), ("R16", "title"), ("X04", "xmp")):
    dst = root / f"{tag}-{mid}" / "scripts"
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__"))
    text = (dst / "gen_toc.py").read_text()
    assert text.count(CLOSE) == 1
    text = text.replace(CLOSE, CLOSE.replace('"|".join(RAW_HTML_TAGS)',
                                             f'"|".join(RAW_HTML_TAGS + ("{name}",))'))
    (dst / "gen_toc.py").write_text(text)
    print(dst, "gen_toc.py sha256", hashlib.sha256(text.encode()).hexdigest())
