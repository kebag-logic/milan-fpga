#!/usr/bin/env python3
"""Check that no byte size in the given texts derives the capture's channel count.

usage: b5_size_derive_check.py <repo> <old_rev> <file>...

The withheld count is derived in memory from the page at <old_rev> (an every-channel
row's byte size over its seconds x 48,000 x 3 bytes) and is never printed or written.

A byte size is a number in the Bytes cell of an artifact row (`| label | N | `sha` |`)
or a number written before "bytes". Each byte size is tested two ways:

  exact:  N == secs x 48,000 x 3 x count for a duration `secs` stated in its row, or
          anywhere in the same file (any number followed by " s");
  near:   N is a whole multiple of 3 x count and N / (3 x count x 48,000) lies between
          0.5 s and 3,600 s, so the count would follow from a rough duration and
          integrality.

A near hit on a row labelled as a pair (two channels) is reported as explained when N
is a whole multiple of 6 bytes, the pair's own 2 x 3 bytes per frame: there the
divisor a reader takes is the row's own channel count, not the capture's. Every hit is
reported by file and line only; values are never printed. A planted control line,
built from the derived count, must hit both tests first.
"""
import re
import subprocess
import sys

PAGE = "docs/findings/117_AUDIO_CONTINUITY.md"
ROW = re.compile(r"^\| (?P<label>[^|]*) \| (?P<n>\d[\d,]*) \| `[0-9a-f]{64}` \|$")
BYTES = re.compile(r"(\d[\d,]*) bytes\b")
DUR = re.compile(r"(\d+(?:\.\d+)?) s\b")


def derive(repo, rev):
    text = subprocess.run(["git", "-C", repo, "show", f"{rev}:{PAGE}"], check=True,
                          capture_output=True, text=True).stdout
    counts = set()
    for line in text.splitlines():
        m = re.match(r"\| .*every channel, (\d+) s \| (\d+) \|", line)
        if m:
            secs, size = int(m.group(1)), int(m.group(2))
            q, r = divmod(size, secs * 48000 * 3)
            if r == 0:
                counts.add(q)
    assert len(counts) == 1, "expected one derived count"
    return counts.pop()


def sizes(text):
    for i, line in enumerate(text.splitlines(), 1):
        m = ROW.match(line)
        if m:
            yield i, int(m.group("n").replace(",", "")), m.group("label"), line
        for tok in BYTES.findall(line):
            yield i, int(tok.replace(",", "")), "", line


def scan(text, count):
    durs = {float(d) for d in DUR.findall(text)}
    unit = 3 * count
    out = []
    for i, n, label, line in sizes(text):
        row_durs = {float(d) for d in DUR.findall(line)} | durs
        exact = any(abs(n - d * 48000 * unit) < 0.5 for d in row_durs)
        near = n % unit == 0 and 0.5 <= n / (unit * 48000) <= 3600
        pair = "pair" in label and n % 6 == 0
        out.append((i, exact, near, pair))
    return out


def main(repo, rev, files):
    count = derive(repo, rev)
    plant = f"| control, every channel, 7 s | {7 * 48000 * 3 * count} | `{'0' * 64}` |"
    ph = scan(plant, count)
    ok = bool(ph and ph[0][1] and ph[0][2])
    print(f"control: planted line hits exact={'YES' if ph and ph[0][1] else 'no'} "
          f"near={'YES' if ph and ph[0][2] else 'no'}")
    for f in files:
        res = scan(open(f, encoding="utf-8").read(), count)
        bad = [r for r in res if r[1] or (r[2] and not r[3])]
        print(f"{f}: {len(res)} byte size(s) tested; {len(bad)} unexplained hit(s)")
        for i, e, n, p in res:
            if e or n:
                print(f"  line {i}: exact={'YES' if e else 'no'} near={'YES' if n else 'no'}"
                      f"{' (pair row, whole multiple of 6 bytes: explained)' if n and p and not e else ''}")
        ok = ok and not bad
    print("RESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2], sys.argv[3:]))
