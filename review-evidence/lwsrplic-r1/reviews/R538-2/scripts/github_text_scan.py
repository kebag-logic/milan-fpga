#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Scan a repository's issue and pull-request titles, bodies and comments.

Usage: TERMS_FILE=<terms> github_text_scan.py <owner/repo>
Read-only GitHub API calls through the GitHub CLI.  Reports locations only,
with the matched term replaced by [TERM<n>].
"""
import json
import os
import re
import subprocess
import sys


def api(path):
    out = subprocess.run(["gh", "api", "--paginate", "--slurp", path],
                         capture_output=True, check=True).stdout
    return [x for page in json.loads(out) for x in page]


def main():
    repo = sys.argv[1]
    pats = [re.compile(t.strip(), re.I) for t in open(os.environ["TERMS_FILE"])
            if t.strip()]
    items = api(f"repos/{repo}/issues?state=all&per_page=100")
    hits = 0
    texts = []
    for it in items:
        kind = "pr" if "pull_request" in it else "issue"
        texts.append((f"{kind} #{it['number']} title+body", (it["title"] or "") + "\n" + (it["body"] or "")))
        for c in api(f"repos/{repo}/issues/{it['number']}/comments?per_page=100"):
            texts.append((f"{kind} #{it['number']} comment {c['id']}", c["body"] or ""))
        if kind == "pr":
            for c in api(f"repos/{repo}/pulls/{it['number']}/comments?per_page=100"):
                texts.append((f"pr #{it['number']} review-comment {c['id']}", c["body"] or ""))
            for c in api(f"repos/{repo}/pulls/{it['number']}/reviews?per_page=100"):
                texts.append((f"pr #{it['number']} review {c['id']}", c["body"] or ""))
    for where, text in texts:
        for n, p in enumerate(pats):
            for ln, line in enumerate(text.split("\n"), 1):
                if p.search(line):
                    hits += 1
                    print(f"HIT {where} line {ln} [TERM{n}]")
    print(f"items={len(items)} texts={len(texts)} hits={hits}")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
