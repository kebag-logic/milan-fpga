#!/usr/bin/env python3
"""Test power of the sweep cancellation report assertions (R257-2-F1 follow-up).

Each arm is a disposable `git archive` copy of `scripts/` at the head under
review. One textual single-defect edit is applied to that copy's production
sweep (or none), and one version of scripts/test_suite_cancellation.py (the
head's or its parent's) is run unmodified against it. The review clone is
never written.

Usage:
  probe_report_mutations.py CLONE SCRATCH OUT_JSON JOBS [MUTANT,...] [TESTS]
    MUTANT  names from MUTANTS below, or "all" (default)
    TESTS   comma list of head,base (default head,base)

Exit 0 once every requested arm ran; the verdicts are in OUT_JSON.
"""
import concurrent.futures
import ctypes
import hashlib
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path

HEAD = "015edd9ab2248289ff000f6ef14890be1812ba7b"
BASE = "26353960ae2763cc09741d0f7bcc720621bd5148"
SWEEP = "scripts/run_all_suites.sh"
TEST = "scripts/test_suite_cancellation.py"

# name -> (file, old, new, what the edit restores or corrupts)
MUTANTS = {
    "none": (None, None, None, "unmodified head"),
    # The four single-defect copies named in R257-2-F1.
    "logs-ready-early": (SWEEP, "LOGS_READY=0\ncancelled() {", "LOGS_READY=1\ncancelled() {",
                         "report claims this run's logs before any preparation"),
    "logs-ready-never-set": (SWEEP, "|| exit 2\n  LOGS_READY=1\n}", "|| exit 2\n}",
                             "report denies partial logs that exist"),
    "no-partial-logs-message": (SWEEP, '    echo "partial logs: $OUT" >&2\n', "    :\n",
                                "prepared boundary prints no logs line"),
    "no-term-trap": (SWEEP, "trap 'cancelled TERM 143' TERM\n", "",
                     "shell's TERM report is gone (owner line only)"),
    # Further corruptions of the report or its boundary.
    "no-int-trap": (SWEEP, "trap 'cancelled INT 130' INT\n", "", "shell's INT report is gone"),
    "no-unprepared-message": (SWEEP, '    echo "logs were not prepared for this invocation" >&2\n',
                              "    :\n", "unprepared boundary prints nothing"),
    "report-inverted": (SWEEP, '[ "$LOGS_READY" = 1 ]', '[ "$LOGS_READY" != 1 ]',
                        "the two reports are swapped"),
    "report-by-out-exists": (SWEEP, '[ "$LOGS_READY" = 1 ]', '[ -d "$OUT" ]',
                             "attribution by OUT existing, not by this run's preparation"),
    "partial-logs-wrong-dir": (SWEEP, "partial logs: $OUT", "partial logs: $ROOT/.suite-logs",
                               "names the default directory, not the requested OUT"),
    "partial-logs-basename": (SWEEP, "partial logs: $OUT", "partial logs: ${OUT##*/}",
                              "names a relative basename, not the requested OUT"),
    "both-report-lines": (SWEEP, '  else\n    echo "logs were not prepared',
                          '  fi\n  if :; then\n    echo "logs were not prepared',
                          "prints the not-prepared line at every boundary"),
    "int-reported-as-term": (SWEEP, "cancelled INT 130", "cancelled TERM 130",
                             "INT reported under the TERM name"),
    "no-cancel-line": (SWEEP, '  echo "CANCELLED: $1; no completed sweep result" >&2\n', "",
                       "shell keeps the logs report but drops its CANCELLED line"),
    "no-trap-exit": (SWEEP, '    echo "logs were not prepared for this invocation" >&2\n  fi\n  exit "$2"\n}',
                     '    echo "logs were not prepared for this invocation" >&2\n  fi\n}',
                     "the trap returns and the shell continues"),
    "prepare-before-lock": (SWEEP, "  acquire_lock\n  prepare_logs\n", "  prepare_logs\n  acquire_lock\n",
                            "logs cleared and claimed before the lock wait"),
    "prepare-before-selection": (SWEEP, '  parse_args "$@"\n  select_suites\n  acquire_lock\n  prepare_logs\n',
                                 '  parse_args "$@"\n  prepare_logs\n  select_suites\n  acquire_lock\n',
                                 "logs cleared and claimed before selection and lock"),
    "no-wait-queue": (SWEEP, "      flock 9 ||", "      flock -n 9 ||",
                      "--wait no longer queues behind a holder"),
    "no-stale-clear": (SWEEP, '  rm -f "$OUT"/*.log "$OUT/preflight"/*.log || exit 2\n', "",
                       "previous logs survive into this run's OUT"),
    "clear-before-lock": (SWEEP, '  LOCK="${SUITE_SWEEP_LOCK:-$ROOT/.run_all_suites.lock}"\n',
                          '  rm -f "$OUT"/*.log "$OUT/preflight"/*.log\n'
                          '  LOCK="${SUITE_SWEEP_LOCK:-$ROOT/.run_all_suites.lock}"\n',
                          "a queued sweep deletes the holder's previous logs before locking, report unchanged"),
    "logs-ready-before-clear":(SWEEP, '  mkdir -p "$OUT/preflight" || exit 2\n  rm -f "$OUT"/*.log "$OUT/preflight"/*.log || exit 2\n  LOGS_READY=1\n',
                                '  LOGS_READY=1\n  mkdir -p "$OUT/preflight" || exit 2\n  rm -f "$OUT"/*.log "$OUT/preflight"/*.log || exit 2\n',
                                "order inside prepare_logs (no command boundary between them is observable)"),
}


