#!/usr/bin/env python3
"""Value-blind scan for the external capture's channel count and sample format.

The two private values are the spans removed by the masking commits, as
recorded by mask_analysis.py in a private token file (never published).
Patterns are derived from them; only pattern IDs, paths, line numbers and
counts are printed, never a value.

Usage: privacy_scan.py <repo> <private-token-file> <pr-body-json> <label=rev:path-or-dir>...
  A target "label=FILE:<local path>" scans a local file instead.
"""
import json, re, subprocess, sys

REPO, TOKFILE, PRJSON = sys.argv[1:4]
targets = sys.argv[4:]
tok = json.load(open(TOKFILE))
CH = tok["SPAN1"]   # first removed span (docstrings, then the capture file name): the channel count
FMT = tok["SPAN2"]  # second removed span (the capture command's format argument): the format

n = re.sub(r"\D", "", CH)
words = {"1": "one", "2": "two", "4": "four", "6": "six", "8": "eight", "10": "ten",
         "12": "twelve", "16": "sixteen", "18": "eighteen", "20": "twenty",
         "24": "twenty-four", "32": "thirty-two", "64": "sixty-four"}
pats = {
    # a bare number is not distinctive; require capture/channel context
    "CH-near": rf"(?<![\d.,]){n}(?![\d.,]).{{0,40}}\b(chan|capture|cap-all|arecord)"
               rf"|\b(chan|capture|cap-all|arecord)[^\n]{{0,40}}(?<![\d.,#x]){n}(?![\d.,])",
    "CH-Nch": rf"(?<![\d.]){n}\s*-?ch\b",
    "CH-N-channel": rf"(?<![\d.,]){n}[- ]channels?\b",
    "CH-arg": rf"-c\s*{n}\b",
    "CH-NCH": rf"\bNCH\b[^\n]{{0,60}}(?<![\d.,]){n}(?![\d.,])",
}
# always present, so the pattern list itself says nothing about the value
pats["CH-word"] = rf"\b{words[n]}[- ]channels?\b" if n in words else r"(?!x)x"
pats["FMT-token"] = re.escape(FMT)
parts = [p for p in re.split(r"[_\W]+", FMT) if len(p) >= 2 and re.search(r"\d", p)]
pats["FMT-parts"] = "|".join(rf"(?<![A-Za-z0-9]){re.escape(p)}(?![A-Za-z0-9])" for p in parts) or r"(?!x)x"
pats["FMT-bitdepth-near-capture"] = r"\b(capture|arecord|cap-lr|cap-all)\b[^\n]{0,60}\b\d+[- ]?(bit|byte)s?\b|\b\d+[- ]?(bit|byte)s?\b[^\n]{0,60}\b(capture|arecord|cap-lr|cap-all)\b"
pats["FMT-nounderscore"] = re.escape(FMT.replace("_", ""))
cre = {k: re.compile(v, re.I) for k, v in pats.items()}
print("patterns:", sorted(cre))


def lines_of(rev, path):
    try:
        b = subprocess.run(["git", "-C", REPO, "show", f"{rev}:{path}"], check=True,
                           capture_output=True).stdout
    except subprocess.CalledProcessError:
        return None
    return b.decode("utf-8", "replace").splitlines()


def tree(rev, path):
    out = subprocess.run(["git", "-C", REPO, "ls-tree", "-r", "--name-only", rev, path],
                         check=True, capture_output=True).stdout.decode().split("\n")
    return [o for o in out if o]


total = 0
def scan(label, name, lines):
    global total
    hits = []
    for i, ln in enumerate(lines, 1):
        for k, c in cre.items():
            if c.search(ln):
                hits.append(f"{label}:{name}:{i} {k}")
    total += len(hits)
    for h in hits:
        print("HIT", h)
    return len(hits)


body = json.load(open(PRJSON))["body"].splitlines()
print(f"PR body: {scan('PR644-body', 'body', body)} hits in {len(body)} lines")
for t in targets:
    label, spec = t.split("=", 1)
    rev, path = spec.split(":", 1)
    if rev == "FILE":
        ls = open(path, encoding="utf-8", errors="replace").read().splitlines()
        print(f"{label}: {scan(label, path, ls)} hits")
        continue
    files = tree(rev, path)
    nh = nf = 0
    for f in files:
        ls = lines_of(rev, f)
        if ls is None:
            continue
        nf += 1
        nh += scan(label, f, ls)
    print(f"{label} ({rev[:8]}:{path}): {nh} hits in {nf} files")
print("TOTAL HITS", total)
