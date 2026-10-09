#!/usr/bin/env python3
"""Check the publishable packet and write a relative SHA-256 manifest."""
import argparse
import hashlib
import json
from pathlib import Path
import re

p = argparse.ArgumentParser()
p.add_argument("packet", type=Path)
a = p.parse_args()
root = a.packet.resolve()
report = (root/"REPORT.md").read_text()
assert report.splitlines()[0] == "[R557] NEGATIVE - exact head b9b9c20a9a44650e176db0c72ad7c752bee20dc4"
assert report.splitlines()[-1] == "R557-1 FINISHED"
assert "SKELETON" not in report
assert all(f"| {lens} | UNCLEAN |" in report for lens in ("Conformance","RTL","Robustness","Tests","Docs"))
for target in re.findall(r"\]\(([^)]+)\)",report):
    if not target.startswith("https://"):
        assert (root/target.split("#",1)[0]).is_file(), target
checkout=json.loads((root/"receipts/checkout-final.json").read_text())
assert checkout["tracked_files"] == 51
assert checkout["clean_status"] and checkout["index_matches_head"] and checkout["worktree_bytes_and_modes_match_head"]
assert checkout["gitlinks"] == []
assert (root/"receipts/published-head.txt").read_text().strip() == checkout["head"]
audit=json.loads((root/"receipts/mutation-audit.json").read_text())
assert audit["results"] == {"CAUGHT":311}
assert audit["required_assertion_kills"] == 325
assert all(x["all_named_assertions_present"] for x in audit["plants"])
probes=json.loads((root/"receipts/probe-results.json").read_text())
assert probes["stale_campaign"]["rc"] == 0 and probes["fresh_campaign"]["rc"] == 1
assert probes["stale_xml_unchanged"]
assert probes["boundary_digraph_outside_include"]["rc"] == 0
assert probes["trace_indented_unknown"]["rc"] == 0
assert probes["trace_indented_runs"]["rc"] == 0
files=[root/"REPORT.md",root/"REPLAY.md"]
files += sorted(f for directory in ("scripts","receipts") for f in (root/directory).rglob("*") if f.is_file() and "__pycache__" not in f.parts)
errors=[]
for f in files:
    text=f.read_text()
    for prefix in ("/"+"home/", "/"+"data/", "/"+"tmp/"):
        if prefix in text: errors.append(str(f.relative_to(root))+": local location")
    for word in ("co"+"dex", "chat"+"gpt", "clau"+"de", "anth"+"ropic", "open"+"ai"):
        if re.search(r"(?i)\b"+word+r"\b",text): errors.append(str(f.relative_to(root))+": restricted attribution")
assert not errors, errors
lines=[hashlib.sha256(f.read_bytes()).hexdigest()+"  "+str(f.relative_to(root)) for f in sorted(set(files))]
(root/"MANIFEST.sha256").write_text("\n".join(lines)+"\n")
print(json.dumps({"publishable_files":len(lines),"manifest":"MANIFEST.sha256","all_checks_pass":True}))
