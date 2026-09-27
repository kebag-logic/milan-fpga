#!/usr/bin/env python3
"""Mutation probes of the harness grader in an isolated mirror; head files untouched.

Usage: mutate.py <repo> <scratch-dir>
For each mutation: fresh mirror copy of run.py with one exact replacement, then
(1) run.py --self-test rc, (2) regrade of the committed receipts vs committed rows.
"""
import shutil, subprocess, sys
from pathlib import Path

repo, scratch = Path(sys.argv[1]), Path(sys.argv[2])
here = Path(__file__).resolve().parent
MUTANTS = {
    'heartbeat_marker_ack': ("e['address'] == 0x93c and e['value'] == 1]", "e['address'] == 0x93c and e['value'] & 2]"),
    'enable_marker_walk_bit': ("e['address'] == 0x920 and e['value'] & 1)", "e['address'] == 0x920 and e['value'] & 2)"),
    'ms_clock_ratio_cpu': ("ms=cycles / 100_000,", "ms=cycles / 50_000,"),
    'cpu_cycles_unhalved': ("cpu_cycles=(cycles + 1) // 2,", "cpu_cycles=cycles,"),
    'grade_threshold_cpu_clock': ("row['budget_ms'] * 100_000, 'over-budget", "row['budget_ms'] * 200_000, 'over-budget"),
    'command_budget_1000': ("else 8000 if command.endswith(' commit') else 500", "else 8000 if command.endswith(' commit') else 1000"),
    'heartbeat_budget_2000': ("interval('maximum_heartbeat_gap', gap_start, gap_end, 500, gap_wait)",
                              "interval('maximum_heartbeat_gap', gap_start, gap_end, 2000, gap_wait)"),
    'heartbeat_no_tail': ("heartbeats[1:] + [ends[-1]['cycle']]", "heartbeats[1:]"),
    'boot_start_zero': ("interval('boot_to_entity_enabled', 64,", "interval('boot_to_entity_enabled', 0,"),
    'status_end_marker_first_byte': ("interval(command, start['cycle'], end['cycle'], budget, wait)",
                                     "interval(command, start['cycle'], start['cycle'] + 1, budget, 0)"),
    'grade_rows_noop': ("            require(row['sys_cycles'] <= row['budget_ms'] * 100_000, 'over-budget duty: ' + row['duty'])",
                        "            pass"),
}
root = scratch / 'mirror'
if root.exists():
    shutil.rmtree(root)
(root / 'tb/verilator').mkdir(parents=True)
for p in ('docs', 'sw', 'configs', 'scripts'):
    (root / p).symlink_to(repo / p)
(root / 'tb/common').symlink_to(repo / 'tb/common')
(root / 'tb/verilator/nvm_capture_cpu').symlink_to(repo / 'tb/verilator/nvm_capture_cpu')
h = root / 'tb/verilator/fw_service_budget'
shutil.copytree(repo / 'tb/verilator/fw_service_budget', h)
orig = (h / 'run.py').read_text()
print(f"{'mutant':32} selftest_rc  regrade_rc")
for name in ['none', *MUTANTS]:
    text = orig
    if name != 'none':
        o, n = MUTANTS[name]
        assert orig.count(o) == 1, name
        text = orig.replace(o, n)
    (h / 'run.py').write_text(text)
    st = subprocess.run([sys.executable, '-B', str(h / 'run.py'), '--self-test'], capture_output=True, text=True)
    rg = subprocess.run([sys.executable, '-B', str(here / 'regrade_check.py'), str(h), str(repo)], capture_output=True, text=True)
    last = (st.stdout + st.stderr).strip().splitlines()[-1][:90] if (st.stdout + st.stderr).strip() else ''
    print(f'{name:32} {st.returncode:^11} {rg.returncode:^10}  selftest: {last}')
    for line in rg.stdout.strip().splitlines():
        print('      regrade| ' + line[:200])
(h / 'run.py').write_text(orig)
