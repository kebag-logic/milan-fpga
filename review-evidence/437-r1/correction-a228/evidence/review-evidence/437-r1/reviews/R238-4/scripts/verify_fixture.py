#!/usr/bin/env python3
"""Independent check of scripts/gen_toc_shapes.json at a checkout.

Usage: verify_fixture.py <repo> <base-rev> <out.json>
Run with an interpreter that has the PR's lock installed.

Per shape: request/response SHA-256, request JSON identity (context, gfm, page),
recorded headings re-read from the response with the STANDARD LIBRARY parser
(not the PR's html5lib path), the head walk's rendered headings, and the BASE
walk's headings (gen_toc.py at <base-rev>, loaded from git into a temp dir).
Agreement at the base is judged on (level, text with Markdown stripped and
blanks collapsed); head agreement uses the head's rendered text.
"""
import hashlib, html.parser, importlib.util, json, subprocess, sys, tempfile
from pathlib import Path

repo, base_rev, out = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
sys.path.insert(0, str(repo / "scripts"))
import gen_toc as head  # noqa: E402

class H(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True); self.out = []; self.cur = None; self.depth = 0
    def handle_starttag(self, tag, attrs):
        if tag in ("h1","h2","h3","h4","h5","h6") and self.cur is None:
            self.cur = [int(tag[1]), ""]
    def handle_endtag(self, tag):
        if self.cur and tag == f"h{self.cur[0]}":
            self.out.append([self.cur[0], " ".join(self.cur[1].split())]); self.cur = None
    def handle_data(self, data):
        if self.cur is not None: self.cur[1] += data

def std_headings(html):
    p = H(); p.feed(html); p.close(); return p.out

tmp = Path(tempfile.mkdtemp(prefix="basewalk."))
for name in ("gen_toc.py", "gen_toc_guards.py"):
    blob = subprocess.run(["git", "-C", str(repo), "show", f"{base_rev}:scripts/{name}"],
                          capture_output=True, check=False)
    if blob.returncode == 0:
        (tmp / name).write_bytes(blob.stdout)
spec = importlib.util.spec_from_file_location("gen_toc_base", tmp / "gen_toc.py")
sys.path.insert(0, str(tmp))
base = importlib.util.module_from_spec(spec); spec.loader.exec_module(base)

def norm(t): return " ".join(head.strip_md(t).split())

shapes = json.loads((repo / "scripts/gen_toc_shapes.json").read_text())["shapes"]
rows, tally = [], {"n": len(shapes), "hash_bad": 0, "request_bad": 0, "std_vs_recorded_bad": 0,
                   "head_disagree": 0, "base_disagree": 0, "regressions": 0, "fixed": 0,
                   "github_only": 0}
for s in shapes:
    rq, rs = s["request_bytes"].encode(), s["response_bytes"].encode()
    hash_ok = (hashlib.sha256(rq).hexdigest() == s["request_sha256"]
               and hashlib.sha256(rs).hexdigest() == s["response_sha256"])
    req_ok = json.loads(rq) == {"context": "kebag-logic/milan-fpga", "mode": "gfm", "text": s["page"]}
    std = std_headings(s["response_bytes"])
    want = [list(h) for h in s["headings"]]
    for extra in s.get("github_only", {}).get("headings", []):
        want.remove(list(extra))
    got_head = [list(h) for h in head.rendered_headings(s["page"])]
    try:
        got_base = [[lvl, norm(raw)] for lvl, raw, _ in base.headings(s["page"])]
    except Exception as exc:  # the base walk may refuse
        got_base = f"error: {exc!r}"
    want_norm = [[l, norm(t)] for l, t in want]
    head_ok = got_head == want
    base_ok = got_base == want_norm
    tally["hash_bad"] += not hash_ok; tally["request_bad"] += not req_ok
    tally["std_vs_recorded_bad"] += std != [list(h) for h in s["headings"]]
    tally["head_disagree"] += not head_ok; tally["base_disagree"] += not base_ok
    tally["regressions"] += base_ok and not head_ok; tally["fixed"] += head_ok and not base_ok
    tally["github_only"] += bool(s.get("github_only"))
    rows.append({"name": s["name"], "set": s["set"], "hash_ok": hash_ok, "request_ok": req_ok,
                 "std_headings": std, "recorded": s["headings"], "head": got_head,
                 "base": got_base, "head_ok": head_ok, "base_ok": base_ok})
out.write_text(json.dumps({"tally": tally, "rows": rows}, indent=1))
print(json.dumps(tally))
for r in rows:
    if not (r["hash_ok"] and r["request_ok"] and r["head_ok"]) or r["std_headings"] != r["recorded"]:
        print("ATTN", r["name"], r["hash_ok"], r["request_ok"], r["head_ok"], r["std_headings"], r["recorded"], r["head"])
