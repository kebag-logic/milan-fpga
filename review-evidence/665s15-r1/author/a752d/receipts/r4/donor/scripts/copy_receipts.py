"""Copy receipt files into the output directory with host paths replaced by placeholders; a file over 200 KB is not
copied, and its size and SHA-256 are appended to DST/not-copied.txt instead.
usage: python3 -I copy_receipts.py DST SRC... (a SRC directory is copied with its tree)"""
import hashlib, sys
from pathlib import Path
SUBS = [("$SCRATCH", "$SCRATCH"), ("$SCRATCH3", "$SCRATCH3"),
        ("$TMP", "$TMP"), ("$TOOLS", "$TOOLS"), ("$LANES", "$LANES"),
        ("$TOOLS2", "$TOOLS2"), ("$MGMT", "$MGMT"), ("$HOME", "$HOME"),
        ("$ACT", "$ACT"), ("$DATA", "$DATA")]
dst = Path(sys.argv[1]); dst.mkdir(parents=True, exist_ok=True)
skipped = []
def one(src: Path, out: Path):
    data = src.read_bytes()
    if len(data) > 200_000:
        skipped.append(f"{out.relative_to(dst)} {len(data)} {hashlib.sha256(data).hexdigest()}")
        return
    try:
        text = data.decode()
        for a, b in SUBS:
            text = text.replace(a, b)
        data = text.encode()
    except UnicodeDecodeError:
        pass
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(data)
for arg in sys.argv[2:]:
    src = Path(arg)
    if src.is_dir():
        for f in sorted(p for p in src.rglob("*") if p.is_file()):
            one(f, dst / src.name / f.relative_to(src))
    else:
        one(src, dst / src.name)
if skipped:
    with open(dst / "not-copied.txt", "a") as fh:
        fh.write("".join(s + "\n" for s in skipped))
print(f"copied into {dst}; {len(skipped)} file(s) recorded by hash only")
