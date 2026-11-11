"""endpoint_compare.py BASE_TREE BASE_OUT HEAD_TREE HEAD_OUT: every file of two exports, byte for byte after the roots."""
import hashlib, json, sys
from pathlib import Path
bt, bo, ht, ho = map(Path, sys.argv[1:5])
def files(root):
    return {p.relative_to(root).as_posix(): p for p in sorted(root.rglob("*")) if p.is_file()}
import re
TIME = re.compile(rb"()\d{4}-\d\d-\d\d[ T]\d\d:\d\d:\d\d")
TREE_LINE = re.compile(rb"^.*[\xe2][\x94\x95][\x80-\xbf].*\n", re.M)   # box-drawing lines of the hierarchy tree
def norm(data, tree, out):
    data = data.replace(str(out).encode(), b"@OUT@").replace(str(tree).encode(), b"@TREE@")
    return TREE_LINE.sub(b"", TIME.sub(rb"\1@TIME@", data))
#: the run's log is not an output of the image: its timestamps and its interleaving of two streams vary
LOGS = {"litex.log"}
b = {k: v for k, v in files(bo).items() if k not in LOGS}
h = {k: v for k, v in files(ho).items() if k not in LOGS}
rows, same = [], 0
for name in sorted(set(b) | set(h)):
    if name not in b or name not in h:
        rows.append({"file": name, "verdict": "only in " + ("head" if name not in b else "base")}); continue
    x, y = norm(b[name].read_bytes(), bt, bo), norm(h[name].read_bytes(), ht, ho)
    raw = b[name].read_bytes() == h[name].read_bytes()
    v = "identical" if x == y else "DIFFERENT"
    same += x == y
    rows.append({"file": name, "verdict": v, "raw_identical": raw, "bytes": len(y),
                 "sha256_normalised": hashlib.sha256(y).hexdigest()})
bad = [r for r in rows if r["verdict"] != "identical"]
print(json.dumps({"files": len(rows), "identical": same, "different": bad, "rows": rows}, indent=1))
sys.exit(1 if bad else 0)
