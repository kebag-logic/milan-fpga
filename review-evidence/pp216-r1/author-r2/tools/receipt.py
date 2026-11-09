#!/usr/bin/env python3
"""receipt.py copy <src>... <dst-dir> | index <root>

copy: copy text files into <dst-dir>, host paths replaced by placeholders; a file over 200 KB (after
scrubbing) or a binary is not copied but listed with its size and full sha256 in <dst-dir>/RAW-RECORDS.txt.
Directories are copied recursively.
index: write INDEX.md in <root> and every directory under it, from the files present.
"""
import hashlib
import sys
from pathlib import Path

LIMIT = 200 * 1024
RULES = [  # longest first
    ("$HOME/milan-fpga-management/2026-09-23/pp216-a754b", "<out>"),
    ("$HOME/milan-fpga-management/2026-09-23/pp216-a754", "<round1-out>"),
    ("$HOME/milan-fpga-management", "<mgmt>"),
    ("$LANES/trusted-dev-20261109-ac0a01e3", "<parent-source>"),
    ("$LANES/665-s6b-cosim", "<cosim-lane>"),
    ("$LANES/pp216-mrp-applicant", "<lane>"),
    ("$VALIDATION_STORAGE/scratch/pp216-parent", "<parent>"),
    ("$VALIDATION_STORAGE/scratch/pp216-a754b", "<scratch>"),
    ("$VALIDATION_STORAGE/scratch/pp216-a754", "<round1-scratch>"),
    ("$VALIDATION_STORAGE/scratch", "<scratch-root>"),
    ("$LANES", "<lanes>"),
    ("$VALIDATION_TOOLS", "<toolchain>"),
    ("$VALIDATION_STORAGE", "<data>"),
    ("$HOME", "<home>"),
    ("/tmp/", "<tmp>/"),
]


def scrub(text: str) -> str:
    for a, b in RULES:
        text = text.replace(a, b)
    return text


def copy_one(src: Path, dst: Path, raw: list) -> None:
    data = src.read_bytes()
    try:
        text = scrub(data.decode("utf-8"))
    except UnicodeDecodeError:
        raw.append((dst, len(data), hashlib.sha256(data).hexdigest(), "binary"))
        return
    out = text.encode()
    if len(out) > LIMIT:
        raw.append((dst, len(data), hashlib.sha256(data).hexdigest(), "over 200 KB"))
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(out)


def copy(srcs: list, dst_dir: Path) -> None:
    raw = []
    for s in map(Path, srcs):
        if s.is_dir():
            for f in sorted(p for p in s.rglob("*") if p.is_file()):
                copy_one(f, dst_dir / s.name / f.relative_to(s), raw)
        else:
            copy_one(s, dst_dir / s.name, raw)
    if raw:
        dst_dir.mkdir(parents=True, exist_ok=True)
        with (dst_dir / "RAW-RECORDS.txt").open("a") as f:
            for d, n, h, why in raw:
                f.write(f"{d.relative_to(dst_dir)}\t{n} bytes\tsha256 {h}\t{why}, not copied\n")


def index(root: Path) -> None:
    for d in sorted([root] + [p for p in root.rglob("*") if p.is_dir()]):
        files = sorted(p for p in d.rglob("*") if p.is_file() and p.name != "INDEX.md")
        rows = []
        for f in files:
            data = f.read_bytes()
            rows.append(f"| `{f.relative_to(d)}` | {len(data)} | `{hashlib.sha256(data).hexdigest()[:16]}` |")
        title = "." if d == root else str(d.relative_to(root))
        (d / "INDEX.md").write_text(
            f"# Index of `{title}`\n\nGenerated from the files present (sha256 truncated to 16 hex).\n\n"
            "| File | Bytes | sha256 |\n|---|---|---|\n" + "\n".join(rows) + "\n")


def main() -> int:
    if sys.argv[1] == "copy":
        copy(sys.argv[2:-1], Path(sys.argv[-1]))
    elif sys.argv[1] == "index":
        index(Path(sys.argv[2]))
    else:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
