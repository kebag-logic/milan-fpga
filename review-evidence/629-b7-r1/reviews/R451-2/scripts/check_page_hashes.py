#!/usr/bin/env python3
"""Check every row of the B7 section's two hash tables against the published packet.

usage: check_page_hashes.py <repo checkout at the PR head> <evidence git dir> <evidence commit>

Raw-file table: the first 19 rows must equal a raw-file record (bytes, SHA-256) in that run's
runs/<case>/events.jsonl (the tone loop: every run's start-event tone_sha256 and its
serve/tone.raw record); the last 7 must equal RAW-ARTIFACTS.json and appear in no events.jsonl.
Evidence-file table: each row must equal the published file's bytes and SHA-256 at the commit
and MANIFEST.json's published_sha256, except the masked tools, which must equal redaction.json's
original_sha256 (bytes are then unverifiable from the packet and are reported as such).
"""
import hashlib, json, re, subprocess, sys
repo, gd, commit = sys.argv[1:4]
P = "review-evidence/629-b7-r1/"
A = P + "author/"
def show(path):
    return subprocess.run(["git", "--git-dir", gd, "show", f"{commit}:{path}"], capture_output=True, check=True).stdout
page = open(f"{repo}/docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md", encoding="utf-8").read()
sec = page[page.index("### B7: artifact hashes"):]
rows = re.findall(r"^\| `([^`]+)`[^|]*\| ([\d,]+) \| `([0-9a-f]{64})` \|$", sec, re.M)
tone = re.search(r"^\| Tone loop \(`b6_tone.py`\) \| ([\d,]+) \| `([0-9a-f]{64})` \|$", sec, re.M)
raw_rows = [("tone", tone.group(1), tone.group(2))] + [r for r in rows if "/" in r[0] and not r[0].startswith(("controls/", "summary/", "identity/", "restore/", "runs/", "tools/"))]
ev_rows = [r for r in rows if r[0].startswith(("controls/", "summary/", "identity/", "restore/", "runs/", "tools/"))]
print(f"rows: raw {len(raw_rows)}, evidence {len(ev_rows)}, total {len(raw_rows)+len(ev_rows)}")
probs = 0
cases = ["a0", "a1", "a2", "b0", "bcrf", "baaf"]
events = {c: [json.loads(l) for l in show(f"{A}runs/{c}/events.jsonl").decode().splitlines() if l.strip()] for c in cases}
rawart = {f["file"]: f for f in json.loads(show(A + "RAW-ARTIFACTS.json"))["files"]}
manifest = {e["file"]: e for e in json.loads(show(P + "MANIFEST.json"))}
red = json.loads(show(A + "redaction.json"))["files"]
for i, (name, nbytes, sha) in enumerate(raw_rows):
    nbytes = int(nbytes.replace(",", ""))
    if name == "tone":
        ok = all(e[0]["tone_sha256"] == sha for e in events.values())
        recs = [r for c in cases for r in events[c] if r.get("kind") == "raw-file" and r["file"] == "serve/tone.raw"]
        ok = ok and len(recs) == 6 and all(r["sha256"] == sha and r["bytes"] == nbytes for r in recs)
        src = "events.jsonl x6 (start tone_sha256 + serve/tone.raw)"
    else:
        case, f = name.split("/", 1)
        recs = [r for r in events[case] if r.get("kind") == "raw-file" and r["file"] == f]
        ra = rawart.get(name)
        if i < 19:
            ok = len(recs) == 1 and recs[0]["sha256"] == sha and recs[0]["bytes"] == nbytes and ra and ra["sha256"] == sha and ra["bytes"] == nbytes
            src = "events.jsonl + RAW-ARTIFACTS.json"
        else:
            ok = not recs and ra is not None and ra["sha256"] == sha and ra["bytes"] == nbytes
            src = "RAW-ARTIFACTS.json only"
    probs += not ok
    print(f"{'OK ' if ok else 'BAD'} raw[{i+1:2}] {name:40} {nbytes:>11} {src}")
for name, nbytes, sha in ev_rows:
    nbytes = int(nbytes.replace(",", ""))
    data = show(A + name)
    pub = hashlib.sha256(data).hexdigest()
    me = manifest.get("author/" + name, {})
    if name in red and red[name]["original_sha256"] == sha:
        ok = me.get("published_sha256") == pub and pub != sha
        src = f"redaction.json original_sha256 (published {len(data)} B {pub[:8]}; page bytes {nbytes} not checkable)"
    else:
        ok = pub == sha and len(data) == nbytes and me.get("published_sha256") == sha
        src = "published file + MANIFEST.json published_sha256"
    probs += not ok
    print(f"{'OK ' if ok else 'BAD'} ev  {name:40} {nbytes:>11} {src}")
print(f"problems: {probs}")
sys.exit(1 if probs else 0)
