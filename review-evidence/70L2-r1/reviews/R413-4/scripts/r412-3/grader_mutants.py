#!/usr/bin/env python3
"""Plant wrong armed-charging rules into a COPY of fw_service_budget/run.py
and require the grader's own --self-test to refuse each one.

usage: grader_mutants.py <repo-root> <scratch-dir>
Prints one line per mutant: KILLED (self-test rc != 0) or SURVIVED."""
import shutil
import subprocess
import sys
from pathlib import Path

root, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
src = (root / "tb/verilator/fw_service_budget/run.py").read_text()
GUARD = "    if armed is None or row['start_sys_cycle'] >= armed:\n        return row['period_bound_ms']\n"
FIRST = "    armed = min((event['first'] for event in events if event['kind'] == 'ticks'), default=None)\n"
PHY = "        publication_ms = phase_ms + bounds[index] - 250 + poll_ms\n"
mutants = {
    # identity control: the unmodified grader must PASS in this harness
    "W0_identity_control": (GUARD, GUARD),
    # the old rule: every duty keeps its whole span
    "W1_old_whole_span": (GUARD, "    return row['period_bound_ms']\n"),
    # a duty that starts before arming is never charged
    "W2_unarmed_never_charged": (GUARD, GUARD + "    return None\n"),
    # each duty charged from the first opportunity INSIDE it (drops every leading tail)
    "W3_first_tick_inside_duty": (FIRST, "    armed = min((event['first'] for event in events if event['kind'] == 'ticks' and event['first'] >= row['start_sys_cycle']), default=None)\n"),
    # arming read from the LAST opportunity block instead of the first
    "W4_last_tick": (FIRST, "    armed = max((event['first'] for event in events if event['kind'] == 'ticks'), default=None)\n"),
    # the PHY stretch keeps the whole span while the tick stretch is armed
    "W5_phy_whole_span": (PHY, "        publication_ms = phase_ms + row['period_bound_ms'] - 250 + poll_ms\n"),
    # the armed bound forgets the UART allowance
    "W6_armed_no_uart": ("    row['armed_period_bound_ms'] = 250 + span['no_tick_ms'] + row['uart_tx_allowance_ms']\n",
                         "    row['armed_period_bound_ms'] = 250 + span['no_tick_ms']\n"),
}
for name, (old, new) in mutants.items():
    assert src.count(old) == 1, name
    tree = scratch / name
    if tree.exists():
        shutil.rmtree(tree)
    shutil.copytree(root / "tb/verilator/fw_service_budget", tree / "tb/verilator/fw_service_budget")
    (tree / "tb/verilator/fw_service_budget/run.py").write_text(src.replace(old, new, 1))
    for extra in ("tb/verilator/nvm_capture_cpu", "tb/common", "sw", "scripts"):
        link = tree / extra
        link.parent.mkdir(parents=True, exist_ok=True)
        if not link.exists():
            link.symlink_to(root / extra)
    run = subprocess.run([sys.executable, "-B", str(tree / "tb/verilator/fw_service_budget/run.py"), "--self-test"],
                         capture_output=True, text=True, cwd=tree)
    tail = (run.stdout + run.stderr).strip().splitlines()[-3:]
    print(f"{name}: {'KILLED' if run.returncode else 'SURVIVED'} rc={run.returncode} :: {' | '.join(tail)[:400]}")
