#!/usr/bin/env python3
"""Check every hash row of the page's "B7: artifact hashes" section against the published packet.

Usage: check_hash_rows.py <repo> <page-head> <evidence-commit>
Raw rows: size and SHA-256 must appear as a raw-file record in some runs/**/events.jsonl
(first 19 rows) and in author/RAW-ARTIFACTS.json (all 26). Evidence rows: bytes and SHA-256 of
the published blob at the pin; for the masked tools, the original_sha256 in author/redaction.json,
and the published blob must equal the MANIFEST's published_sha256. Also checks that the two
masking commits changed no cited file except the masked tools, and that in RAW-ARTIFACTS.json
and events.jsonl the masking changed only the capture file's name.
"""
import hashlib
import json
import re
import subprocess
import sys

repo, head, pin = sys.argv[1:4]
EV = "review-evidence/629-b7-r1"
A = f"{EV}/author"
MASKS = ["d36de704456713fb89b39a59151b72015fa00c6d", "c6ad37e7d9163b5a85aef935a7d8e7f7f6686f7f"]
FIRST = "95448218b342c084efa28ac266ae9415bff4ecce"


def git(*a, binary=False):
    out = subprocess.run(["git", "-C", repo, *a], check=True, capture_output=True).stdout
    return out if binary else out.decode()


import os
_pf = os.environ.get("PAGE_FILE")  # mutation probes: read the page from a file instead of the head
page = (open(_pf).read() if _pf else git("show", f"{head}:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md")).split("\n")
start = page.index("### B7: artifact hashes")
end = next((i for i in range(start + 1, len(page)) if page[i].startswith("## ")), len(page))
sec = page[start:end]
row_re = re.compile(r"^\| (.+?) \| ([0-9,]+) \| `([0-9a-f]{64})` \|$")
raw_rows, ev_rows, table = [], [], 0
for ln, l in enumerate(sec, start + 1):
    if l.startswith("| Raw file |"):
        table = 1
    elif l.startswith("| Evidence file |"):
        table = 2
    m = row_re.match(l)
    if m and table:
        (raw_rows if table == 1 else ev_rows).append((ln, m.group(1), int(m.group(2).replace(",", "")), m.group(3)))
print(f"rows: raw={len(raw_rows)} evidence={len(ev_rows)} total={len(raw_rows) + len(ev_rows)}")

problems = 0
tree = [n for n in git("ls-tree", "-r", "--name-only", pin, A).split("\n") if n]
ev_records = {}
for n in tree:
    if n.endswith("events.jsonl"):
        for l in git("show", f"{pin}:{n}").split("\n"):
            if '"raw-file"' in l:
                r = json.loads(l)
                ev_records.setdefault((r["bytes"], r["sha256"]), []).append(n)
raw_art = json.loads(git("show", f"{pin}:{A}/RAW-ARTIFACTS.json"))
ra = {(f["bytes"], f["sha256"]): f["file"] for f in raw_art["files"]}
for i, (ln, name, b, h) in enumerate(raw_rows):
    in_ev = (b, h) in ev_records
    in_ra = (b, h) in ra
    want_ev = i < 19
    ok = in_ra and (in_ev == want_ev)
    problems += not ok
    print(f"{'ok ' if ok else 'BAD'} raw :{ln} {name[:40]!r} events.jsonl={in_ev} RAW-ARTIFACTS={in_ra} expect_events={want_ev}")

man = {e["file"]: e for e in json.loads(git("show", f"{pin}:{EV}/MANIFEST.json"))}
red = json.loads(git("show", f"{pin}:{A}/redaction.json"))["files"]
masked_cited = []
for ln, name, b, h in ev_rows:
    path = re.match(r"`([^`]+)`", name).group(1)
    blob = git("show", f"{pin}:{A}/{path}", binary=True)
    pub = hashlib.sha256(blob).hexdigest()
    me = man.get(f"author/{path}")
    man_ok = me is not None and me["published_sha256"] == pub
    if pub == h and len(blob) == b:
        kind = "published"
        ok = man_ok
    else:
        kind = "original(redaction.json)"
        # chain: as run (redaction.json original) -> lane packet (redaction.json retained ==
        # MANIFEST original) -> published (MANIFEST published == blob at the pin). The as-run byte
        # count is not recoverable from the published blobs; it is reported, not checked.
        ok = (path in red and red[path]["original_sha256"] == h and man_ok
              and me["original_sha256"] == red[path]["retained_sha256"])
        masked_cited.append(path)
    problems += not ok
    print(f"{'ok ' if ok else 'BAD'} ev  :{ln} {path} bytes={b} match={kind} manifest_published_ok={man_ok}")
print(f"rows matched via original_sha256 (masked tools): {masked_cited}")
if sorted(masked_cited) != ["tools/grade_b7.py", "tools/run_b7.py"]:
    problems += 1
    print("BAD: the masked cited tools are not exactly run_b7.py and grade_b7.py")

cited = {f"{A}/" + re.match(r"`([^`]+)`", r[1]).group(1) for r in ev_rows}
for c in MASKS:
    changed = set(git("show", "--format=", "--name-only", c).split())
    hit = sorted(p.split("author/")[1] for p in changed & cited)
    print(f"{c[:8]} changed {len(changed)} files; cited among them: {hit}")
    if hit != ["tools/grade_b7.py", "tools/run_b7.py"]:
        problems += 1
        print("BAD: a masking commit changed a cited file other than the two masked tools")
c2 = MASKS[1]
changed = [p for p in git("show", "--format=", "--name-only", c2).split() if not p.endswith("MANIFEST.json")]
print(f"c6ad37e7 files excluding MANIFEST.json: {len(changed)}")
name_re = re.compile(r"cap-all-[^\"/ ]*ch\.raw")
for p in changed:
    if p.endswith("events.jsonl") or p.endswith("RAW-ARTIFACTS.json") or p.endswith("-lock.txt"):
        before = git("show", f"{MASKS[0]}:{p}")
        after = git("show", f"{c2}:{p}")
        same = name_re.sub("CAPALL", before) == name_re.sub("CAPALL", after)
        problems += not same
        print(f"{'ok ' if same else 'BAD'} only the capture name changed: {p}")
# pre-masking: raw records unchanged since first publication
fr = json.loads(git("show", f"{FIRST}:{A}/RAW-ARTIFACTS.json"))
same_set = {(f["bytes"], f["sha256"]) for f in fr["files"]} == set(ra)
problems += not same_set
print(f"{'ok ' if same_set else 'BAD'} RAW-ARTIFACTS (bytes, sha256) set identical at 95448218 and the pin")
print("RESULT", "0 problems" if problems == 0 else f"{problems} problems")
sys.exit(0 if problems == 0 else 1)
