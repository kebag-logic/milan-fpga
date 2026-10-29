#!/usr/bin/env python3
"""Scrub host paths from the receipts in place, keep an excerpt of any log over 190 KB, and write the index.

usage: finalize_receipts.py
Every text receipt under receipts/ is first copied whole, unchanged, to the lane's disk scratch (RAW below),
then rewritten with the host path prefixes replaced by the placeholders in HOST; nothing else in it changes.
A file over 190 KB after that keeps its first 120 and last 400 lines; its whole size and sha256 (of the raw file)
go to receipts/WHOLE-LOGS.txt. receipts/INDEX.md lists every file present with its size and sha256.
"""
import hashlib
import re
import shutil
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "receipts"
RAW = Path("$VALIDATION_STORAGE/665s3-a697d/raw-receipts")
LIMIT = 190_000
TEXT = {".log", ".out", ".md", ".txt", ".json", ".sha256", ".excerpt", ".done"}
#: host paths, most specific first, and what replaces each
HOST = [(re.compile(r"$VALIDATION_STORAGE/665s3-a697d/venv-hdl"), "<hdl-venv>"),
        (re.compile(r"$VALIDATION_STORAGE/665s3-a697d"), "<work>"),
        (re.compile(r"$LANES/665-s3-platform"), "<checkout>"),
        (re.compile(r"$VALIDATION_TOOLS/[^ /:'\"]+"), "<tool-env>"),
        (re.compile(r"$VALIDATION_STORAGE/[^ :'\"]*"), "<host-path>"),
        (re.compile(r"$WORKSPACE_HOME/litex-milan"), "<litex-tree>"),
        (re.compile(r"$WORKSPACE_HOME/br-milan-rv32"), "<rv32-sdk>"),
        (re.compile(r"$MANAGEMENT/[^ :'\"]*"), "<lane-output>"),
        (re.compile(r"$WORKSPACE_HOME"), "~"),
        (re.compile(r"(?<![\w.<>~-])/tmp/"), "<tmp>/")]


def clean(text: str) -> str:
    """The text with every host path prefix replaced."""
    for pattern, repl in HOST:
        text = pattern.sub(repl, text)
    return text


def main() -> int:
    """Scrub, excerpt, index."""
    big = []
    for path in sorted(OUT.rglob("*")):
        if not path.is_file() or path.suffix not in TEXT or path.name in ("INDEX.md", "WHOLE-LOGS.txt"):
            continue
        raw = RAW / path.relative_to(OUT)
        if not raw.exists():
            raw.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, raw)
        data = raw.read_bytes()
        text = clean(data.decode("utf-8", "replace"))
        if len(text.encode()) > LIMIT:
            lines = text.splitlines()
            text = "\n".join(lines[:120] + [f"... {len(lines) - 520} lines cut; see WHOLE-LOGS.txt ..."] + lines[-400:])
            big.append(f"{path.relative_to(OUT)} {len(data)} bytes sha256 {hashlib.sha256(data).hexdigest()} "
                       "(excerpt kept)")
            path.unlink()
            path = path.with_name(path.name + ".excerpt")
        path.write_text(text if text.endswith("\n") else text + "\n")
    if big:
        (OUT / "WHOLE-LOGS.txt").write_text("\n".join(big) + "\n")
    rows = ["# Receipts", "", "Generated from the files present by `scripts/finalize_receipts.py`. Host path "
            "prefixes in every text receipt are replaced by placeholders (`<work>`, `<checkout>`, `<lane-output>`, "
            "`<tmp>` and the like); nothing else in a receipt is changed.", "", "| File | Bytes | sha256 |",
            "|---|---:|---|"]
    for path in sorted(OUT.rglob("*")):
        if path.is_file() and path.name != "INDEX.md":
            data = path.read_bytes()
            rows.append(f"| `{path.relative_to(OUT)}` | {len(data)} | `{hashlib.sha256(data).hexdigest()}` |")
    (OUT / "INDEX.md").write_text("\n".join(rows) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
