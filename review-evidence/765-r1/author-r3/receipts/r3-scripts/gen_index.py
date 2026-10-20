#!/usr/bin/env python3
"""Write receipts/INDEX.md from the files present (path, size, SHA-256)."""
import hashlib
from pathlib import Path

RECEIPTS = Path("<home>/milan-fpga-management/2026-09-23/765-a657/receipts")


def main() -> None:
    rows = []
    for path in sorted(RECEIPTS.rglob("*")):
        if not path.is_file() or path.name == "INDEX.md":
            continue
        data = path.read_bytes()
        rows.append(f"| `{path.relative_to(RECEIPTS)}` | {len(data):,} | "
                    f"`{hashlib.sha256(data).hexdigest()[:16]}` |")
    head = ["# Receipts index", "",
            "Generated from the files present in this directory.",
            "Host paths in copied logs are replaced: `<scratch>` is the lane's scratch",
            "directory, `<lane>` the worktree, `<tools>` the tool directory, `<home>` the",
            "home directory, `<base-lane-scratch>` the PR #767 lane's scratch directory.",
            "A `.tail` file stands for a log over 200 KB: its first line holds the",
            "original's SHA-256 and size.", "",
            f"{len(rows)} files.", "",
            "| File | Bytes | SHA-256 (first 16) |", "|---|---:|---|"]
    (RECEIPTS / "INDEX.md").write_text("\n".join(head + rows) + "\n")


if __name__ == "__main__":
    main()
