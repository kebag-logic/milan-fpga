#!/usr/bin/env python3
"""Compare every Markdown table of the findings page across the PR's commits.

usage: table_proof.py <repo> <path> <rev> [<rev> ...]

A table is a maximal run of lines starting with '|'. Tables are matched by
position and named by their header line. For each later revision the script
prints, per table, IDENTICAL or the changed lines (old and new), against the
LAST revision given first in the comparison pair list: every revision is
compared with the final one.
"""
import hashlib
import subprocess
import sys


def tables(text):
    out, cur = [], []
    for line in text.splitlines():
        if line.startswith("|"):
            cur.append(line)
        elif cur:
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


def show(repo, rev, path):
    return subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"],
                          check=True, capture_output=True, text=True).stdout


def main():
    repo, path, *revs = sys.argv[1:]
    head = revs[-1]
    th = tables(show(repo, head, path))
    print(f"head {head}: {len(th)} tables, {sum(map(len, th))} table lines")
    for i, t in enumerate(th):
        h = hashlib.sha256("\n".join(t).encode()).hexdigest()[:16]
        print(f"  T{i + 1:02d} {len(t):3d} lines sha256/16 {h} {t[0][:70]}")
    for rev in revs[:-1]:
        tr = tables(show(repo, rev, path))
        print(f"\n{rev} vs {head}: {len(tr)} tables, {sum(map(len, tr))} table lines")
        if len(tr) != len(th):
            print("  TABLE COUNT DIFFERS")
            continue
        same = 0
        for i, (a, b) in enumerate(zip(tr, th)):
            if a == b:
                same += 1
                continue
            print(f"  T{i + 1:02d} CHANGED ({len(a)} -> {len(b)} lines)")
            if len(a) != len(b):
                print("    line count differs")
                continue
            for k, (x, y) in enumerate(zip(a, b)):
                if x == y:
                    continue
                xc = [c.strip() for c in x.strip("|").split("|")]
                yc = [c.strip() for c in y.strip("|").split("|")]
                diff = [j for j in range(max(len(xc), len(yc)))
                        if j >= len(xc) or j >= len(yc) or xc[j] != yc[j]]
                # Old text is never printed: earlier revisions carry wording a
                # later ruling withdrew from public text. Only its hash is shown.
                print(f"    line {k + 1}: row '{yc[0][:60]}', changed cell index {diff} of {len(yc)}")
                for j in diff:
                    old = hashlib.sha256(xc[j].encode()).hexdigest()[:16] if j < len(xc) else "-"
                    print(f"      cell {j}: old sha256/16 {old}; head text: {yc[j] if j < len(yc) else '-'}")
        print(f"  identical: {same} of {len(th)}")


if __name__ == "__main__":
    main()
