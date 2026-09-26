#!/usr/bin/env python3
"""Mutation probes for the #517 simulation pool.

usage: mutate_pool.py TREE OUTDIR [NAME ...]
TREE is a disposable full copy of the head checkout. Each mutant rewrites one
file in TREE (an exact, single-occurrence substitution), runs the shipped
control files, records their output, and restores the original bytes. A mutant
is KILLED when at least one shipped control file exits non-zero.
"""
import hashlib, os, signal, subprocess, sys
from pathlib import Path

POOL = "tb/verilator/milan_dp/sim_pool.py"
MAKE = "tb/verilator/milan_dp/Makefile"

MUTANTS = {
    # claim: at most two legs alive at once
    "bound-plus-one": (POOL, "while pending and len(running) < self.jobs and not self.failed:",
                       "while pending and len(running) < self.jobs + 1 and not self.failed:"),
    "ceiling-three": (POOL, "MAX_JOBS = 2", "MAX_JOBS = 3"),
    # claim: the bound ignores make's job count
    "jobs-from-makeflags": (POOL, "    frame_dump = FRAME_DUMP_VAR in os.environ\n",
                            "    frame_dump = FRAME_DUMP_VAR in os.environ\n"
                            "    if '-j' in os.environ.get('MAKEFLAGS', ''): jobs = 1\n"),
    # claim: shared-header group is exclusive
    "no-exclusion": (POOL, "group_busy = any(leg.exclusive for leg in running)", "group_busy = False"),
    # claim: group keeps recipe order
    "group-reverse-order": (POOL, "eligible = next((leg for leg in pending\n",
                            "eligible = next((leg for leg in reversed(pending)\n"),
    # claim: independent legs overlap the group
    "no-independent-overlap": (POOL, "if not leg.exclusive or not group_busy), None)",
                               "if not group_busy), None)"),
    # claim: fail-fast, no start after a failure
    "no-fail-fast": (POOL, "while pending and len(running) < self.jobs and not self.failed:",
                     "while pending and len(running) < self.jobs:"),
    # claim: a failing/missing leg fails the run
    "failure-masked": (POOL, "    return 0 if passed else 1\n", "    return 0\n"),
    "missing-exe-not-failure": (POOL, "                leg.error = str(exc)\n                leg.done = True\n                self.failed = True\n",
                                "                leg.error = str(exc)\n                leg.done = True\n                leg.proc = subprocess.Popen(['true'])\n                leg.proc.wait()\n"),
    # claim: the failing leg is named
    "failing-leg-unnamed": (POOL, "            self.note(f\"first leg in recipe order that did not pass: {first.exe}\")",
                            "            pass"),
    # claim: SIGINT/SIGTERM/SIGHUP kill every running leg's group
    "stop-no-kill": (POOL, "        for leg in running:\n            kill_group(leg)\n        for leg in running:\n            leg.proc.wait()",
                     "        for leg in running:\n            pass\n        for leg in running:\n            leg.proc.wait()"),
    # claim: new-session descendants are adopted and killed
    "no-subreaper": (POOL, "    if libc.prctl(36, 1, 0, 0, 0) != 0:", "    if 0:"),
    "no-adopted-reap": (POOL, "    active = {leg.proc.pid for leg in running}\n",
                        "    return\n    active = {leg.proc.pid for leg in running}\n"),
    # claim: a leg that exits leaves nothing in its group
    "exit-no-group-kill": (POOL, "            kill_group(leg)\n            leg.proc.wait()\n            leg.done = True\n            running.remove(leg)",
                           "            leg.proc.wait()\n            leg.done = True\n            running.remove(leg)"),
    # claim: ends by the same signal
    "exit-status-not-signal": (POOL, "        if interrupt is not None:\n            return end_by(interrupt)",
                               "        if interrupt is not None:\n            return 1"),
    # claim: an inherited ignore stays ignored
    "ignored-rewatched": (POOL, "watched.update(sig for sig in INTERRUPTS if signal.getsignal(sig) != signal.SIG_IGN)",
                          "watched.update(INTERRUPTS)"),
    # claim: legs get the original signal mask / stdin
    "child-mask-blocked": (POOL, "        mask = self.child_mask\n", "        mask = set(signal.Signals)-{signal.SIGKILL, signal.SIGSTOP}\n"),
    "stdin-inherited": (POOL, "[leg.exe], stdin=subprocess.DEVNULL,", "[leg.exe], stdin=None,"),
    # claim: replay in recipe order
    "replay-completion-order": (POOL, "        while self.replayed < len(self.legs) and self.legs[self.replayed].done:\n            leg = self.legs[self.replayed]\n",
                                "        for leg in [l for l in self.legs if l.done and not getattr(l, 'shown', False)]:\n            leg.shown = True\n"),
    # claim: frame-dump presence forces sequential
    "frame-dump-ignored": (POOL, "    frame_dump = FRAME_DUMP_VAR in os.environ\n", "    frame_dump = False\n"),
    "frame-dump-empty-ignored": (POOL, "    frame_dump = FRAME_DUMP_VAR in os.environ\n", "    frame_dump = bool(os.environ.get(FRAME_DUMP_VAR))\n"),
    # claim: cancellation independent of stdout backpressure
    "drain-blocking-write": (POOL, "        os.set_blocking(self.fd, False)\n", "        os.set_blocking(self.fd, True)\n"),
    "drain-ignores-signals": (POOL, "        pending = signal.sigtimedwait(self.interrupts, seconds)\n",
                              "        pending = signal.sigtimedwait(set(), seconds)\n"),
    "final-drain-waits": (POOL, "            replay.drain(wait=interrupt is None)", "            replay.drain(wait=True)"),
    "fd-flags-not-restored": (POOL, "            os.set_blocking(self.fd, blocking)\n", "            pass\n"),
    # claim: unstarted legs named on interrupt
    "unstarted-unnamed": (POOL, "                self.note(f\"{leg.exe} was not started {why}\")\n", "                pass\n"),
    # claim: killed legs attributed
    "killed-unattributed": (POOL, "                leg.stopped_by = signo\n", "                pass\n"),
    # claim: duplicate legs refused (each runs exactly once)
    "duplicates-allowed": (POOL, "    if len({leg.exe for leg in legs}) != len(legs):\n", "    if False:\n"),
    # Makefile: inventory, exclusion marks, default, error propagation
    "mk-drop-crflic": (MAKE, "\t  ./$(CRFLIC_MDIR)/Vmilan_dp_crflic \\\n", ""),
    "mk-notify-not-exclusive": (MAKE, "\t  --exclusive ./$(NOTIFY_MDIR)/Vmilan_dp_notify \\\n", "\t  ./$(NOTIFY_MDIR)/Vmilan_dp_notify \\\n"),
    "mk-nxn8-not-exclusive": (MAKE, "\t  --exclusive ./obj_nxn8/Vmilan_dp_nxn8 \\\n", "\t  ./obj_nxn8/Vmilan_dp_nxn8 \\\n"),
    "mk-default-one": (MAKE, "SIM_JOBS ?= 2", "SIM_JOBS ?= 1"),
    "mk-ignore-errors": (MAKE, "\t@exec python3 sim_pool.py", "\t-@exec python3 sim_pool.py"),
    "mk-swap-order": (MAKE, "\t  ./obj_nolpf/Vmilan_dp_nolpf \\\n\t  --banner \"---- all six tier-1 blocks pruned ----\" \\\n\t  ./obj_prune/Vmilan_dp_prune \\\n",
                      "\t  ./obj_prune/Vmilan_dp_prune \\\n\t  --banner \"---- all six tier-1 blocks pruned ----\" \\\n\t  ./obj_nolpf/Vmilan_dp_nolpf \\\n"),
    "mk-double-run-after-pool": (MAKE, "\t@echo \"---- #386 render law:", "\t./obj_nolpf/Vmilan_dp_nolpf\n\t@echo \"---- #386 render law:"),
}

