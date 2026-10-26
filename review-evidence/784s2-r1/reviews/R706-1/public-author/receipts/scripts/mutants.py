#!/usr/bin/env python3
"""Plant one defect per scratch copy and record which named checks fail.

usage: mutants.py <checkout> <python> <outdir> <dev-sha> [act] [vacuity] [tree]

act_ci.py mutants: one exact replacement (exactly one occurrence) in a scratch
copy of the head's scripts/act_ci.py, installed 0555 and run the way the runner
contract gate runs it: python3 -I <copy> --selftest --worktree <checkout>.
Tree mutants: a scratch detached worktree of HEAD, one exact edit, optionally
regenerated through scripts/ci_gate_workflows.py, then the named gates.
Every scratch copy and worktree is removed; the checkout is never edited.
"""

import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

LABELS = 'RUNS_ON_LABELS = ("ubuntu-24.04",)'
PLATFORMS = '*(word for label in RUNS_ON_LABELS for word in ("--platform", f"{label}={RUNNER_IMAGE}")),'
REFUSAL = 'f"workflow {relative} job {job_id} runs on {runs_on!r}; only the "'
ACT_MUTANTS = {
    "readd-ubuntu-latest": (LABELS, 'RUNS_ON_LABELS = ("ubuntu-latest", "ubuntu-24.04")'),
    "latest-only": (LABELS, 'RUNS_ON_LABELS = ("ubuntu-latest",)'),
    "label-unchecked": ("if runs_on not in RUNS_ON_LABELS:", "if runs_on is None:"),
    "platform-entry-dropped": (PLATFORMS, "*(),"),
    "platform-maps-latest-too": (PLATFORMS, PLATFORMS.replace("in RUNS_ON_LABELS", 'in ("ubuntu-latest", *RUNS_ON_LABELS)')),
    "refusal-omits-label": (REFUSAL, 'f"workflow {relative} job {job_id} runs on an unaccepted label; only the "'),
    "container-refusal-removed": ('if "container" in job or "services" in job:', "if False:"),
    "action-refusal-removed": ("if not isinstance(action, str) or action not in TRUSTED_ACTION_USES:",
                               "if not isinstance(action, str):"),
    "reusable-refusal-removed": ('            if "uses" in job:\n', "            if False:\n"),
}
#: Why the fixtures and the sandbox-policy arms had to follow the label.
#: dev-narrowed-only: dev's act_ci.py with only its labels narrowed, the
#: step-2 edit without the fixture follow-up. old-sandbox-arms*: the head with
#: dev's selftest_sandbox_policy (Refusal-only arms on ubuntu-latest fixtures)
#: put back, alone and with one authority refusal deleted: the deleted refusal
#: is not seen, because the fixture is refused by its label first.
DEV_LABELS = 'RUNS_ON_LABELS = ("ubuntu-latest", "ubuntu-24.04")'
CONTAINER = ('if "container" in job or "services" in job:', "if False:")
ACTION = ("if not isinstance(action, str) or action not in TRUSTED_ACTION_USES:", "if not isinstance(action, str):")
OLD_ARMS = "old-sandbox-arms"
VACUITY = {
    "dev-narrowed-only": ("dev", [(DEV_LABELS, LABELS)]),
    "old-sandbox-arms": (OLD_ARMS, []),
    "old-sandbox-arms-container-refusal-removed": (OLD_ARMS, [CONTAINER]),
    "old-sandbox-arms-action-refusal-removed": (OLD_ARMS, [ACTION]),
}


def function_text(source: str, name: str) -> str:
    """The text of top-level function `name` in `source`, up to the next top-level def."""
    start = source.index(f"\ndef {name}(") + 1
    return source[start:source.index("\ndef ", start) + 1]
