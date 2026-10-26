#!/usr/bin/env python3
"""Plant one exact edit per tree mutant in its own scratch copy of the checkout, optionally
regenerate the workflows through scripts/ci_gate_workflows.py, commit it in the copy, and run
three gates against it: the generator check mode, ci_events.py --check, and the runner
contract gate (the reviewed head's act_ci.py installed 0555, --selftest --worktree <copy>).

Usage: tree_mutants.py <checkout> <python-bin-dir> <scratch-dir> <out-dir>
Every edit must match exactly once. Offline only; nothing is pushed.
"""
import concurrent.futures
import pathlib
import shutil
import subprocess
import sys

YOSYS_SHARD_TEMPLATE = (
    "    name: Yosys shard ${{ matrix.shard }}/${{ matrix.total }}\n"
    "    needs: full-ci-gate\n"
    "    if: ${{ needs.full-ci-gate.outputs.run_full == 'true' }}\n"
    "    runs-on: ubuntu-24.04\n")
MUTANTS = {
    "control": ([], False),
    "template-job-latest-regen": (
        [(".github/ci-templates/rtl.yml", YOSYS_SHARD_TEMPLATE,
          YOSYS_SHARD_TEMPLATE.replace("ubuntu-24.04", "ubuntu-latest"))], True),
    "template-job-latest-noregen": (
        [(".github/ci-templates/rtl.yml", YOSYS_SHARD_TEMPLATE,
          YOSYS_SHARD_TEMPLATE.replace("ubuntu-24.04", "ubuntu-latest"))], False),
    "union-generator-latest-noregen": (
        [("scripts/ci_suite_workflows.py", '"runs-on": "ubuntu-24.04", "timeout-minutes": 2,',
          '"runs-on": "ubuntu-latest", "timeout-minutes": 2,')], False),
    "union-generator-latest-regen": (
        [("scripts/ci_suite_workflows.py", '"runs-on": "ubuntu-24.04", "timeout-minutes": 2,',
          '"runs-on": "ubuntu-latest", "timeout-minutes": 2,')], True),
    "tail-guard-generator-2604-regen": (
        [("scripts/ci_runtime_workflows.py", '"name": "Cancel late CI failures", "runs-on": "ubuntu-24.04"',
          '"name": "Cancel late CI failures", "runs-on": "ubuntu-26.04"')], True),
    "workflow-hand-edit-2204": (
        [(".github/workflows/elaborate.yml", "  elaborate:\n    runs-on: ubuntu-24.04\n",
          "  elaborate:\n    runs-on: ubuntu-22.04\n")], False),
    "ci-events-physical-latest": (
        [("scripts/ci_events.py", "    'runs-on': 'ubuntu-24.04',\n", "    'runs-on': 'ubuntu-latest',\n")], False),
}


def sh(args, cwd, env, log):
    proc = subprocess.run(args, cwd=cwd, env=env, capture_output=True, text=True, timeout=1500)
    log.append(f"$ {' '.join(map(str, args))}\nrc={proc.returncode}\n{proc.stdout}{proc.stderr}")
    return proc


def run(name, edits, regen, checkout, bindir, scratch, out):
    tree = scratch / f"tree-{name}"
    if tree.exists():
        shutil.rmtree(tree)
    shutil.copytree(checkout, tree, symlinks=True)
    env = {"PATH": f"{bindir}:/usr/bin:/bin", "HOME": str(tree.parent), "PYTHONDONTWRITEBYTECODE": "1",
           "DOCKER_HOST": "unix:///nonexistent/docker.sock", "GIT_AUTHOR_NAME": "probe",
           "GIT_AUTHOR_EMAIL": "probe@invalid", "GIT_COMMITTER_NAME": "probe",
           "GIT_COMMITTER_EMAIL": "probe@invalid"}
    log = []
    for rel, old, new in edits:
        path = tree / rel
        text = path.read_text(encoding="utf-8")
        if text.count(old) != 1:
            return f"{name}: NOT APPLIED ({rel}: {text.count(old)} matches)"
        path.write_text(text.replace(old, new), encoding="utf-8")
    if regen:
        sh(["python3", "scripts/ci_gate_workflows.py"], tree, env, log)
    if edits:
        sh(["git", "commit", "-qam", f"probe {name}"], tree, env, log)
    diff = sh(["git", "diff", "--stat", "HEAD~1" if edits else "HEAD"], tree, env, log)
    gen = sh(["python3", "scripts/ci_gate_workflows.py", "--check"], tree, env, log)
    events = sh(["python3", "scripts/ci_events.py", "--check"], tree, env, log)
    install = scratch / f"install-{name}"
    install.mkdir(parents=True, exist_ok=True)
    copy = install / "act_ci.py"
    if copy.exists():
        copy.chmod(0o644)
    shutil.copyfile(checkout / "scripts" / "act_ci.py", copy)
    copy.chmod(0o555)
    gate = sh(["python3", "-I", str(copy), "--selftest", "--worktree", str(tree)], install, env, log)
    (out / f"{name}.log").write_text("\n".join(log), encoding="utf-8")
    fails = [l.strip() for l in (gate.stdout + gate.stderr).splitlines() if l.lstrip().startswith("FAIL")]
    gen_find = [l.strip() for l in (gen.stdout + gen.stderr).splitlines() if l.strip()][-2:]
    ev_find = [l.strip() for l in (events.stdout + events.stderr).splitlines()
               if "physical-gptp" in l or "must" in l][:2]
    lines = [f"{name}: changed={diff.stdout.strip().splitlines()[-1] if diff.stdout.strip() else 'none'}",
             f"    generator --check rc={gen.returncode}" + (f" :: {gen_find}" if gen.returncode else ""),
             f"    ci_events --check rc={events.returncode}" + (f" :: {ev_find}" if events.returncode else ""),
             f"    runner contract gate rc={gate.returncode} FAIL={len(fails)}"]
    lines += [f"        {f}" for f in fails]
    shutil.rmtree(tree)
    return "\n".join(lines)


def main():
    checkout, bindir, scratch, out = (pathlib.Path(sys.argv[1]), sys.argv[2],
                                      pathlib.Path(sys.argv[3]), pathlib.Path(sys.argv[4]))
    out.mkdir(parents=True, exist_ok=True)
    scratch.mkdir(parents=True, exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        futures = {n: pool.submit(run, n, e, r, checkout, bindir, scratch, out) for n, (e, r) in MUTANTS.items()}
        results = [futures[n].result() for n in MUTANTS]
    text = "\n".join(results) + "\n"
    (out / "summary.txt").write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
