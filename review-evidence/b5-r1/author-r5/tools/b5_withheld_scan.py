#!/usr/bin/env python3
"""Scan for the withheld capture sizes and the capture's channel count.

usage: b5_withheld_scan.py <archive_git_dir> <repo> <range>[,<range>...] <path>...

Built in memory and never written:
  - the withheld sizes: every RAW-ARTIFACTS.json size that archive commit 9006c78e
    withholds, read from 8e6be432, and every `cap-all-<n>ch.raw` size in the
    8e6be432 run logs;
  - the capture's channel count, from the page at e216dfe4 (an every-channel row's
    size over its seconds x 48,000 x 3 bytes).

Labels:
  withheld size         a withheld size, as digits or with thousands commas
  capture channel count the count before "channels", "ch", "-channel" or
                        "capture channels", as digits or as a word

Searched: every file under each <path>, the lines each range adds, and each range's
commit messages. A hit prints the label and the place only. Positive control, in
memory before the scan: one planted line per value and form must hit.
"""
import glob
import json
import os
import re
import subprocess
import sys

OLD, NEW, PAGE_REV = ("8e6be4329008137a152f9171638e48a43e549fb7",
                      "9006c78e354d5a2f244fd606c55790a825304bd3",
                      "e216dfe4f0cab7b0c7352d7973acb4d33c157f70")
ROOT = "review-evidence/b5-r1/author"
WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
         "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
         "seventeen", "eighteen", "nineteen", "twenty", "twenty-one", "twenty-two",
         "twenty-three", "twenty-four", "twenty-five", "twenty-six", "twenty-seven",
         "twenty-eight", "twenty-nine", "thirty", "thirty-one", "thirty-two"]


def show(gitdir, rev, path):
    return subprocess.run(["git", "-C", gitdir, "show", f"{rev}:{path}"], check=True,
                          capture_output=True, text=True).stdout


def build(archive, repo):
    a = json.loads(show(archive, OLD, f"{ROOT}/RAW-ARTIFACTS.json"))["files"]
    b = json.loads(show(archive, NEW, f"{ROOT}/RAW-ARTIFACTS.json"))["files"]
    sizes = {x["bytes"] for x, y in zip(a, b) if not isinstance(y["bytes"], int)}
    for run in ("a-long", "diag1", "cap-test1"):
        for m in re.finditer(r'"file": "cap-all-<n>ch\.raw", "bytes": (\d+)',
                             show(archive, OLD, f"{ROOT}/runs/{run}/console.txt")):
            sizes.add(int(m.group(1)))
    counts = set()
    for line in show(repo, PAGE_REV, "docs/findings/117_AUDIO_CONTINUITY.md").splitlines():
        m = re.match(r"\| .*every channel, (\d+) s \| (\d+) \|", line)
        if m:
            q, r = divmod(int(m.group(2)), int(m.group(1)) * 48000 * 3)
            if r == 0:
                counts.add(q)
    assert len(counts) == 1 and sizes
    n = counts.pop()
    pats = []
    for s in sorted(sizes):
        pats.append(("withheld size", re.compile(rf"(?<![\d,]){s}(?!\d)")))
        pats.append(("withheld size", re.compile(rf"(?<![\d,]){s:,}(?![\d,])")))
    forms = [str(n)] + ([WORDS[n]] if n < len(WORDS) else [])
    alt = "|".join(re.escape(f) for f in forms)
    pats.append(("capture channel count",
                 re.compile(rf"(?<![\w.-])(?:{alt})(?:\s*-?\s*(?:capture\s+)?channels?\b|\s*ch\b|-?ch\.raw)", re.I)))
    plants = [f"x {s} y" for s in sorted(sizes)] + [f"x {s:,} y" for s in sorted(sizes)]
    plants += [f"a {f} channels b" for f in forms] + [f"a {n}ch b"]
    return sizes, n, pats, plants


def main(archive, repo, ranges, paths):
    sizes, n, pats, plants = build(archive, repo)
    ctl = all(any(rx.search(p) for _, rx in pats) for p in plants)
    each = all(any(rx.search(p) for p in plants) for _, rx in pats)
    print(f"built in memory: {len(sizes)} withheld size(s) and the capture's channel count; "
          f"{len(pats)} patterns; labels {sorted({l for l, _ in pats})}")
    print(f"positive control in memory: every planted line hits: {ctl}; every pattern hits a plant: {each}")
    if not (ctl and each):
        print("positive control FAILED; scan not run")
        return 2
    texts = []
    for rng in ranges.split(","):
        diff = subprocess.run(["git", "-C", repo, "diff", "-U0", rng], check=True,
                              capture_output=True, text=True).stdout
        cur, k = None, 0
        for line in diff.splitlines():
            if line.startswith("+++ "):
                cur = line[6:]
            elif line.startswith("@@"):
                k = int(re.search(r"\+(\d+)", line).group(1))
            elif line.startswith("+"):
                texts.append((f"{rng} added {cur}", k, line[1:]))
                k += 1
        log = subprocess.run(["git", "-C", repo, "log", "--format=%B", rng], check=True,
                             capture_output=True, text=True).stdout
        for i, line in enumerate(log.splitlines(), 1):
            texts.append((f"{rng} commit messages", i, line))
    nfiles = 0
    for p in paths:
        for f in sorted(glob.glob(os.path.join(p, "**"), recursive=True)) if os.path.isdir(p) else [p]:
            if os.path.isfile(f):
                nfiles += 1
                for i, line in enumerate(open(f, errors="replace").read().splitlines(), 1):
                    texts.append((os.path.relpath(f, p) if os.path.isdir(p) else os.path.basename(f), i, line))
    hits = 0
    for place, i, line in texts:
        for lab, rx in pats:
            if rx.search(line):
                hits += 1
                print(f"HIT {lab}: {place}:{i}")
    print(f"scanned: {nfiles} files, {len(texts)} lines in all")
    print(f"hits: {hits}")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]))
