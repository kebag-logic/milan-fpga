#!/usr/bin/env python3
"""Probe: repeatedly re-pin a 'changed declared script' in ci/image/command-table.json
to its current sha256 and rerun ci_tool_inventory.py --check, listing every refusal the
first one masked. Run from a disposable clone; argument: max iterations."""
import hashlib, json, re, subprocess, sys
from pathlib import Path
seen = []
for _ in range(int(sys.argv[1]) if len(sys.argv) > 1 else 20):
    r = subprocess.run([sys.executable, 'scripts/ci_tool_inventory.py', '--check'], capture_output=True, text=True)
    msg = (r.stdout + r.stderr).strip().splitlines()[-1] if (r.stdout + r.stderr).strip() else ''
    print(f'rc={r.returncode} {msg}')
    m = re.search(r"changed declared script '([^']+)'", msg)
    if r.returncode == 0 or not m:
        break
    path = m.group(1); seen.append(path)
    table = Path('ci/image/command-table.json'); data = json.loads(table.read_text())
    data['scripts'][path]['sha256'] = hashlib.sha256(Path(path).read_bytes()).hexdigest()
    table.write_text(json.dumps(data, indent=2, sort_keys=False) + '\n')
print('re-pinned:', seen)
