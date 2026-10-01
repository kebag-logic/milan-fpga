#!/usr/bin/env python3
"""Round 5 table proof for the #117 B5 page, without printing withheld values.

usage: b5_table_proof5.py <repo> <scratch_dir> <new_rev> <old_rev>...

Every table (a run of lines starting with "|") of docs/findings/117_AUDIO_CONTINUITY.md
is taken at <new_rev> and at each <old_rev>, in order, and compared by SHA-256. For a
changed table every changed cell is named by row and column; the new cell's text is
printed, and the old cell is described only by its class (numeric or text). Old table
text is never printed: older revisions hold the withheld sizes and the withdrawn peer
counts. Each table's lines are also written to <scratch_dir> and compared with a
literal `diff`, whose rc and output line count are printed; the artifact table is
diffed a second time with its Bytes column cut out. The index row file
docs/findings/README.md is compared too.
"""
import hashlib
import os
import re
import subprocess
import sys

PAGE = "docs/findings/117_AUDIO_CONTINUITY.md"
INDEX = "docs/findings/README.md"


def show(repo, rev, path):
    return subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"], check=True,
                          capture_output=True).stdout.decode()


def tables(text):
    out, cur, start = [], [], 0
    for i, line in enumerate(text.split("\n"), 1):
        if line.startswith("|"):
            if not cur:
                start = i
            cur.append(line)
        elif cur:
            out.append((start, cur))
            cur = []
    if cur:
        out.append((start, cur))
    return out


def h(lines):
    return hashlib.sha256(("\n".join(lines) + "\n").encode()).hexdigest()


def cells(row):
    return [c.strip() for c in row.strip().strip("|").split("|")]


def is_artifact(tbl):
    return cells(tbl[0])[:3] == ["Artifact", "Bytes", "SHA-256"]


def write(path, lines):
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")


def diff(a, b):
    p = subprocess.run(["diff", a, b], capture_output=True, text=True)
    return p.returncode, p.stdout


def main(repo, scratch, new, olds):
    os.makedirs(scratch, exist_ok=True)
    tn = tables(show(repo, new, PAGE))
    res = 0
    for old in olds:
        to = tables(show(repo, old, PAGE))
        print(f"==== {old} -> {new}")
        print(f"tables: {len(to)} at {old[:8]}, {len(tn)} at {new[:8]}; "
              f"table lines {sum(len(t) for _, t in to)} and {sum(len(t) for _, t in tn)}")
        if len(to) != len(tn):
            print("TABLE COUNT DIFFERS")
            res = 1
            continue
        same_n = 0
        for i, ((lo, a), (ln, b)) in enumerate(zip(to, tn), 1):
            same = h(a) == h(b)
            same_n += same
            fa = os.path.join(scratch, f"{old[:8]}-t{i:02d}.txt")
            fb = os.path.join(scratch, f"{new[:8]}-t{i:02d}.txt")
            write(fa, a)
            write(fb, b)
            rc, out = diff(fa, fb)
            art = is_artifact(a)
            print(f"table {i:2d} (line {lo} -> {ln}, {len(a)} lines, header {cells(a[0])[:3]}): "
                  f"{'byte-identical' if same else 'CHANGED'} sha256 {h(a)[:16]}"
                  + ("" if same else f" -> {h(b)[:16]}") + f"; literal diff rc={rc}")
            if same:
                continue
            print(f"  literal diff: rc={rc}, {len(out.splitlines())} output line(s), not printed")
            if art:
                ca = [[c for k, c in enumerate(cells(r)) if k != 1] for r in a]
                cb = [[c for k, c in enumerate(cells(r)) if k != 1] for r in b]
                write(fa + ".nobytes", ["| " + " | ".join(r) + " |" for r in ca])
                write(fb + ".nobytes", ["| " + " | ".join(r) + " |" for r in cb])
                rc2, out2 = diff(fa + ".nobytes", fb + ".nobytes")
                print(f"  literal diff with the Bytes column cut out: rc={rc2}, "
                      f"{len(out2.splitlines())} output line(s)")
            if len(a) != len(b):
                print("  ROW COUNT DIFFERS")
                res = 1
                continue
            for r, (x, y) in enumerate(zip(a, b), 1):
                if x == y:
                    continue
                cx, cy = cells(x), cells(y)
                for k, (u, v) in enumerate(zip(cx, cy), 1):
                    if u != v:
                        kind = "numeric" if re.fullmatch(r"\d[\d,]*", u) else "text"
                        print(f"  row {r} {cy[0]!r}: column {k} ({cells(a[0])[k - 1]}) changed:"
                              f" old cell {kind}, new cell {v!r}")
                if len(cx) != len(cy):
                    print(f"  row {r}: CELL COUNT DIFFERS")
                    res = 1
        print(f"{same_n} of {len(to)} tables byte-identical")
        io, inn = show(repo, old, INDEX), show(repo, new, INDEX)
        print(f"index {INDEX}: {'byte-identical' if io == inn else 'CHANGED'}")
        print()
    return res


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]))
