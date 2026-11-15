#!/usr/bin/env python3
"""List every hit of round 14's stale-figure tokens (R837-7-F1) in its scope, one line each.

Scope: SPLIT_CONTROL_MEMORY.md section 13, FR_NFR.md 3.4.1, every tracked README, and every tracked
C, C++, header, Python, SystemVerilog and workflow file (comments and code alike). Run from the tree's top.
"""
import re
import subprocess
import sys

N = r"(?<![\d.,])"
U = r" ?(?:us|µs|u)\b"
TOKENS = [
    ("725", re.compile(N + r"725(?![\d])"), None),
    ("33.01", re.compile(r"33\.01(?!\d)"), None),
    ("900 us", re.compile(N + r"900" + U), None),
    ("0.515", re.compile(r"0\.515(?!\d)"), None),
    ("0.511", re.compile(r"0\.511(?!\d)"), None),
    ("13.05", re.compile(r"13\.05(?!\d)"), None),
    ("132.71", re.compile(r"132\.71(?!\d)"), None),
    ("50 us TICK", re.compile(N + r"50(?:" + U + r"|\b)"), re.compile(r"TICK")),
    ("65 AECP timer", re.compile(N + r"65(?:" + U + r"|\b)"), re.compile(r"(?i)aecp|timer|slot")),
    ("150 LINK", re.compile(N + r"150(?:" + U + r"|\b)"), re.compile(r"LINK|(?i:\blink\b)")),
    ("250 SRP drain", re.compile(N + r"250(?:" + U + r"|\b)"), re.compile(r"(?i)srp|drain")),
]


def section(lines, start, stop):
    """Line numbers (1-based) from the heading matching start up to the next matching stop."""
    out, on = [], False
    for i, s in enumerate(lines, 1):
        if on and stop.match(s):
            break
        if start.match(s):
            on = True
        if on:
            out.append(i)
    return out


def main():
    files = subprocess.run(["git", "ls-files"], capture_output=True, text=True, check=True).stdout.split()
    scope = {}
    sec = "docs/design/SPLIT_CONTROL_MEMORY.md"
    lines = open(sec, encoding="utf-8").read().split("\n")
    scope[sec] = (lines, section(lines, re.compile(r"## 13\b"), re.compile(r"## (?!13\b)\d")))
    fr = "docs/reference/FR_NFR.md"
    lines = open(fr, encoding="utf-8").read().split("\n")
    scope[fr] = (lines, section(lines, re.compile(r"#+ .*3\.4\.1\b"), re.compile(r"#+ .*3\.4\.(?!1\b)\d|#+ .*3\.5\b")))
    ext = (".c", ".h", ".cpp", ".hpp", ".py", ".sv", ".svh", ".v", ".yml", ".yaml")
    for f in files:
        if f in scope:
            continue
        if f.rsplit("/", 1)[-1].startswith("README") or f.endswith(ext):
            try:
                lines = open(f, encoding="utf-8").read().split("\n")
            except (UnicodeDecodeError, FileNotFoundError):
                continue
            scope[f] = (lines, range(1, len(lines) + 1))
    for name, pat, ctx in TOKENS:
        for f in sorted(scope):
            lines, nums = scope[f]
            for i in nums:
                s = lines[i - 1]
                if pat.search(s) and (ctx is None or ctx.search(s)):
                    print(f"{name}\t{f}:{i}\t{s.strip()[:220]}")


if __name__ == "__main__":
    sys.exit(main())
