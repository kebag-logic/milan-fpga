#!/usr/bin/env python3
"""Round-2 port of round1/probe_mutants.py to the head's generator, plus mutants aimed at the round-2 delta.

Usage: probe_mutants_r2.py <git-backed-head-copy> <scratch-dir> <receipt-dir>

Same procedure as round 1: each mutant gets its own disposable copy; a generator-code
mutant regenerates the workflow with the mutated generator (as an author would), then the
exact-head judges run: ci_gate_workflows.py --check, ci_gate_workflows_selftest.py and
ci_events.py --check. A workflow hand edit runs only the two check modes. CAUGHT means at
least one judge (or the regeneration itself) exits non-zero. `named` records the refusal
words the probe expects to find in the judges' output, when the mutant has one.
Only the anchors changed from round 1 where the head refactored the code they matched.
"""
import concurrent.futures
import json
import pathlib
import shutil
import subprocess
import sys

GEN = "scripts/ci_gate_workflows.py"
WF = ".github/workflows/rtl-fast.yml"

SPLICE = ('                                              "fail-on-cache-miss": True}}]\n'
          '    require_fast_tool(jobs[FAST_AGGREGATE])\n')


def drop_consumer_step(name: str) -> tuple[str, str, str]:
    """Generator mutant: drop one retained check from yosys-elaboration right after the splice."""
    return (SPLICE, SPLICE.replace("    require_fast_tool", '    consumer["steps"] = [s for s in consumer["steps"] if '
                                   's.get("name") != ' + json.dumps(name) + "]\n    require_fast_tool"),
            "yosys-elaboration drops " + name)


BIND = "    for job_id, name in keyed:\n"
TOOL_KEY_LINE = ("86f2ddebce7e98ce7cacc27e8a5c14cb53b51b51-recipe-e15c97b1c78fe65063d60516fd3cc9f594e30beee1e2862da"
                 "7554b41692ebc1b-${{\n            hashFiles('scripts/ci_install_cache.py') }}-ubuntu-24.04-${{ runner.os }}\n"
                 "      - name: Resolve")

GENERATOR_MUTANTS = {
    # Round-1 mutants, re-anchored to the head's code (same defect).
    "G01 consumer drops 'Elaborate the integration-heavy tops'": drop_consumer_step("Elaborate the integration-heavy tops"),
    "G02 consumer drops 'Install the pinned Yosys and prove the version'":
        drop_consumer_step("Install the pinned Yosys and prove the version"),
    "G03 consumer drops 'Fetch RTL dependencies'": drop_consumer_step("Fetch RTL dependencies"),
    "G04 consumer drops 'Prove the result cache refuses a planted entry'":
        drop_consumer_step("Prove the result cache refuses a planted entry"),
    "G05 consumer drops 'Install the pinned sv2v release'": drop_consumer_step("Install the pinned sv2v release"),
    "G08 recipe digest is a constant": ("hashlib.sha256(json.dumps(inputs,", "hashlib.sha256(json.dumps({},", None),
    "G09 key drops the runner image": ('FAST_TOOL_RECIPE + "-" + image)', "FAST_TOOL_RECIPE)", None),
    "G10 key keeps the workflow-file digest": ("return key.replace(WORKFLOW_FILES_DIGEST, FAST_TOOL_RECIPE",
                                               'return key.replace("@@never@@", FAST_TOOL_RECIPE', None),
    "G15 consumer keeps its build (no splice)": ('    consumer["steps"][at:at + 2] = [{"name": FAST_TOOL_RESTORE',
                                                 '    consumer["steps"][at + 2:at + 2] = [{"name": FAST_TOOL_RESTORE',
                                                 None),
    # Round-2 delta: each removes one input or guard the delta added.
    "N01 digest omits the workflow env and defaults": ('for key in ("env", "defaults")}', "for key in ()}", None),
    "N02 digest omits the tool job's own keys": ('if key not in (*FAST_TOOL_SCHEDULING, "steps")}', "if False}", None),
    "N03 digest over the build step only (round-1 behaviour)": (
        'recipe = "recipe-" + recipe_digest(inputs)', 'recipe = "recipe-" + recipe_digest(inputs["job"]["steps"][-1])',
        None),
    "N04 key drops the script binding": ("    if reads:\n", "    if False:\n",
                                         "tool key does not bind the scripts its build steps run"),
    "N05 restore not rebound to the digest": (BIND, "    for job_id, name in keyed[:1]:\n", None),
    "N06 tool job carries no job env": ("for carried in FAST_TOOL_CARRIED[1:] if carried in consumer",
                                        "for carried in () if carried in consumer", "tool job lost the consumer env"),
    "N07 after-build step guard removed": ("    if [step.get(\"id\") for step in after] != list(FAST_TOOL_EVIDENCE):\n",
                                           "    if False:\n", "accepted a step after the build"),
    "N08 key never bound (stand-in left)": ("        bind_fast_tool_key(result)\n", "        pass\n", None),
    "N09 repository-read scan never matches": ('REPOSITORY_READ = re.compile(r"(?<!', 'REPOSITORY_READ = re.compile(r"(?!x)x(?<!',
                                               "tool key does not bind the scripts its build steps run"),
    "N10 unmodelled consumer job keys accepted": ("    if unmodelled:\n", "    if False:\n",
                                                  "job keys the tool job does not carry into the build: container"),
    # A drop after the derivation, inside the delta's own post-transform hook.
    "N11 post-transform hook drops a retained self-test": (
        BIND, BIND.replace("    for", '    workflow["jobs"][FAST_TOOL_CONSUMER]["steps"] = [s for s in workflow["jobs"]'
                           '[FAST_TOOL_CONSUMER]["steps"] if s.get("name") != "Prove the result cache refuses a planted '
                           'entry"]\n    for'), None),
}

