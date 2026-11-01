#!/usr/bin/env python3
"""Style probe over the lines a change adds to Markdown pages.

For each changed page: paragraph word counts (prose blocks only: not fences,
tables, headings, list items, HTML comments), dashes other than ASCII hyphen,
and hexadecimal literals in prose.

Usage: style_probe.py <repo> <base> <head>
"""
import re
import subprocess
import sys

WORD = re.compile(r"[A-Za-z0-9]+(?:['’][A-Za-z0-9]+)?(?:-[A-Za-z0-9]+)*")
LINK = re.compile(r"\[([^]]+)]\([^)]*\)")
CODE = re.compile(r"`[^`]*`")
HEX = re.compile(r"\b0x[0-9A-Fa-f_]+\b")
DASHES = {"‐": "HYPHEN", "‑": "NB-HYPHEN", "‒": "FIGURE DASH",
          "–": "EN DASH", "—": "EM DASH", "―": "HORIZONTAL BAR",
          "−": "MINUS SIGN"}


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], check=True,
                          capture_output=True, text=True).stdout


def added_lines(repo, base, head, path):
    out = git(repo, "diff", "-U0", base, head, "--", path)
    added = set()
    for line in out.splitlines():
        m = re.match(r"@@ -\S+ \+(\d+)(?:,(\d+))? @@", line)
        if m:
            start, n = int(m.group(1)), int(m.group(2) or "1")
            added.update(range(start, start + n))
    return added


def blocks(text):
    lines = text.split("\n")
    fence = False
    cur, start = [], None
    for i, ln in enumerate(lines, 1):
        s = ln.strip()
        if s.startswith("```"):
            fence = not fence
            if cur:
                yield start, cur
            cur, start = [], None
            continue
        prose = (not fence and s and not s.startswith(("#", "|", "<!--", ">"))
                 and not re.match(r"^\s*(?:[-+*]|\d+[.)])\s+", ln)
                 and not ln.startswith("  "))
        if prose:
            if not cur:
                start = i
            cur.append((i, ln))
        else:
            if cur:
                yield start, cur
            cur, start = [], None
    if cur:
        yield start, cur


def main():
    repo, base, head = sys.argv[1:4]
    pages = [p for p in git(repo, "diff", "--name-only", base, head).split()
             if p.endswith(".md")]
    for p in pages:
        text = git(repo, "show", f"{head}:{p}")
        added = added_lines(repo, base, head, p)
        counts = []
        for start, blk in blocks(text):
            if not any(i in added for i, _ in blk):
                continue
            t = " ".join(ln for _, ln in blk)
            t = LINK.sub(r"\1", CODE.sub(" x ", t))
            counts.append((start, len(WORD.findall(t))))
        lines = text.split("\n")
        dash_hits = [(i, DASHES[c]) for i in sorted(added) if i <= len(lines)
                     for c in lines[i - 1] if c in DASHES]
        hex_prose = []
        fence = False
        for i, ln in enumerate(lines, 1):
            if ln.strip().startswith("```"):
                fence = not fence
                continue
            if i in added and not fence and not ln.lstrip().startswith("|"):
                if HEX.search(CODE.sub("", ln)):
                    hex_prose.append(i)
        n = len(counts)
        lt20 = sum(1 for _, c in counts if c < 20)
        gt30 = sum(1 for _, c in counts if c > 30)
        within = n - lt20 - gt30
        print(f"{p}: added prose paragraphs {n}; <20 words {lt20}; 20-30 {within}; >30 {gt30}; "
              f"max {max((c for _, c in counts), default=0)}")
        if gt30:
            print("  over 30 at lines: " + ", ".join(f"{s}({c})" for s, c in counts if c > 30))
        print(f"  non-ASCII dashes on added lines: {dash_hits or 'none'}")
        print(f"  hexadecimal outside tables and fences on added lines: {hex_prose or 'none'}")


if __name__ == "__main__":
    main()
