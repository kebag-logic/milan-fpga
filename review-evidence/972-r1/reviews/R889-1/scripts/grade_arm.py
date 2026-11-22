#!/usr/bin/env python3
"""grade_arm.py ROOT - the split boot simulation's PHY grade (tb/verilator/ctrl_split_boot/run.py grade_phy) on its
own native stand-in's PHY rows (phy_rows, with its PHYT line): as given, without the arm's link-down publication,
with it after the first frame, and with it publishing link up. Only the first must carry no #972 finding."""
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "tb/verilator/ctrl_split_boot"))
sys.dont_write_bytecode = True
import run  # noqa: E402

spec = {'sys_hz': 100_000_000, 'cpu_hz': 100_000_000, 'shape': 'endstation_ax7101_1x1_tdm8', 'interfaces': 1}
rows = run.phy_rows(spec['sys_hz']) + ['PHYT 50 60 120']
assert rows[0] == 'PHYP 500000 0', rows[0]
first_frame = next(r for r in rows if r.startswith('PHYF'))
cases = {
    'as-given': rows,
    'no-arm-publication': rows[1:],
    'arm-after-first-frame': rows[1:2] + [f"PHYP {int(first_frame.split()[2]) + 1} 0"] + rows[2:],
    'arm-publishes-up': ['PHYP 500000 13'] + rows[1:],
}
bad = 0
for name, r in cases.items():
    findings, report = run.grade_phy("\n".join(r) + "\n", spec, 30_000_000)
    arm = [f for f in findings if '#972' in f]
    want = name != 'as-given'
    ok = bool(arm) == want
    bad += not ok
    print(f"{'OK ' if ok else 'BAD'} {name}: {len(findings)} finding(s), #972 finding {'present' if arm else 'absent'}"
          f"{'; ' + arm[0][:160] if arm else ''}; other findings {[f[:90] for f in findings if '#972' not in f]}")
sys.exit(1 if bad else 0)
