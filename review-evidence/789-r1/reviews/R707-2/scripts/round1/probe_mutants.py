#!/usr/bin/env python3
"""Plant generator-code and generated-workflow mutants in disposable copies of an exported head tree.

Usage: probe_mutants.py <exported-head-tree> <scratch-dir> <receipt-dir>

Each mutant gets its own copy. For a generator-code mutant the copy's workflow is
regenerated with the mutated generator (as an author would), then the exact-head
judges run: ci_gate_workflows.py --check, ci_gate_workflows_selftest.py and
ci_events.py --check. For a hand edit of the generated workflow only the two
check modes run. A mutant is CAUGHT when at least one judge exits non-zero.
"""
import concurrent.futures
import json
import pathlib
import shutil
import subprocess
import sys

GEN = "scripts/ci_gate_workflows.py"
WF = ".github/workflows/rtl-fast.yml"

CONSUMER_SPLICE = ('    consumer["steps"][at:at + 2] = [{"name": "Restore the pinned Yosys build", "uses": cache["uses"],\n'
                   '                                     "with": {"path": cache["with"]["path"], "key": key,\n'
                   '                                              "fail-on-cache-miss": True}}]\n')


def drop_consumer_step(name: str) -> tuple[str, str]:
    """Generator mutant: drop one retained check from yosys-elaboration after the splice."""
    return (CONSUMER_SPLICE, CONSUMER_SPLICE + '    consumer["steps"] = [s for s in consumer["steps"] if s.get("name") != '
            + json.dumps(name) + "]\n")


GENERATOR_MUTANTS = {
    "G01 consumer drops 'Elaborate the integration-heavy tops'": drop_consumer_step("Elaborate the integration-heavy tops"),
    "G02 consumer drops 'Install the pinned Yosys and prove the version'":
        drop_consumer_step("Install the pinned Yosys and prove the version"),
    "G03 consumer drops 'Fetch RTL dependencies'": drop_consumer_step("Fetch RTL dependencies"),
    "G04 consumer drops 'Prove the result cache refuses a planted entry'":
        drop_consumer_step("Prove the result cache refuses a planted entry"),
    "G05 consumer drops 'Install the pinned sv2v release'": drop_consumer_step("Install the pinned sv2v release"),
    "G06 restore accepts a miss": ('"fail-on-cache-miss": True}}]', '}}]'),
    "G07 restore gains a fallback": ('"fail-on-cache-miss": True}}]', '"fail-on-cache-miss": True, "restore-keys": "yosys-"}}]'),
    "G08 recipe digest is a constant": ('json.dumps(build, sort_keys=True', 'json.dumps({}, sort_keys=True'),
    "G09 key drops the runner image": ('"recipe-" + recipe_digest(build) + "-" + image)', '"recipe-" + recipe_digest(build))'),
    "G10 key keeps the workflow-file digest": ('return key.replace(WORKFLOW_FILES_DIGEST, "recipe-"',
                                               'return key.replace("@@never@@", "recipe-"'),
    "G11 verdict not wired": ('    require_fast_tool(jobs[FAST_AGGREGATE])\n', ''),
    "G12 tool timeout 31": ('FAST_TOOL_TIMEOUT = 30', 'FAST_TOOL_TIMEOUT = 31'),
    "G13 tool job runs unconditionally": ('"if": consumer["if"],', '"if": "${{ always() }}",'),
    "G14 tool job appended after the aggregate": (
        '        if job_id == FAST_TOOL_CONSUMER:\n            ordered[FAST_TOOL_JOB] = tool\n        ordered[job_id] = job\n',
        '        ordered[job_id] = job\n    ordered[FAST_TOOL_JOB] = tool\n'),
    "G15 consumer keeps its build (no splice)": (CONSUMER_SPLICE, CONSUMER_SPLICE.replace('consumer["steps"][at:at + 2] =', 'consumer["steps"][at + 2:at + 2] =')),
    "G16 tool job saves under the unpinned template key": ('    moved["with"]["key"] = key\n', ''),
    "G17 recipe digest over the whole consumer job": ('fast_tool_key(cache, build, consumer["runs-on"])',
                                                    'fast_tool_key(cache, {"steps": consumer["steps"]}, consumer["runs-on"])'),
}

