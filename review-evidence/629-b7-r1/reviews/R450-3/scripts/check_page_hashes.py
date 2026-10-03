#!/usr/bin/env python3
"""Check every hash row of the page's "B7: artifact hashes" section against the
published packet at a given evidence commit.

Raw rows (first table): against the packet's RAW-ARTIFACTS.json (all rows) and,
for the first 19, against runs/<case>/events.jsonl ("raw-file" records; the
tone loop against the "start" record's tone_sha256).
Evidence rows (second table): the blob at <commit>:review-evidence/629-b7-r1/author/<path>
(bytes and SHA-256) and MANIFEST.json's published_sha256, except the masked
tools, which are checked against redaction.json's original_sha256.
Also reports whether each cited evidence file is byte-identical between the
first publication 95448218 and <commit>.

Usage: check_page_hashes.py <repo> <page-rev> <evidence-commit>
"""
import hashlib, json, re, subprocess, sys

REPO, PAGEREV, EV = sys.argv[1:4]
FIRST = "95448218b342c084efa28ac266ae9415bff4ecce"
E = "review-evidence/629-b7-r1"
CASEMAP = {"a0": "a0", "a1": "a1", "a2": "a2", "b0": "b0", "bcrf": "bcrf", "baaf": "baaf"}


def show(rev, path):
    r = subprocess.run(["git", "-C", REPO, "show", f"{rev}:{path}"], capture_output=True)
    return r.stdout if r.returncode == 0 else None


if PAGEREV.startswith("FILE:"):  # fault probes: a local copy of the page
    page = open(PAGEREV[5:]).read().splitlines()
else:
    page = show(PAGEREV, "docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md").decode().splitlines()
start = page.index("### B7: artifact hashes")
rows = []
for ln in page[start + 1:]:
    if ln.startswith("## ") or ln.startswith("### "):
        break
    m = re.match(r"\| (.+?) \| ([\d,]+) \| `([0-9a-f]{64})` \|$", ln)
    if m:
        rows.append((m.group(1), int(m.group(2).replace(",", "")), m.group(3)))
print(f"page {PAGEREV[:8]}: {len(rows)} hash rows in B7: artifact hashes")

raw = json.loads(show(EV, f"{E}/author/RAW-ARTIFACTS.json"))
rawmap = {f["file"]: (f["bytes"], f["sha256"]) for f in raw["files"]}
manifest = {m["file"]: m for m in json.loads(show(EV, f"{E}/MANIFEST.json"))}
red = json.loads(show(EV, f"{E}/author/redaction.json"))["files"]
problems = 0
raw_rows = [r for r in rows if not r[0].startswith("`") or "/" in r[0].strip("`").split(" ")[0] and r[0].split("`")[1].split("/")[0] in CASEMAP or r[0].startswith("Tone")]
for label, nbytes, sha in rows:
    name = label.split("`")[1] if "`" in label else label
    ok = []
    if label.startswith("Tone loop"):
        recs = []
        for c in CASEMAP:
            ev = show(EV, f"{E}/author/runs/{c}/events.jsonl").decode().splitlines()
            st = [json.loads(x) for x in ev if '"kind": "start"' in x]
            recs.append(st[0].get("tone_sha256") == sha)
        ok.append(f"events.jsonl start.tone_sha256 in {sum(recs)}/{len(recs)} runs")
        rm = [v for k, v in rawmap.items() if "tone" in k.lower()]
        ok.append(f"RAW-ARTIFACTS tone entry match: {(nbytes, sha) in rm}")
        bad = sum(recs) != len(recs) or (nbytes, sha) not in rm
    elif name.split("/")[0] in CASEMAP and not name.startswith("tools/"):
        case, fn = name.split("/", 1)
        in_raw = rawmap.get(name) == (nbytes, sha)
        ok.append(f"RAW-ARTIFACTS: {in_raw}")
        bad = not in_raw
        if not fn.startswith("grade-"):
            ev = show(EV, f"{E}/author/runs/{case}/events.jsonl").decode().splitlines()
            rf = [json.loads(x) for x in ev if '"kind": "raw-file"' in x]
            hit = [r for r in rf if r["file"] == fn]
            m = bool(hit) and (hit[-1]["bytes"], hit[-1]["sha256"]) == (nbytes, sha)
            ok.append(f"runs/{case}/events.jsonl: {m}")
            bad = bad or not m
        else:
            ev = show(EV, f"{E}/author/runs/{case}/events.jsonl").decode()
            ok.append(f"in events.jsonl: {sha in ev}")
    else:
        path = f"author/{name}"
        blob = show(EV, f"{E}/{path}")
        first = show(FIRST, f"{E}/{path}")
        same = blob == first
        if name in ("tools/run_b7.py", "tools/grade_b7.py"):
            m = red[name]["original_sha256"] == sha
            ok.append(f"redaction.json original_sha256: {m}; published blob unchanged since 95448218: {same}")
            bad = not m
        else:
            h = hashlib.sha256(blob).hexdigest() if blob is not None else None
            m = h == sha and len(blob) == nbytes
            mp = manifest.get(path, {}).get("published_sha256") == sha
            ok.append(f"blob bytes+sha: {m}; MANIFEST published_sha256: {mp}; unchanged since 95448218: {same}")
            bad = not (m and mp and same)
    problems += bad
    print(("PROBLEM " if bad else "ok      ") + f"{name}: " + "; ".join(ok))
print(f"rows {len(rows)} problems {problems}")
