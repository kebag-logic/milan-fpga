#!/usr/bin/env python3
"""Copy round-4 records into the output directory, host paths replaced by
tokens; files over 200 KB (and binaries) stay in scratch and are listed by
sha256 and size in EXTERNAL-RECORDS.csv.

usage: collect_r4.py <src> <dst>   (a file or a directory; build trees skipped)
"""
import csv
import hashlib
import re
import sys
from pathlib import Path

LIMIT = 200 * 1024
SUBS = [
    (re.compile(r"<parent>(-[a-e])?"), "<parent>"),
    (re.compile(r"<scratch>"), "<scratch>"),
    (re.compile(r"<lane>"), "<lane>"),
    (re.compile(r"<review-evidence>"), "<review-evidence>"),
    (re.compile(r"<home>/\.local/share/containers/storage/overlay/[0-9a-f]+/diff"), "<toolroot>"),
    (re.compile(r"<tools>"), "<tools>"),
    (re.compile(r"<management>"), "<management>"),
    (re.compile(r"<home>"), "<home>"),
    (re.compile(r"<data>"), "<data>"),
    (re.compile(r"<tmp>/"), "<tmp>/"),
]
SKIP_DIRS = {"obj_dir", "__pycache__", "scratch", "tree", "head-tree", "base-tree",
             "s2", "repark", "repark-mut", "camp"}  # source exports stay in scratch


def clean(text: str) -> str:
    for rx, tok in SUBS:
        text = rx.sub(tok, text)
    return text


def skipped(rel: Path) -> bool:
    return any(p in SKIP_DIRS or p.startswith("obj_") or p.startswith("tree-")
               for p in rel.parts)


src, dst = Path(sys.argv[1]), Path(sys.argv[2])
csv_path = Path(sys.argv[3]) if len(sys.argv) > 3 else None
files = [src] if src.is_file() else sorted(p for p in src.rglob("*") if p.is_file())
ext_rows = []
for f in files:
    rel = Path(f.name) if src.is_file() else f.relative_to(src)
    if skipped(rel):
        continue
    data = f.read_bytes()
    try:
        body = clean(data.decode("utf-8")).encode("utf-8")
    except UnicodeDecodeError:
        body = None
    out = dst if src.is_file() else dst / rel
    if body is None or len(body) > LIMIT:
        ext_rows.append([clean(str(f)), len(data), hashlib.sha256(data).hexdigest(),
                         "binary" if body is None else "over 200 KB"])
        continue
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(body)
if csv_path is not None:
    old = (list(csv.reader(csv_path.open())) if csv_path.exists()
           else [["scratch record", "bytes", "sha256", "why not here"]])
    seen = {r[0] for r in old}
    with csv_path.open("w", newline="") as fh:
        w = csv.writer(fh)
        for r in old:
            w.writerow(r)
        for r in ext_rows:
            if r[0] not in seen:
                w.writerow(r)
print(f"{src.name}: copied; {len(ext_rows)} kept in scratch")
