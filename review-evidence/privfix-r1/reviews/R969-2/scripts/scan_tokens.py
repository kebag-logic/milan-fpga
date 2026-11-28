#!/usr/bin/env python3
"""Count removed bench tokens in a git tree without spelling them.

Tokens are assembled from code points, as CONTRIBUTING section 6 asks of the
deny-list, so this script and its output never carry them. Prints per-token
hit counts over every tracked text blob at <rev>, and per-path counts.
Usage: scan_tokens.py <repo> <rev> [pathspec...]
"""
import re
import subprocess
import sys

c = lambda *cp: "".join(map(chr, cp))
TOKENS = {
    "T1 tap product": re.compile(c(112, 114, 111, 102, 105) + r"[\s_-]?" + c(115, 104, 97, 114, 107), re.I),
    "T2 tap vendor": re.compile(c(112, 114, 111, 102, 105, 116, 97, 112), re.I),
    "T3 host A": re.compile(r"(?<![A-Za-z0-9_])" + c(112, 119, 48) + r"(?![A-Za-z0-9_])", re.I),
    "T4 host B": re.compile(r"(?<![A-Za-z0-9_])" + c(112, 119, 49) + r"(?![A-Za-z0-9_])", re.I),
    "T5 switch model": re.compile(r"(?<![A-Za-z0-9])" + c(68, 78) + r"-?" + c(49) + r"(?![0-9])"),
    "T6 old fixture addr": re.compile(re.escape(c(49, 48, 46, 48, 46, 48, 46, 50))),
    "T7 old gateway fixture": re.compile(re.escape(c(49, 48, 46, 50, 51, 49, 46, 50, 46, 49))),
}
repo, rev, *spec = sys.argv[1:]
files = subprocess.run(["git", "-C", repo, "ls-tree", "-r", "--name-only", rev, "--", *spec],
                       capture_output=True, check=True, text=True).stdout.split()
total = {k: 0 for k in TOKENS}
for f in files:
    data = subprocess.run(["git", "-C", repo, "show", f"{rev}:{f}"], capture_output=True).stdout
    if b"\0" in data[:8192]:
        continue
    text = data.decode("utf-8", "replace")
    for k, rx in TOKENS.items():
        n = len(rx.findall(text))
        if n:
            total[k] += n
            print(f"{k}\t{n}\t{f}")
print(f"# rev {rev} files {len(files)}")
for k, n in total.items():
    print(f"# {k}: {n}")
