#!/usr/bin/env python3
"""Copy the lane's records into the output directory, host paths replaced by
tokens; files over 200 KB stay in scratch and are listed by sha256 and size.

usage: collect.py <scratch rec dir> <output receipts dir> <name> [<name> ...]
       (each <name> is a file or directory under the rec dir)
"""
import csv, hashlib, re, sys
from pathlib import Path

LIMIT = 200 * 1024
SUBS = [
    (re.compile(r"<scratch>"), "<scratch>"),
    (re.compile(r"<lane>"), "<lane>"),
    (re.compile(r"<home>/\.local/share/containers/storage/overlay/[0-9a-f]+/diff"), "<toolroot>"),
    (re.compile(r"<tools>"), "<tools>"),
    (re.compile(r"<vendor>"), "<vendor>"),
    (re.compile(r"<home>"), "<home>"),
    (re.compile(r"<data>"), "<data>"),
    (re.compile(r"<tmp>/"), "<tmp>/"),
]

def clean(text: str) -> str:
    for rx, tok in SUBS:
        text = rx.sub(tok, text)
    return text

rec, out = Path(sys.argv[1]), Path(sys.argv[2])
ext_rows = []
for name in sys.argv[3:]:
    src = rec / name
    files = [src] if src.is_file() else sorted(p for p in src.rglob("*") if p.is_file())
    for f in files:
        rel = f.relative_to(rec)
        if any(part in ("obj_dir", "__pycache__") or part.startswith("obj_") for part in rel.parts):
            continue
        data = f.read_bytes()
        try:
            text = clean(data.decode("utf-8"))
            body = text.encode("utf-8")
        except UnicodeDecodeError:
            body = None
        if body is None or len(body) > LIMIT:
            ext_rows.append([str(rel), len(data), hashlib.sha256(data).hexdigest(),
                             "binary" if body is None else "over 200 KB"])
            continue
        dst = out / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(body)
csv_path = out / "EXTERNAL-RECORDS.csv"
old = list(csv.reader(csv_path.open())) if csv_path.exists() else [["scratch record", "bytes", "sha256", "why not here"]]
seen = {r[0] for r in old}
with csv_path.open("w", newline="") as fh:
    w = csv.writer(fh)
    for r in old:
        w.writerow(r)
    for r in ext_rows:
        if r[0] not in seen:
            w.writerow(r)
print(f"copied; {len(ext_rows)} kept in scratch")
