#!/usr/bin/env python3
"""R246-1 disposable mutation probes for PR #524 (issue #517).

Usage: python3 mutants.py <probe-tree> <receipt-dir> [MUTANT_ID ...]

<probe-tree> is a disposable copy of the reviewed checkout at the exact head.
Each mutant rewrites one anchor (asserted to occur exactly once) in
tb/verilator/milan_dp/sim_pool.py or its Makefile, runs both shipped test
files under a hard guard, records the raw output, and restores the exact
original bytes. A mutant is KILLED when either test file exits non-zero or
is stopped by the guard (HANG); SURVIVED when both exit 0.
"""
import hashlib
import signal
import subprocess
import sys
from pathlib import Path

POOL = "tb/verilator/milan_dp/sim_pool.py"
MAKE = "tb/verilator/milan_dp/Makefile"
TESTS = ("test_sim_pool.py", "test_sim_pool_backpressure.py")
GUARD_S = 90

REPLAY_READY_ORIG = '''        while self.replayed < len(self.legs) and self.legs[self.replayed].done:
            leg = self.legs[self.replayed]
'''
REPLAY_READY_MUT = '''        while self.replayed < len(self.legs) and any(
                l.done and not getattr(l, "_r", False) for l in self.legs):
            leg = next(l for l in self.legs if l.done and not getattr(l, "_r", False))
            leg._r = True
'''

MUTANTS = {
    "M01-bound-plus-one": (POOL, "len(running) < self.jobs and not self.failed",
                           "len(running) < self.jobs + 1 and not self.failed"),
    "M02-one-worker-ignored": (POOL, "Pool(legs, 1 if frame_dump else jobs, transcript)",
                               "Pool(legs, 1 if frame_dump else 2, transcript)"),
    "M03-no-exclusion": (POOL, "group_busy = any(leg.exclusive for leg in running)",
                         "group_busy = False"),
    "M04-group-order-reversed": (POOL, "eligible = next((leg for leg in pending\n",
                                 "eligible = next((leg for leg in sorted(pending, key=lambda l: (0, -l.position) if l.exclusive else (1, l.position))\n"),
    "M05-no-fail-fast": (POOL, "self.failed = self.failed or leg.proc.returncode != 0",
                         "pass"),
    "M06-exit-zero": (POOL, "return 0 if passed else 1", "return 0"),
    "M07-failure-unnamed": (POOL, 'return f"{leg.exe} exited with status {code}"',
                            "return None"),
    "M08-crash-is-pass": (POOL, "self.proc is not None and self.proc.returncode == 0",
                          "self.proc is not None and self.proc.returncode <= 0"),
    "M09-unstartable-not-fail-fast": (POOL, "                leg.done = True\n                self.failed = True\n",
                                      "                leg.done = True\n"),
    "M10-kill-leader-only": (POOL, "os.killpg(leg.proc.pid, signal.SIGKILL)",
                             "os.kill(leg.proc.pid, signal.SIGKILL)"),
    "M11-no-adopted-reap": (POOL, '    active = {leg.proc.pid for leg in running}\n',
                            '    return\n    active = {leg.proc.pid for leg in running}\n'),
    "M12-no-subreaper": (POOL, "if libc.prctl(36, 1, 0, 0, 0) != 0:", "if False:"),
    "M13-sighup-unwatched": (POOL, "INTERRUPTS = (signal.SIGINT, signal.SIGTERM, signal.SIGHUP)",
                             "INTERRUPTS = (signal.SIGINT, signal.SIGTERM)"),
    "M14-ignored-interrupt-watched": (POOL, "watched.update(sig for sig in INTERRUPTS if signal.getsignal(sig) != signal.SIG_IGN)",
                                      "watched.update(INTERRUPTS)"),
    "M15-blocking-stdout": (POOL, "os.set_blocking(self.fd, False)", "os.set_blocking(self.fd, True)"),
    "M16-final-drain-waits": (POOL, "replay.drain(wait=interrupt is None)", "replay.drain(wait=True)"),
    "M17-flags-not-restored": (POOL, "            os.set_blocking(self.fd, blocking)\n",
                               "            pass\n"),
    "M18-replay-completion-order": (POOL, REPLAY_READY_ORIG, REPLAY_READY_MUT),
    "M19-late-signal-ignored": (POOL, "late = signal.sigpending() & set(INTERRUPTS)", "late = set()"),
    "M20-duplicate-leg-allowed": (POOL, "if len({leg.exe for leg in legs}) != len(legs):", "if False:"),
    "M21-stale-logs-kept": (POOL, "        stale.unlink()\n", "        pass\n"),
    "M22-empty-frame-var-ignored": (POOL, "frame_dump = FRAME_DUMP_VAR in os.environ",
                                    "frame_dump = bool(os.environ.get(FRAME_DUMP_VAR))"),
    "M23-frame-var-ignored": (POOL, "frame_dump = FRAME_DUMP_VAR in os.environ", "frame_dump = False"),
    "M24-child-mask-inherited": (POOL, "            signal.pthread_sigmask(signal.SIG_SETMASK, mask)\n",
                                 "            pass\n"),
    "M25-no-new-session": (POOL, "start_new_session=True,", "start_new_session=False,"),
    "M26-stdin-inherited": (POOL, "[leg.exe], stdin=subprocess.DEVNULL,", "[leg.exe],"),
    "M27-interrupt-no-kill": (POOL, "        for leg in running:\n            kill_group(leg)\n",
                              "        pass\n"),
    "M33-children-file-unavailable": (POOL, 'children = Path(f"/proc/self/task/{os.getpid()}/children")',
                                      'children = Path(f"/proc/self/task/{os.getpid()}/children-absent")'),
    "M28-make-drop-prune": (MAKE, '\t  --banner "---- all six tier-1 blocks pruned ----" \\\n\t  ./obj_prune/Vmilan_dp_prune \\\n', ""),
    "M29-make-notify-not-exclusive": (MAKE, "--exclusive ./$(NOTIFY_MDIR)/Vmilan_dp_notify", "./$(NOTIFY_MDIR)/Vmilan_dp_notify"),
    "M30-make-errors-ignored": (MAKE, "\t@exec python3 sim_pool.py", "\t-@exec python3 sim_pool.py"),
    "M31-make-default-one": (MAKE, "SIM_JOBS ?= 2", "SIM_JOBS ?= 1"),
    "M32-make-crflic-exclusive": (MAKE, "\t  ./$(CRFLIC_MDIR)/Vmilan_dp_crflic \\\n",
                                  "\t  --exclusive ./$(CRFLIC_MDIR)/Vmilan_dp_crflic \\\n"),
}


