#!/usr/bin/env python3
"""Deterministic container x tag-column x follower matrix (the R237-2 F1 class,
rebuilt independently): walk every page under two revisions, render the pages
on which they differ, and classify them as fuzz_diff.py does.

Usage: matrix_diff.py <walkA-root> <walkB-root> <out.jsonl> [jobs]
"""
import concurrent.futures
import hashlib
import json
import sys

sys.path.insert(0, sys.argv[0].rsplit("/", 1)[0])
from fuzz_diff import render, walk  # noqa: E402
from probe import rendered_headings  # noqa: E402

F = "```"
PREFIXES = {
    "live bullet": "- item", "resumed bullet": "- item\n\n  text", "live ordered": "1. item",
    "two-digit live": "10. item", "two-digit resumed": "10. item\n\n    text",
    "nested quote": "- item\n  > quote", "nested bullet": "- item\n  - nested",
    "nested footnote": "- item\n  [^1]: note", "table in item": "- item\n\n  | a |\n  | - |",
    "setext in item": "- item\n\n  text\n  ---", "quote-first item": "- > quote",
    "empty item": "-", "empty item gains": "-\n  text", "lazy": "- item\nlazy",
    "quote nested list": "> - item", "footnote": "[^1]: note", "task": "- [ ] item",
    "thematic in item": "- item\n  ***", "fence in item": "- item\n  " + F + "\n  x\n  " + F,
}
TAGS = ["<span>", "</span>", "<custom-tag>"]
FOLLOWERS = {
    "heading": "## Old\n",
    "fence": F + "\n\n## Old\n" + F + "\n",
    "in-item fence": "  " + F + "\n\ntext\n\n" + F + "\n## Old\n" + F + "\n",
    "comment": "<!--\n\n## Old\n-->\n",
    "pre": "<pre>\n\n## Old\n</pre>\n",
    "in-item comment": "  <!--\n\n## Old\n",
}


def pages():
    for pname, prefix in PREFIXES.items():
        for col in range(6):
            for tag in TAGS:
                for fname, follow in FOLLOWERS.items():
                    yield (f"{pname} | col {col} {tag} | {fname}",
                           f"{prefix}\n{' ' * col}{tag}\n{follow}\n## Real\n")


def main():
    root_a, root_b, out_path = sys.argv[1:4]
    jobs = int(sys.argv[4]) if len(sys.argv) > 4 else 3
    rows = list(pages())
    a, b = walk(root_a, [p for _, p in rows]), walk(root_b, [p for _, p in rows])
    kept = [(n, p, x, y) for (n, p), x, y in zip(rows, a, b) if x != y]
    print(f"matrix {len(rows)} pages, {len(kept)} differ")
    tally = {}
    with concurrent.futures.ThreadPoolExecutor(jobs) as pool, open(out_path, "w") as out:
        for (name, text, x, y), (request, response, code) in zip(kept, pool.map(lambda k: render(k[1]), kept)):
            github = rendered_headings(response.decode())
            verdict = ("render-failed" if code else "regression" if x == github and y != github else
                       "fix" if y == github and x != github else "both-wrong")
            tally[verdict] = tally.get(verdict, 0) + 1
            out.write(json.dumps({"name": name, "page": text, "A": x, "B": y, "github": github,
                                  "verdict": verdict, "exit": code,
                                  "request_sha256": hashlib.sha256(request).hexdigest(),
                                  "response_sha256": hashlib.sha256(response).hexdigest(),
                                  "response_bytes": response.decode()}, sort_keys=True) + "\n")
            out.flush()
    print(json.dumps(tally, sort_keys=True))


if __name__ == "__main__":
    main()
