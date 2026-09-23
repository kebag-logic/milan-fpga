#!/usr/bin/env python3
"""Compare walks at several revisions against every recorded GitHub rendering.

Reads the public renderer receipts extracted under ../public-inputs (R237-r1,
R238-r1, the A168 author packet and the A172 correction packet), plus any
extra JSON receipts named on the command line (list of {id, page, html}).
For every unique page it reports the rendered headings, each walk's headings
and a verdict. Walks: base 88e9276b (walk identical at live dev 483a133e),
a172 b5e6c23e, and the lane working tree ("head").

Usage: three_way.py OUT.json [EXTRA_RECEIPTS.json ...]
"""
import glob
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path

LANE = Path("$LANES/437-container-paragraph-scopes")
HERE = Path(__file__).resolve().parent.parent
PUB = HERE / "public-inputs" / "review-evidence" / "437-r1"
REVS = {"base": "88e9276b2a220c716f64a843f7e1eb8f9265e896",
        "a172": "b5e6c23e1b9802b5cacbc62db212064d7e429862",
        "head": None}


class Headings(HTMLParser):
    """Collect (level, text) of every h1..h6 element in rendered HTML."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.out, self.level, self.buf = [], 0, []

    def handle_starttag(self, tag: str, attrs: list) -> None:
        if len(tag) == 2 and tag[0] == "h" and tag[1] in "123456":
            self.level, self.buf = int(tag[1]), []

    def handle_endtag(self, tag: str) -> None:
        if self.level and tag == f"h{self.level}":
            self.out.append((self.level, " ".join("".join(self.buf).split())))
            self.level = 0

    def handle_data(self, data: str) -> None:
        if self.level:
            self.buf.append(data)


def rendered(html: str) -> list:
    p = Headings()
    p.feed(html)
    p.close()
    return [list(h) for h in p.out]


def load(name: str, rev: str | None, tmp: Path):
    """Import gen_toc.py at REV (or the working tree) under module NAME."""
    if rev is None:
        src = (LANE / "scripts" / "gen_toc.py").read_text()
    else:
        src = subprocess.run(["git", "-C", str(LANE), "show", f"{rev}:scripts/gen_toc.py"],
                             check=True, capture_output=True, text=True).stdout
    path = tmp / f"{name}_gen_toc.py"
    path.write_text(src)
    spec = importlib.util.spec_from_file_location(f"walk_{name}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod, hashlib.sha256(src.encode()).hexdigest()


def walk_headings(mod, page: str):
    if mod.refusals(page):
        return "REFUSED"
    return [[lvl, " ".join(mod.strip_md(raw).split())] for lvl, raw, _ in mod.headings(page)]


def receipts(extra: list[str]) -> list[dict]:
    rows = []
    def add(src, rid, page, html):
        rows.append({"source": src, "id": rid, "page": page, "html": html})
    for x in json.load(open(PUB / "reviews/R237-1/renderer-responses.json")):
        add("R237 renderer", x["id"], x["request"]["text"], x["html"])
    for x in json.load(open(PUB / "reviews/R237-1/published-replay-responses.json")):
        add("R237 replay", x["id"], x["request"]["text"], x["html"])
    cache = json.load(open(PUB / "reviews/R238-1/receipts/renderer-cache.json"))
    for key, x in cache.items():
        add("R238 cache", key[:12], json.loads(x["request"])["text"], x["response"])
    for key, x in json.load(open(PUB / "author/renderer-cache.json")).items():
        add("A168 cache", key[:12], x["request"]["text"], x["html"])
    for f in sorted(glob.glob(str(PUB / "correction-a172/renderer/*.json"))):
        x = json.load(open(f))
        add("A172 renderer", Path(f).stem[:12], x["request"]["text"], x["html"])
    for f in extra:
        for x in json.load(open(f)):
            add(Path(f).stem, x["id"], x["page"], x.get("html", x.get("response_bytes")))
    return rows


def main() -> int:
    out_path, extra = sys.argv[1], sys.argv[2:]
    with tempfile.TemporaryDirectory(prefix="a184.walks.") as tmp:
        walks = {n: load(n, r, Path(tmp)) for n, r in REVS.items()}
        pages: dict[str, dict] = {}
        for r in receipts(extra):
            g = rendered(r["html"])
            entry = pages.setdefault(r["page"], {"page": r["page"], "ids": [], "github": g,
                                                 "github_variants": []})
            entry["ids"].append(f'{r["source"]}:{r["id"]}')
            if g != entry["github"] and g not in entry["github_variants"]:
                entry["github_variants"].append(g)
        for e in pages.values():
            for n, (mod, _) in walks.items():
                e[n] = walk_headings(mod, e["page"])
                e[f"{n}_agrees"] = e[n] == e["github"]
        rows = list(pages.values())
        def cls(e):
            if e["github_variants"]:
                return "renderer-inconsistent"
            b, h = e["base_agrees"], e["head_agrees"]
            if b and h:
                return "agree-both"
            if b and not h:
                return "REGRESSION"
            if not b and h:
                return "fixed"
            return "pre-existing-identical" if e["base"] == e["head"] else "pre-existing-changed"
        for e in rows:
            e["class"] = cls(e)
            e["a172_class"] = ("REGRESSION" if e["base_agrees"] and not e["a172_agrees"] else "")
        summary = {"walk_sha256": {n: s for n, (_, s) in walks.items()},
                   "revisions": REVS, "unique_pages": len(rows),
                   "receipt_rows": sum(len(e["ids"]) for e in rows)}
        for key in ("class", "a172_class"):
            counts = {}
            for e in rows:
                counts[e[key]] = counts.get(e[key], 0) + 1
            summary[f"{key}_counts"] = counts
        json.dump({"summary": summary, "rows": rows}, open(out_path, "w"), indent=1)
        print(json.dumps(summary, indent=1))
        for e in rows:
            if e["class"] in ("REGRESSION", "pre-existing-changed", "renderer-inconsistent"):
                print(e["class"], e["ids"][:2], repr(e["page"])[:140])
                print("   github", e["github"], "base", e["base"], "a172", e["a172"], "head", e["head"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
