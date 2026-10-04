"""Name the delimited table blocks in which a page and a tables.md differ."""
import re, sys
from pathlib import Path
BLOCK = re.compile(r"<!-- table: ([a-z0-9-]+) -->\n(.*?)<!-- end table: \1 -->", re.S)
page = dict(BLOCK.findall(Path(sys.argv[1]).read_text()))
fresh = dict(BLOCK.findall(Path(sys.argv[2]).read_text()))
diff = sorted(n for n in page if page[n] != fresh.get(n))
print(f"{len(page)} page blocks, {len(page) - len(diff)} equal, differing: {diff}")
for n in diff:
    a, b = page[n].splitlines(), fresh.get(n, "").splitlines()
    for line in a:
        if line not in b: print(f"  - {n}: {line[:200]}")
    for line in b:
        if line not in a: print(f"  + {n}: {line[:200]}")
