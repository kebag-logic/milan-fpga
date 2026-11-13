"""The tier model's measured inputs from a harness leg's log: the largest legal command's record (the two longest
aecp_mbx:frame spans, CPU cycles) and poll_grade.held's heaviest items (aecp_long, aecp, base), each with the stated
cost the model's rule gives it (the most measured plus 5 %, rounded up to 5 us).

usage: python3 -I measured_inputs.py TREE INTERFACES LOG"""
import math
import sys
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree / 'tb/verilator/ctrl_service_budget'))
import grade  # noqa: E402
import poll_grade  # noqa: E402

n_if, path = int(sys.argv[2]), Path(sys.argv[3])
text = path.read_text(errors='replace')
text = text[:text.rfind('\n') + 1]
spans = sorted(int(line.split()[3]) for line in text.splitlines()
               if line.startswith('SPAN ') and line.endswith('aecp_mbx:frame'))
log = grade.parse(text, 100_000_000, 100_000_000)
held = poll_grade.held(log, n_if)


def rule(cycles: int) -> int:
    """The stated cost in us: cycles at 100 MHz, plus 5 %, rounded up to 5 us."""
    return 5 * math.ceil(cycles / 100 * 1.05 / 5 - 1e-9)


print(f'{path.parent.parent.name}: the two longest aecp_mbx:frame records {spans[-2:]} CPU cycles, '
      f'rule {rule(spans[-1])} us')
for kind in ('aecp_long', 'aecp', 'base'):
    cycles = held['heaviest'].get(kind, 0)
    print(f'  {kind}: heaviest {cycles} CPU cycles, rule {rule(cycles)} us, stated {held["limits"][kind] // 100} us')
print(f"  items over their stated cost: {len(held['over'])} {[o['kind'] for o in held['over']][:8]}")
