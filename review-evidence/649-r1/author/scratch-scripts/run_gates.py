#!/usr/bin/env python3
"""Scratch (never committed), #649: run every gate the change touches at the lane head, in the
foreground, no pipelines, GNU make 4.3 first on PATH; record rc and logs. Derived from the
#234 lane's runner, with this lane's own self-tests added."""
import json
import os
import subprocess
import sys
import time
from pathlib import Path

LANE = Path("$LANES/649-resmap")
OUT = Path(os.environ.get("GATES_OUT", "$MANAGEMENT/2026-09-23/649-a527/receipts/gates"))
MD = "$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python"
BASE = "241f91845230ae410506dffb16b71937127fd175"  # dev, the lane base
ENV = dict(os.environ, PATH="$VALIDATION_STORAGE/234-a516/make43/bin:" + os.environ["PATH"], PYTHONDONTWRITEBYTECODE="1")

GATES = [
    # this lane's scripts
    ("resmap-map-selftest", ["python3", "syn/resmap/resmap_map.py", "--selftest"], {}),
    ("resmap-sweep-selftest", ["python3", "syn/resmap/yosys_sweep.py", "--selftest"], {}),
    ("resmap-soc-selftest", ["python3", "syn/resmap/soc_sweep.py", "--selftest"], {}),
    ("resmap-models-selftest", ["python3", "syn/resmap/resmap_models.py", "--selftest"], {}),
    ("resmap-tables-selftest", ["python3", "syn/resmap/resmap_tables.py", "--selftest"], {}),
    # the OOC and resource-gate tooling the new scripts import or read
    ("dp-srcs-selftest", ["python3", "syn/ooc/dp_srcs.py", "--selftest"], {}),
    ("pp-baseline-reports-selftest", ["python3", "syn/ooc/pp_baseline_reports_selftest.py"], {}),
    ("resource-gate-check-baseline", ["python3", "syn/ooc/pp_resource_gate.py", "check-baseline"], {}),
    ("dp-srcs-milan-datapath", ["python3", "syn/ooc/dp_srcs.py", "--top", "milan_datapath"], {"quiet": True}),
    ("dp-srcs-kl-pp-shadow", ["python3", "syn/ooc/dp_srcs.py", "--top", "KL_pp_shadow"], {"quiet": True}),
    ("ooc-sh-selftest", ["python3", "syn/yosys/ooc_selftest.py"], {}),
    # derived-source rule over every tracked file
    ("pp-srcs-check-selftest", ["python3", "scripts/pp_srcs.py", "--check", "--selftest"], {}),
    ("rtl-source-lists", ["python3", "scripts/check_rtl_source_lists.py"], {}),
    # docs job and docs-check-no-git
    ("docs-check", [MD, "scripts/docs_check.py"], {}),
    ("docs-check-no-git", [MD, "scripts/docs_check.py"], {"env": {"GIT_DIR": "/dev/null"}}),
    ("feature-status-no-git", [MD, "scripts/check_feature_status.py"], {"env": {"GIT_DIR": "/dev/null"}}),
    ("feature-status-selftest", [MD, "scripts/check_feature_status.py", "--self-test"], {}),
    ("em-dash", [MD, "scripts/check_em_dash.py", "--base", BASE], {}),
    ("em-dash-selftest", [MD, "scripts/check_em_dash.py", "--selftest"], {}),
    ("doc-style", [MD, "scripts/check_doc_style.py"], {}),
    ("doc-style-selftest", [MD, "scripts/check_doc_style.py", "--selftest"], {}),
    ("doc-paths", [MD, "scripts/check_doc_paths.py"], {}),
    ("toc-selftest", [MD, "scripts/gen_toc.py", "--selftest"], {}),
    ("toc-verify-anchors", [MD, "scripts/gen_toc.py", "--verify-anchors"], {}),
    ("toc-check", [MD, "scripts/gen_toc.py", "--check"], {}),
    ("archive", [MD, "scripts/check_archive.py"], {}),
    ("archive-selftest", [MD, "scripts/check_archive.py", "--selftest"], {}),
    ("doc-map-check", [MD, "docs/DOC_MAP.gen.py", "--check"], {}),
    ("module-matrix-check", [MD, "docs/traceability/gen_module_matrix.py", "--check"], {}),
    ("solution-docs", [MD, "scripts/check_solution_docs.py"], {}),
    ("baremetal-only", ["python3", "scripts/check_baremetal_only.py", "--check"], {}),
    ("gptp-docs-make", ["make", "-C", "gptp-processor", "docs"], {}),
    ("ci-scope-selftest", ["python3", "scripts/ci_scope.py", "--selftest"], {}),
    ("ci-events-check", ["python3", "scripts/ci_events.py", "--check"], {}),
    ("ci-events-selftest", ["python3", "scripts/ci_events.py", "--selftest"], {}),
    # code-quality ratchets over the new Python
    ("py-idiom", ["python3", "scripts/check_py_idiom.py"], {}),
    ("py-idiom-selftest", ["python3", "scripts/check_py_idiom.py", "--selftest"], {}),
    ("fail-fast", ["python3", "scripts/measure_fail_fast.py", "--check"], {}),
    ("hygiene", ["python3", "scripts/check_hygiene.py", "--check"], {}),
    ("todo-ownership", ["python3", "scripts/check_todo_ownership.py"], {}),
    ("test-evidence", ["python3", "scripts/measure_test_evidence.py", "--check"], {}),
    ("naming", ["python3", "scripts/measure_naming.py", "--check"], {}),
    ("control-flow-selftest", ["python3", "scripts/measure_control_flow.py", "--selftest"], {}),
    ("cohesion-selftest", ["python3", "scripts/measure_cohesion.py", "--selftest"], {}),
    ("diff-check-base", ["git", "diff", "--check", BASE, "HEAD"], {}),
    ("diff-check-worktree", ["git", "diff", "--check"], {}),
]


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=LANE, capture_output=True, text=True, check=True).stdout.strip()
    status = subprocess.run(["git", "status", "--porcelain", "--ignored"], cwd=LANE, capture_output=True, text=True,
                            check=True).stdout
    results = {"head": head, "worktree_status_ignored_included": status, "worktree_clean": status == "",
               "make": subprocess.run(["make", "--version"], env=ENV, capture_output=True, text=True).stdout.splitlines()[0],
               "gates": []}
    only = set(sys.argv[1:])
    for name, argv, opts in GATES:
        if only and name not in only:
            continue
        env = dict(ENV, **opts.get("env", {}))
        log = OUT / f"{name}.log"
        start = time.time()
        with log.open("w") as handle:
            handle.write(f"$ {' '.join(argv)}\n# cwd {LANE}; head {head}\n")
            handle.flush()
            sink = subprocess.DEVNULL if opts.get("quiet") else handle
            rc = subprocess.run(argv, cwd=LANE, env=env, stdout=sink, stderr=handle).returncode
            handle.write(f"\n# rc={rc}\n")
        results["gates"].append({"name": name, "command": argv, "rc": rc,
                                 "seconds": round(time.time() - start, 1), "log": log.name})
        print(f"rc={rc} {name}", flush=True)
    status_after = subprocess.run(["git", "status", "--porcelain", "--ignored"], cwd=LANE, capture_output=True,
                                  text=True, check=True).stdout
    results["worktree_status_after"] = status_after
    (OUT / "gate-results.json").write_text(json.dumps(results, indent=1) + "\n")
    bad = [g["name"] for g in results["gates"] if g["rc"] != 0]
    print(f"head {head} clean={results['worktree_clean']} failed={bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
