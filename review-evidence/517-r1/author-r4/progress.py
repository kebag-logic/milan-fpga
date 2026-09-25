import json
from pathlib import Path
import sys

out = Path(__file__).resolve().parent
name = sys.argv[1]
path = out/name/'resources.jsonl'
if path.exists() and path.stat().st_size:
    with path.open('rb') as handle:
        handle.seek(max(0,path.stat().st_size-131072))
        lines = handle.read().splitlines()
    for line in reversed(lines):
        try:
            row = json.loads(line)
        except (ValueError,UnicodeDecodeError):
            continue
        simulations = sorted({p['executable'] for p in row['processes'] if p['executable'].startswith('Vmilan')})
        print(json.dumps(dict(run=name,seconds=round(row['seconds'],1),pool_active=row['pool'],simulations=simulations)))
        break
log = out/name/'milan_dp.log'
if log.exists():
    with log.open('rb') as handle:
        handle.seek(max(0,log.stat().st_size-32768))
        lines=handle.read().decode(errors='replace').splitlines()
    for line in lines[-3:]:
        print(line[:260])
