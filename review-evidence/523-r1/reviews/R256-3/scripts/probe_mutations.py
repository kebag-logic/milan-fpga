#!/usr/bin/env python3
"""Reviewer negative controls: plant one regression per disposable copy and
require the owning focused test to go red, recording the first failing arm.

Usage: probe_mutations.py SOURCE_CLONE WORKDIR RECEIPT.json BATCH
BATCH is 1 or 2. At most four copies run at once.
"""
import json, os, shutil, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

SOURCE = Path(sys.argv[1]).resolve()
WORK = Path(sys.argv[2]).resolve()
RECEIPT = Path(sys.argv[3]).resolve()
BATCH = sys.argv[4]
SWEEP = "scripts/test_suite_cancellation.py"
LIFE = "tb/verilator/gptp_shadow/test_mutant_lifecycle.py"
OP, RS, MU, PI, MK = ("scripts/owned_process.py", "scripts/run_all_suites.sh", "tb/verilator/gptp_shadow/mutants.py",
                      "tb/verilator/gptp_shadow/private_inputs.py", "tb/verilator/gptp_shadow/Makefile")

MUTANTS = {
    "1": [
        ("M01-no-parent-death-binding", OP, "preexec_fn=self._die_with_owner,", "", [SWEEP, LIFE]),
        ("M02-no-owner-reexec", RS, '  exec python3 "$ROOT/scripts/owned_process.py" -- bash "$0" --owned-sweep "$@"\n',
         '  set -- --owned-sweep "$@"\n', [SWEEP]),
        ("M03-cancel-trap-continues", RS, '  exit "$2"\n}', '  return 0\n}', [SWEEP]),
        ("M04-no-kill-escalation", OP, "signum = signal.SIGKILL if now >= deadline else signal.SIGTERM",
         "signum = signal.SIGTERM", [SWEEP]),
        ("M05-no-root-stop", OP, "                self._signal(self.root_fd, signal.SIGSTOP)\n                self._signal(self.root_fd, signum)\n",
         "                self._signal(self.root_fd, signum)\n", [SWEEP]),
        ("M06-mutate-caller-path", MU, "path = private / original.relative_to(REPO)\n        pristine", "path = original\n        pristine", [LIFE]),
        ("M07-no-mode-check", PI, 'if actual != blob or executable != (mode == "100755"):', "if actual != blob:", [LIFE]),
        ("M08-no-index-vs-head", PI, '    if expected != indexed:\n        raise InputRefused(f"index differs from {revision}: {root}")\n', "", [LIFE]),
        ("M09-hardlink-copy", PI, "        destination.write_bytes(content)\n", "        os.link(source, destination)\n", [LIFE]),
        ("M10-no-git-env-scrub", PI, 'env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}',
         "env = dict(os.environ)", [LIFE]),
    ],
    "2": [
        # (an earlier plant here left GIT_INDEX_FILE in the set; superseded by batch 3)
        ("M12-build-failure-counts-as-caught", MU, "        return int(tally.group(1)) != 0\n    return False\n",
         "        return int(tally.group(1)) != 0\n    return status != 0\n", [LIFE]),
        ("M13-lifecycle-not-default", MK, "all: lifecycle mutants\n", "all: mutants\n", [LIFE]),
        ("M14-no-cancellation-preflight", RS,
         '  if ! selftest_out=$(preflight test_suite_cancellation python3 "$ROOT/scripts/test_suite_cancellation.py" 2>&1); then\n    echo "$selftest_out" >&2\n    echo "ABORTING: sweep cancellation controls failed." >&2\n    exit 2\n  fi\n',
         "", [SWEEP]),
        ("M15-no-linked-directory-check", PI, "    for name in sorted(names):\n        _directory(root, str(Path(name).parent))\n", "", [LIFE]),
        ("M16-logs-cleared-after-preflight", RS, "  prepare_logs\n  run_preflight_gates\n",
         "  mkdir -p \"$OUT/preflight\"; LOGS_READY=1\n  run_preflight_gates\n  rm -f \"$OUT\"/*.log\n", [SWEEP]),
        ("M17-no-identity-recheck", OP, "                    if _identity(pid) == identity:\n", "                    if True:\n", [SWEEP]),
        ("M18-no-pin-revision-check", PI, 'if mode != "160000" or _git(root, owner, "rev-parse", "HEAD").strip() != revision:',
         'if mode != "160000":', [LIFE]),
        ("M19-no-toplevel-check", PI, '        if Path(_git(root, owner, "rev-parse", "--show-toplevel").strip()) != root:\n            raise InputRefused(f"required dependency has no checkout: {name}")\n',
         "", [LIFE]),
        ("M20-no-cleanup-on-normal-exit", OP, "            if self.process is None:\n                self._cleanup()\n", "            pass\n", [SWEEP, LIFE]),
    ],
    "3": [
        ("M11-accept-GIT_INDEX_FILE", PI, '"GIT_DIR", "GIT_WORK_TREE", "GIT_COMMON_DIR", "GIT_INDEX_FILE",',
         '"GIT_DIR", "GIT_WORK_TREE", "GIT_COMMON_DIR",', [LIFE]),
    ],
}


def one(item):
    ident, rel, old, new, tests = item
    base = WORK / ident
    if base.exists():
        shutil.rmtree(base)
    base.mkdir(parents=True)
    repo = base / "repo"
    shutil.copytree(SOURCE, repo, symlinks=True)
    path = repo / rel
    text = path.read_text()
    count = text.count(old)
    rec = dict(id=ident, file=rel, anchor_count=count, tests={})
    if count != 1:
        rec["error"] = "anchor not unique"
        return rec
    path.write_text(text.replace(old, new, 1))
    (base / "tmp").mkdir()
    env = {k: v for k, v in os.environ.items()}
    env.update(TMPDIR=str(base / "tmp"), PYTHONDONTWRITEBYTECODE="1")
    for test in tests:
        t0 = time.monotonic()
        try:
            done = subprocess.run([sys.executable, str(repo / test)], cwd=repo, env=env, capture_output=True,
                                  text=True, timeout=420)
            status, out = done.returncode, done.stdout + done.stderr
        except subprocess.TimeoutExpired as exc:
            status, out = "TIMEOUT-420s", (exc.stdout or b"").decode(errors="replace") if isinstance(exc.stdout, bytes) else str(exc.stdout)
        lines = [l for l in out.splitlines() if l.strip()]
        err = [l for l in lines if "Error" in l or "assert" in l.lower()]
        rec["tests"][test] = dict(exit=status, seconds=round(time.monotonic() - t0, 1), red=status != 0,
                                  last_lines=lines[-4:], error_lines=err[-3:])
    return rec


def main():
    WORK.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(one, MUTANTS[BATCH]))
    prior = json.loads(RECEIPT.read_text()) if RECEIPT.exists() else []
    ids = {r["id"] for r in results}
    RECEIPT.write_text(json.dumps([r for r in prior if r["id"] not in ids] + results, indent=1) + "\n")
    for r in results:
        verdicts = {Path(t).name: (v["exit"], "RED" if v["red"] else "GREEN") for t, v in r["tests"].items()}
        why = [v["error_lines"][-1][:150] if v["error_lines"] else (v["last_lines"][-1][:150] if v["last_lines"] else "")
               for v in r["tests"].values()]
        print(f"{r['id']:36s} {verdicts} {r.get('error', '')} :: {why}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
