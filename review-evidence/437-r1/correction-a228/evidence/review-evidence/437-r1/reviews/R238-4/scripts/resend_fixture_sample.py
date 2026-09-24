#!/usr/bin/env python3
"""Re-send a sample of the fixture's recorded requests to GitHub unchanged.

Usage: resend_fixture_sample.py <repo> <out.json>
Sample: every `r86_5` shape, every #516 shape, every family-two shape, both
`github_only` shapes, and every 12th remaining shape. Each recorded
`request_bytes` is POSTed byte-for-byte (`gh api POST markdown --input -`);
the fresh response is compared with the recorded one (bytes, and headings
read with the standard-library parser).
"""
import hashlib, html.parser, json, subprocess, sys
from pathlib import Path
repo, out = Path(sys.argv[1]), Path(sys.argv[2])
shapes = json.loads((repo / "scripts/gen_toc_shapes.json").read_text())["shapes"]
class H(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True); self.out = []; self.cur = None
    def handle_starttag(self, tag, attrs):
        if tag in ("h1","h2","h3","h4","h5","h6") and self.cur is None: self.cur = [int(tag[1]), ""]
    def handle_endtag(self, tag):
        if self.cur and tag == f"h{self.cur[0]}":
            self.out.append([self.cur[0], " ".join(self.cur[1].split())]); self.cur = None
    def handle_data(self, d):
        if self.cur is not None: self.cur[1] += d
def heads(h):
    p = H(); p.feed(h); p.close(); return p.out
rest = [s for s in shapes if not (s.get("r86_5") or s["set"] in ("#516", "family two") or s.get("github_only"))]
sample = [s for s in shapes if s.get("r86_5") or s["set"] in ("#516", "family two") or s.get("github_only")] + rest[::12]
rows, same_bytes, same_heads = [], 0, 0
for s in sample:
    r = subprocess.run(["gh", "api", "--method", "POST", "markdown", "--input", "-"],
                       input=s["request_bytes"].encode(), capture_output=True, check=True, timeout=60)
    fresh = r.stdout.decode()
    b = fresh == s["response_bytes"]; h = heads(fresh) == s["headings"]
    same_bytes += b; same_heads += h
    rows.append({"name": s["name"], "set": s["set"], "fresh_sha256": hashlib.sha256(fresh.encode()).hexdigest(),
                 "recorded_sha256": s["response_sha256"], "bytes_equal": b, "headings_equal": h,
                 "fresh_headings": heads(fresh), "recorded_headings": s["headings"]})
    if not (b and h):
        print("DIFF", s["name"], "bytes_equal", b, "headings_equal", h)
out.write_text(json.dumps({"sampled": len(sample), "bytes_equal": same_bytes, "headings_equal": same_heads, "rows": rows}, indent=1))
print(f"sampled {len(sample)}: response bytes identical {same_bytes}, headings identical {same_heads}")