def clean_env(extra=None):
    env = {k: v for k, v in os.environ.items()
           if not k.startswith("GIT_") and k not in ("VERIFICATION_TEST_LOGS", "SUITE_TIMEOUT",
                                                     "SUITE_SWEEP_LOCK")}
    env.update(extra or {})
    return env


def git(clone, *args):
    return subprocess.run(["git", "--no-optional-locks", "-C", str(clone), *args],
                          env=clean_env(), capture_output=True, check=True).stdout


def prepare(clone, scratch, mutant, test):
    """A disposable copy of scripts/ at HEAD with one edit and one test version."""
    arm = scratch / f"{mutant}--{test}"
    if arm.exists():
        shutil.rmtree(arm)
    arm.mkdir(parents=True)
    tar = git(clone, "archive", "--format=tar", HEAD, "scripts")
    subprocess.run(["tar", "-x", "-C", str(arm)], input=tar, check=True)
    if test == "base":
        (arm / TEST).write_bytes(git(clone, "show", f"{BASE}:{TEST}"))
    edit = {"mutant": mutant, "test": test}
    relative, old, new, what = MUTANTS[mutant.split("@")[0]]  # "name@k" repeats an arm
    edit["what"] = what
    if relative:
        path = arm / relative
        text = path.read_text()
        count = text.count(old)
        assert count == 1, (mutant, count)
        mutated = text.replace(old, new)
        path.write_text(mutated)
        edit["file"] = relative
        diff = subprocess.run(["diff", "-u", "--label", f"a/{relative}", "--label", f"b/{relative}", "-",
                               str(path)], input=text.encode(), capture_output=True)
        edit["diff"] = diff.stdout.decode()
    edit["test_sha256"] = hashlib.sha256((arm / TEST).read_bytes()).hexdigest()
    edit["sweep_sha256"] = hashlib.sha256((arm / SWEEP).read_bytes()).hexdigest()
    return arm, edit


FRAME = re.compile(r'File ".*/scripts/test_suite_cancellation\.py", line (\d+), in (\w+)')