def sweep(root: Path) -> int:
    """SIGKILL every process whose working directory is under `root`."""
    killed = 0
    for entry in os.listdir("/proc"):
        if not entry.isdigit():
            continue
        try:
            cwd = os.readlink(f"/proc/{entry}/cwd")
        except OSError:
            continue
        if cwd.startswith(str(root)):
            try:
                os.kill(int(entry), signal.SIGKILL)
                killed += 1
            except ProcessLookupError:
                pass
    return killed


CONTROLS = (["python3", "test_sim_pool.py"], ["python3", "test_sim_pool_backpressure.py"])


def main() -> int:
    tree, out = Path(sys.argv[1]), Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    names = sys.argv[3:] or list(MUTANTS)
    survivors = []
    for name in names:
        rel, old, new = MUTANTS[name]
        path = tree / rel
        original = path.read_bytes()
        text = original.decode()
        assert text.count(old) == 1, f"{name}: pattern occurs {text.count(old)} times"
        path.write_text(text.replace(old, new, 1))
        verdicts = []
        try:
            for argv in CONTROLS:
                tmp = out / "tmp" / f"{name}.{argv[1]}"
                tmp.mkdir(parents=True, exist_ok=True)
                proc = subprocess.Popen(argv, cwd=tree / "tb/verilator/milan_dp",
                                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                        text=True, start_new_session=True,
                                        env={**os.environ, "TMPDIR": str(tmp)})
                try:
                    text_out, _ = proc.communicate(timeout=120)
                    rc = proc.returncode
                except subprocess.TimeoutExpired:
                    # a hung control is a detection only if it is not PASS; record it
                    for sig in (signal.SIGTERM, signal.SIGKILL):
                        try:
                            os.killpg(proc.pid, sig)
                        except ProcessLookupError:
                            pass
                    text_out, _ = proc.communicate()
                    rc = "TIMEOUT"
                stray = sweep(tmp)
                if stray:
                    text_out += f"\n[mutate_pool] killed {stray} stray process(es) left under {tmp}\n"
                verdicts.append(rc)
                (out / f"{name}.{argv[1]}.txt").write_text(f"exit={rc}\n{text_out}")
        finally:
            path.write_bytes(original)
            assert hashlib.sha256(path.read_bytes()).digest() == hashlib.sha256(original).digest()
        killed = any(v != 0 for v in verdicts)
        fails = []
        for argv in CONTROLS:
            body = (out / f"{name}.{argv[1]}.txt").read_text()
            fails += [l for l in body.splitlines() if l.startswith("[FAIL]")]
        line = (f"{name}: {'KILLED' if killed else 'SURVIVED'} "
                f"test_sim_pool={verdicts[0]} backpressure={verdicts[1]} "
                f"failing_arms={len(fails)} first={fails[0][:110] if fails else '-'}")
        print(line, flush=True)
        if not killed:
            survivors.append(name)
    print(f"mutants={len(names)} killed={len(names)-len(survivors)} survived={survivors}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
