#!/usr/bin/env python3
"""R246-2 timestamp audit: snapshot or diff every file AND directory under roots.

  snap.py take <out.json> <root>...   record path -> [kind, mtime_ns, ctime_ns, size, ino]
  snap.py diff <before.json> <after.json>   print added / removed / changed paths

Directories are included on purpose: a file created and deleted between the two
snapshots (a mkdtemp scratch dir, a replaced .pyc) still advances its parent
directory's mtime, so a transient write is visible as a changed directory.
"""
import json
import os
import stat
import sys


def take(roots):
    rows = {}
    for root in roots:
        for dirpath, dirnames, filenames in os.walk(root):
            for name in [*dirnames, *filenames, ""]:
                path = os.path.join(dirpath, name) if name else dirpath
                try:
                    st = os.lstat(path)
                except OSError:
                    continue
                kind = "d" if stat.S_ISDIR(st.st_mode) else "l" if stat.S_ISLNK(st.st_mode) else "f"
                rows[path] = [kind, st.st_mtime_ns, st.st_ctime_ns, st.st_size, st.st_ino]
    return rows


def main():
    if sys.argv[1] == "take":
        rows = take(sys.argv[3:])
        with open(sys.argv[2], "w") as fh:
            json.dump(rows, fh)
        print(f"snapshot {len(rows)} entries")
        return 0
    before = json.load(open(sys.argv[2]))
    after = json.load(open(sys.argv[3]))
    added = sorted(set(after) - set(before))
    removed = sorted(set(before) - set(after))
    changed = sorted(p for p in set(before) & set(after) if before[p][1:4] != after[p][1:4]
                     or before[p][4] != after[p][4])
    for label, paths in (("ADDED", added), ("REMOVED", removed), ("CHANGED", changed)):
        for p in paths:
            print(label, (after.get(p) or before.get(p))[0], p)
    print(f"summary added={len(added)} removed={len(removed)} changed={len(changed)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
