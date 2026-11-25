#!/usr/bin/env python3
"""Compare two hosted runs' Verilator suite evidence suite by suite, whatever legs each run dealt.

usage: python3 -I hosted_compare5.py OLD_DIR NEW_DIR
Each DIR holds suite-logs-<n>/ (gh run download -n suite-logs-<n>), any number of workers.

Receipts: every piece receipt (cases/<suite>__<leg>.json) of a suite is merged into one case table,
case -> (outcome, returncode, output_sha256). Each case must appear exactly once per run. A suite with
receipts in both runs must have equal inventories and equal tables; only head, tree, shard and the
grouping into legs may differ.

Verdicts: a suite's verdict lines are those of its whole log (<suite>.log) or of all its piece logs
(<suite>__<leg>.log) together, by round 4's hosted_compare.py VERDICT pattern, with the staging path
normalised, as a sorted multiset. They must be equal whether the suite ran whole or in pieces.
"""
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

VERDICT = re.compile(r"(\[(PASS|FAIL|ok|FAIL )\]|^(PASS|FAIL|ok|FAIL)\b|\bchecks?:|RESULT:|mutant caught|caught)")
PIECE = re.compile(r"^(.+)__(0|[1-9][0-9]*)$")


def suite_of(stem: str) -> str:
    match = PIECE.match(stem)
    return match[1] if match else stem


def verdict_lines(path: Path) -> list[str]:
    lines = []
    for line in path.read_text(errors="replace").splitlines():
        if VERDICT.search(line):
            lines.append(re.sub(r"/[^\s:'\"]*milan-mutant-stage-\d+/[^\s/:'\"]+|/tmp/[A-Za-z0-9_.-]+", "<STAGE>", line))
    return lines


def index(root: Path):
    tables, inventories, verdicts, legs, problems = defaultdict(dict), {}, defaultdict(list), defaultdict(set), []
    for shard in sorted(root.glob("suite-logs-*")):
        for receipt in sorted((shard / "cases").glob("*.json")):
            value = json.loads(receipt.read_text())
            suite = value["suite"]
            legs[suite].add((receipt.stem, value["shard"]))
            if inventories.setdefault(suite, value["inventory"]) != value["inventory"]:
                problems.append(f"{suite}: two inventories in one run")
            for row in value["results"]:
                key = row["case"]
                if key in tables[suite]:
                    problems.append(f"{suite}/{key}: twice in one run")
                tables[suite][key] = (row["outcome"], row["returncode"], row.get("output_sha256"))
        for log in shard.glob("*.log"):
            verdicts[suite_of(log.stem)].extend(verdict_lines(log))
    for suite, table in tables.items():
        if sorted(table) != sorted(inventories[suite]):
            problems.append(f"{suite}: receipts cover {len(table)} of {len(inventories[suite])} cases")
    return tables, inventories, {k: sorted(v) for k, v in verdicts.items()}, legs, problems


def main() -> int:
    old_t, old_i, old_v, old_l, old_p = index(Path(sys.argv[1]))
    new_t, new_i, new_v, new_l, new_p = index(Path(sys.argv[2]))
    bad = len(old_p) + len(new_p)
    for problem in old_p + new_p:
        print("PROBLEM", problem)
    same_r = same_v = 0
    for suite in sorted(set(old_t) | set(new_t)):
        if suite not in old_t or suite not in new_t:
            side = "new" if suite in new_t else "old"
            print(f"receipts {suite:20} only in the {side} run: {len((new_t if side == 'new' else old_t)[suite])} cases, "
                  f"{len((new_l if side == 'new' else old_l)[suite])} legs")
            continue
        ok = old_i[suite] == new_i[suite] and old_t[suite] == new_t[suite]
        same_r += ok
        bad += not ok
        diff = sorted(k for k in set(old_t[suite]) | set(new_t[suite]) if old_t[suite].get(k) != new_t[suite].get(k))
        print(f"receipts {suite:20} {len(old_t[suite]):3} cases, legs {len(old_l[suite])} -> {len(new_l[suite])}: "
              + ("IDENTICAL" if ok else f"DIFFER {diff[:5]}"))
    for suite in sorted(set(old_v) | set(new_v)):
        if suite not in old_v or suite not in new_v:
            print(f"verdicts {suite:20} present in one run only")
            bad += 1
            continue
        ok = old_v[suite] == new_v[suite]
        same_v += ok
        bad += not ok
        print(f"verdicts {suite:20} {len(old_v[suite]):5} lines: " + ("IDENTICAL" if ok else
              f"DIFFER (old {len(old_v[suite])}, new {len(new_v[suite])})"))
    both_r = len(set(old_t) & set(new_t))
    both_v = len(set(old_v) & set(new_v))
    print(f"case tables identical {same_r}/{both_r}; suite verdict sets identical {same_v}/{both_v}; "
          f"problems {len(old_p) + len(new_p)}")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
