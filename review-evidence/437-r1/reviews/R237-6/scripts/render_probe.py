#!/usr/bin/env python3
"""Reviewer render probe: GitHub's Markdown API against the walk, for raw
wrapper tags the recorded shape set does not carry.

Each request is POST /markdown (through `gh api --input`), stateless and
creating nothing. Exact request and response bytes are kept with their
sha256 and UTC time. The walk's headings (`gen_toc.headings()` of the tree
given) are recorded beside GitHub's headings read with the walk's own
HTML parse (`anchored_headings_of` for `markdown` mode, `headings_of` for
`gfm`).

Usage: render_probe.py PYTHON HEAD_TREE OUT_JSON
"""
import datetime
import hashlib
import json
import subprocess
import sys

TAGS = ("noscript", "template", "svg", "math")
PROBES = ([(tag, "markdown") for tag in TAGS]
          + [(tag, "gfm") for tag in ("noscript", "template")])


def page(tag: str) -> str:
    return f"## A\n\n<{tag}>\n\n## Mid\n\n</{tag}>\n\n## B\n"


READ = r"""
import json, sys
sys.path.insert(0, sys.argv[1] + "/scripts")
import gen_toc, gen_toc_renderer as r
rec = json.load(open(sys.argv[2]))
for row in rec:
    row["walk_headings"] = [list(h) for h in gen_toc.headings(row["page"])]
    html = row["response_bytes"]
    row["github_headings"] = ([list(h) for h in r.anchored_headings_of(html)]
                              if row["mode"] == "markdown"
                              else [list(h) for h in r.headings_of(html)])
json.dump(rec, open(sys.argv[2], "w"), indent=1)
"""


def main() -> int:
    py, tree, out = sys.argv[1:]
    rows = []
    for tag, mode in PROBES:
        text = page(tag)
        request = json.dumps({"text": text, "mode": mode,
                              "context": "kebag-logic/milan-fpga"})
        when = datetime.datetime.now(datetime.timezone.utc).isoformat(
            timespec="seconds")
        r = subprocess.run(["gh", "api", "-X", "POST", "/markdown",
                            "--input", "-"], input=request.encode(),
                           capture_output=True)
        response = r.stdout.decode("utf-8", "replace")
        rows.append({"name": f"{tag} wrapper", "tag": tag, "mode": mode,
                     "page": text, "rc": r.returncode,
                     "request_bytes": request,
                     "request_sha256": hashlib.sha256(
                         request.encode()).hexdigest(),
                     "response_bytes": response,
                     "response_sha256": hashlib.sha256(r.stdout).hexdigest(),
                     "recorded_utc": when})
    with open(out, "w") as fh:
        json.dump(rows, fh, indent=1)
    subprocess.run([py, "-c", READ, tree, out], check=True)
    for row in json.load(open(out)):
        print(f"{row['tag']:9} {row['mode']:8} rc={row['rc']} "
              f"github={row['github_headings']} walk={row['walk_headings']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
