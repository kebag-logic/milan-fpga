#!/usr/bin/env python3
"""List archive files that still carry a withheld every-channel capture size.

Usage: archive_size_scan.py <evidence-git-dir> <old-page> <commit> [<commit> ...]
The withheld sizes are derived in memory from the old page's three
every-channel rows and never printed; output is commit, path and row label.
"""
import re
import subprocess
import sys

ROW = re.compile(r"^\| ([^|]*every channel, [0-9.]+ s) \| ([0-9]+) \|", re.M)


def main(gitdir, old, *commits):
    rows = ROW.findall(open(old, encoding="utf-8").read())
    assert len(rows) == 3
    pats = [(label.strip(), re.compile(r"(?<![0-9])(%s|%s)(?![0-9])" % (s, f"{int(s):,}"))) for label, s in rows]
    for c in commits:
        names = subprocess.run(["git", f"--git-dir={gitdir}", "ls-tree", "-r", "--name-only", c,
                                "review-evidence/b5-r1"], check=True, capture_output=True, text=True).stdout.split()
        found = 0
        for n in names:
            data = subprocess.run(["git", f"--git-dir={gitdir}", "show", f"{c}:{n}"],
                                  check=True, capture_output=True).stdout.decode("utf-8", "ignore")
            for label, p in pats:
                k = len(p.findall(data))
                if k:
                    found += 1
                    print(f"{c[:8]} {n}: {k} x '{label}' size")
        print(f"{c[:8]}: {len(names)} files scanned, {found} file/size hits")


if __name__ == "__main__":
    main(*sys.argv[1:])
