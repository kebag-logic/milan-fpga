"""export_compare.py BASE_TREE BASE_OUT HEAD_TREE HEAD_OUT: every file of two SoC exports,
byte for byte after normalising the two checkout roots, the two output roots, run
timestamps and LiteX's box-drawing hierarchy-tree lines. litex.log is skipped.
Prints a JSON verdict; exit 0 when every file is identical, 1 otherwise."""
import hashlib
import json
import re
import sys
from pathlib import Path

bt, bo, ht, ho = map(Path, sys.argv[1:5])
TIME = re.compile(rb"\d{4}-\d\d-\d\d[ T]\d\d:\d\d:\d\d")
TREE_LINE = re.compile(rb"^.*\xe2[\x94\x95][\x80-\xbf].*\n", re.M)
SKIP = {"litex.log"}


def files(root: Path) -> dict:
    return {p.relative_to(root).as_posix(): p for p in sorted(root.rglob("*"))
            if p.is_file() and p.name not in SKIP}


def norm(data: bytes, tree: Path, out: Path) -> bytes:
    data = data.replace(str(out).encode(), b"@OUT@").replace(str(tree).encode(), b"@TREE@")
    return TREE_LINE.sub(b"", TIME.sub(b"@TIME@", data))


b, h = files(bo), files(ho)
rows = []
for name in sorted(set(b) | set(h)):
    if name not in b or name not in h:
        rows.append({"file": name, "verdict": "only in " + ("head" if name not in b else "base")})
        continue
    x, y = norm(b[name].read_bytes(), bt, bo), norm(h[name].read_bytes(), ht, ho)
    rows.append({"file": name, "verdict": "identical" if x == y else "DIFFERENT",
                 "raw_identical": b[name].read_bytes() == h[name].read_bytes(), "bytes": len(y),
                 "sha256_normalised": hashlib.sha256(y).hexdigest()})
bad = [r for r in rows if r["verdict"] != "identical"]
print(json.dumps({"files": len(rows), "identical": len(rows) - len(bad), "different": bad, "rows": rows}, indent=1))
sys.exit(1 if bad else 0)
