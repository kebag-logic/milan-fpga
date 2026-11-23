"""Probe: does tb/verilator/ctrl_service_budget/shape_costs.listed() read ctrl_loop.h at a given revision?
# (dont_write_bytecode added after the recorded run, which left a cache the reviewer removed; see receipts/integrity.txt)
Usage: python3 -I probe_shape_costs.py <repo-root> <rev>...  (reads each revision's ctrl_loop.h via git show)."""
import subprocess, sys
root = sys.argv[1]
sys.path.insert(0, root + '/tb/verilator/ctrl_service_budget')
sys.dont_write_bytecode = True
import shape_costs
rc = 0
for rev in sys.argv[2:]:
    text = subprocess.run(['git', '-C', root, 'show', f'{rev}:sw/firmware/ctrl/loop/ctrl_loop.h'],
                          capture_output=True, text=True, check=True).stdout
    try:
        table = shape_costs.listed(text)
        print(f'{rev}: listed OK, shapes {sorted(tuple(s) for s in table)}')
        for n in (1, 2):
            print(f'{rev}:   at({n}) = {shape_costs.at(n, texts={shape_costs.HEADER: text})}')
    except Exception as exc:
        rc = 1
        print(f'{rev}: listed RAISED {type(exc).__name__}: {exc}')
sys.exit(rc)
