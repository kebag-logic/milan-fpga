#!/usr/bin/env python3
"""The normal sweep entry point owns the new cancellation-report controls.

Disposable `git archive` copies of the head (scripts/, tb/verilator/, syn/yosys/)
run the real `bash scripts/run_all_suites.sh OUT` with a PATH `make` guard, so
no suite can build. Variants:
  mutant:<name>  one single-defect edit from probe_report_mutations.MUTANTS;
                 expected: preflight ABORT, exit 2, the failing arm in the
                 sweep's own preflight/test_suite_cancellation.log.
  unmodified     expected: the cancellation preflight passes, including both
                 lock-wait arms; the entry is then sent TERM during the next
                 preflight gate and must report "partial logs: OUT" and 143.
The unmodified variant exports SUITE_SWEEP_LOCK at a shared path, the
documented machine-wide serialisation setting.

Usage: probe_entry_ownership.py CLONE SCRATCH OUT_JSON VARIANT[,VARIANT...]
"""
import json
import os
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_report_mutations as pm  # noqa: E402

GUARD = "#!/bin/sh\necho \"MAKE GUARD: $*\" >> \"$MAKE_GUARD_LOG\"\nexit 1\n"


def copy(clone, arm):
    if arm.exists():
        shutil.rmtree(arm)
    arm.mkdir(parents=True)
    tar = pm.git(clone, "archive", "--format=tar", pm.HEAD, "scripts", "tb/verilator", "syn/yosys")
    subprocess.run(["tar", "-x", "-C", str(arm)], input=tar, check=True)


def variant(clone, scratch, name):
    arm = scratch / name.replace(":", "-")
    copy(clone, arm / "tree")
    edit = {"variant": name}
    if name.startswith("mutant:"):
        mutant = name.split(":", 1)[1]
        relative, old, new, what = pm.MUTANTS[mutant]
        path = arm / "tree" / relative
        text = path.read_text()
        assert text.count(old) == 1
        path.write_text(text.replace(old, new))
        edit["what"] = what
    guard = arm / "guard-bin"
    guard.mkdir()
    (guard / "make").write_text(GUARD)
    (guard / "make").chmod(0o755)
    out = arm / "OUT"
    env = pm.clean_env({"PATH": f"{guard}{os.pathsep}{os.environ['PATH']}",
                        "MAKE_GUARD_LOG": str(arm / "make-guard.log"), "TMPDIR": str(arm)})
    if name == "unmodified":
        env["SUITE_SWEEP_LOCK"] = str(arm / "shared-sweep.lock")
    began = time.monotonic()
    with (arm / "entry.log").open("wb") as log:
        entry = subprocess.Popen(["bash", "scripts/run_all_suites.sh", str(out)], cwd=arm / "tree",
                                 env=env, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
    signalled = None
    if name == "unmodified":
        target = out / "preflight/test_suite_cancellation.log"
        deadline = time.monotonic() + 400
        while time.monotonic() < deadline and entry.poll() is None:
            if target.exists() and "suite cancellation: PASS" in target.read_text():
                fd = os.pidfd_open(entry.pid)
                try:
                    signal.pidfd_send_signal(fd, signal.SIGTERM)
                finally:
                    os.close(fd)
                signalled = round(time.monotonic() - began, 1)
                break
            time.sleep(0.02)
    status = entry.wait(timeout=450)
    transcript = (arm / "entry.log").read_text()
    pre = out / "preflight/test_suite_cancellation.log"
    pre_text = pre.read_text() if pre.exists() else ""
    frames = pm.FRAME.findall(pre_text)
    edit.update(
        exit=status, seconds=round(time.monotonic() - began, 1), term_sent_at=signalled,
        transcript=transcript.splitlines()[-12:],
        preflight_logs=sorted(p.name for p in (out / "preflight").glob("*.log")) if out.exists() else [],
        cancellation_preflight_pass=next((l for l in pre_text.splitlines()
                                          if l.startswith("suite cancellation: PASS")), None),
        lock_wait_arms=[l.split(":", 1)[0] for l in pre_text.splitlines() if l.startswith("cancel-lock-wait-")],
        failing_frames=[f"{fn}:{ln}" for ln, fn in frames],
        make_guard_hits=(arm / "make-guard.log").read_text().splitlines() if (arm / "make-guard.log").exists() else [],
        suite_logs=sorted(p.name for p in out.glob("*.log")) if out.exists() else [])
    return edit


def main():
    clone, scratch, out_json = (Path(a).resolve() for a in sys.argv[1:4])
    scratch.mkdir(parents=True, exist_ok=True)
    pm.subreaper()
    results = [variant(clone, scratch, name) for name in sys.argv[4].split(",")]
    contained = pm.contain()
    out_json.write_text(json.dumps({"head": pm.HEAD, "leftover_descendants_killed": contained,
                                    "results": results}, indent=1) + "\n")
    for r in results:
        print(r["variant"], "exit", r["exit"], r["seconds"], "s; frames", r["failing_frames"][-2:],
              "; lock-wait arms", r["lock_wait_arms"], "; tail:", r["transcript"][-3:])
    return 0


if __name__ == "__main__":
    sys.exit(main())
