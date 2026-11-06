#!/usr/bin/env python3
"""Real-tree acceptance probes on a disposable clone: `--check` after each edit, the tree reset between edits.

usage: probes848b.py <disposable clone> <scratch dir>
Fails unless every probe gives the exit status the acceptance asks for.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

root, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
SCRIPT = ["python3", "-B", "scripts/docs_inventory.py"]


def sh(*argv: str) -> subprocess.CompletedProcess:
    """One command in the clone."""
    return subprocess.run(argv, cwd=root, capture_output=True, text=True, check=False, timeout=120)


def reset() -> None:
    """Back to the committed head, with nothing left over."""
    sh("git", "reset", "-q", "--hard", "HEAD")
    sh("git", "clean", "-qfd")


page_text = (root / "docs/DOCUMENTATION_AUDIT.md").read_text(encoding="utf-8")
rows = re.findall(r"^\| \[([^\]]+?)(?: \(historical\))?\]\(", page_text.split("## Inventory", 1)[1].split("## Findings", 1)[0], re.M)
pages = [p for p in rows if p != "docs/DOCUMENTATION_AUDIT.md"]
data = json.loads((root / "scripts/docs_inventory.json").read_text(encoding="utf-8"))
recorded = sorted({f["page"] for f in data["findings"]})
current = next(line.split("|")[1].strip("[] ").split("]")[0] for line in page_text.splitlines()
               if line.startswith("| [") and " | current | " in line and "DOCUMENTATION_AUDIT" not in line)


def touch_all(text: str, top: bool, chosen: list[str]) -> None:
    """Add `text` at the top or the end of each chosen page."""
    for name in chosen:
        target = root / name
        body = target.read_text(encoding="utf-8", errors="surrogateescape")
        target.write_text(text + body if top else body + text, encoding="utf-8", errors="surrogateescape")


def banner() -> None:
    """A supersession banner on a current page."""
    target = root / current
    target.write_text(target.read_text(encoding="utf-8").replace("\n", "\n\n> Superseded by [A](README.md).\n", 1), encoding="utf-8")


def judged() -> None:
    """A recorded status judgement, with no document edit."""
    changed = dict(data)
    changed["judged"] = dict(data.get("judged", {}), **{current: {"status": "superseded", "evidence": "probe"}})
    (root / "scripts/docs_inventory.json").write_text(json.dumps(changed), encoding="utf-8")


def added() -> None:
    """A new tracked page."""
    (root / "docs/PROBE_PAGE.md").write_text("# Probe\n", encoding="utf-8")
    sh("git", "add", "docs/PROBE_PAGE.md")


PROBES = [
    (f"one line appended to all {len(pages)} pages", lambda: touch_all("\nAdded line.\n", False, pages), 0),
    (f"500 lines appended to all {len(pages)} pages", lambda: touch_all("\nAdded.\n" * 500, False, pages), 0),
    (f"one blank line above every recorded finding ({len(recorded)} pages)", lambda: touch_all("\n", True, recorded), 0),
    ("supersession banner on a current page", banner, 1),
    ("status recorded as a judgement, no document edit", judged, 1),
    ("new tracked page", added, 1),
    ("page removed with git rm", lambda: sh("git", "rm", "-q", current), 1),
]
bad = 0
for name, edit, want in PROBES:
    reset()
    edit()
    done = sh(*SCRIPT, "--check")
    ok = done.returncode == want
    bad += not ok
    print(f"{'ok ' if ok else 'BAD'} rc={done.returncode} want {want} :: {name}", flush=True)
reset()

# The route the page names, run as the page spells it, against the page's own Findings table.
lanes = scratch / "lanes"
done = sh(*SCRIPT, "--findings-dir", str(lanes))
entries = re.findall(r"^## (D0-\d+): (.+):(\d+|\?)$", "".join(p.read_text(encoding="utf-8") for p in sorted(lanes.glob("*.md"))), re.M)
findings_table = page_text.split("## Findings", 1)[1]
table = re.findall(r"^\| (D0-\d+) \| \[([^\]]+?)(?: \(historical\))?\]\(", findings_table, re.M)
lost = sorted(i for i, _, line in entries if line == "?")
flagged = sorted(re.findall(r"^\| (D0-\d+) \| .*? \| re-verify: quote not found \|", findings_table, re.M))
same = sorted((i, p) for i, p, _ in entries) == sorted(table)
statements = sum(1 for p in lanes.glob("*.md") for line in p.read_text(encoding="utf-8").splitlines() if line.startswith("- Statement: "))
print(f"route rc={done.returncode}; lane entries {len(entries)}; page rows {len(table)}; one to one {same}; statements {statements}")
print(f"unlocated in lane files {lost}; flagged on the page {flagged}; agree {lost == flagged}")
print(f"page names the command {'--findings-dir DIR' in page_text}; literal re-verify phrase in the intro {'re-verify' in findings_table.split('| ID |', 1)[0]}")
bad += not (done.returncode == 0 and same and lost == flagged and statements == len(entries))


def plain(text: str) -> str:
    """Words only: no wrapping, list or quote markers, emphasis or code spans."""
    return " ".join(re.sub(r"[>*_`]", " ", text).lower().split())


# The rows a text search misses, by the reviewer's criterion, each followed down the route the page names.
where = {(i, p): line for i, p, line in entries}
missed = reached = 0
for raw in findings_table.split("\n"):
    if not raw.startswith("| D0"):
        continue
    parts = [c.strip() for c in re.split(r"(?<!\\)\|", raw)[1:-1]]
    name = re.match(r"\[(.+?)(?: \(historical\))?\]", parts[1]).group(1)
    quote = parts[3].replace("\\|", "|")
    lines = (root / name).read_text(encoding="utf-8", errors="replace").split("\n")
    if parts[2] != "on page" or any(" ".join(quote.split()) in " ".join(line.split()) for line in lines):
        continue
    missed += 1
    line = where[(parts[0], name)]
    hit = line != "?" and plain(quote)[:32] in plain(" ".join(lines[int(line) - 1:int(line) + 3]))
    reached += hit
    print(f"{'ok ' if hit else 'BAD'} {parts[0]} {name}:{line} :: {quote[:60]}")
print(f"rows a text search misses {missed}; reached through the route {reached}")
bad += not (missed == 7 and reached == 7)
print(f"{len(PROBES)} probes, {bad} bad")
sys.exit(1 if bad else 0)
