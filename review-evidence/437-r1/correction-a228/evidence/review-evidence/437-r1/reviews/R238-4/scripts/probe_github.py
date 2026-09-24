#!/usr/bin/env python3
"""Render probe pages through GitHub's Markdown API and compare with the pin.

Usage: probe_github.py <repo> <pages.json> <out.json> [modes, default gfm,markdown]
<pages.json> is a list of {"name", "page"}. For every page and mode the exact
request and response bytes and their SHA-256 are kept, the headings GitHub
rendered are read with the standard library parser (level, text, and the
`user-content-` anchor id when the mode emits one), and compared with
gen_toc.rendered_headings() and gen_toc.headings() anchors at <repo>.
Requests go through `gh api --method POST markdown --input -` (no repository
state is written). Run with an interpreter that has the PR's lock installed.
"""
import datetime, hashlib, html.parser, json, subprocess, sys
from pathlib import Path

repo, pages_path, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
modes = (sys.argv[4] if len(sys.argv) > 4 else "gfm,markdown").split(",")
sys.path.insert(0, str(repo / "scripts"))
import gen_toc  # noqa: E402

class H(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True); self.out = []; self.cur = None; self.pending = None
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("h1","h2","h3","h4","h5","h6") and self.cur is None:
            self.cur = [int(tag[1]), "", None]
        elif tag == "a" and (a.get("id") or "").startswith("user-content-") and "anchor" in (a.get("class") or ""):
            if self.out and self.out[-1][2] is None:
                self.out[-1][2] = a["id"][len("user-content-"):]
    def handle_endtag(self, tag):
        if self.cur and tag == f"h{self.cur[0]}":
            self.cur[1] = " ".join(self.cur[1].split()); self.out.append(self.cur); self.cur = None
    def handle_data(self, data):
        if self.cur is not None: self.cur[1] += data

def gh_render(text, mode):
    req = json.dumps({"context": "kebag-logic/milan-fpga", "mode": mode, "text": text},
                     separators=(",", ":"))
    r = subprocess.run(["gh", "api", "--method", "POST", "markdown", "--input", "-"],
                       input=req.encode(), capture_output=True, timeout=60)
    if r.returncode != 0:
        raise SystemExit(f"gh api failed: {r.stderr.decode()}")
    return req, r.stdout.decode("utf-8")

rows = []
for p in json.loads(pages_path.read_text()):
    local = [list(h) for h in gen_toc.rendered_headings(p["page"])]
    anchors = [a for _, _, a in gen_toc.headings(p["page"])]
    row = {"name": p["name"], "page": p["page"], "local": local, "local_anchors": anchors}
    for mode in modes:
        req, resp = gh_render(p["page"], mode)
        h = H(); h.feed(resp); h.close()
        row[mode] = {"request_bytes": req, "request_sha256": hashlib.sha256(req.encode()).hexdigest(),
                     "response_bytes": resp, "response_sha256": hashlib.sha256(resp.encode()).hexdigest(),
                     "recorded_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
                     "headings": [[l, t] for l, t, _ in h.out],
                     "anchors": [a for _, _, a in h.out]}
        row[mode]["agrees"] = row[mode]["headings"] == local
    rows.append(row)
    flags = " ".join(f"{m}={'ok' if row[m]['agrees'] else 'DIFF'}" for m in modes)
    print(f"{flags}  {p['name']}: local={local}", *(f"{m}={row[m]['headings']}" for m in modes if not row[m]['agrees']))
out.write_text(json.dumps(rows, indent=1))
