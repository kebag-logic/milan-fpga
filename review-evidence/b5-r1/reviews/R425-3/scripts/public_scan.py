#!/usr/bin/env python3
"""Label-only public-text scan.  Usage: public_scan.py <token-file> <path>...
The token file holds 'label|regex' lines and stays outside the published packet;
this script prints only labels, file paths and line numbers, never the match."""
import os, re, sys
def rules(path):
    out = []
    for line in open(path, encoding="utf-8"):
        line = line.rstrip("\n")
        if line:
            label, rx = line.split("|", 1)
            out.append((label, re.compile(rx, re.I if label in ("bus-type",) else 0)))
    return out
def files(paths):
    for p in paths:
        if os.path.isdir(p):
            for d, _, fs in os.walk(p):
                for f in sorted(fs):
                    yield os.path.join(d, f)
        else:
            yield p
def main():
    rs = rules(sys.argv[1]); total = 0
    for f in files(sys.argv[2:]):
        try:
            text = open(f, encoding="utf-8").read()
        except (UnicodeDecodeError, OSError):
            continue
        for n, line in enumerate(text.splitlines(), 1):
            for label, rx in rs:
                if rx.search(line):
                    total += 1
                    print(f"{label}\t{f}:{n}")
    print(f"total hits {total}")
if __name__ == "__main__":
    main()
