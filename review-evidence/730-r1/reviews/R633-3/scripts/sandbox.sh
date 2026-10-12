#!/usr/bin/env python3
"""Retain each unchanged campaign subprocess's raw output without changing its status."""
from pathlib import Path
import os,subprocess,sys
p=Path(__file__).resolve().parent.parent
tree=Path(sys.argv[1]).resolve()
mode='selftest' if '--selftest' in sys.argv else 'probe'
name=tree.name
assert name.startswith('K') and name[1:].isdigit(),name
sandbox=p/'public-inputs/reviews/R632-2/scripts/sandbox.sh'
r=subprocess.run(['bash',str(sandbox),*sys.argv[1:]],capture_output=True)
out=p/'receipts'/'mutant-logs';out.mkdir(exist_ok=True)
(out/f'{name}-{mode}.stdout').write_bytes(r.stdout)
(out/f'{name}-{mode}.stderr').write_bytes(r.stderr)
(out/f'{name}-{mode}.rc').write_text(str(r.returncode)+'\n')
sys.stdout.buffer.write(r.stdout);sys.stderr.buffer.write(r.stderr)
sys.exit(r.returncode)
