#!/usr/bin/env python3
"""Reproduce the review's scope, ownership-search and approval-text receipts."""
import argparse
import hashlib
import html
import json
from pathlib import Path
import re
import subprocess

p = argparse.ArgumentParser()
p.add_argument("repository", type=Path)
p.add_argument("packet", type=Path)
p.add_argument("--standards", type=Path)
a = p.parse_args()
repo, out = a.repository.resolve(), a.packet.resolve()
base = "423ac5d910d09ab189b3acc39ae3ae1d10d50b19"
head = "a27808375427859dc357f6bfd0a88842062b20ed"

def git(*args):
    return subprocess.check_output(["git", "-C", str(repo), *args]).decode()

queries = {
    "Q1": r"NFR-SCOUT-0[123]",
    "Q2": r"never on firmware|fabric-only|fabric.only|no firmware round trip|never becomes a packet|all per-frame protocol",
    "Q3": r"(?i)(ADP|ACMP|AECP|MAAP|SRP|protocol control).{0,70}(fabric|processor)|(fabric|processor).{0,70}(ADP|ACMP|AECP|MAAP|SRP|protocol control)",
    "Q4": r"NFR-LAT-02|NFR-SCUP-0[24]|NFR-REL-02|FR-CTRL-04",
}
sweep = {"queries": queries, "revisions": {}}
for rev in (base, head):
    hits = []
    files = [f for f in git("ls-tree", "-r", "--name-only", rev).splitlines() if f.endswith(".md")]
    for file in files:
        for number, line in enumerate(git("show", rev + ":" + file).splitlines(), 1):
            for name, pattern in queries.items():
                if re.search(pattern, line):
                    hits.append({"query": name, "artifact": f"{file}:{number}"})
    sweep["revisions"][rev] = {"count": len(hits), "hits": hits}
(out / "ownership-search.json").write_text(json.dumps(sweep, indent=2) + "\n")

changed = git("diff", "--name-status", base, head).splitlines()
scope = {"base": base, "head": head, "tree": git("rev-parse", head + "^{tree}").strip(),
         "changes": changed, "documentation_only": all(line.endswith(".md") for line in changed),
         "history": git("log", "--format=%H %s", base + ".." + head).splitlines(),
         "hostplane_exists_at_base": "tb/verilator/hostplane" in git("ls-tree", "-r", "--name-only", base)}
(out / "scope.json").write_text(json.dumps(scope, indent=2) + "\n")

def normalized(text):
    text = html.unescape(text).replace("<br>", "\n")
    text = re.sub(r"\[([^\]]+)\]\([^\n)]*\)", r"\1", text)
    return " ".join(text.split())

body = json.loads((out / "pr-674.json").read_text())["body"]
body_normal = normalized(body)
before = git("show", base + ":docs/reference/FR_NFR.md").splitlines()
after = git("show", head + ":docs/reference/FR_NFR.md").splitlines()
approval = []
for line in after:
    if not re.match(r"\| (?:FR|NFR)-[A-Z]+-\d+ \|", line) or line in before:
        continue
    rowid = line.split("|")[1].strip()
    old = next(x for x in before if x.startswith("| " + rowid + " |"))
    approval.append({"row": rowid, "old_matches": normalized(old.strip("| ")) in body_normal,
                     "new_matches": normalized(line.strip("| ")) in body_normal})
for rev, name in ((base, "old"), (head, "new")):
    section = git("show", rev + ":REQUIREMENTS.md").split("## 1. Product ownership\n", 1)[1].split("## 2. Reference standards", 1)[0]
    approval.append({"row": "REQUIREMENTS.md section 1 " + name, "matches": normalized(section) in body_normal})
section = "### 3.4.1" + "\n".join(after).split("### 3.4.1", 1)[1].split("### 3.5", 1)[0]
approval.append({"row": "New timing and hook sections", "matches": normalized(section) in body_normal})
(out / "approval-text.json").write_text(json.dumps(approval, indent=2) + "\n")

if a.standards:
    names = ["Milan_Specification_Consolidated_v1.2_Final_Approved 20231130.pdf",
             "1722.1-2021.pdf", "1722-2016.pdf", "802.1Q-2018.pdf"]
    hashes = [{"document": name, "sha256": hashlib.sha256((a.standards/name).read_bytes()).hexdigest()}
              for name in names]
    (out / "standards-identities.json").write_text(json.dumps(hashes, indent=2) + "\n")
print(json.dumps({"scope_documentation_only": scope["documentation_only"],
                  "sweep_counts": {r: v["count"] for r, v in sweep["revisions"].items()},
                  "approval": approval}, indent=2))
