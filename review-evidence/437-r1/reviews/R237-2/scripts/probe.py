#!/usr/bin/env python3
"""R237-2 reviewer probe: base walk, head walk and GitHub's gfm rendering.

Usage:
    probe.py walk   --repo R --base REV --head REV CORPUS.json
    probe.py render --repo R --base REV --head REV CORPUS.json OUT.json

CORPUS.json is a list of {"name": str, "page": str}. `walk` prints the
headings each walk lists. `render` also POSTs each page to GitHub's Markdown
API (mode gfm, context kebag-logic/milan-fpga) through `gh api`, records the
exact request and response bytes with SHA-256, extracts the rendered heading
elements, and classifies each page:
    agree-both, fix (base disagrees, head agrees), REGRESSION (base agrees,
    head disagrees), both-disagree-same, both-disagree-differently.
For a disagreement the direction is ESCAPE when the walk lists a heading the
rendering lacks, WITHHOLD when it lacks one the rendering has.
The walks are loaded from `git show REV:scripts/gen_toc.py`, never from a
working tree, so the probe reads committed bytes only.
"""
import argparse
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import time
from html.parser import HTMLParser
from pathlib import Path

CONTEXT = "kebag-logic/milan-fpga"


def load_walk(repo: str, rev: str, tag: str):
    src = subprocess.run(["git", "-C", repo, "show", f"{rev}:scripts/gen_toc.py"],
                         check=True, capture_output=True).stdout
    tmp = Path(tempfile.mkdtemp(prefix=f"r237walk.{tag}."))
    path = tmp / "gen_toc.py"
    path.write_bytes(src)
    spec = importlib.util.spec_from_file_location(f"gen_toc_{tag}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod, hashlib.sha256(src).hexdigest()


class Headings(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.found, self.level, self.text = [], 0, ""

    def handle_starttag(self, tag, attrs):
        if len(tag) == 2 and tag[0] == "h" and tag[1] in "123456":
            self.level, self.text = int(tag[1]), ""

    def handle_endtag(self, tag):
        if self.level and tag == f"h{self.level}":
            self.found.append([self.level, " ".join(self.text.split())])
            self.level = 0

    def handle_data(self, data):
        if self.level:
            self.text += data


def rendered(html: str) -> list:
    p = Headings()
    p.feed(html)
    p.close()
    return p.found


def request_bytes(page: str) -> bytes:
    body = json.dumps({"context": CONTEXT, "mode": "gfm", "text": page},
                      sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    body = body.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    return body.encode("ascii")


def render(page: str) -> tuple[bytes, bytes]:
    req = request_bytes(page)
    for attempt in range(4):
        r = subprocess.run(["gh", "api", "-X", "POST", "/markdown", "--input", "-"],
                           input=req, capture_output=True)
        if r.returncode == 0:
            return req, r.stdout
        time.sleep(2 + attempt * 3)
    raise SystemExit(f"render failed: {r.stderr.decode(errors='replace')}")


def walk_headings(mod, page: str) -> list:
    return [[lvl, raw] for lvl, raw, _ in mod.headings(page)]


def classify(rend, base, head) -> str:
    b, h = base == rend, head == rend
    if b and h:
        return "agree-both"
    if h:
        return "fix"
    if b:
        return "REGRESSION"
    return "both-disagree-same" if base == head else "both-disagree-differently"


def direction(rend, walk) -> str:
    extra = [x for x in walk if x not in rend]
    missing = [x for x in rend if x not in walk]
    parts = []
    if extra:
        parts.append(f"ESCAPE lists {extra}")
    if missing:
        parts.append(f"WITHHOLD omits {missing}")
    return "; ".join(parts) or ("order" if walk != rend else "")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=("walk", "render"))
    ap.add_argument("--repo", required=True)
    ap.add_argument("--base", required=True)
    ap.add_argument("--head", required=True)
    ap.add_argument("corpus")
    ap.add_argument("out", nargs="?")
    a = ap.parse_args()
    base, bsha = load_walk(a.repo, a.base, "base")
    head, hsha = load_walk(a.repo, a.head, "head")
    corpus = json.loads(Path(a.corpus).read_text())
    rows = []
    for item in corpus:
        page = item["page"]
        row = {"name": item["name"], "page": page,
               "base_walk": walk_headings(base, page),
               "head_walk": walk_headings(head, page)}
        if a.mode == "render":
            req, resp = render(page)
            html = resp.decode("utf-8")
            row.update({"request_bytes": req.decode("ascii"),
                        "request_sha256": hashlib.sha256(req).hexdigest(),
                        "response_bytes": html,
                        "response_sha256": hashlib.sha256(resp).hexdigest(),
                        "recorded_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                        "rendered": rendered(html)})
            row["class"] = classify(row["rendered"], row["base_walk"], row["head_walk"])
            row["base_direction"] = direction(row["rendered"], row["base_walk"])
            row["head_direction"] = direction(row["rendered"], row["head_walk"])
            print(f"{row['class']:26} {item['name']} | R={row['rendered']} "
                  f"B={row['base_walk']} H={row['head_walk']} {row['head_direction']}")
        else:
            flag = "DIFF" if row["base_walk"] != row["head_walk"] else "same"
            print(f"{flag} {item['name']} | B={row['base_walk']} H={row['head_walk']}")
        rows.append(row)
    if a.out:
        Path(a.out).write_text(json.dumps({"base": a.base, "base_gen_toc_sha256": bsha,
                                           "head": a.head, "head_gen_toc_sha256": hsha,
                                           "rows": rows}, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
