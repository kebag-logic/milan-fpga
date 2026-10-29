"""Compare one adoption section of a Markdown record between two revisions.

Usage: section_check.py <repo> <path> <start-regex> <end-regex> <revA> <revB>
Prints the lines only in A and only in B (order-insensitive multiset diff).
"""
import collections, re, subprocess, sys

def section(repo, rev, path, start, end):
    text = subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"], check=True,
                          capture_output=True, text=True).stdout.splitlines()
    out, on = [], False
    for line in text:
        if on and re.search(end, line):
            break
        if re.search(start, line):
            on = True
        if on and line.strip():
            out.append(line)
    return out

repo, path, start, end, a, b = sys.argv[1:7]
sa, sb = section(repo, a, path, start, end), section(repo, b, path, start, end)
ca, cb = collections.Counter(sa), collections.Counter(sb)
print(f"{path} [{start}] {a}: {len(sa)} lines, {b}: {len(sb)} lines")
for line in sorted((ca - cb).elements()): print("  only", a, ":", line[:160])
for line in sorted((cb - ca).elements()): print("  only", b, ":", line[:160])