def run(clone, scratch, mutant, test, path_override=None):
    arm, edit = prepare(clone, scratch, mutant, test)
    extra = {"TMPDIR": str(arm)}
    if path_override:
        extra["PATH"] = path_override
    began = time.monotonic()
    proc = subprocess.run(["timeout", "-k", "10", "400", "python3", str(arm / TEST)], cwd=arm,
                          env=clean_env(extra), capture_output=True, start_new_session=True)
    elapsed = round(time.monotonic() - began, 1)
    out = (proc.stdout + proc.stderr).decode("utf-8", errors="replace")
    (arm.parent / f"{arm.name}.log").write_text(out)
    frames = FRAME.findall(out)
    final_error = next((line for line in reversed(out.splitlines())
                        if line.startswith(("AssertionError", "RuntimeError", "OSError", "Traceback"))), "")
    arms_passed = [line.split(":", 1)[0] for line in out.splitlines()
                   if line.startswith(("cancel-", "unsafe-", "hard-", "facility-", "owner-", "normal-",
                                       "relative-", "pass:", "fail:", "masked:", "timeout:"))]
    edit.update(rc=proc.returncode, verdict="GREEN" if proc.returncode == 0 else "RED",
                seconds=elapsed, test_frames=[f"{fn}:{ln}" for ln, fn in frames],
                final_error=final_error[:400], arms_completed=len(arms_passed),
                last_arm_completed=arms_passed[-1] if arms_passed else None,
                pass_line=next((l for l in out.splitlines() if l.startswith("suite cancellation: PASS")), None),
                log=f"{arm.name}.log")
    return edit


def subreaper():
    libc = ctypes.CDLL(None, use_errno=True)
    assert libc.prctl(36, 1, 0, 0, 0) == 0


def leftovers():
    """Descendants of this probe (adopted as subreaper) still present."""
    me = os.getpid()
    table = {}
    for entry in Path("/proc").iterdir():
        if entry.name.isdecimal():
            try:
                fields = (entry / "stat").read_text().rsplit(")", 1)[1].split()
                table[int(entry.name)] = (int(fields[1]), fields[19], fields[0])
            except (FileNotFoundError, ProcessLookupError):
                pass
    owned = {me}
    while True:
        more = {p for p, (pp, _s, _st) in table.items() if pp in owned} - owned
        if not more:
            break
        owned |= more
    owned.discard(me)
    return {p: table[p] for p in owned}


def contain():
    """Kill and reap only this probe's own adopted descendants, through pidfds."""
    found = leftovers()
    for pid, (_pp, start, _st) in found.items():
        try:
            fd = os.pidfd_open(pid)
        except ProcessLookupError:
            continue
        try:
            now = Path(f"/proc/{pid}/stat").read_text().rsplit(")", 1)[1].split()[19]
            if now == start:
                signal.pidfd_send_signal(fd, signal.SIGKILL)
        except (FileNotFoundError, ProcessLookupError):
            pass
        finally:
            os.close(fd)
    deadline = time.monotonic() + 5
    while time.monotonic() < deadline:
        try:
            pid, _status = os.waitpid(-1, os.WNOHANG)
        except ChildProcessError:
            break
        if not pid:
            time.sleep(0.05)
    return {str(p): list(v) for p, v in found.items()}


def main():
    clone, scratch, out_json = (Path(arg).resolve() for arg in sys.argv[1:4])
    jobs = int(sys.argv[4])
    names = list(MUTANTS) if len(sys.argv) < 6 or sys.argv[5] == "all" else sys.argv[5].split(",")
    tests = sys.argv[6].split(",") if len(sys.argv) > 6 else ["head", "base"]
    path_override = os.environ.get("PROBE_PATH_OVERRIDE")
    scratch.mkdir(parents=True, exist_ok=True)
    subreaper()
    arms = [(m, t) for m in names for t in tests]
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as pool:
        futures = {pool.submit(run, clone, scratch, m, t, path_override): (m, t) for m, t in arms}
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            print(f"{result['mutant']:28s} {result['test']:4s} {result['verdict']:5s} rc={result['rc']:<4} "
                  f"{result['seconds']:6.1f}s {','.join(result['test_frames'][-2:])}", flush=True)
            results.append(result)
    order = {name: i for i, name in enumerate(MUTANTS)}
    results.sort(key=lambda r: (order.get(r["mutant"], 99), r["test"]))
    contained = contain()
    out_json.write_text(json.dumps({"head": HEAD, "base_test_from": BASE, "jobs": jobs,
                                    "path_override": bool(path_override),
                                    "leftover_descendants_killed": contained,
                                    "results": results}, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
