#!/usr/bin/env python3
"""[R238] the author's published renderer receipt against independent renders.

Reads the JSON lines of the public [A168] FACTUAL RENDERER RECEIPT (issue
#437 comment 5775985191, fetched into scratch/issue437-comments.json), renders
each published `page` independently (cached with the probes), and compares
the response bytes and heading lists; it also re-derives the base and head
walk answers the receipt states.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_render as probes  # noqa: E402


def main() -> int:
    comments = json.loads((probes.SCRATCH / "issue437-comments.json").read_text())["comments"]
    body = next(c["body"] for c in comments
                if c["url"].endswith("5775985191"))
    # The pages themselves carry fences, so the block ends at its own
    # closing fence line followed by the details closer.
    block = re.search(r"```json\n(.*?)\n```\s*</details>", body, re.S).group(1)
    rows = [json.loads(line) for line in block.splitlines() if line.strip()]
    cache = probes.load_cache()
    same_html = same_heads = walks_ok = 0
    lines = []
    for r in rows:
        got = probes.render(r["page"], cache)
        mine = [s for _, s in probes.rendered_headings(got["response"])]
        html_equal = got["response"] == r["html"]
        heads_equal = mine == r["github"]
        walks = ([h[1] for h in probes.BASE.headings(r["page"])] == r["base"]
                 and [h[1] for h in probes.HEAD.headings(r["page"])] == r["head"])
        same_html += html_equal
        same_heads += heads_equal
        walks_ok += walks
        if not (html_equal and heads_equal and walks):
            lines.append(f"  {r['id']}: html_equal={html_equal} headings_equal={heads_equal} "
                         f"walks_equal={walks}")
    lines.insert(0, f"{len(rows)} published rows: response bytes identical {same_html}, "
                    f"heading lists identical {same_heads}, base/head walk answers "
                    f"reproduced {walks_ok}")
    (probes.OUT / "receipts" / "author-receipt-check.txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
