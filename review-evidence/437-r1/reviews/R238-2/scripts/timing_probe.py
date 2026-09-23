#!/usr/bin/env python3
"""Wall time of blocks() on adversarial single pages, for one walk revision.
Usage: timing_probe.py <walk-root>"""
import sys
import time

sys.path.insert(0, sys.argv[1] + "/scripts")
import gen_toc  # noqa: E402

N = 4000
PAGES = {
    "inline open tag, many bare attributes, no closer": "text <a" + " b" * N + "\n\n## X\n",
    "inline open tag, many valued attributes, no closer": "text <a" + " b=c" * N + "\n\n## X\n",
    "inline tag spread over many lines": "text <a\n" + "b\n" * N + "\n## X\n",
    "raw tag, many attributes, no closer": "<div\n" + "a=\"b\" " * N + "\n\n## X\n",
    "raw run of many opener-free lines": "<div>\n" + "x <y\n" * N + "\n## X\n",
    "backtick runs without closers": "text " + "`" * 1 + " a `` b" * N + "\n\n## X\n",
    "long paragraph of escapes": "text " + "\\<a " * N + "\n\n## X\n",
    "many list items": "- a\n" * N + "\n## X\n",
    "deeply nested quotes": "> " * 200 + "a\n\n## X\n",
    "deeply nested items": "".join("  " * i + "- a\n" for i in range(200)) + "\n## X\n",
}
PAGES.update({"after an open raw comment: " + k: "<div>\n<!--\n\n" + v for k, v in list(PAGES.items())})
for name, page in PAGES.items():
    start = time.perf_counter()
    gen_toc.blocks(page)
    print(f"{time.perf_counter() - start:8.3f}s  {len(page):7d} chars  {name}")
