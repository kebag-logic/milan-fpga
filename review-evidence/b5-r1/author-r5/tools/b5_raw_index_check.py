#!/usr/bin/env python3
"""Check the page's artifact table against the archive's RAW-ARTIFACTS.json.

usage: b5_raw_index_check.py <page.md> <archive_git_dir> <commit>

For each artifact row on the page (`| label | bytes | `sha256` |`), the raw-index
entry with that SHA-256 is found at <commit>. A numeric page size must equal the
entry's bytes; a page cell `withheld` must meet a withheld entry. Every withheld
entry must be an every-channel capture: its path is `cap-all-...`, or the page row
with its SHA-256 is labelled "every channel". Sizes are reported as equal or withheld,
never printed.
"""
import json
import re
import subprocess
import sys

ROOT = "review-evidence/b5-r1"
ROW = re.compile(r"^\| (?P<label>[^|]*) \| (?P<n>[^|]*) \| `(?P<h>[0-9a-f]{64})` \|$")


def main(page, gitdir, commit):
    raw = json.loads(subprocess.run(["git", "-C", gitdir, "show", f"{commit}:{ROOT}/author/RAW-ARTIFACTS.json"],
                                    check=True, capture_output=True).stdout)
    entries = raw if isinstance(raw, list) else next(v for v in raw.values() if isinstance(v, list))
    byhash = {e["sha256"]: e for e in entries if e.get("sha256")}
    withheld = [e for e in entries if not isinstance(e.get("bytes"), int)]
    print(f"archive {commit}: RAW-ARTIFACTS.json {len(entries)} entries, {len(byhash)} with a SHA-256, "
          f"{len(withheld)} with the size withheld")
    bad = 0
    rows = {m.group("h"): m.group("label") for m in
            (ROW.match(x) for x in open(page, encoding="utf-8").read().splitlines()) if m}
    for e in withheld:
        name = str(e.get("path", e.get("file", "")))
        by_path = "cap-all-" in name
        by_page = "every channel" in rows.get(e["sha256"], "")
        ok = by_path or by_page
        bad += not ok
        why = ", ".join(w for w, c in (("path cap-all-", by_path), ("page row labelled every channel", by_page)) if c)
        print(f"  withheld entry {e['sha256'][:12]}: "
              f"{'an every-channel capture (' + why + ')' if ok else 'NOT SHOWN TO BE an every-channel capture'}")
    for i, line in enumerate(open(page, encoding="utf-8").read().splitlines(), 1):
        m = ROW.match(line)
        if not m:
            continue
        e = byhash.get(m.group("h"))
        cell = m.group("n").strip()
        if e is None:
            print(f"  :{i} {m.group('h')[:12]} not in RAW-ARTIFACTS.json")
            continue
        if cell == "withheld":
            ok = not isinstance(e.get("bytes"), int)
            res = "withheld on the page and in the index" if ok else "WITHHELD ON THE PAGE ONLY"
        else:
            ok = isinstance(e.get("bytes"), int) and int(cell.replace(",", "")) == e["bytes"]
            res = "size equal" if ok else "SIZE DIFFERS OR WITHHELD IN THE INDEX"
        bad += not ok
        print(f"  :{i} {m.group('h')[:12]} {m.group('label')}: {res}")
    print(f"result: {'PASS' if not bad else 'FAIL'} ({bad} problem(s))")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:4]))
