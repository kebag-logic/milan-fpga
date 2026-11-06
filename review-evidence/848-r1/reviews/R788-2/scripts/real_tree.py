#!/usr/bin/env python3
"""Read-only probes of the real tree: --findings-dir against the page, and the rows a text search misses.

Usage: python3 -I real_tree.py REPO LANE_DIR

LANE_DIR holds the output of `docs_inventory.py --findings-dir`. Nothing in REPO is written.
"""
import re
import subprocess
import sys
from pathlib import Path

ROW = re.compile(r"^\| (D0-\d+) \| \[(.+?)(?: \(historical\))?\]\([^)]*\) \| ([^|]+) \| (.*?) \| ")


def lanes_of(repo):
    sys.path.insert(0, str(repo / "scripts"))
    import docs_inventory as inv
    return inv.first_match, inv.LANES


def main():
    repo, lanes = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    first_match, table = lanes_of(repo)
    page = (repo / "docs/DOCUMENTATION_AUDIT.md").read_text(encoding="utf-8")
    section = page.split("\n## Findings\n", 1)[1]
    rows = []
    for line in section.split("\n"):
        hit = ROW.match(line)
        if hit:
            rows.append(hit.groups())
    entries = {}
    misfiled = 0
    for lane_file in sorted(lanes.glob("*.md")):
        text = lane_file.read_text(encoding="utf-8")
        title = text.split("\n", 1)[0].removeprefix("# D0 findings: ")
        for ident, path, number, statement in re.findall(
                r"^## (D0-\d+): (.+):(\d+|\?)\n\n- Statement: (.*)$", text, re.MULTILINE):
            entries[(ident, path)] = (number, statement, lane_file.name)
            if first_match(table, path) != title:
                misfiled += 1
    print("page rows:", len(rows), "lane entries:", len(entries), "misfiled entries:", misfiled)
    keys = {(r[0], r[1]) for r in rows}
    print("rows without an entry:", sorted(keys - set(entries)), "entries without a row:", sorted(set(entries) - keys))
    flagged = [r for r in rows if r[2].strip() != "on page"]
    unknown = [k for k, v in entries.items() if v[0] == "?"]
    print("rows flagged re-verify:", sorted((r[0], r[1]) for r in flagged))
    print("entries at line ?:", sorted(unknown))
    print("flagged rows equal unknown entries:", {(r[0], r[1]) for r in flagged} == set(unknown))
    missed, wrong = [], []
    for (ident, path), (number, statement, _) in sorted(entries.items()):
        if number == "?":
            continue
        text = (repo / path).read_text(encoding="utf-8", errors="replace")
        if statement not in text:
            missed.append((ident, path, number))
            lines = text.split("\n")
            window = " ".join(lines[int(number) - 1:int(number) + 3]).casefold()
            first = re.sub(r"[`*_\[\]]", "", statement).casefold().split()[0]
            if first not in re.sub(r"[`*_\[\]]", "", window):
                wrong.append((ident, path, number))
    print("rows a verbatim text search misses:", len(missed))
    for item in missed:
        print("  ", item)
    print("of those, named line does not open the statement:", wrong)


if __name__ == "__main__":
    main()
