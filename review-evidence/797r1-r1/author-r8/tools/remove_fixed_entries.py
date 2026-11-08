#!/usr/bin/env python3
"""Remove the D0 entries this lane fixed from scripts/docs_inventory.json, byte-preserving the format.

Usage: python3 -I remove_fixed_entries.py <repo-root>
Refuses unless every ID is present exactly once on a register reference page, and the file
round-trips through json.dumps(indent=1) unchanged before the edit.
"""
import json
import sys
from pathlib import Path

REMOVE = ["D0-006", "D0-007", "D0-008", "D0-014", "D0-015", "D0-016", "D0-017", "D0-018",
          "D0-041", "D0-042", "D0-043", "D0-044", "D0-058", "D0-059", "D0-060"]
KEEP = ["D0-040", "D0-057"]
PAGES = ("docs/reference/REGISTER_MAP.md", "docs/reference/REGISTER_MAP_CLASSES.md")

path = Path(sys.argv[1]) / "scripts/docs_inventory.json"
raw = path.read_text(encoding="utf-8")
data = json.loads(raw)
if json.dumps(data, indent=1, ensure_ascii=False) + "\n" != raw:
    sys.exit("refused: file does not round-trip")
ids = [f["id"] for f in data["findings"]]
for i in REMOVE + KEEP:
    if ids.count(i) != 1:
        sys.exit(f"refused: {i} appears {ids.count(i)} times")
for f in data["findings"]:
    if f["id"] in REMOVE + KEEP and f["page"] not in PAGES:
        sys.exit(f"refused: {f['id']} is on {f['page']}")
before = len(data["findings"])
data["findings"] = [f for f in data["findings"] if f["id"] not in REMOVE]
path.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"findings {before} -> {len(data['findings'])}; removed {len(REMOVE)}: {', '.join(REMOVE)}; kept {', '.join(KEEP)}")
