#!/usr/bin/env python3
"""Screen candidate edge mutants against every owner control (scratch, not committed).

usage: python3 -B edge_mutants.py <repo> <jobs> [NAME ...]
"""
import concurrent.futures
import sys
import tempfile
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
jobs = int(sys.argv[2])
sys.path.insert(0, str(repo / "scripts"))
import process_test_support as pts  # noqa: E402
import test_suite_cancellation as tsc  # noqa: E402
from owned_process import OwnedProcesses  # noqa: E402

SEND = "            self._signal(fd, signum)\n            self._signal(fd, signal.SIGCONT)\n"
EDGE = {
    1: ("sigcont-by-number-after-kill", (SEND, "            self._signal(fd, signum)\n"
        "            if signum == signal.SIGKILL:\n                os.kill(pid, signal.SIGCONT)\n"
        "            else:\n                self._signal(fd, signal.SIGCONT)\n")),
    101: ("recheck-spares-sigkill", ("            if identity is None or identity[1] != start:\n",
          "            if identity is None or identity[1] != start and signum != signal.SIGKILL:\n")),
    2: ("grace-a-tick-short", ("GRACE_SECONDS = 2.0", "GRACE_SECONDS = 2.0 - 2 ** -19")),
    3: ("kill-all-a-tick-early", ("                elif clock < kill_all:\n", "                elif clock < kill_all - 2 ** -19:\n")),
    4: ("verdict-a-tick-early", ("limit = kill_all + REAP_SECONDS\n", "limit = kill_all + REAP_SECONDS - 2 ** -19\n")),
    104: ("verdict-waits-for-resume", ("if clock >= limit and (owned or clock >= limit + REAP_SECONDS):",
          "if clock >= limit and (resumed is not None or not self.root_notified) and (owned or"
          " clock >= limit + REAP_SECONDS):")),
    5: ("no-resume-before-verdict", ("and root_pid in owned and not (live - {root_pid}):",
        "and root_pid in owned and not (live - {root_pid}) and clock + MAX_PASS_SECONDS < kill_all + REAP_SECONDS:")),
    6: ("trap-window-a-tick-short", ("TRAP_SECONDS = 10.0", "TRAP_SECONDS = 10.0 - 2 ** -19")),
    7: ("no-window-inside-grace", ("kill_all = max(kill_all, clock + TRAP_SECONDS)",
        "kill_all = max(kill_all, clock + TRAP_SECONDS) if clock >= deadline else kill_all")),
    8: ("trap-commands-spared-only-past-grace", ("if (pid, start) not in initial and resumed is not None:",
        "if (pid, start) not in initial and resumed is not None and resumed >= deadline:")),
    9: ("cap-lifted-past-a-minute", ("clock += min(now - last, MAX_PASS_SECONDS)",
        "clock += min(now - last, MAX_PASS_SECONDS) if now - last < 60 else now - last")),
    10: ("tick-passes-count-nothing", ("clock += min(now - last, MAX_PASS_SECONDS)",
         "clock += min(now - last, MAX_PASS_SECONDS) if now - last >= 0.001 else 0")),
    11: ("vanishing-verdict-ignores-resume", ("(owned or clock >= limit + REAP_SECONDS)",
         "(owned or clock >= GRACE_SECONDS + KILL_ALL_SECONDS + 2 * REAP_SECONDS)")),
    12: ("no-reap-after-first-census", ("reaped = self._reap()", "reaped = self._reap() if passes > 1 else set()")),
    13: ("sigterm-rechecks-parent", ("                key = (pid, start, signum)\n",
         "                if signum == signal.SIGTERM and _identity(pid) != (_parent, start):\n                    continue\n"
         "                key = (pid, start, signum)\n")),
    14: ("resume-collected-shell-past-grace", ("resumed is None and root_pid in owned and not (live - {root_pid}):",
         "resumed is None and (root_pid in owned or clock >= deadline) and not (live - {root_pid}):")),
    15: ("verdict-sends-sigterm", ("self._send(pid, start, signal.SIGKILL)", "self._send(pid, start, signal.SIGTERM)")),
    16: ("killed-ago-from-start", ("now - killed[pid] if pid in killed else None", "now - started if pid in killed else None")),
    116: ("rv6-return-before-confirm", ("            owned = {pid: entry for pid, entry in census.items() if pid not in reaped}\n",
          "            owned = {pid: entry for pid, entry in census.items() if pid not in reaped}\n"
          "            if not owned:\n                return\n")),
    117: ("pass-floor-cap", ("clock += min(now - last, MAX_PASS_SECONDS)", "clock += max(now - last, MAX_PASS_SECONDS)")),
}
pick = set(sys.argv[3:])
names = []
for row, (name, edit) in EDGE.items():
    if pick and name not in pick:
        continue
    pts.MUTANTS[name] = (None, f"edge of row {row % 100}", edit)
    names.append(name)
targets = tsc.OWNER_CONTROLS
runs = [(name, control) for name in names for control in targets]
with OwnedProcesses():
    with tempfile.TemporaryDirectory(prefix="edge-", dir="$VALIDATION_STORAGE/833-a726g/tmp") as scratch:
        trees = {name: pts.mutant_tree(Path(scratch), name) for name in names}
        with concurrent.futures.ThreadPoolExecutor(jobs) as pool:
            results = dict(zip(runs, pool.map(lambda run: pts.run_mutant(trees[run[0]], run[1]), runs)))
for name in names:
    red = []
    for control in targets:
        status, seconds, output = results[(name, control)]
        lines = [line for line in output.splitlines() if line.strip()]
        if status != 0:
            red.append(control)
            print(f"  {name} / {control}: {'cut' if status is None else 'red'} {seconds:.1f} s: "
                  f"{lines[-1][:200] if lines else ''}", flush=True)
    print(f"== {pts.MUTANTS[name][1]}: {name}: {'SURVIVES' if not red else 'red on ' + ', '.join(red)}", flush=True)
