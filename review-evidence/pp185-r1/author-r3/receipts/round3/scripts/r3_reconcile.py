"""usage: r3_reconcile.py <replayed-audit.json> <published-audit.json> <round2-compare-dir>
Reconcile the corrected comparison's populations with the reviewer's audit: the audit
replayed on the round-2 records must equal the audit as published, and each campaign's
mutant, baseline, unchanged, changed and added figures must equal this comparison's."""
import json
import sys
from pathlib import Path


def main() -> int:
    replayed = json.loads(Path(sys.argv[1]).read_text())
    published = json.loads(Path(sys.argv[2]).read_text())
    compare = Path(sys.argv[3])
    bad = 0
    same = replayed == published
    bad += not same
    print(f"{'MATCH' if same else 'MISMATCH'}: the audit replayed on these records equals the published audit")
    print("| Campaign | Figure | Audit | This comparison | |")
    print("|---|---|---:|---:|---|")
    for c, unchanged_key, changed_key in (("notify", "same_failure_ids", "changed_failure_ids"),
                                          ("aecp_dispatch", "same_failure_count", "changed_failure_count"),
                                          ("d3", "same_failure_ids", "changed_failure_ids")):
        a = replayed[c]
        m = json.loads((compare / f"{c}-base-vs-head.json").read_text())
        rows = [("base mutants", a["base_mutants"], m["base_mutants"]),
                ("head mutants", a["head_mutants"], m["head_mutants"]),
                ("unchanged mutants", a[unchanged_key], m["mutants"]["unchanged"]),
                ("changed mutants", a[changed_key], m["mutants"]["changed"]),
                ("added mutants", a["new_mutants"], m["mutants"]["added"]),
                ("removed mutants", [], m["mutants"]["removed"]),
                ("head baselines", a["goldens"], m["head_baselines"])]
        for figure, x, y in rows:
            ok = x == y
            bad += not ok
            show = (lambda v: len(v) if isinstance(v, list) else v)
            print(f"| {c} | {figure} | {show(x)} | {show(y)} | {'MATCH' if ok else 'MISMATCH'} |")
    print(f"{bad} mismatches")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
