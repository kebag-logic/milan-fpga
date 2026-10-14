#!/usr/bin/env python3
"""Re-verify published full/sharded case receipts with the PR's own verify().

Usage: verify_published_cases.py <checkout> <receipt-root> <head> <tree>
Each <receipt-root>/<suite>/ holds inventory.json, full.json and leg<N>.json.
Retained per-case logs are not published, so the digest-to-log binding of
read_receipts() is not re-checked here; union and observation equality are.
Also re-derives each inventory from the driver at <checkout> (exact head).
"""
import json, subprocess, sys
from pathlib import Path

checkout, root, head, tree = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], sys.argv[4]
sys.path.insert(0, str(checkout / "scripts"))
from ci_case_receipts import verify  # noqa: E402
import ci_suite_pieces  # noqa: E402

report = {}
for suite_dir in sorted(p for p in root.iterdir() if p.is_dir()):
    suite = suite_dir.name
    names = json.loads((suite_dir / "inventory.json").read_text())
    full = json.loads((suite_dir / "full.json").read_text())
    legs = [json.loads(p.read_text()) for p in sorted(suite_dir.glob("leg[0-9]*.json"))]
    row = {"cases": len(names), "legs": len(legs)}
    try:
        original = verify(names, [full], suite, head, tree)
        sharded = verify(names, legs, suite, head, tree)
        diff = [n for n in names if original[n] != sharded[n]]
        row["union"] = "pass"
        row["observations_equal"] = not diff
        row["differing"] = diff
        # Planted control: drop the first case from every leg and the inventory claim.
        planted = json.loads(json.dumps(legs))
        victim = names[0]
        for leg in planted:
            leg["results"] = [r for r in leg["results"] if r["case"] != victim]
        try:
            verify(names, planted, suite, head, tree)
            row["drop_control"] = "NOT REFUSED"
        except ValueError as exc:
            row["drop_control"] = "refused: " + str(exc)[:80]
    except ValueError as exc:
        row["union"] = "refused: " + str(exc)
    try:
        fresh = subprocess.run([*ci_suite_pieces.driver(suite), "--list"], cwd=checkout,
                               capture_output=True, text=True, check=True, timeout=300)
        row["inventory_at_checkout_equal"] = json.loads(fresh.stdout) == names
    except Exception as exc:  # report, do not hide
        row["inventory_at_checkout_equal"] = "error: " + type(exc).__name__ + ": " + str(exc)[:200]
    report[suite] = row
print(json.dumps(report, indent=2, sort_keys=True))
