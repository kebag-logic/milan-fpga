"""Scratch: compare two LiteX tops with every comment removed (the header tree's order and dates vary)."""
import hashlib, re, sys
from pathlib import Path
def code(p):
    t = Path(p).read_text()
    t = re.sub(r"/\*.*?\*/", "", t, flags=re.S)
    t = re.sub(r"//[^\n]*", "", t)
    return "\n".join(line.rstrip() for line in t.splitlines() if line.strip())
digests = {p: hashlib.sha256(code(p).encode()).hexdigest() for p in sys.argv[1:]}
for p, d in digests.items():
    print(d[:16], p)
print("ALL EQUAL" if len(set(digests.values())) == 1 else "DIFFER")