def normalized() -> None:
    """Foreground-terminal signal state: interrupts default, nothing blocked."""
    for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
        signal.signal(sig, signal.SIG_DFL)
    signal.pthread_sigmask(signal.SIG_SETMASK, set())


def main() -> int:
    tree = Path(sys.argv[1]).resolve()
    out = Path(sys.argv[2]).resolve()
    out.mkdir(parents=True, exist_ok=True)
    chosen = sys.argv[3:] or list(MUTANTS)
    originals = {rel: (tree / rel).read_bytes() for rel in (POOL, MAKE)}
    summary = []
    for mid in chosen:
        rel, old, new = MUTANTS[mid]
        text = originals[rel].decode()
        assert text.count(old) == 1, f"{mid}: anchor count {text.count(old)}"
        try:
            (tree / rel).write_text(text.replace(old, new))
            verdicts = []
            for test in TESTS:
                cmd = ["timeout", "-k", "5", str(GUARD_S), sys.executable, test]
                proc = subprocess.run(cmd, cwd=tree / "tb/verilator/milan_dp",
                                      capture_output=True, text=True, preexec_fn=normalized)
                (out / f"{mid}.{test}.log").write_text(
                    f"$ {' '.join(cmd)}\nrc={proc.returncode}\n{proc.stdout}{proc.stderr}")
                rc = proc.returncode
                verdicts.append("HANG" if rc in (124, 137) else ("PASS" if rc == 0 else "FAIL"))
        finally:
            (tree / rel).write_bytes(originals[rel])
        killed = any(v != "PASS" for v in verdicts)
        line = f"{mid}\t{'KILLED' if killed else 'SURVIVED'}\t" + "\t".join(
            f"{t}={v}" for t, v in zip(TESTS, verdicts))
        print(line, flush=True)
        summary.append(line)
    for rel, data in originals.items():
        assert (tree / rel).read_bytes() == data
        print(f"restored {rel} sha256={hashlib.sha256(data).hexdigest()}")
    with (out / "summary.tsv").open("a") as fh:
        fh.write("\n".join(summary) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