CONTRACT_GATE = "contract-gate"
TREE_MUTANTS = {
    "template-job-on-latest": {
        "edit": (".github/ci-templates/docs.yml",
                 "  wire-accountability:\n    runs-on: ubuntu-24.04\n",
                 "  wire-accountability:\n    runs-on: ubuntu-latest\n"),
        "regenerate": True,
        "gates": ["gen-check", "ci-events-check", CONTRACT_GATE]},
    "generator-emits-latest": {
        "edit": ("scripts/ci_runtime_workflows.py",
                 '"name": "Fail fast across this head", "runs-on": "ubuntu-24.04"',
                 '"name": "Fail fast across this head", "runs-on": "ubuntu-latest"'),
        "regenerate": False,
        "gates": ["gen-check"]},
    "generator-emits-latest-regenerated": {
        "edit": ("scripts/ci_runtime_workflows.py",
                 '"name": "Fail fast across this head", "runs-on": "ubuntu-24.04"',
                 '"name": "Fail fast across this head", "runs-on": "ubuntu-latest"'),
        "regenerate": True,
        "gates": ["gen-check", "ci-events-check", CONTRACT_GATE]},
    "hand-edited-workflow": {
        "edit": (".github/workflows/rtl.yml",
                 "  verilator-suites:\n", None),
        "regenerate": False,
        "gates": ["gen-check", "ci-events-check"]},
    "physical-job-on-latest": {
        "edit": (".github/ci-templates/rtl.yml",
                 "    name: Physical gPTP (nightly and manual)\n", None),
        "regenerate": True,
        "gates": ["gen-check", "ci-events-check", CONTRACT_GATE]},
}


def replace_once(text: str, old: str, new: str, where: str) -> str:
    """`text` with the single occurrence of `old` replaced; anything else is an error."""
    if text.count(old) != 1:
        raise SystemExit(f"{where}: expected exactly one {old!r}, found {text.count(old)}")
    return text.replace(old, new)


def next_runs_on(text: str, anchor: str, where: str) -> str:
    """Move the first `runs-on: ubuntu-24.04` after the single `anchor` to ubuntu-latest."""
    if text.count(anchor) != 1:
        raise SystemExit(f"{where}: expected exactly one {anchor!r}")
    start = text.index(anchor)
    at = text.index("runs-on: ubuntu-24.04", start)
    return text[:at] + "runs-on: ubuntu-latest" + text[at + len("runs-on: ubuntu-24.04"):]


