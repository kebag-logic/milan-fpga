#!/usr/bin/env python3
"""R238-2 renderer probe: render synthetic pages with GitHub's Markdown API
(gfm mode, repository context) and compare the heading list GitHub emits with
what three revisions of the Contents walk list.

Usage: probe.py <cases.json> <out.jsonl> <walk-root>...
  cases.json : [{"name": ..., "page": ...}, ...]
  walk-root  : label=path, where path/scripts holds that revision's gen_toc*.py

Every request and response is kept byte for byte with its SHA-256. Only
synthetic text is submitted; no repository page is sent.
"""
import datetime
import hashlib
import json
import subprocess
import sys
from html.parser import HTMLParser

CONTEXT = "kebag-logic/milan-fpga"

WALK_HELPER = r'''
import json, sys
sys.path.insert(0, sys.argv[1])
import gen_toc
pages = json.load(sys.stdin)
out = []
for page in pages:
    out.append({"headings": [[lvl, raw] for lvl, raw, _ in gen_toc.headings(page)],
                "blocks": gen_toc.blocks(page)})
json.dump(out, sys.stdout)
'''


class Headings(HTMLParser):
    """[level, collapsed text] of every h1..h6 element."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.found, self.level, self.text = [], 0, ""

    def handle_starttag(self, tag, attrs):
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.level, self.text = int(tag[1]), ""

    def handle_endtag(self, tag):
        if self.level and tag == f"h{self.level}":
            self.found.append([self.level, " ".join(self.text.split())])
            self.level = 0

    def handle_data(self, data):
        if self.level:
            self.text += data


def rendered_headings(html):
    parser = Headings()
    parser.feed(html)
    parser.close()
    return parser.found


def render(page):
    request = json.dumps({"text": page, "mode": "gfm", "context": CONTEXT},
                         sort_keys=True).encode()
    proc = subprocess.run(["gh", "api", "markdown", "--input", "-"],
                          input=request, capture_output=True, check=False)
    return request, proc.stdout, proc.returncode, proc.stderr.decode(errors="replace")


def walk(root, pages):
    proc = subprocess.run([sys.executable, "-B", "-c", WALK_HELPER, root + "/scripts"],
                          input=json.dumps(pages).encode(), capture_output=True, check=True)
    return json.loads(proc.stdout)


def main():
    cases = json.load(open(sys.argv[1], encoding="utf-8"))
    roots = [arg.split("=", 1) for arg in sys.argv[3:]]
    pages = [case["page"] for case in cases]
    walks = {label: walk(path, pages) for label, path in roots}
    with open(sys.argv[2], "w", encoding="utf-8") as out:
        for i, case in enumerate(cases):
            request, response, code, err = render(case["page"])
            html = response.decode()
            github = rendered_headings(html)
            row = {"name": case["name"], "page": case["page"],
                   "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                   "exit": code, "stderr": err,
                   "request_bytes": request.decode(),
                   "request_sha256": hashlib.sha256(request).hexdigest(),
                   "response_bytes": html,
                   "response_sha256": hashlib.sha256(response).hexdigest(),
                   "github": github}
            for label, _ in roots:
                row[label] = walks[label][i]["headings"]
                row[label + "_agrees"] = walks[label][i]["headings"] == github
            out.write(json.dumps(row, sort_keys=True) + "\n")
            verdicts = " ".join(f"{label}={'ok' if row[label + '_agrees'] else 'DIFF'}"
                                for label, _ in roots)
            print(f"{case['name']}: github={github} {verdicts} "
                  + " ".join(f"{label}={row[label]}" for label, _ in roots))


if __name__ == "__main__":
    main()
