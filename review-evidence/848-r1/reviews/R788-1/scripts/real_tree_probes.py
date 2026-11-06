#!/usr/bin/env python3
"""Real-tree probes of docs_inventory.py --check on a disposable clone.

Usage: real_tree_probes.py CLONE. Each probe edits CLONE, runs --check, prints rc and
the first differing line, then restores the tree with git reset and clean.
Per-page window effects are measured by window_sweep.py.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

clone = Path(sys.argv[1]).resolve()
TOOL = ["python3", "-I", "scripts/docs_inventory.py"]


def run(*argv):
    return subprocess.run(argv, cwd=clone, capture_output=True, text=True, check=False)


def restore():
    run("git", "reset", "-q", "--hard", "HEAD")
    run("git", "clean", "-qfd", "-e", "protocol-processor", "-e", "gptp-processor")


def check(label):
    done = run(*TOOL, "--check")
    lines = done.stdout.strip().splitlines()
    print(f"{label}: rc={done.returncode} :: {lines[0][:110] if lines else ''}", flush=True)
    for extra in lines[1:3]:
        print("     " + extra[:170])
    return done.returncode


def docs():
    listed = run("git", "ls-files", "-z").stdout.split("\0")
    keep = [p for p in listed if p and (p.endswith(".md") or Path(p).name.upper().startswith("README"))
            and p != "docs/DOCUMENTATION_AUDIT.md" and (clone / p).is_file()]
    return keep


def edit(path, change):
    target = clone / path
    target.write_text(change(target.read_text(encoding="utf-8", errors="surrogateescape")),
                      encoding="utf-8", errors="surrogateescape")


restore()
pages = docs()
print("pages edited per sweep:", len(pages))
check("unchanged")

for page in pages:
    edit(page, lambda t: t + "\nAdded plain line.\n")
check("LENGTH one line appended to every page")
restore()

for page in pages:
    edit(page, lambda t: "\n".join(t.split("\n") + ["x"] * 500))
check("LENGTH 500 lines appended to every page")
restore()

data = json.loads((clone / "scripts/docs_inventory.json").read_text(encoding="utf-8"))
stale_pages = sorted({f["page"] for f in data["findings"]})
for page in stale_pages:
    edit(page, lambda t: "\n" + t)
check(f"LENGTH blank line above every recorded finding ({len(stale_pages)} pages)")
restore()


target = "docs/guides/README.md"
edit(target, lambda t: t.split("\n")[0] + "\n\n> Superseded by [the index](../README.md).\n" + "\n".join(t.split("\n")[1:]))
check("STATUS supersession banner")
restore()

data2 = json.loads(json.dumps(data))
data2.setdefault("judged", {})["docs/guides/README.md"] = {"status": "superseded", "evidence": "judged"}
(clone / "scripts/docs_inventory.json").write_text(json.dumps(data2), encoding="utf-8")
check("STATUS recorded judgement, no document edit")
restore()

(clone / "docs/guides/NEW_PAGE.md").write_text("# New page\n", encoding="utf-8")
check("PAGESET untracked new page (not in the population)")
run("git", "add", "docs/guides/NEW_PAGE.md")
check("PAGESET tracked new page")
restore()

run("git", "rm", "-q", "docs/guides/README.md")
check("PAGESET git rm of a tracked page")
restore()
(clone / "docs/guides/README.md").unlink()
check("PAGESET page deleted on disk only")
restore()

first = data["findings"][0]
edit(first["page"], lambda t: t.replace(first["quote"], "Reworded statement.", 1))
check(f"FINDING quote {first['id']} removed from its page")
restore()

data3 = json.loads(json.dumps(data))
data3["findings"].append({"id": "D0-999", "page": "docs/guides/README.md", "quote": "Documentation",
                          "source": "probe", "correction": "probe"})
(clone / "scripts/docs_inventory.json").write_text(json.dumps(data3), encoding="utf-8")
check("FINDING added to the data file")
restore()

edit("docs/DOCUMENTATION_AUDIT.md", lambda t: t.replace("| on page |", "| re-verify: quote not found |", 1))
check("HAND edit of a Located cell")
restore()
edit("docs/DOCUMENTATION_AUDIT.md", lambda t: re.sub(r"\| stale \| \d+ finding\(s\): [^|]*\|", "| current | no recorded contradiction |", t, count=1))
check("HAND edit marking a stale page current")
restore()
check("restored")
