#!/usr/bin/env python3
"""R635-1: bind the page's evidence-file and raw-capture hash tables to the published packet, check the packet's
MANIFEST.json (published vs redacted) and author MANIFEST.sha256, and list the console polls that took more than
0.15 s (firmware activity after each ACMP change) against each slip's interval.
usage: python3 -I check_evidence_hashes.py <evidence_dir (review-evidence/645-b17-r1)> <findings_page>"""
import hashlib, json, re, sys
E, PAGE = sys.argv[1], sys.argv[2]
A = f"{E}/author"
page = open(PAGE).read()
page = page[page.index("## Dev 5603c353, 2026-10-15: lane B17"):]  # the B17 section only
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
for m in re.finditer(r"^\| `([^`]+)`[^|]*\| ([\d,]+) \| `([0-9a-f]{64})` \|$", page, re.M):
    f, size, h = m.group(1), int(m.group(2).replace(",", "")), m.group(3)
    try:
        d = open(f"{A}/{f}", "rb").read()
        print(f"page-evidence {f}: bytes {'OK' if len(d) == size else 'MISMATCH'} sha {'OK' if hashlib.sha256(d).hexdigest() == h else 'MISMATCH'}")
    except FileNotFoundError:
        print(f"page-evidence {f}: not in packet")
for c in range(1, 11):
    ev = [json.loads(x) for x in open(f"{A}/cycles/c{c:02d}/events.jsonl")]
    ce = [e for e in ev if e["kind"] == "capture-end"][0]
    row = f"| c{c:02d} | `{ce['file']}` | {ce['bytes']:,} | `{ce['sha256']}` |"
    print(f"raw-capture c{c:02d}: page row matches capture-end event: {row in page}; remote_equal {ce['remote_equal']} removed {ce['removed_from_tap']}")
man = json.load(open(f"{E}/MANIFEST.json"))
bad = [e["file"] for e in man if sha(f"{E}/{e['file']}") != e["published_sha256"]]
red = [e["file"] for e in man if e["original_sha256"] != e["published_sha256"] or e.get("path_redacted")]
print(f"MANIFEST.json: {len(man)} entries, published-hash mismatches {bad}, redacted on publication {red}")
for c in range(1, 11):
    ev = [json.loads(x) for x in open(f"{A}/cycles/c{c:02d}/events.jsonl")]
    tb = [e for e in ev if e["kind"] == "bind-time"][0]["t_bind_local"]
    tu = [e for e in ev if e["kind"] == "unbind"][0]["t_cmd_local"]
    s = json.load(open(f"{A}/summary/c{c:02d}.json"))["poll"]["slips"][0]
    po = [json.loads(x) for x in open(f"{A}/cycles/c{c:02d}/poll.jsonl")]
    lp = [(round(r["t0"] - tb, 3), round(r["t1"] - r["t0"], 3)) for r in po if r["t1"] - r["t0"] > 0.15]
    inside = [x for x in lp if s["s_lo"] <= x[0] <= s["s_hi"]]
    print(f"c{c:02d} long polls (start s from bind, duration s) {lp}; unbind at {tu - tb:+.3f}; slip [{s['s_lo']}, {s['s_hi']}] contains a long poll: {bool(inside)}")
