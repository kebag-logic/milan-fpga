"""Probe: the firmware gate's text cross-check of builders (ctrl_configs.held, its builder_texts loop) at a
checkout, with the module's OUTSIDE as committed, and with the named entries removed (the parent head's table).

Usage: python3 -I probe_outside.py <checkout> [removed-path ...]
Prints every builder found by text that the cross-check would refuse, then 'REFUSED n' or 'CLEAN'.
It reproduces only the loop's classification (a program named by none of BUILDERS, PART_OF, OUTSIDE or SUITES);
it compiles and runs nothing.
"""
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / 'sw/firmware/ctrl/test'))
import ctrl_configs as c  # noqa: E402

outside = dict(c.OUTSIDE)
for name in sys.argv[2:]:
    del outside[name]
names = {b.path for b in c.BUILDERS}
refused = []
for path, text in c.builder_texts().items():
    name = c.rel(path)
    if name in names or name in outside or name in c.SUITES:
        continue
    if c.program(path, text) and name not in c.PART_OF:
        refused.append(name)
for name in refused:
    print('would refuse (program, unlisted):', name)
print(f'REFUSED {len(refused)}' if refused else 'CLEAN')
