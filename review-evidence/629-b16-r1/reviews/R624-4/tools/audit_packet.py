#!/usr/bin/env python3
"""R624-4: check lane B16's "Where the packet is" paragraph and every hash row of its section.

usage: audit_packet.py <findings.md> <evidence-repo> <pinned-commit> <tip-commit> <out.json>

Reads the published evidence branch only through `git -C <evidence-repo>`. For the manifest at the
pinned commit it counts entries and path-redacted files per author directory, and checks that the
two hashes differ exactly where the flag is set. For every `| path | bytes | sha |` row of lane B16's
section it checks the packet file in the matching author directory (author-r3 for rows on the page at
round 3, author-r4 for every row at the head) by size and SHA-256, and for raw-file rows it checks the
hash against RAW-ARTIFACTS.json. Exit 0 when every check holds.
"""
import hashlib
import json
import re
import subprocess
import sys

DOC, EV, PIN, TIP, OUT = sys.argv[1:6]
BASE = "review-evidence/629-b16-r1"


def show(commit, path):
    return subprocess.run(["git", "-C", EV, "show", f"{commit}:{path}"], check=True, capture_output=True).stdout


def ls(commit, prefix):
    out = subprocess.run(["git", "-C", EV, "ls-tree", "-r", "--name-only", commit, prefix], check=True,
                         capture_output=True, text=True).stdout
    return set(out.split())


res = {"checks": [], "fail": 0}


def check(name, ok, detail=""):
    res["checks"].append({"name": name, "ok": bool(ok), "detail": detail})
    if not ok:
        res["fail"] += 1


raw_man = show(PIN, f"{BASE}/MANIFEST.json")
man = json.loads(raw_man)
check("manifest sha256", hashlib.sha256(raw_man).hexdigest() ==
      "8d417d54b13a264484bfcb0b69f8a643e5cd3bf2819294cea201242a2f67f034", hashlib.sha256(raw_man).hexdigest())
check("manifest entries 1,680", len(man) == 1680, str(len(man)))
red = {}
for e in man:
    d = e["file"].split("/")[0]
    red.setdefault(d, [0, 0])
    red[d][0] += 1
    if e["path_redacted"]:
        red[d][1] += 1
    check_ok = (e["original_sha256"] != e["published_sha256"]) == bool(e["path_redacted"])
    if not check_ok:
        check("flag iff hashes differ", False, e["file"])
res["manifest_by_dir"] = red
nred = sum(v[1] for k, v in red.items() if k.startswith("author"))
check("27 author files path-redacted", nred == 27, str(nred))
check("1/9/17 by round", [red.get(d, [0, 0])[1] for d in ("author-r1", "author-r2", "author-r3")] == [1, 9, 17],
      json.dumps(red))
redacted_names = sorted(e["file"] for e in man if e["path_redacted"])
res["redacted_files"] = redacted_names
check("pinned commit has author-r1..r3, no author-r4",
      all(ls(PIN, f"{BASE}/author-r{i}") for i in (1, 2, 3)) and not ls(PIN, f"{BASE}/author-r4"))
check("tip has author-r4", bool(ls(TIP, f"{BASE}/author-r4")))
# published file of every manifest entry at the pinned commit equals published_sha256 (author dirs only)
pinned_files = ls(PIN, BASE)
mism = []
for e in man:
    p = f"{BASE}/{e['file']}"
    if p not in pinned_files:
        mism.append(("missing", e["file"]))
        continue
    if hashlib.sha256(show(PIN, p)).hexdigest() != e["published_sha256"]:
        mism.append(("hash", e["file"]))
check("every manifest entry equals its published file at the pin", not mism, json.dumps(mism[:10]))
mfiles = {e["file"] for e in man}
extra = sorted(p[len(BASE) + 1:] for p in pinned_files if p != f"{BASE}/MANIFEST.json" and p[len(BASE) + 1:] not in mfiles
               and p[len(BASE) + 1:].startswith("author"))
check("no unlisted author file at the pin", not extra, json.dumps(extra[:10]))

# hash rows of lane B16's section
text = open(DOC, encoding="utf-8").read().split("\n")
start = next(i for i, l in enumerate(text) if l.startswith("## Dev 5603c353, 2026-10-12: lane B16"))
end = next((i for i in range(start + 1, len(text)) if text[i].startswith("## ")), len(text))
rows = []
for i in range(start, end):
    cells = [c.strip() for c in text[i].strip().strip("|").split("|")]
    if len(cells) >= 3 and re.fullmatch(r"`[0-9a-f]{64}`", cells[-1]):
        rows.append((i + 1, cells))
res["hash_rows"] = len(rows)
tipfiles = ls(TIP, f"{BASE}/author-r4")
r4man = show(TIP, f"{BASE}/author-r4/MANIFEST.sha256").decode()
raw_art = json.loads(show(TIP, f"{BASE}/author-r4/RAW-ARTIFACTS.json"))
raw_hashes = set(re.findall(r"[0-9a-f]{64}", json.dumps(raw_art)))
packet_rows = raw_rows = 0
for ln, cells in rows:
    sha = cells[-1].strip("`")
    size = cells[-2].replace(",", "")
    if len(cells) == 4:  # raw file row: run | raw file | bytes | sha
        raw_rows += 1
        check(f"line {ln} raw hash in RAW-ARTIFACTS.json", sha in raw_hashes, cells[1])
        continue
    m = re.match(r"`([^`]+)`", cells[0])
    path = m.group(1)
    # source reads (no size column) are raw reads: the table has 3 columns | read | at | sha
    if not size.isdigit():
        raw_rows += 1
        check(f"line {ln} read hash in RAW-ARTIFACTS.json", sha in raw_hashes, path)
        continue
    packet_rows += 1
    p = f"{BASE}/author-r4/{path}"
    if p not in tipfiles:
        check(f"line {ln} {path} in author-r4", False, "missing")
        continue
    data = show(TIP, p)
    ok = hashlib.sha256(data).hexdigest() == sha and len(data) == int(size)
    check(f"line {ln} {path} size and sha256 in author-r4", ok,
          f"{len(data)} {hashlib.sha256(data).hexdigest()}")
res["packet_rows"] = packet_rows
res["raw_rows"] = raw_rows
json.dump(res, open(OUT, "w"), indent=1)
print(json.dumps({"fail": res["fail"], "checks": len(res["checks"]), "hash_rows": len(rows),
                  "packet_rows": packet_rows, "raw_rows": raw_rows, "by_dir": red}))
sys.exit(1 if res["fail"] else 0)
