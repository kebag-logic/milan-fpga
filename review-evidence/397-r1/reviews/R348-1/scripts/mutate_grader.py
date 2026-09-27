#!/usr/bin/env python3
"""Reviewer mutation probes of the fw_service_budget grader (run.py).

usage: mutate_grader.py <tree>   (a disposable export of the exact head)
For each mutation: patch run.py in <tree>, run its --self-test, then regrade
both committed receipts' raw logs with the mutated grade() and compare the
derived rows with the committed rows. Restores run.py after each probe.
"""
import importlib.util, json, subprocess, sys
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
run = tree / 'tb/verilator/fw_service_budget/run.py'
orig = run.read_text()
M = {
 'hb-marker-start': ("e['address'] == 0x93c and e['value'] == 1]", "e['address'] == 0x93c and e['value'] == 4]"),
 'hb-marker-bitmask': ("e['address'] == 0x93c and e['value'] == 1]", "e['address'] == 0x93c and e['value'] & 1]"),
 'hb-drop-final-tail': ("heartbeats[1:] + [ends[-1]['cycle']]", "heartbeats[1:]"),
 'enable-marker-bit1': ("e['address'] == 0x920 and e['value'] & 1)", "e['address'] == 0x920 and e['value'] & 2)"),
 'boot-start-zero': ("interval('boot_to_entity_enabled', 64,", "interval('boot_to_entity_enabled', 0,"),
 'walk-end-first-write': ("and e['cycle'] > walk_start['cycle'])", "and e['cycle'] >= 0)"),
 'cpu-ratio-1to1': ("cpu_cycles=(cycles + 1) // 2", "cpu_cycles=cycles"),
 'ms-at-50mhz': ("ms=cycles / 100_000,", "ms=cycles / 50_000,"),
 'budget-at-50mhz': ("row['budget_ms'] * 100_000", "row['budget_ms'] * 50_000"),
 'budget-at-200mhz': ("row['budget_ms'] * 100_000", "row['budget_ms'] * 200_000"),
 'command-end-shift': ("for index, (start, end) in enumerate(zip(starts, ends)):", "for index, (start, end) in enumerate(zip(starts, ends[1:] + ends[-1:])):"),
 'status-budget-8000': ("else 8000 if command.endswith(' commit') else 500", "else 8000"),
 'commit-budget-500': ("else 8000 if command.endswith(' commit') else 500", "else 500"),
 'wait-not-subtracted': ("service_ms=(cycles - wait_cycles) / 100_000", "service_ms=cycles / 100_000"),
 'erase-envelope-to-ack': ("interval('erase_enclosed_to_first_program', erase['cycle'], program['cycle']", "interval('erase_enclosed_to_first_program', erase['cycle'], end['cycle']"),
}
spec = importlib.util.spec_from_file_location
results = {}
for name, (a, b) in M.items():
    assert orig.count(a) == 1, (name, orig.count(a))
    run.write_text(orig.replace(a, b))
    try:
        st = subprocess.run([sys.executable, '-B', str(run), '--self-test'], capture_output=True, text=True)
        s = importlib.util.spec_from_file_location('m_' + name.replace('-', '_'), run)
        mod = importlib.util.module_from_spec(s); s.loader.exec_module(mod)
        diffs = {}
        for shape in ('1X1', '8X8'):
            rec = json.loads((tree / f'docs/findings/397_SERVICE_BUDGET_{shape}.json').read_text())
            try:
                got = mod.grade(rec['raw_log'], rec['media'])
                same_rows = got['rows'] == rec['rows']
                same_find = got['budget_findings'] == rec['budget_findings']
                diffs[shape] = 'rows-identical' if same_rows and same_find else 'DIFFERS(rows=%s,findings=%s)' % (same_rows, same_find)
            except Exception as exc:  # grader refusal
                diffs[shape] = 'REFUSED: ' + str(exc)[:80]
        results[name] = dict(selftest_rc=st.returncode, selftest_tail=(st.stdout + st.stderr).strip().splitlines()[-1][:120], receipt_regrade=diffs)
    finally:
        run.write_text(orig)
for k, v in results.items():
    print(f"{k:24s} self-test rc={v['selftest_rc']} ({'CAUGHT' if v['selftest_rc'] else 'ESCAPED'}) | {v['receipt_regrade']} | {v['selftest_tail']}")
json.dump(results, sys.stdout if False else open(sys.argv[2], 'w'), indent=2)
