"""Copy receipts into the output directory, scrubbed of host paths and bounded
in size, and write receipts/INDEX.md from the files present.

usage: receipts.py <out-dir> <label>=<source> [<label>=<source> ...]
       receipts.py <out-dir> --index-only

A source directory contributes its *.log, *.json, *.rc, *.txt, *.md and
*.patch files to <out-dir>/receipts/<label>/; a source file is copied to
<out-dir>/receipts/<label>. Host paths become placeholders. A file over the
size cap keeps its head and tail with a marked elision and the full file's
SHA-256, so the index never cites a file it does not hold.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

CAP = 190 * 1024
SUBS = [
    ("<parent-a>", "<parent-a>"),
    ("<parent-b>", "<parent-b>"),
    ("<parent-c>", "<parent-c>"),
    ("<parent-snapshot>", "<parent-snapshot>"),
    ("<lane-clone-make>", "<lane-clone-make>"),
    ("<lane-clone-mutants>", "<lane-clone-mutants>"),
    ("<base-clone-make>", "<base-clone-make>"),
    ("<base-clone-mutants>", "<base-clone-mutants>"),
    ("<base-clone>", "<base-clone>"),
    ("<probe-tree>", "<probe-tree>"),
    ("<scratch>", "<scratch>"),
    ("<pinned-tool-bin>", "<pinned-tool-bin>"),
    ("<lane>", "<lane>"),
    ("<pinned-verilator>", "<pinned-verilator>"),
    ("<pinned-sv2v>", "<pinned-sv2v>"),
    ("<tools>", "<tools>"),
    ("<home>/.local/share/containers/storage/overlay/"
     "9517af577e2019496be7a9f3df0cdeafba0a4f827989b59cb358abf6403fbbde/diff",
     "<pinned-verilator-root>"),
    ("<management>", "<management>"),
    ("<home>", "<home>"),
    ("<data>", "<data>"),
]
KEEP = {".log", ".json", ".rc", ".txt", ".md", ".patch", ".tsv"}


def scrub(text: str) -> str:
    for a, b in SUBS:
        text = text.replace(a, b)
    return re.sub(r"/tmp/engine-mutants-[A-Za-z0-9_]+", "<mutants-tmp>", text)


def copy(src: Path, dst: Path) -> None:
    text = scrub(src.read_bytes().decode("utf-8", errors="replace"))
    if src.suffix != ".py":
        text = re.sub(r"(?<![\w<>])/tmp/", "<tmp>/", text)
    data = text.encode()
    if len(data) > CAP:
        data = (data[: CAP // 2] + b"\n[... elided: the full scrubbed file is "
                + str(len(data)).encode() + b" bytes, SHA-256 "
                + hashlib.sha256(data).hexdigest().encode() + b" ...]\n"
                + data[-CAP // 2:])
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(data)


def index(out: Path) -> None:
    rec = out / "receipts"
    lines = ["# Receipts index", "", "Generated from the files present under this directory.", "",
             "| File | Bytes | SHA-256 | Note |", "|---|---:|---|---|"]
    for p in sorted(x for x in rec.rglob("*") if x.is_file() and x.name != "INDEX.md"):
        data = p.read_bytes()
        note = ""
        if p.suffix == ".json":
            try:
                row = json.loads(data)
                if isinstance(row, dict) and "exit_code" in row:
                    note = f"rc {row['exit_code']}"
            except ValueError:
                pass
        if b"[... elided:" in data:
            note = (note + "; " if note else "") + "head and tail kept"
        lines.append(f"| `{p.relative_to(rec)}` | {len(data)} | `{hashlib.sha256(data).hexdigest()[:16]}` | {note} |")
    (rec / "INDEX.md").write_text("\n".join(lines) + "\n")


def main() -> None:
    out = Path(sys.argv[1])
    if sys.argv[2:] != ["--index-only"]:
        for arg in sys.argv[2:]:
            label, _, src = arg.partition("=")
            src = Path(src)
            if src.is_dir():
                for f in sorted(src.iterdir()):
                    if f.is_file() and f.suffix in KEEP:
                        copy(f, out / "receipts" / label / f.name)
            else:
                copy(src, out / "receipts" / label)
    index(out)


if __name__ == "__main__":
    main()
