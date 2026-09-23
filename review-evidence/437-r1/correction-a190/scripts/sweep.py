#!/usr/bin/env python3
"""Classify corpora: base walk, candidate walk, GitHub rendering.

Usage:
  sweep.py need   CORPUS.json... > NEED.json   pages where the walks differ and no rendering is cached
  sweep.py report CORPUS.json...               classes against cached renderings
Env: CAND=module:function (headings), BASE_REV (default 483a133e), CACHES (colon list).
"""
import importlib, importlib.util, json, os, subprocess, sys, tempfile
from pathlib import Path

REPO = "$LANES/437-container-paragraph-scopes"
PKT = Path("$REVIEWS/437-a190-packet")


def load_rev(rev, tag):
    src = subprocess.run(["git", "-C", REPO, "show", f"{rev}:scripts/gen_toc.py"],
                         check=True, capture_output=True).stdout
    d = Path(tempfile.mkdtemp(prefix=f"walk.{tag}."))
    (d / "gen_toc.py").write_bytes(src)
    spec = importlib.util.spec_from_file_location(f"gen_toc_{tag}", d / "gen_toc.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def walk_fn(mod_or_fn):
    f = mod_or_fn.headings if hasattr(mod_or_fn, "headings") else mod_or_fn
    return lambda page: [[l, r] for l, r, _ in f(page)]


def caches():
    out = {}
    pub = PKT / "work/public-cache.json"
    if pub.exists():
        out.update(json.loads(pub.read_text())["pages"])
    for c in os.environ.get("CACHES", str(PKT / "work/render-cache.jsonl")).split(":"):
        p = Path(c)
        if p.exists():
            for line in p.read_text().splitlines():
                if line.strip():
                    row = json.loads(line)
                    out[row["page"]] = row["headings"]
    return out


def corpus(paths):
    pages = []
    for p in paths:
        for item in json.loads(Path(p).read_text()):
            pages.append(item["page"] if isinstance(item, dict) else item)
    return list(dict.fromkeys(pages))


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
    mode, paths = sys.argv[1], sys.argv[2:]
    base = walk_fn(load_rev(os.environ.get("BASE_REV", "483a133ed08867ea0d300d2b4a027b5b48a4282f"), "base"))
    sys.path.insert(0, str(PKT / "work/prototype"))
    modname, fname = os.environ.get("CAND", "proto_a:headings").split(":")
    cand = walk_fn(getattr(importlib.import_module(modname), fname))
    cache = caches()
    pages = corpus(paths)
    if mode == "need":
        need = [p for p in pages if p not in cache and base(p) != cand(p)]
        print(json.dumps(need))
        print(f"{len(pages)} pages; {sum(base(p) != cand(p) for p in pages)} differ; {len(need)} need rendering",
              file=sys.stderr)
        return 0
    counts, rows = {}, []
    for p in pages:
        b, h = base(p), cand(p)
        if p not in cache:
            c = "same-unrendered" if b == h else "DIFF-UNRENDERED"
        else:
            c = classify(cache[p], b, h)
        counts[c] = counts.get(c, 0) + 1
        rows.append({"page": p, "class": c, "rendered": cache.get(p), "base": b, "head": h})
    print(json.dumps(counts, sort_keys=True))
    show = int(os.environ.get("SHOW", "20"))
    for r in rows:
        if r["class"] in ("REGRESSION", "DIFF-UNRENDERED") and show > 0:
            show -= 1
            print(f"  {r['class']} {r['page']!r}\n     R={r['rendered']} B={r['base']} H={r['head']}")
    out = os.environ.get("OUT")
    if out:
        Path(out).write_text(json.dumps({"counts": counts, "rows": rows}, indent=0) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
