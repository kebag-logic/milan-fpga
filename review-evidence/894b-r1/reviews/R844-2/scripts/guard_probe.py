"""Probe the declared charger contract without changing source. Usage: guard_probe.py CHECKOUT SCRATCH."""
from pathlib import Path
import subprocess
import sys

root, scratch = (Path(x).resolve() for x in sys.argv[1:3])
scratch.mkdir(parents=True, exist_ok=True)
ctrl = root / 'sw/firmware/ctrl'
inc = [f'-I{ctrl / p}' for p in ('aecp', 'loop', 'mbx', 'port')]
words = "THE SHAPES: a unit that charges a refused attempt (AECP_ATTEMPT_US) has no shape's table (ctrl_loop.h) in force"
cases = {
    'charger-correct-order': ('#include "ctrl_loop.h"\n#define AECP_CHARGES_ATTEMPTS\n#include "aecp.h"\nint x = AECP_ATTEMPT_US;\n', 0, None),
    'charger-no-table': ('#define AECP_CHARGES_ATTEMPTS\n#include "aecp.h"\n', 1, words),
    'charger-table-too-late': ('#define AECP_CHARGES_ATTEMPTS\n#include "aecp.h"\n#include "ctrl_loop.h"\n', 1, words),
    'noncharger-header-only': ('#include "aecp.h"\n', 0, None),
    'undeclared-charger-limit': ('#include "aecp.h"\nint x = AECP_ATTEMPT_US;\n', 1, 'CTRL_LOOP_RETRY_ATTEMPT_US'),
}
for name, (source, failure, diagnostic) in cases.items():
    path = scratch / (name + '.c')
    path.write_text(source)
    r = subprocess.run(['cc', '-std=c11', '-fsyntax-only', *inc, str(path)], capture_output=True, text=True)
    assert bool(r.returncode) == bool(failure), (name, r.stderr)
    assert diagnostic is None or diagnostic in r.stderr, (name, r.stderr)
    print(f'PASS {name}: rc={r.returncode}; expected diagnostic={diagnostic!r}')
    if name == 'undeclared-charger-limit':
        assert '#error "THE SHAPES' not in r.stderr
print('PASS: correct use and noncharging units compile; both declared misuse cases fail with the guard; undeclared misuse has the documented ordinary diagnostic')
