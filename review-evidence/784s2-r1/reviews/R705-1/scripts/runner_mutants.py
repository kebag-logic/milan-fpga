#!/usr/bin/env python3
"""Plant one exact replacement per mutant in a scratch copy of scripts/act_ci.py and run
it as the runner contract gate runs it (python3 -I <0555 copy> --selftest --worktree <checkout>).

Usage: runner_mutants.py <checkout> <python> <scratch-dir> <out-dir>
Each mutant must apply exactly once. The control (no edit) must exit 0; every mutant
is expected to exit non-zero with named FAIL lines, recorded in <out-dir>/<name>.log.
Runs at most 16 mutants at once. Offline only: DOCKER_HOST names a missing socket.
"""
import concurrent.futures
import os
import pathlib
import subprocess
import sys

MUTANTS = {
    "control": None,
    # Re-admit ubuntu-latest beside ubuntu-24.04 (the reverse order of dev's tuple).
    "readmit-latest": ('RUNS_ON_LABELS = ("ubuntu-24.04",)',
                       'RUNS_ON_LABELS = ("ubuntu-24.04", "ubuntu-latest")'),
    # Only ubuntu-latest accepted.
    "latest-only": ('RUNS_ON_LABELS = ("ubuntu-24.04",)', 'RUNS_ON_LABELS = ("ubuntu-latest",)'),
    # Drop the platform entry from the act command entirely.
    "drop-platform-entry": (
        '        *(word for label in RUNS_ON_LABELS for word in ("--platform", f"{label}={RUNNER_IMAGE}")),\n',
        ""),
    # Platform entry names ubuntu-latest instead of the accepted label.
    "platform-wrong-label": ('("--platform", f"{label}={RUNNER_IMAGE}")',
                             '("--platform", f"ubuntu-latest={RUNNER_IMAGE}")'),
    # Platform entry maps the label to act's default node image.
    "platform-wrong-image": ('("--platform", f"{label}={RUNNER_IMAGE}")',
                             '("--platform", f"{label}=node:16-buster-slim")'),
    # The sandbox also admits ubuntu-latest, which the platform list does not map.
    "sandbox-admits-latest": ("            if runs_on not in RUNS_ON_LABELS:\n",
                              '            if runs_on not in (*RUNS_ON_LABELS, "ubuntu-latest"):\n'),
    # The sandbox admits any ubuntu- prefix.
    "sandbox-prefix": ("            if runs_on not in RUNS_ON_LABELS:\n",
                       '            if not str(runs_on).startswith("ubuntu-"):\n'),
    # The runs-on check is removed (every label passes).
    "sandbox-no-label-check": ("            if runs_on not in RUNS_ON_LABELS:\n",
                               "            if False:\n"),
    # Refusal text no longer names the refused label.
    "refusal-unnamed": ('runs on {runs_on!r}; only the "', 'runs on an unsupported label; only the "'),
    # Job/service container refusal deleted.
    "container-refusal-deleted": ('            if "container" in job or "services" in job:\n',
                                  "            if False:\n"),
}


def run(name: str, edit, checkout: pathlib.Path, python: str, scratch: pathlib.Path, out: pathlib.Path) -> str:
    source = (checkout / "scripts" / "act_ci.py").read_text(encoding="utf-8")
    if edit is not None:
        old, new = edit
        count = source.count(old)
        if count != 1:
            return f"{name}: NOT APPLIED (pattern occurs {count} times)"
        source = source.replace(old, new)
    directory = scratch / name
    directory.mkdir(parents=True, exist_ok=True)
    copy = directory / "act_ci.py"
    if copy.exists():
        copy.chmod(0o644)
    copy.write_text(source, encoding="utf-8")
    copy.chmod(0o555)
    env = {"PATH": f"{pathlib.Path(python).parent}:/usr/bin:/bin", "HOME": str(directory),
           "DOCKER_HOST": "unix:///nonexistent/docker.sock", "PYTHONDONTWRITEBYTECODE": "1"}
    proc = subprocess.run([python, "-I", str(copy), "--selftest", "--worktree", str(checkout)],
                          capture_output=True, text=True, env=env, cwd=directory, timeout=1500)
    log = proc.stdout + proc.stderr
    (out / f"{name}.log").write_text(log, encoding="utf-8")
    fails = [line.strip() for line in log.splitlines() if line.lstrip().startswith("FAIL")]
    oks = sum(1 for line in log.splitlines() if line.startswith("  ok "))
    lines = [f"{name}: rc={proc.returncode} ok={oks} FAIL={len(fails)}"]
    lines += [f"    {line}" for line in fails]
    if proc.returncode != 0 and not fails:
        lines += [f"    (no FAIL line) last: {log.strip().splitlines()[-1] if log.strip() else ''}"]
    return "\n".join(lines)


def main() -> int:
    checkout, python, scratch, out = (pathlib.Path(sys.argv[1]), sys.argv[2],
                                      pathlib.Path(sys.argv[3]), pathlib.Path(sys.argv[4]))
    out.mkdir(parents=True, exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as pool:
        futures = {name: pool.submit(run, name, edit, checkout, python, scratch, out)
                   for name, edit in MUTANTS.items()}
        results = [futures[name].result() for name in MUTANTS]
    text = "\n".join(results) + "\n"
    (out / "summary.txt").write_text(text, encoding="utf-8")
    print(text, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