WORKFLOW_MUTANTS = {
    "W01 hand edit: tool job saves under a different key than the restore": (
        "86f2ddebce7e98ce7cacc27e8a5c14cb53b51b51-recipe-06e5a02fa8b585ca1b3cc3153245cd97f8b1009666d3b15728f325ed9bd22279-ubuntu-24.04-${{\n            runner.os }}\n      - name: Resolve",
        "86f2ddebce7e98ce7cacc27e8a5c14cb53b51b51-recipe-0000000000000000000000000000000000000000000000000000000000000000-ubuntu-24.04-${{\n            runner.os }}\n      - name: Resolve"),
    "W02 hand edit: consumer timeout 45": (
        "      - yosys-tool\n    if: ${{ needs.changes.outputs.rtl == 'true' }}\n    runs-on: ubuntu-24.04\n    timeout-minutes: 30\n",
        "      - yosys-tool\n    if: ${{ needs.changes.outputs.rtl == 'true' }}\n    runs-on: ubuntu-24.04\n    timeout-minutes: 45\n"),
    "W03 hand edit: restore gains restore-keys": (
        "          fail-on-cache-miss: true\n", "          fail-on-cache-miss: true\n          restore-keys: yosys-\n"),
}


def run(cmd: list[str], cwd: pathlib.Path) -> tuple[int, str]:
    """One judge's exit status and last output line."""
    done = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=900, check=False)
    tail = (done.stdout + done.stderr).strip().splitlines()
    return done.returncode, (tail[-1] if tail else "")[:400]


def probe(label: str, kind: str, old: str, new: str, base: pathlib.Path, scratch: pathlib.Path) -> dict:
    """Copy, mutate, regenerate when the mutant is generator code, then judge."""
    copy = scratch / ("m" + label.split()[0])
    if copy.exists():
        shutil.rmtree(copy)
    shutil.copytree(base, copy, symlinks=True)
    target = copy / (GEN if kind == "generator" else WF)
    text = target.read_text()
    if text.count(old) != 1:
        return {"mutant": label, "error": "anchor count " + str(text.count(old))}
    target.write_text(text.replace(old, new))
    row = {"mutant": label}
    if kind == "generator":
        row["regenerate"] = run([sys.executable, GEN], copy)
        row["selftest"] = run([sys.executable, "scripts/ci_gate_workflows_selftest.py"], copy)
    row["gate_check"] = run([sys.executable, GEN, "--check"], copy)
    row["events_check"] = run([sys.executable, "scripts/ci_events.py", "--check"], copy)
    judges = [row[k][0] for k in ("selftest", "gate_check", "events_check") if k in row]
    row["caught"] = any(code != 0 for code in judges) or row.get("regenerate", (0,))[0] != 0
    shutil.rmtree(copy)
    return row


def main() -> int:
    base, scratch, receipts = (pathlib.Path(arg).resolve() for arg in sys.argv[1:4])
    scratch.mkdir(parents=True, exist_ok=True)
    receipts.mkdir(parents=True, exist_ok=True)
    jobs = [(label, "generator", *pair) for label, pair in GENERATOR_MUTANTS.items()]
    jobs += [(label, "workflow", *pair) for label, pair in WORKFLOW_MUTANTS.items()]
    jobs.insert(0, ("C00 control (no mutation)", "generator", "FAST_TOOL_TIMEOUT = 30", "FAST_TOOL_TIMEOUT = 30"))
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
        rows = list(pool.map(lambda job: probe(*job, base, scratch), jobs))
    (receipts / "mutants.json").write_text(json.dumps(rows, indent=1) + "\n")
    for row in rows:
        verdict = "ERROR" if "error" in row else ("CAUGHT" if row["caught"] else "SURVIVED")
        print(verdict, row["mutant"])
        for key in ("regenerate", "selftest", "gate_check", "events_check"):
            if key in row:
                print("    ", key, row[key][0], row[key][1])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
