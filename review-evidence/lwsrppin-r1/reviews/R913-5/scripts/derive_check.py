"""Independent check: TRAIN/PINNED equal the round-4 egress receipts; each figure = hold + (largest-hold)*1.05,
rounded up to 0.01 ms, computed in Decimal; equal to the ruling's figures and the tool's LEDGER.
Usage: python3 -I derive_check.py <tool dir> <round-4 egress-ledger-8x8-1if.log> <round-4 train egress log>"""
import re, sys, importlib.util
from decimal import Decimal, ROUND_CEILING
tool, merge_log, train_log = sys.argv[1:4]
spec = importlib.util.spec_from_file_location('egress_ledger', tool + '/egress_ledger.py')
sys.path.insert(0, tool); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
def receipt(path):
    return {r: float(v) for r, v in re.findall(r'^\| `([^`]+)` \| ([\d.]+) \|', open(path).read(), re.M)}
ruling = {'backlog.owed.if0': '64.31', 'backlog.owed_behind0.if0': '64.51', 'backlog.owed_behind1.if0': '64.71',
          'backlog.owed_behind2.if0': '64.91', 'backlog.owed_behind3.if0': '65.11',
          'backlog-owed.service.acmp.last.if0': '63.29', 'backlog-owed.service.aecp.last.if0': '63.23'}
ok = True
rm, rt = receipt(merge_log), receipt(train_log)
print('PINNED == round-4 merge receipt:', m.PINNED == rm); ok &= m.PINNED == rm
print('TRAIN  == round-4 train receipt:', m.TRAIN == rt); ok &= m.TRAIN == rt
hold = Decimal(m.HOLD_MS); print('hold', hold)
for row in m.MERGED:
    vals = {n: Decimal(repr(getattr(m, n)[row])) for n in ('MERGED', 'COMPOSED', 'LISTENED', 'TRAIN', 'PINNED')}
    big = max(vals.values()); setby = [n for n, v in vals.items() if v == big]
    fig = (hold + (big - hold) * Decimal('1.05')).quantize(Decimal('0.01'), rounding=ROUND_CEILING)
    tool_fig = Decimal(repr(m.LEDGER['8x8-1if'][row]))
    good = fig == Decimal(ruling[row]) == tool_fig and Decimal(repr(m.MEASURED['8x8-1if'][row])) == big
    ok &= good
    print(f'{row}: largest {big} set by {setby} -> {fig}; ruling {ruling[row]}; tool {tool_fig}; {"ok" if good else "DIFF"}')
print('RESULT', 'PASS' if ok else 'FAIL'); sys.exit(0 if ok else 1)
