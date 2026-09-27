"""Verify the corrected page against its original rows and public archive."""
import hashlib
import importlib.metadata
import json
from pathlib import Path
import re
import subprocess
import sys

import cmarkgfm
import html5lib

root = Path(sys.argv[1]).resolve()
page_name = "docs/findings/394_387_E1_SWITCH_CYCLES.md"
page = (root / page_name).read_text()
old_head = "fddc58e43733afd90d6222e58999e0f416a30df9"
archive_head = "8f983d245a12e18a47ced37904d405b624c7e024"
archive_root = "review-evidence/394-387-r1"

def git(*args):
    return subprocess.check_output(["git", *args], cwd=root, stderr=subprocess.DEVNULL, timeout=60)

def public(name):
    return git("show", f"{archive_head}:{archive_root}/{name}")

def block(text):
    lines = text.splitlines()
    start = next(i for i, line in enumerate(lines) if line.startswith("| Cycle | OFF duration"))
    rows = []
    for line in lines[start:]:
        if not line.startswith("|"):
            break
        rows.append([cell.strip() for cell in line.strip().strip("|").split("|")])
    return start + 1, rows

head = git("rev-parse", "HEAD").decode().strip()
print("Head:", head)
assert git("diff", "--name-only", old_head, "HEAD").decode().splitlines() == [page_name]
assert git("show", "HEAD:" + page_name).decode() == page
assert not git("status", "--porcelain").strip()
line, rows = block(page)
assert len(rows) == 12
for index, row in enumerate(rows):
    label = "header" if index == 0 else "delimiter" if index == 1 else f"cycle {index - 1}"
    print(f"Line {line + index}: {label}: {len(row)} cells")
    assert len(row) == 9
assert rows[2:] == block(git("show", old_head + ":" + page_name).decode())[1][2:]
print("All ten measured rows unchanged from round 1")
assert importlib.metadata.version("cmarkgfm") == "2025.10.22"
assert importlib.metadata.version("html5lib") == "1.1"
html = cmarkgfm.github_flavored_markdown_to_html(page)
doc = html5lib.parseFragment(html, namespaceHTMLElements=False)
tables = list(doc.iter("table"))
assert len(tables) == 6
per_cycle = [table for table in tables if "".join(next(table.iter("th")).itertext()) == "Cycle"]
assert len(per_cycle) == 2
per_cycle = [table for table in per_cycle if "OFF duration" in "".join(table.itertext())]
assert len(per_cycle) == 1
rendered_rows = list(per_cycle[0].iter("tr"))
assert len(rendered_rows) == 11
assert all(len(list(row)) == 9 for row in rendered_rows)
print("Pinned renderer: six tables; per-cycle table has nine columns and ten data rows")

manifest = json.loads(public("MANIFEST.json"))
for entry in manifest:
    assert hashlib.sha256(public(entry["file"])).hexdigest() == entry["published_sha256"], entry["file"]
print(f"Publisher index: {len(manifest)}/{len(manifest)} published SHA-256 values match")
raw = json.loads(public("author/RAW-ARTIFACTS.json"))
raw_pairs = {(row["size"], row["sha256"]) for row in raw}
hashes = re.findall(r"^\| (\d+) \| `([^`]+)` \| (\d+) \| `([0-9a-f]{64})` \|$", page, re.M)
assert len(hashes) == 50
for cycle, name, size, sha in hashes:
    index = json.loads(public(f"author/cycle{int(cycle):02d}/raw-artifacts.json"))
    matches = [row for row in index if Path(row["path"]).name == name]
    assert len(matches) == 1
    assert (int(size), sha) == (matches[0]["size"], matches[0]["sha256"])
    assert (int(size), sha) in raw_pairs
print("All 50 raw-artifact rows match both public indexes")

for n in range(1, 11):
    data = json.loads(public(f"author/cycle{n:02d}/analysis.json"))
    b0, b1 = data["large_phc_discontinuities"][0]["bracket"]
    before = [(t, state) for t, state in data["servo_states"] if t <= b0]
    assert before[-1][1] == 5  # A_MCSRV_STAT state 5 is HOLDOVER.
    assert data["last_wire_before_gap"] < b0
    assert all(data["wire"][role]["first_after_on"] > b1 for role in ("dut", "peer"))
    peer = data["counter_endpoints"]["peer:counter-9-0"]
    assert peer["delta"]["0"] == peer["delta"]["1"] == 0
print("All ten steps: HOLDOVER, before either stream returns; peer link-counter deltas zero")
assert "NOT MET (not exercised)" in page
assert "This run never wrote" not in page
assert "MANIFEST.sha256" not in page
assert not re.search(r"(?<![\w.])/(?:tmp|home|data|root|mnt|opt|srv|var|Users)(?:/|`)", page)
assert not re.search(r"\d{4}-\d{2}-\d{2}/\d+-a\d+", page)
print("Corrected verdict and public locator checks passed")
print("PASS")
