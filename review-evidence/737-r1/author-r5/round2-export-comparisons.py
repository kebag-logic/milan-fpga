"""Export public-source comparisons through the source tree's production verifier."""

import argparse
from collections import Counter
import copy
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

INVENTORIES = {
    "milan_dp": (4, "tb/verilator/milan_dp/Makefile:595 ci-list / RUN_CASES"),
    "capture_coherence": (4, "tb/verilator/capture_coherence/mutants.py:580 arm_units"),
    "maap": (4, "tb/verilator/maap/mutants.py:253 run_inventory"),
    "milan_dp_mclk": (4, "tb/verilator/milan_dp_mclk/mclk_mutants.py:251 run_inventory"),
    "milan_dp_render": (3, "tb/verilator/milan_dp_render/Makefile:212 ci-list / RUN_CASES"),
    "pp_shadow": (4, "tb/verilator/pp_shadow/Makefile:157 ci-list / RUN_CASES"),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--runs", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--suite", action="append", choices=INVENTORIES)
    args = parser.parse_args()
    sys.path.insert(0, str(args.source / "scripts"))
    from ci_case_receipts import read_receipts, verify
    from ci_suite_pieces import inventory

    def git(*words):
        return subprocess.check_output(["git", "-C", str(args.source), *words], text=True).strip()

    head, tree = git("rev-parse", "HEAD"), git("rev-parse", "HEAD^{tree}")
    assert head == "cf9c936697a06e44c41681bcc12dc612a3242eb2"
    assert not git("status", "--porcelain", "--untracked-files=no")
    args.output.mkdir(parents=True, exist_ok=True)
    summaries = []
    artifacts = []
    for suite in args.suite or INVENTORIES:
        count, origin = INVENTORIES[suite]
        source = args.runs / suite
        expected = inventory(suite)
        full = read_receipts([source / "full.json"])
        legs = read_receipts([source / f"leg{leg}.json" for leg in range(count)])
        reference = verify(expected, full, suite, head, tree)
        assert verify(expected, legs, suite, head, tree) == reference
        dropped = copy.deepcopy(legs)
        for row in dropped:
            row["inventory"] = expected[1:]
            row["results"] = [result for result in row["results"] if result["case"] != expected[0]]
        try:
            verify(expected, dropped, suite, head, tree)
        except ValueError:
            pass
        else:
            raise AssertionError("case dropped everywhere was accepted")
        altered = copy.deepcopy(legs)
        altered[0]["results"][0]["output_sha256"] = "0" * 64
        assert verify(expected, altered, suite, head, tree) != reference
        timings = {}
        for tag in ["full", *[f"leg{leg}" for leg in range(count)]]:
            run = json.loads((source / (tag + ".run.json")).read_text())
            assert run["rc"] == 0 and run["head"] == head and run["tree"] == tree
            timings[tag] = run["seconds"]
        summaries.append({"suite": suite, "head": head, "tree": tree,
                          "inventory_source": origin, "inventory": expected, "legs": count,
                          "comparison": "equal outcomes, return codes and checked-output digests",
                          "dropped_from_every_claim": "refused", "changed_observation": "different",
                          "receipt_outcomes": dict(Counter(row["outcome"] for leg in legs
                                                           for row in leg["results"])),
                          "timings_seconds": timings,
                          "unit_note": "Inventory units may contain internal mutation campaigns."})
        destination = args.output / suite
        destination.mkdir(exist_ok=True)
        for path in sorted(source.iterdir()):
            if not path.is_file() or path.name == "comparison.json":
                continue
            size = path.stat().st_size
            with path.open("rb") as stream:
                digest = hashlib.file_digest(stream, "sha256").hexdigest()
            retained = size <= 200000
            if retained:
                shutil.copyfile(path, destination / path.name)
            artifacts.append({"path": suite + "/" + path.name, "bytes": size,
                              "sha256": digest, "copied": retained})
    (args.output / "comparison-summary.json").write_text(json.dumps(summaries, indent=2) + "\n")
    (args.output / "artifact-index.json").write_text(json.dumps(artifacts, indent=2) + "\n")
    print(json.dumps({"head": head, "compared_suites": [row["suite"] for row in summaries],
                      "cases": sum(len(row["inventory"]) for row in summaries)}))


if __name__ == "__main__":
    main()
