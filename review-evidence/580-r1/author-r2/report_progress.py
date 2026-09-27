"""Show capture progress and enforce the assignment's immediate stop threshold."""
from pathlib import Path
import re
import sys

count = 0
for path in sorted(Path('/tmp/580-a368').glob('capture-*/capture.log')):
    rows = [{k:int(v) for k,v in re.findall(r'(\w+)=(\d+)', line)}
            for line in path.read_text(errors='replace').splitlines()
            if line.startswith('CAPTURE index=')]
    count += len(rows)
    maximum = max([row['sys_cycles']/100000 for row in rows], default=None)
    print(path.parent.name, len(rows), 'of 16', maximum)
    if any(row['sys_cycles'] > 2450000 for row in rows):
        sys.exit('STOP CONDITION EXCEEDED: report on issue #580 and stop')
print('TOTAL', count, 'of 96')
for name in ['builder-absent','milan-dp']:
    print(name, Path('/tmp/580-a368',name+'.log').read_text(errors='replace').splitlines()[-1][:220])
