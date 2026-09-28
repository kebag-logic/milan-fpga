"""Run the unchanged full builder entry point with cross candidates absent."""
import json
from pathlib import Path
import runpy
import subprocess
import sys
from unittest.mock import patch

ROOT = Path('$LANES/602-phc-step-mr')
OUT = Path(__file__).resolve().parent
CROSS = {str(Path.home()/'br-milan-rv32/host/bin/riscv32-linux-gcc'),
         'riscv64-elf-gcc', 'riscv32-unknown-elf-gcc'}
real_run = subprocess.run
hidden = []


def absent_run(argv, **kwargs):
    """Hide only the three cross candidates; leave all other calls intact."""
    if isinstance(argv, (list, tuple)) and str(argv[0]) in CROSS:
        hidden.append([str(item) for item in argv])
        raise FileNotFoundError('deliberately absent RV32 candidate')
    return real_run(argv, **kwargs)


entry = ROOT/'sw/builder/test_builder.py'
sys.path.insert(0, str(entry.parent))
with patch.object(subprocess, 'run', side_effect=absent_run), \
        patch.object(sys, 'argv', [str(entry)]):
    result = runpy.run_path(str(entry), run_name='__main__')
assert {argv[0] for argv in hidden} == CROSS, hidden
assert any('THREE INSTRUMENTS' in why for _, why, _ in result['SKIPPED'])
(OUT/'builder-absent-audit.json').write_text(json.dumps({
    'hidden_candidate_calls': hidden,
    'skipped': result['SKIPPED'],
    'entry_point': str(entry),
    'host_calls': 'unchanged',
}, indent=2)+'\n')
print('Full bank completed with all cross candidates absent; host calls unchanged.')
