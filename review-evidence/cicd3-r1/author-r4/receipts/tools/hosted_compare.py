#!/usr/bin/env python3
"""Compare two hosted runs' Verilator suite artifacts suite by suite, wherever the dealer put each.

usage: python3 -I hosted_compare.py OLD_DIR NEW_DIR
Each DIR holds suite-logs-<n>/ for n in 0..18 (gh run download -n suite-logs-<n>). For every piece receipt
(cases/<piece>.json) present in both: per-case (case, outcome, returncode, output_sha256) must be equal; only
the receipts' head and tree may differ. For every suite log: the PASS/FAIL tally line set ("checks:", "[PASS]",
"[FAIL]", "RESULT") must be equal as a multiset. Prints one line per suite and a total.
"""
import json
import re
import sys
from pathlib import Path

VERDICT = re.compile(r"(\[(PASS|FAIL|ok|FAIL )\]|^(PASS|FAIL|ok|FAIL)\b|\bchecks?:|RESULT:|mutant caught|caught)")


def index(root: Path) -> tuple[dict, dict]:
    receipts, logs = {}, {}
    for shard in sorted(root.glob("suite-logs-*")):
        for r in (shard / "cases").glob("*.json"):
            receipts[r.stem] = (shard.name, json.loads(r.read_text()))
        for log in shard.glob("*.log"):
            logs[log.stem] = (shard.name, log)
    return receipts, logs


def verdicts(path: Path) -> list[str]:
    lines = []
    for line in path.read_text(errors="replace").splitlines():
        if VERDICT.search(line):
            lines.append(re.sub(r"/[^\s:'\"]*milan-mutant-stage-\d+/[^\s/:'\"]+|/tmp/[A-Za-z0-9_.-]+", "<STAGE>", line))
    return sorted(lines)


def main() -> int:
    old_r, old_l = index(Path(sys.argv[1]))
    new_r, new_l = index(Path(sys.argv[2]))
    bad = same_r = same_l = 0
    for piece in sorted(set(old_r) & set(new_r)):
        (so, a), (sn, b) = old_r[piece], new_r[piece]
        key = lambda d: [(x["case"], x["outcome"], x["returncode"], x.get("output_sha256")) for x in d["results"]]
        extra = sorted(k for k in set(a) | set(b) if a.get(k) != b.get(k) and k not in ("head", "tree"))
        ok = key(a) == key(b) and not extra
        same_r += ok
        bad += not ok
        print(f"receipt {piece:24} {so:>14} -> {sn:<14} {len(a['results']):3} cases {'IDENTICAL' if ok else 'DIFFER ' + str(extra)}")
    for suite in sorted(set(old_l) & set(new_l)):
        (so, a), (sn, b) = old_l[suite], new_l[suite]
        va, vb = verdicts(a), verdicts(b)
        ok = va == vb
        same_l += ok
        bad += not ok
        print(f"log     {suite:24} {so:>14} -> {sn:<14} {len(va):5} verdict lines {'IDENTICAL' if ok else 'DIFFER'}")
    only = sorted((set(old_r) ^ set(new_r)) | (set(old_l) ^ set(new_l)))
    print(f"receipts identical {same_r}/{len(set(old_r) & set(new_r))}; suite-log verdict sets identical "
          f"{same_l}/{len(set(old_l) & set(new_l))}; present in one run only: {only or 'none'}")
    return 1 if bad or only else 0


if __name__ == "__main__":
    raise SystemExit(main())
