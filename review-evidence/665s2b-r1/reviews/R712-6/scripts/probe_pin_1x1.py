"""Probe: does load_grade.py --check (findings with its own ceiling) hold 1x1/1if at the pin's column?
Raises one WALK cost in STATED_US (the pin column) at 1x1/1if in memory only, leaving the donor column unchanged,
and prints the pin load, the graded load and the merge gate's findings. Usage: python3 -I probe_pin_1x1.py <repo>"""
import sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_budget'))
import load_grade as lg
base_pin = sum(lg.load(root, '1x1/1if', lg.STATED_US).values())
base_grd = sum(lg.load(root, '1x1/1if', lg.GRADED).values())
print(f'head: 1x1/1if pin {base_pin:.3f} graded {base_grd:.3f} findings {lg.findings(root)}')
for key, val in (('record.acmp', 2000), ('event.ACMP', 20000), ('base', 400)):
    saved = lg.STATED_US['1x1/1if'].get(key)
    lg.STATED_US['1x1/1if'][key] = val
    pin = sum(lg.load(root, '1x1/1if', lg.STATED_US).values())
    f = lg.findings(root)
    print(f'plant pin 1x1/1if {key}={val}: pin load {pin:.3f} (> 0.70: {pin > 0.70}); merge gate findings: {f}; '
          f'{"ESCAPED" if pin > 0.70 and not any("1x1/1if: the load" in x for x in f) else "held"}')
    if saved is None:
        del lg.STATED_US['1x1/1if'][key]
    else:
        lg.STATED_US['1x1/1if'][key] = saved
