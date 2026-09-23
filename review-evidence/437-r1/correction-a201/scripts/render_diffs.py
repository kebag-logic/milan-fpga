#!/usr/bin/env python3
"""Render every page of a sweep diff with GitHub and classify the working
tree against the base: fix, regression (by direction), or both wrong."""
import json
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import render


def verdict(walk, gh):
    if walk == gh:
        return "AGREE"
    extra = [h for h in walk if h not in gh]
    missing = [h for h in gh if h not in walk]
    return "ESCAPE" if extra and not missing else "WITHHOLD" if missing and not extra else "MIXED"


def main():
    rows = json.loads(Path(sys.argv[1]).read_text())
    with ThreadPoolExecutor(max_workers=4) as pool:
        recs = list(pool.map(lambda r: render.render(r["page"]), rows))
    out, c = [], Counter()
    for r, rec in zip(rows, recs):
        gh = rec["headings"]
        vb, vp, vw = verdict(r["base"], gh), verdict(r["prev"], gh), verdict(r["work"], gh)
        cls = ("regression-" + vw if vb == "AGREE" and vw != "AGREE" else
               "fix" if vw == "AGREE" else "both-wrong")
        c[cls] += 1
        out.append({**r, "github": gh, "request_sha256": rec["request_sha256"],
                    "response_sha256": rec["response_sha256"], "base_v": vb, "prev_v": vp, "work_v": vw,
                    "class": cls})
    Path(sys.argv[2]).write_text(json.dumps(out, indent=1) + "\n")
    print(sys.argv[1], dict(c))


if __name__ == "__main__":
    main()
