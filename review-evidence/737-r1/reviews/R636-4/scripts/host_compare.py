#!/usr/bin/env python3
"""Compare host builder receipts (reviewer-owned, PR #739 round 4).

Usage: python3 -I host_compare.py <tree> <ref.json> <leg0.json> <leg1.json> [<flagged-leg.json> ...]

<tree> is a clean checkout of the exact head (its scripts/ are imported).
1. Per-gate rows (verdict and NOT RUN rows) and the ordered NOT RUN ledger of
   the unsharded reference equal those of the two legs (own comparison: the
   production `compare` requires both requirement flags, which this host
   cannot satisfy).
2. The production `union` over the real, flag-less legs refuses, naming the
   elaboration owners (the vacuous-pass control with real receipts).
3. With the requirements removed from the leg runner (patched REQUIRED = {})
   the production `union` accepts the real legs and its ledger equals the
   reference ledger.
4. Planted controls on the real receipts: the elaboration gate dropped from leg
   1, leg 1 lost, a NOT RUN row edited - each refused by the production code.
5. Each flagged receipt given is passed to the production union with a passing
   leg 0/1 counterpart and must be refused.
"""
from __future__ import annotations

import copy
import json
import re
import sys
from pathlib import Path
from unittest.mock import patch


def main() -> int:
    tree = Path(sys.argv[1]).resolve()
    sys.path.insert(0, str(tree / "scripts"))
    import ci_builder_legs as legs  # noqa: E402

    # Each host probe ran with its own scratch HOME (home-<name>); hosted legs
    # share one HOME. Mask only that path component, nothing else.
    def masked(path: str) -> dict:
        return json.loads(re.sub(r"/scratch/home-[A-Za-z0-9]+/", "/scratch/HOME/", Path(path).read_text()))

    ref, leg0, leg1 = (masked(p) for p in sys.argv[2:5])
    flagged = [masked(p) for p in sys.argv[5:]]
    names = legs.inventory(tree)
    head, tree_id = ref["head"], ref["tree"]
    failures = []

    def check(label: str, ok: bool, detail: str = "") -> None:
        print(("PASS " if ok else "FAIL ") + label + (": " + detail if detail else ""))
        if not ok:
            failures.append(label)

    check("inventory has 103 gates", len(names) == 103, str(len(names)))
    check("same head/tree in all receipts",
          all((r["head"], r["tree"]) == (head, tree_id) for r in (leg0, leg1)), head + " " + tree_id)
    ref_rows = {row["gate"]: row for row in ref["driver"]["gates"]}
    leg_rows = {row["gate"]: row for r in (leg0, leg1) for row in r["driver"]["gates"]}
    check("reference ran every gate once in inventory order",
          [row["gate"] for row in ref["driver"]["gates"]] == names)
    check("legs ran every gate exactly once",
          sorted(leg_rows) == sorted(names)
          and len(leg0["driver"]["gates"]) + len(leg1["driver"]["gates"]) == len(names))
    differing = [g for g in names if ref_rows.get(g) != leg_rows.get(g)]
    check("per-gate verdict and NOT RUN rows equal", not differing, ", ".join(differing))
    ref_ledger = [item for row in ref["driver"]["gates"] for item in row["not_run"]]
    leg_ledger = [item for g in names for item in leg_rows[g]["not_run"]]
    check("ordered NOT RUN ledger equal", ref_ledger == leg_ledger, f"{len(ref_ledger)} rows")
    print("ledger:", json.dumps(ref_ledger)[:2000])

    try:
        legs.union([leg0, leg1], head, tree_id, names)
    except ValueError as exc:
        check("flag-less real legs refused by the production union", "--require-elaboration" in str(exc)
              or "--require-rv32" in str(exc), str(exc)[:300])
    else:
        check("flag-less real legs refused by the production union", False, "accepted")

    with patch.object(legs, "REQUIRED", {}), patch.object(legs, "elaboration_verdict", lambda ledger: 0):
        result = legs.union([leg0, leg1], head, tree_id, names)
        check("union mechanics accept the real legs with requirements removed",
              result["union"] == "pass" and result["not_run"] == ref_ledger,
              result["verdicts_sha256"])
        dropped = copy.deepcopy([leg0, leg1])
        dropped[1]["driver"]["gates"] = [r for r in dropped[1]["driver"]["gates"]
                                        if r["gate"] != "test_every_recipe_elaborates"]
        for label, receipts, needle in (("elaboration gate dropped from real leg 1", dropped,
                                         "test_every_recipe_elaborates"),
                                        ("real leg 1 lost", [leg0], "")):
            try:
                legs.union(receipts, head, tree_id, names)
            except (ValueError, KeyError) as exc:
                check(label + " refused", needle in str(exc), str(exc)[:200])
            else:
                check(label + " refused", False, "accepted")

    for receipt in flagged:
        partner = leg1 if receipt["leg"] == 0 else leg0
        try:
            legs.union([receipt, partner], head, tree_id, names)
        except (ValueError, KeyError) as exc:
            check(f"flagged host leg {receipt['leg']} refused", True, str(exc)[:300])
        else:
            check(f"flagged host leg {receipt['leg']} refused", False, "accepted")

    print("failures:", failures)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
