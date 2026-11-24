#!/usr/bin/env python3
"""In-memory negative controls for the reviewed self-tests: plant one defect at
a time in the generated workflow or in the case runner, and require the
self-test that claims to guard it to fail. No file is written in the tree.

usage: python3 -I negative_controls.py REPO
"""

import copy
import json
import sys
import tempfile
from pathlib import Path


def expect_refusal(label, action) -> bool:
    """Run one planted defect; it must raise (the guard fires)."""
    try:
        action()
    except (AssertionError, KeyError, ValueError) as error:
        print(f"CAUGHT  {label}: {type(error).__name__}: {str(error)[:140]!r}")
        return True
    print(f"MISSED  {label}")
    return False


def main() -> int:
    repo = Path(sys.argv[1]).resolve()
    sys.path.insert(0, str(repo / "scripts"))
    import ci_suite_pieces_selftest as pieces
    from ci_gate_workflows import generate, load_template
    import ci_make_cases
    import ci_make_cases_selftest as cases

    import yaml
    workflow = yaml.safe_load((repo / ".github/workflows/rtl.yml").read_text())
    pieces.preflight_controls(copy.deepcopy(workflow))
    print("clean   generated rtl.yml passes preflight_controls")
    results = []

    def planted(mutate):
        def run():
            w = copy.deepcopy(workflow)
            mutate(w)
            pieces.preflight_controls(w)
        return run

    def check_step(w):
        return [s for s in w["jobs"]["verilator-suites"]["steps"]
                if "verilator-preflight" in json.dumps(s.get("env", {}))][0]

    def drop_result_test(w):
        step = check_step(w)
        step["run"] = step["run"].split("if [")[0] + "echo ok\n"

    def drop_sha_record(w):
        step = check_step(w)
        step["run"] = "\n".join(step["run"].splitlines()[3:]) + "\n"

    def drop_need(w):
        w["jobs"]["verilator-suites"]["needs"].remove("verilator-preflight")

    def tolerate(w):
        check_step(w)["continue-on-error"] = True

    def unwatch(w):
        for step in w["jobs"]["ci-fail-fast"]["steps"]:
            if step.get("name") == "Observe the first failed job":
                jobs = json.loads(step["env"]["EXPECTED_JOBS"])
                jobs.remove("Verilator preflight")
                step["env"]["EXPECTED_JOBS"] = json.dumps(jobs)

    def worker_keeps_skip_without_job(w):
        for step in w["jobs"]["verilator-preflight"]["steps"]:
            if "run_all_suites.sh" in step.get("run", ""):
                step["run"] = step["run"].replace("--preflight-only", "--list")

    def preflight_skipped_on_other_condition(w):
        w["jobs"]["verilator-preflight"]["if"] = "${{ false }}"

    for label, mutate in (
            ("aggregate step loses its result test", drop_result_test),
            ("aggregate step loses its SHA-record check", drop_sha_record),
            ("verilator-suites no longer needs the preflight", drop_need),
            ("aggregate preflight step continues on error", tolerate),
            ("fail-fast no longer watches the preflight", unwatch),
            ("preflight job runs something other than --preflight-only", worker_keeps_skip_without_job),
            ("preflight job condition differs from the workers'", preflight_skipped_on_other_condition)):
        results.append(expect_refusal(label, planted(mutate)))

    # The case runner's start order, against ci_make_cases_selftest's controls.
    original_order, original_all = ci_make_cases.start_order, cases.execute_all

    def with_patch(order=None, execute_all=None, table=None):
        def run():
            saved = copy.deepcopy(ci_make_cases.CASE_SECONDS)
            try:
                if order is not None:
                    ci_make_cases.start_order = order
                if execute_all is not None:
                    cases.execute_all = execute_all
                with tempfile.TemporaryDirectory(prefix="nc-cases-") as root:
                    cases.start_order_controls(Path(root))
                if table is not None:
                    ci_make_cases.CASE_SECONDS.update(table)
                    for suite, cost in ci_make_cases.CASE_SECONDS.items():
                        live = ci_make_cases.inventory(ci_make_cases.ROOT / "tb/verilator" / suite)
                        assert set(cost) <= set(live), (suite, sorted(set(cost) - set(live)))
            finally:
                ci_make_cases.start_order, cases.execute_all = original_order, original_all
                ci_make_cases.CASE_SECONDS.clear()
                ci_make_cases.CASE_SECONDS.update(saved)
        return run

    def drops_unmeasured(suite, selected):
        cost = ci_make_cases.CASE_SECONDS.get(suite, {})
        return sorted((n for n in selected if n in cost), key=lambda n: -cost[n])

    def ignores_cost(suite, selected):
        return list(selected)

    def results_in_start_order(directory, suite, selected, forms, jobs):
        order = ci_make_cases.start_order(suite, selected)
        out = original_all(directory, suite, selected, forms, jobs)
        by_name = dict(zip(selected, out))
        return [by_name[n] for n in order]

    for label, kwargs in (
            ("start order drops a case the table does not name", dict(order=drops_unmeasured)),
            ("start order ignores the table", dict(order=ignores_cost)),
            ("results returned in start order, not driver order", dict(execute_all=results_in_start_order)),
            ("the table names a case the suite does not have",
             dict(table={"milan_dp": {**ci_make_cases.CASE_SECONDS["milan_dp"], "aclk-typo": 9999}}))):
        results.append(expect_refusal(label, with_patch(**kwargs)))
    print(f"negative controls: {sum(results)}/{len(results)} caught")
    return 0 if all(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
