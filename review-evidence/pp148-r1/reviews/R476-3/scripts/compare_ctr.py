#!/usr/bin/env python3
"""Compare two ctr_mutants.py driver logs record by record.

A record is a verdict line ("control ..." or "<arm>: rc=... KILLED|UNPROVEN") with
its indented FAIL lines, plus the final tally. Paths, timestamps and banner lines
are ignored. Prints each record's status and rc 0 only when every record matches.
Usage: compare_ctr.py PUBLISHED_LOG REVIEW_LOG
"""
import re
import sys

VERDICT = re.compile(r"^(control pp_top \w+: rc=\d+ \w+|[\w-]+: rc=\d+ failures=\d+ named=\d+ \w+)$")
TALLY = re.compile(r"^\d+ checks: \d+ PASS, \d+ FAIL$")


def records(path):
    out, key = {}, None
    for line in open(path, encoding="utf-8", errors="replace").read().splitlines():
        if VERDICT.match(line):
            key = line.split(":")[0]
            out[key] = [line]
        elif TALLY.match(line):
            out["tally"] = [line]
            key = None
        elif key and line.startswith("    FAIL:"):
            out[key].append(line)
        else:
            key = None if not line.startswith("    ") else key
    return out


def main():
    a, b = records(sys.argv[1]), records(sys.argv[2])
    bad = 0
    for key in list(a) + [k for k in b if k not in a]:
        same = a.get(key) == b.get(key)
        bad += not same
        print(f"{'SAME' if same else 'DIFF'} {key}: {b.get(key, ['(missing)'])[0]}")
        if not same:
            print("  published:", a.get(key))
            print("  review:   ", b.get(key))
    print(f"{len(a)} published records, {len(b)} review records, {bad} differ")
    return int(bad != 0)


if __name__ == "__main__":
    raise SystemExit(main())
