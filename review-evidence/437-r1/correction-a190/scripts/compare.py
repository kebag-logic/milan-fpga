#!/usr/bin/env python3
"""Compare walks against recorded GitHub renderings.

Usage: compare.py CACHE.json [extra_corpus.json ...]
Walks: base (git show REV:scripts/gen_toc.py), and any candidates given by
WALKS env (module:function pairs). Prints class counts per candidate.
"""
import importlib.util, json, subprocess, sys, tempfile, os
from pathlib import Path

REPO = "$LANES/437-container-paragraph-scopes"


def load_rev(rev, tag):
    src = subprocess.run(["git", "-C", REPO, "show", f"{rev}:scripts/gen_toc.py"],
                         check=True, capture_output=True).stdout
    d = Path(tempfile.mkdtemp(prefix=f"walk.{tag}."))
    (d / "gen_toc.py").write_bytes(src)
    spec = importlib.util.spec_from_file_location(f"gen_toc_{tag}", d / "gen_toc.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return lambda page: [[l, r] for l, r, _ in mod.headings(page)]


def classify(rend, base, head):
    b, h = base == rend, head == rend
    if b and h:
        return "agree-both"
    if h:
        return "fix"
    if b:
        return "REGRESSION"
    return "both-disagree-same" if base == head else "both-disagree-differently"


def main():
    cache = json.loads(Path(sys.argv[1]).read_text())["pages"]
    sys.path.insert(0, os.environ.get("PROTO_DIR", "$REVIEWS/437-a190-packet/work/prototype"))
    base = load_rev("483a133ed08867ea0d300d2b4a027b5b48a4282f", "base")
    cands = {"head": load_rev("4741498f3b2b4f67f431037d327c96cf65691278", "head")}
    for spec in os.environ.get("WALKS", "").split():
        mod, fn = spec.split(":")
        m = importlib.import_module(mod)
        f = getattr(m, fn)
        cands[spec] = (lambda f: lambda page: [[l, r] for l, r, _ in f(page)])(f)
    show = int(os.environ.get("SHOW", "20"))
    for name, walk in cands.items():
        counts, regress = {}, []
        for page, rend in cache.items():
            b, h = base(page), walk(page)
            c = classify(rend, b, h)
            counts[c] = counts.get(c, 0) + 1
            if c in ("REGRESSION",):
                regress.append((page, rend, b, h))
        print(f"== {name}: {counts}")
        for page, rend, b, h in regress[:show]:
            print(f"  REGRESSION {page!r}\n     R={rend} B={b} H={h}")


if __name__ == "__main__":
    main()
