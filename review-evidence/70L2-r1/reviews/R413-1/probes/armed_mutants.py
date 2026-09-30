#!/usr/bin/env python3
"""Plant wrong service-stretch rules into the SCRATCH tree's run.py (argv[1]
= tree) one at a time and require the grader's self-test to fail each.
The original bytes come from the review clone at the exact head."""
import subprocess, sys
from pathlib import Path
tree = Path(sys.argv[1])
orig = Path("$REVIEWS/r413-1-70L2/tb/verilator/fw_service_budget/run.py").read_text()
target = tree / "tb/verilator/fw_service_budget/run.py"
A = "    armed = min((event['first'] for event in events if event['kind'] == 'ticks'), default=None)\n"
S = "    span = tick_span(events, armed, row['end_sys_cycle'])\n"
G = "    if armed is None or row['start_sys_cycle'] >= armed:\n        return row['period_bound_ms']\n"
MUT = {
  "skip_every_unarmed_start": (G, G + "    return None\n"),
  "anchor_last_tick": (A, A.replace("min((event['first']", "max((event['last']")),
  "anchor_first_heartbeat_write": (A, "    armed = min((event['cycle'] for event in events if event['kind'] == 'write' and event.get('address') == 0x93c and event.get('value') == 1), default=None)\n"),
  "span_from_duty_start": (S, "    span = tick_span(events, row['start_sys_cycle'], row['end_sys_cycle'])\n"),
  "exempt_aem_by_name": (G, "    if row['duty'] == 'aem_copy_crc':\n        return None\n" + G),
  "armed_bound_without_250_base": ("    row['armed_period_bound_ms'] = 250 + span['no_tick_ms']", "    row['armed_period_bound_ms'] = span['no_tick_ms']"),
}
ok = True
for name, (old, new) in MUT.items():
    assert orig.count(old) == 1, name
    target.write_text(orig.replace(old, new))
    r = subprocess.run([sys.executable, str(target), "--self-test"], capture_output=True, text=True, timeout=600)
    last = (r.stderr.strip().splitlines() or r.stdout.strip().splitlines() or [""])[-1]
    print(f"{name}: rc={r.returncode} {'KILLED' if r.returncode else 'SURVIVED'} :: {last}")
    ok &= r.returncode != 0
target.write_text(orig)
print("restored run.py; all mutants killed" if ok else "restored run.py; SOME MUTANT SURVIVED")