def run(argv: list[str], cwd: pathlib.Path) -> tuple[int, str]:
    """Return code and combined output of `argv`, never through a shell pipe."""
    done = subprocess.run(argv, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return done.returncode, done.stdout


def contract_gate(python: str, source: str, worktree: pathlib.Path) -> tuple[int, str]:
    """Install `source` as a 0555 flat copy and run it as docs-gates-2 does."""
    with tempfile.TemporaryDirectory(prefix="a679-install-") as raw:
        copy = pathlib.Path(raw) / "act_ci.py"
        copy.write_text(source, encoding="utf-8")
        copy.chmod(0o555)
        return run([python, "-I", str(copy), "--selftest", "--worktree", str(worktree)], worktree)


def fails(output: str) -> list[str]:
    """The FAIL lines of a self-test; for a check gate, every line that is not an ok or note line."""
    if "\n  ok " in output:
        return [line.strip() for line in output.splitlines() if line.startswith("  FAIL")]
    return [line.strip() for line in output.splitlines()
            if line.strip() and not line.lstrip().startswith(("ok ", "note "))][:40]


def record(out: pathlib.Path, name: str, row: dict, output: str) -> None:
    """Write the mutant's JSON receipt and its full log."""
    (out / f"{name}.log").write_text(output, encoding="utf-8")
    (out / f"{name}.json").write_text(json.dumps(row, indent=2) + "\n", encoding="utf-8")
    print(f"{name}: rc={row.get('rc', row.get('gates'))} failures={len(row.get('failures', []))}", flush=True)


def act_mutants(checkout: pathlib.Path, python: str, out: pathlib.Path) -> None:
    """The control and each act_ci.py mutant."""
    head = (checkout / "scripts/act_ci.py").read_text(encoding="utf-8")
    rc, output = contract_gate(python, head, checkout)
    record(out, "control", {"rc": rc, "failures": fails(output), "ok": output.count("\n  ok ")}, output)
    for name, (old, new) in ACT_MUTANTS.items():
        rc, output = contract_gate(python, replace_once(head, old, new, name), checkout)
        record(out, name, {"replace": old, "with": new, "rc": rc, "failures": fails(output)}, output)


def vacuity(checkout: pathlib.Path, python: str, out: pathlib.Path, dev: str) -> None:
    """The demonstrations that the fixtures and the sandbox-policy arms had to follow the label."""
    head = (checkout / "scripts/act_ci.py").read_text(encoding="utf-8")
    base = subprocess.run(["git", "-C", str(checkout), "show", f"{dev}:scripts/act_ci.py"],
                          check=True, stdout=subprocess.PIPE, text=True).stdout
    old_arms = head.replace(function_text(head, "selftest_sandbox_policy"),
                            function_text(base, "selftest_sandbox_policy"))
    for name, (start, edits) in VACUITY.items():
        source = base if start == "dev" else old_arms
        for old, new in edits:
            source = replace_once(source, old, new, name)
        rc, output = contract_gate(python, source, checkout)
        watched = [line.strip() for line in output.splitlines()
                   if "container authority is refused" in line or "step-level action" in line]
        tail = [line for line in output.splitlines() if line.startswith("Refusal: ")][-1:]
        record(out, name, {"start": start, "edits": edits, "rc": rc, "watched_arms": watched,
                           "failures": fails(output), "uncaught": tail}, output)


def tree_mutants(checkout: pathlib.Path, python: str, out: pathlib.Path) -> None:
    """Each tree mutant in its own scratch worktree, removed afterwards."""
    head_act = (checkout / "scripts/act_ci.py").read_text(encoding="utf-8")
    for name, spec in TREE_MUTANTS.items():
        scratch = pathlib.Path(tempfile.mkdtemp(prefix=f"a679-mut-{name}-"))
        shutil.rmtree(scratch)
        subprocess.run(["git", "-C", str(checkout), "worktree", "add", "--quiet", "--detach", str(scratch), "HEAD"],
                       check=True)
        try:
            path, old, new = spec["edit"]
            target = scratch / path
            text = target.read_text(encoding="utf-8")
            target.write_text(next_runs_on(text, old, name) if new is None else replace_once(text, old, new, name),
                              encoding="utf-8")
            logs = []
            if spec["regenerate"]:
                rc, output = run([python, "scripts/ci_gate_workflows.py"], scratch)
                logs.append(f"$ regenerate rc={rc}\n{output}")
            gates = {}
            failures = {}
            for gate in spec["gates"]:
                if gate == CONTRACT_GATE:
                    rc, output = contract_gate(python, head_act, scratch)
                else:
                    argv = {"gen-check": ["scripts/ci_gate_workflows.py", "--check"],
                            "ci-events-check": ["scripts/ci_events.py", "--check"]}[gate]
                    rc, output = run([python, *argv], scratch)
                gates[gate] = rc
                failures[gate] = fails(output)
                logs.append(f"$ {gate} rc={rc}\n{output}")
            diff = run(["git", "diff", "--stat"], scratch)[1]
            record(out, name, {"edit": spec["edit"], "regenerated": spec["regenerate"], "gates": gates,
                               "failures": failures, "diff_stat": diff.splitlines()}, "\n".join(logs))
        finally:
            subprocess.run(["git", "-C", str(checkout), "worktree", "remove", "--force", str(scratch)], check=True)


def main() -> int:
    checkout, python, outdir, dev, *parts = sys.argv[1:]
    out = pathlib.Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    root = pathlib.Path(checkout).resolve()
    parts = parts or ["act", "vacuity", "tree"]
    if "act" in parts:
        act_mutants(root, python, out)
    if "vacuity" in parts:
        vacuity(root, python, out, dev)
    if "tree" in parts:
        tree_mutants(root, python, out)
    return 0


if __name__ == "__main__":
    os.umask(0o022)
    raise SystemExit(main())
