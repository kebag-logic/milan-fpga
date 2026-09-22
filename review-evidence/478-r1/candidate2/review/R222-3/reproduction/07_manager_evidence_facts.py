#!/usr/bin/env python3
"""R222-3: factual summary of the manager's candidate2 evidence (attributed,
not rerun). Reads only review-evidence/478-r1/candidate2 at the given commit.
Usage: 07_manager_evidence_facts.py <bare-repo> <commit> <out>
"""
import json
import re
import subprocess
import sys

repo, commit, out = sys.argv[1:4]
P = "review-evidence/478-r1/candidate2"
CAND = "72e16c6172db723734317b105cff6c6e9168571a"
TREE = "93be2b5788c4b79e88bfe22fbaf985686bbdc8f2"
DEV = "52711029f374650dc93830d5ea28e81cb5c8f410"


def show(path: str) -> str:
    return subprocess.run(["git", "-C", repo, "show", f"{commit}:{P}/{path}"],
                          check=True, capture_output=True, text=True).stdout


L = []
spec = json.loads(show("manager-builder-spec.json"))
res = json.loads(show("manager-builder/results.json"))
fin = json.loads(show("manager-builder-final/results.json"))
L.append(f"spec head={spec['head']} base={spec['base']} commands={len(spec['commands'])}")
L.append(f"results head={res['head']} base={res['base']} n={len(res['results'])}")
L.append(f"final head={fin.get('head')} base={fin.get('base')} n={len(fin.get('results', []))}")
assert spec["head"] == res["head"] == CAND and spec["base"] == res["base"] == DEV
same = [r["command"] for r in res["results"]] == spec["commands"]
L.append(f"results commands == spec commands in order: {same}")
L.append(f"all original exits zero: {all(r['exit_code'] == 0 for r in res['results'])}")
for i, (a, b) in enumerate(zip(res["results"], fin["results"]), 1):
    if a["command"] != b["command"] or a["exit_code"] != b["exit_code"]:
        L.append(f"final ledger differs at {i}: original {a['command']} exit {a['exit_code']}"
                 f" -> final {b['command']} exit {b['exit_code']}"
                 f" note={ {k: v for k, v in b.items() if k not in ('command', 'exit_code', 'seconds')} }")
L.append(f"final ledger all exits zero: {all(r['exit_code'] == 0 for r in fin['results'])}")

# selected raw-log facts
def log(i: int) -> str:
    return show(f"manager-builder/{i:02d}.log")

l01 = log(1)
L.append("01 gen_aem_store --self-test: ok-arms=%d fail-arms=%d verdict=%s" % (
    len(re.findall(r"\[ok  \]", l01)), len(re.findall(r"\[FAIL\]", l01)),
    (re.findall(r"gen_aem_store self-test: (\w+)", l01) or ["?"])[-1]))
for i in (5, 7, 13, 36):
    tail = [ln for ln in log(i).strip().splitlines() if ln.strip()][-2:]
    L.append(f"{i:02d} {spec['commands'][i-1]} tail: {tail}")
l40 = log(40)
L.append(f"40 original stale-endpoint log bytes={len(l40)}")
l41 = log(41)
L.append("41 builder gate36a lines:")
L += ["   " + ln.strip() for ln in l41.splitlines() if "gate 36a" in ln]
L.append("41 builder verdict lines: " + str([ln.strip() for ln in l41.splitlines()
                                              if "ALL GATES" in ln or "NOT RUN" in ln][-4:]))
wc = json.loads(show("whitespace-correction/results.json"))
L.append(f"whitespace correction: {wc['results'][0]['command']} exit {wc['results'][0]['exit_code']}")
wl = show("whitespace-correction/01.log")
L.append(f"whitespace correction log bytes={len(wl)}")

for f in ("builder-tree-integrity.json", "builder-corrected-final-integrity.json"):
    d = json.loads(show(f))
    flat = json.dumps(d)
    L.append(f"{f}: keys={list(d.keys())[:14]}")
    L.append(f"   mentions candidate={CAND in flat} tree={TREE in flat}")
    for k in ("head", "tree", "index_tree", "files", "file_count", "tracked_files",
              "mismatches", "ok", "submodules", "pins", "result"):
        if k in d:
            L.append(f"   {k}: {json.dumps(d[k])[:400]}")
text = "\n".join(L) + "\n"
open(out, "w").write(text)
print(text)
