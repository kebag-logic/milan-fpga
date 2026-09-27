#!/usr/bin/env python3
"""Reviewer mutants of the round-2 analysis code; self-test rc per mutant in a disposable mirror.

Usage: mutate_r2.py <repo> <scratch-dir>
Mirror: copies tb/verilator/fw_service_budget, symlinks the rest read-only. Each mutant is one
exact replacement in run.py; 'none' is the unmutated control. Prints rc and the failing line.
"""
import shutil, subprocess, sys
from pathlib import Path

repo, scratch = Path(sys.argv[1]), Path(sys.argv[2])
M = {
    'liveness_ppstat_bit5': ("(int(pp[1], 16) >> 6) & 1", "(int(pp[1], 16) >> 5) & 1"),
    'liveness_backed_forced_1': ("backed = int(match[1]) if match else", "backed = 1 if match else"),
    'period_phase_0': ("row['period_bound_ms'] = 250 +", "row['period_bound_ms'] = 0 +"),
    'tx_allowance_8bit_frame': ("row['uart_tx_allowance_ms'] = tx_bytes * 10_000 / 115200", "row['uart_tx_allowance_ms'] = tx_bytes * 8_000 / 115200"),
    'tx_allowance_zero': ("if a['cycle'] <= start and end <= b['cycle']]", "if False]"),
    'period_margin_1000': ("row['period_bound_margin_ms'] = 500 -", "row['period_bound_margin_ms'] = 1000 -"),
    'liveness_margin_4000': ("row['liveness_bound_margin_ms'] = 2000 -", "row['liveness_bound_margin_ms'] = 4000 -"),
    'tick_drop_internal_gap': ("            spans.append((event['gap_start'], event['gap_start'] + event['max_gap']))", "            pass"),
    'tick_drop_tail': ("    spans.append((previous, end))", "    spans.append((previous, previous))"),
    'tick_drop_head': ("        spans.append((previous, event['first']))", "        spans.append((event['first'], event['first']))"),
    'aem_marker_walk_end': ("aem = next(e for e in events if e['kind'] == 'aem_read')", "aem = walk_end"),
    'right_censored_false': ("right_censored=gap_end == ends[-1]['cycle'],", "right_censored=False,"),
    'heartbeat_liveness_margin_2500': ("liveness_margin_ms=2000 - rows[-1]['ms']", "liveness_margin_ms=2500 - rows[-1]['ms']"),
    'queued_1x1_count_11': ("(3 if shape == SHAPES[1] else 12)", "(3 if shape == SHAPES[1] else 11)"),
    'erase_limit_refuses_corner': ("0 <= erase_us <= 3_000_000", "0 <= erase_us <= 2_999_999"),
    'program_limit_50ms': ("0 <= program_us <= 5_000", "0 <= program_us <= 50_000"),
    'boot_budget_n_a': ("interval('boot_to_entity_enabled', 64, enable['cycle'], 20000)", "interval('boot_to_entity_enabled', 64, enable['cycle'], None)"),
    'wipe_erase_budget_8000': ("rows.append(interval('wipe_erase_envelope', erase['cycle'], stop['cycle'], 3500,", "rows.append(interval('wipe_erase_envelope', erase['cycle'], stop['cycle'], 8000,"),
    'heartbeat_500_met_flag': ("heartbeat_500ms_met=rows[-1]['sys_cycles'] <= 50_000_000", "heartbeat_500ms_met=rows[-1]['sys_cycles'] <= 200_000_000"),
}
root = scratch / 'mirror_r2'
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
print(f"{'mutant':34} selftest_rc  result")
for name in ['none', *M]:
    text = orig
    if name != 'none':
        o, n = M[name]
        assert orig.count(o) == 1, name
        text = orig.replace(o, n)
    (h / 'run.py').write_text(text)
    st = subprocess.run([sys.executable, '-B', str(h / 'run.py'), '--self-test'], capture_output=True, text=True)
    out = (st.stdout + st.stderr).strip().splitlines()
    verdict = 'control' if name == 'none' else ('CAUGHT' if st.returncode else 'ESCAPED')
    print(f'{name:34} {st.returncode:^11}  {verdict}: {out[-1][:110] if out else ""}')
(h / 'run.py').write_text(orig)
