#!/usr/bin/env python3
"""Walk a generated page set under the base, the reviewed head and the
working tree; write every page where the working tree differs from the base,
with all three answers."""
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import walks

BASE, PREV = "574c29fa111c74e5e5ed63e4670aff1f492e28e2", "e4906bfca65c61e7e109e3532ac1b2dd5b4c0096"


def chunked(rev, pages, n=8):
    size = (len(pages) + n - 1) // n
    parts = [pages[i:i + size] for i in range(0, len(pages), size)]
    with ThreadPoolExecutor(max_workers=n) as pool:
        out = list(pool.map(lambda p: walks.walk(rev, p), parts))
    return [h["headings"] for part in out for h in part]


def main():
    pages = json.loads(Path(sys.argv[1]).read_text())
    names, texts = list(pages), list(pages.values())
    res = {}
    for rev in (BASE, PREV, "work"):
        res[rev] = chunked(rev, texts)
    diff = []
    for i, name in enumerate(names):
        b, p, w = res[BASE][i], res[PREV][i], res["work"][i]
        if w != b:
            diff.append({"name": name, "page": texts[i], "base": b, "prev": p, "work": w})
    Path(sys.argv[2]).write_text(json.dumps(diff, indent=0))
    same_prev = sum(1 for d in diff if d["work"] == d["prev"])
    print(f"{len(names)} pages; work differs from base on {len(diff)}; of those equal to the reviewed head: {same_prev}")


if __name__ == "__main__":
    main()
