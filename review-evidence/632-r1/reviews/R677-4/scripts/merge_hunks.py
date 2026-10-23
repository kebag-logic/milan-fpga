#!/usr/bin/env python3
"""List every diff3 conflict hunk of a merge and, per side, the words it changed
against the merge base, so a resolution can be judged against both parents.

Usage: merge_hunks.py <repo> <ours> <theirs>
Prints, per conflicted file and hunk: the words base->ours and base->theirs
changed, and whether each side's changed words survive in the recorded merge
result is left to the reader (the resolved file is printed by path:line).
"""
import difflib
import subprocess
import sys


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], check=True,
                          capture_output=True, text=True).stdout


def words_changed(a, b):
    sa, sb = a.split(), b.split()
    out = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, sa, sb, autojunk=False).get_opcodes():
        if op != "equal":
            out.append(f"  {op}: -[{' '.join(sa[i1:i2])[:300]}] +[{' '.join(sb[j1:j2])[:300]}]")
    return out


def main():
    repo, ours, theirs = sys.argv[1:4]
    tree_out = subprocess.run(
        ["git", "-C", repo, "-c", "merge.conflictStyle=diff3", "merge-tree",
         "--write-tree", "--name-only", ours, theirs],
        capture_output=True, text=True).stdout.splitlines()
    tree = tree_out[0]
    files = [l for l in tree_out[1:] if l and not l.startswith(("Auto-merging", "CONFLICT"))]
    for f in files:
        text = git(repo, "show", f"{tree}:{f}").splitlines()
        i, n = 0, 0
        while i < len(text):
            if text[i].startswith("<<<<<<< "):
                n += 1
                o, b, t = [], [], []
                cur = o
                start = i + 1
                i += 1
                while not text[i].startswith(">>>>>>> "):
                    if text[i].startswith("||||||| "):
                        cur = b
                    elif text[i] == "=======":
                        cur = t
                    else:
                        cur.append(text[i])
                    i += 1
                base, oo, tt = "\n".join(b), "\n".join(o), "\n".join(t)
                print(f"=== {f} hunk {n} (diff3 line {start})")
                print(" base->ours:")
                print("\n".join(words_changed(base, oo)) or "  (none)")
                print(" base->theirs:")
                print("\n".join(words_changed(base, tt)) or "  (none)")
            i += 1


if __name__ == "__main__":
    main()