WORKFLOW_MUTANTS = {
    "W01 hand edit: tool job saves under a different key than the restore": (
        TOOL_KEY_LINE, TOOL_KEY_LINE.replace("e15c97b1c78fe65063d60516fd3cc9f594e30beee1e2862da7554b41692ebc1b",
                                             "0" * 64), None),
    "W02 hand edit: consumer timeout 45": (
        "      - yosys-tool\n    if: ${{ needs.changes.outputs.rtl == 'true' }}\n    runs-on: ubuntu-24.04\n    timeout-minutes: 30\n",
        "      - yosys-tool\n    if: ${{ needs.changes.outputs.rtl == 'true' }}\n    runs-on: ubuntu-24.04\n    timeout-minutes: 45\n",
        None),
    "W03 hand edit: restore gains restore-keys": (
        "          fail-on-cache-miss: true\n", "          fail-on-cache-miss: true\n          restore-keys: yosys-\n", None),
    "W04 hand edit: tool job env CXXFLAGS": (
        "    needs: changes\n    if: ${{ needs.changes.outputs.rtl == 'true' }}\n    steps:\n      - uses: actions/checkout@v4\n",
        "    needs: changes\n    if: ${{ needs.changes.outputs.rtl == 'true' }}\n    env:\n      CXXFLAGS: -O0\n    steps:\n"
        "      - uses: actions/checkout@v4\n", None),
}


def run(cmd: list[str], cwd: pathlib.Path) -> tuple[int, str, str]:
    """One judge's exit status, last output line and whole output."""
    done = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=900, check=False)
    text = done.stdout + done.stderr
    tail = text.strip().splitlines()
    return done.returncode, (tail[-1] if tail else "")[:400], text


def probe(label: str, kind: str, old: str, new: str, words: str | None, base: pathlib.Path,
          scratch: pathlib.Path) -> dict:
    """Copy, mutate, regenerate when the mutant is generator code, then judge."""
    copy = scratch / ("m" + label.split()[0])
    if copy.exists():
        shutil.rmtree(copy)
    shutil.copytree(base, copy, symlinks=True)
    target = copy / (GEN if kind == "generator" else WF)
    text = target.read_text()
    if text.count(old) != 1:
        shutil.rmtree(copy)
        return {"mutant": label, "error": "anchor count " + str(text.count(old))}
    target.write_text(text.replace(old, new))
    row, outputs = {"mutant": label}, []
    if kind == "generator":
        code, tail, out = run([sys.executable, GEN], copy)
        row["regenerate"], outputs = (code, tail), outputs + [out]
        code, tail, out = run([sys.executable, "scripts/ci_gate_workflows_selftest.py"], copy)
        row["selftest"], outputs = (code, tail), outputs + [out]
    for key, cmd in (("gate_check", [sys.executable, GEN, "--check"]),
                     ("events_check", [sys.executable, "scripts/ci_events.py", "--check"])):
        code, tail, out = run(cmd, copy)
        row[key], outputs = (code, tail), outputs + [out]
    judges = [row[k][0] for k in ("regenerate", "selftest", "gate_check", "events_check") if k in row]
    row["caught"] = any(code != 0 for code in judges)
    if words:
        row["named"] = words
        row["named_found"] = any(words in out for out in outputs)
    shutil.rmtree(copy)
    return row


def main() -> int:
    base, scratch, receipts = (pathlib.Path(arg).resolve() for arg in sys.argv[1:4])
    scratch.mkdir(parents=True, exist_ok=True)
    receipts.mkdir(parents=True, exist_ok=True)
    jobs = [(label, "generator", *triple) for label, triple in GENERATOR_MUTANTS.items()]
    jobs += [(label, "workflow", *triple) for label, triple in WORKFLOW_MUTANTS.items()]
    jobs.insert(0, ("C00 control (no mutation)", "generator", "FAST_TOOL_TIMEOUT = 30", "FAST_TOOL_TIMEOUT = 30", None))
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
        rows = list(pool.map(lambda job: probe(*job, base, scratch), jobs))
    (receipts / "mutants.json").write_text(json.dumps(rows, indent=1) + "\n")
    for row in rows:
        verdict = "ERROR" if "error" in row else ("CAUGHT" if row["caught"] else "SURVIVED")
        named = "" if "named" not in row else (" named=" + str(row["named_found"]))
        print(verdict + named, row["mutant"], row.get("error", ""))
        for key in ("regenerate", "selftest", "gate_check", "events_check"):
            if key in row:
                print("    ", key, row[key][0], row[key][1])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
