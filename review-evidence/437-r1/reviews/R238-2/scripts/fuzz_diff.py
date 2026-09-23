#!/usr/bin/env python3
"""Seeded differential sweep: generate synthetic pages from container and leaf
fragments, keep those on which two walk revisions list different headings,
render each kept page with GitHub's Markdown API (gfm, repository context)
and classify it: regression (A agrees, B does not), fix (B agrees, A does
not), both-wrong, or no-diff.

Set FUZZ_MODE=no35 to drop type 3-5, PI and CDATA fragments and add nested prefixes.
Usage: fuzz_diff.py <seed> <count> <max-render> <walkA-root> <walkB-root> <out.jsonl> [jobs]
Every request/response is kept with its SHA-256.
"""
import concurrent.futures
import hashlib
import json
import random
import subprocess
import os
import sys

MODE = os.environ.get("FUZZ_MODE", "all")
sys.path.insert(0, sys.argv[0].rsplit("/", 1)[0])
from probe import CONTEXT, rendered_headings  # noqa: E402

PREFIXES = ["", "", "", "> ", ">", "- ", "  ", "   ", "    ", "1. ", "10. ", "   ", "* ",
            "[^1]: ", "\t", " - ", "> - ", "- > ", ">  ", "-   ", "2. ", "+ "]
LEAVES = ["text", "text", "more text", "<span>", "</span>", "<div>", "</div>", "<!--", "-->",
          "x <!-- y", "x --> y", "```", "~~~", "<pre>", "</pre>", "<? x", "?>", "<![CDATA[",
          "]]>", "<!X y", ">", "", "", "---", "***", "===", "| a | b |", "|---|---|",
          "text <? > <!-- ?>", "text `-->`", 'text <a title="-->">', '<a title="<!--">',
          "<textarea>", "[x](<a-->)", "text <!-- a --> b", "<!-->", "<b>", "</b>",
          "<custom-tag>", "- item", "1. item", "> q", "[^2]: note", "a <!-- b\nc --> d",
          "<!-- c -->", "text \\-->", "<div title=\"x\">", "</pre> tail", "<script>", "<x-y>"]


def page(rng):
    leaves = LEAVES if MODE != "no35" else [x for x in LEAVES if not any(k in x for k in ("<?", "<!X", "<![CDATA["))]
    prefixes = PREFIXES + (["  - ", "1.  ", "-\t", ">\t", "> > ", "   > ", " 1. ", "- - ", "    - "] if MODE == "no35" else [])
    lines = []
    for _ in range(rng.randint(3, 8)):
        if rng.random() < 0.22:
            lines.append("## X%d" % len(lines))
        else:
            lines.append(rng.choice(prefixes) + rng.choice(leaves))
    lines.append("## Z")
    return "\n".join(lines) + "\n"


HELPER = r'''
import json, sys
sys.path.insert(0, sys.argv[1])
import gen_toc
json.dump([[[l, r] for l, r, _ in gen_toc.headings(p)] for p in json.load(sys.stdin)], sys.stdout)
'''


def walk(root, pages):
    proc = subprocess.run([sys.executable, "-B", "-c", HELPER, root + "/scripts"],
                          input=json.dumps(pages).encode(), capture_output=True, check=True)
    return json.loads(proc.stdout)


def render(text):
    request = json.dumps({"text": text, "mode": "gfm", "context": CONTEXT}, sort_keys=True).encode()
    for _ in range(3):
        proc = subprocess.run(["gh", "api", "markdown", "--input", "-"], input=request,
                              capture_output=True, check=False)
        if proc.returncode == 0:
            break
    return request, proc.stdout, proc.returncode


def main():
    seed, count, cap = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    root_a, root_b, out_path = sys.argv[4], sys.argv[5], sys.argv[6]
    jobs = int(sys.argv[7]) if len(sys.argv) > 7 else 6
    rng = random.Random(seed)
    pages = list(dict.fromkeys(page(rng) for _ in range(count)))
    a, b = walk(root_a, pages), walk(root_b, pages)
    kept = [(p, x, y) for p, x, y in zip(pages, a, b) if x != y][:cap]
    print(f"generated {len(pages)} unique, {sum(x != y for x, y in zip(a, b))} differ, rendering {len(kept)}")
    tally = {}
    with concurrent.futures.ThreadPoolExecutor(jobs) as pool, open(out_path, "w") as out:
        for (text, x, y), (request, response, code) in zip(kept, pool.map(lambda k: render(k[0]), kept)):
            github = rendered_headings(response.decode())
            verdict = ("regression" if x == github and y != github else
                       "fix" if y == github and x != github else "both-wrong")
            if code != 0:
                verdict = "render-failed"
            tally[verdict] = tally.get(verdict, 0) + 1
            out.write(json.dumps({"page": text, "A": x, "B": y, "github": github, "verdict": verdict,
                                  "exit": code, "request_sha256": hashlib.sha256(request).hexdigest(),
                                  "response_sha256": hashlib.sha256(response).hexdigest(),
                                  "response_bytes": response.decode()}, sort_keys=True) + "\n")
    print(json.dumps(tally, sort_keys=True))


if __name__ == "__main__":
    main()
