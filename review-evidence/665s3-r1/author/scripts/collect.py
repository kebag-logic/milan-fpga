#!/usr/bin/env python3
"""Copy gate logs into the lane's receipts, host paths replaced, and write the receipts index from the files present.

usage: collect.py SRC_DIR DEST_SUBDIR [GLOB...]
A log over 190 KB is not copied whole: its first 120 and last 400 lines are kept as an excerpt, and the
whole log's size and sha256 are recorded in the index. Every receipt's size and sha256 is listed in
receipts/INDEX.md, which is regenerated from the files present on every run.
"""
import hashlib
import re
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "receipts"
LIMIT = 190_000
#: host paths, longest first, and what replaces each
HOST = [(re.compile(r"$VALIDATION_STORAGE/665s3-a697c/(?:gates/[^ /]*/?)?"), "<work>/"),
        (re.compile(r"$VALIDATION_STORAGE/665s3-a697/(?:gates/[^ /]*/?)?"), "<work-a697>/"),
        (re.compile(r"$LANES/665-s3-platform"), "<checkout>"),
        (re.compile(r"$VALIDATION_TOOLS/[^ /]+"), "<md-venv>"),
        (re.compile(r"$VALIDATION_STORAGE/[^ /]+/venv-hdl"), "<hdl-venv>"),
        (re.compile(r"$VALIDATION_STORAGE/[^ :'\"]*"), "<host-path>"),
        (re.compile(r"(?<![\w.<>-])/tmp/"), "<tmp>/"),
        (re.compile(r"-I/tmp/"), "-I<tmp>/"),
        (re.compile(r"$WORKSPACE_HOME/litex-milan"), "<litex-tree>"),
        (re.compile(r"$WORKSPACE_HOME/br-milan-rv32"), "<rv32-sdk>"),
        (re.compile(r"$MANAGEMENT/[^ ]*"), "<lane-output>"),
        (re.compile(r"$WORKSPACE_HOME"), "~"),
        (re.compile(r"/tmp/a697b"), "<scratch>")]


def clean(text: str) -> str:
    for pattern, repl in HOST:
        text = pattern.sub(repl, text)
    return text


def main() -> int:
    src, dest = Path(sys.argv[1]), OUT / sys.argv[2]
    globs = sys.argv[3:] or ["*.log", "*.out", "*.md", "*.txt", "*.json"]
    dest.mkdir(parents=True, exist_ok=True)
    big = {}
    for pattern in globs:
        for path in sorted(src.glob(pattern)):
            if not path.is_file():
                continue
            data = path.read_bytes()
            text = clean(data.decode("utf-8", "replace"))
            if len(text.encode()) > LIMIT:
                lines = text.splitlines()
                text = "\n".join(lines[:120] + [f"... {len(lines) - 520} lines cut; see INDEX.md ..."] + lines[-400:])
                big[path.name] = (len(data), hashlib.sha256(data).hexdigest())
                (dest / (path.name + ".excerpt")).write_text(text + "\n")
            else:
                (dest / path.name).write_text(text)
    if big:
        with (dest / "WHOLE-LOGS.txt").open("a") as sink:
            for name, (size, digest) in big.items():
                sink.write(f"{name} {size} bytes sha256 {digest} (excerpt kept)\n")
    rows = ["# Receipts", "", "Generated from the files present by `scripts/collect.py`.", "",
            "| File | Bytes | sha256 |", "|---|---:|---|"]
    for path in sorted(p for p in OUT.rglob("*") if p.is_file() and p.name != "INDEX.md"):
        data = path.read_bytes()
        rows.append(f"| `{path.relative_to(OUT)}` | {len(data)} | `{hashlib.sha256(data).hexdigest()[:16]}` |")
    (OUT / "INDEX.md").write_text("\n".join(rows) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
