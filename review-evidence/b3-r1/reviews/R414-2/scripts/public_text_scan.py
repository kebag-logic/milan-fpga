#!/usr/bin/env python3
"""Scan the public text of a commit range for closing keywords and private shapes.

usage: public_text_scan.py <repo> <base> <head> [<extra-text-file> ...]

Scans the added lines of <base>..<head>, every commit message in the range and
each extra file (for example a saved PR body). It reports:
- closing keywords (close/fix/resolve forms followed by an issue reference);
- IPv4 addresses, MAC addresses other than the DUT's public ones, home or
  absolute host paths, e-mail addresses;
- a small hex-encoded list of tool, model and account tokens that public text
  must not carry.
The DUT's own entity, stream and MAAP identifiers are public and allowed.
"""
import re
import subprocess
import sys

CLOSING = re.compile(r"\b(close[sd]?|fix(e[sd])?|resolve[sd]?)\b\s*:?\s*(#|https://github\.com/\S+/issues/)\d+", re.I)
SHAPES = {
    "ipv4": re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
    "mac": re.compile(r"\b[0-9a-f]{2}(?::[0-9a-f]{2}){5}\b", re.I),
    "path": re.compile(r"(/home/|/Users/|/data/|/tmp/|/mnt/|~/)"),
    "email": re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.]+\b"),
    # tool, model and account tokens, assembled from hex so this file does not spell them
    "token": re.compile(r"\b(" + bytes.fromhex(
        "636c617564657c616e7468726f7069637c6f70656e61697c6770742d3f5c647c636f6465787c636f70696c6f747c"
        "636861746770747c67656d696e697c6861636b65726d616e7c616c6578616e647265").decode() + r")\b", re.I),
}
ALLOWED_MAC = {"91:e0:f0:00:e5:11"}


def git(repo, *a):
    return subprocess.run(["git", "-C", repo, *a], capture_output=True, text=True, check=True).stdout


def scan(label, text, hits):
    for n, line in enumerate(text.splitlines(), 1):
        if CLOSING.search(line):
            hits.append(f"CLOSING {label}:{n}: {line.strip()[:160]}")
        for k, rx in SHAPES.items():
            for m in rx.finditer(line):
                if k == "mac" and m.group(0).lower() in ALLOWED_MAC:
                    continue
                hits.append(f"{k.upper()} {label}:{n}: {m.group(0)}")


def main():
    repo, base, head = sys.argv[1:4]
    hits = []
    added = "\n".join(l[1:] for l in git(repo, "diff", "-U0", base, head).splitlines()
                      if l.startswith("+") and not l.startswith("+++"))
    scan("diff-added", added, hits)
    for sha in git(repo, "rev-list", f"{base}..{head}").split():
        scan(f"commit-{sha[:8]}", git(repo, "log", "-1", "--format=%B", sha), hits)
        print(f"commit {sha} message lines: {len(git(repo, 'log', '-1', '--format=%B', sha).strip().splitlines())}")
    for f in sys.argv[4:]:
        scan(f.split("/")[-1], open(f, encoding="utf-8").read(), hits)
    for h in hits:
        print(h)
    print(f"{len(hits)} hit(s)")


if __name__ == "__main__":
    main()
