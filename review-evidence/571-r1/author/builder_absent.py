"""Run the entire builder bank with its RV32 candidates unavailable."""
import json
from pathlib import Path
import runpy
import subprocess
import sys
from unittest.mock import patch

ROOT = Path('$LANES/571-pp-unit-counts')
sys.path.insert(0, str(ROOT / 'sw/builder'))
real_run = subprocess.run
cross = {str(Path.home() / 'br-milan-rv32/host/bin/riscv32-linux-gcc'),
         'riscv64-elf-gcc', 'riscv32-unknown-elf-gcc'}
hidden = set()


def without_cross(argv, **kwargs):
    """Hide only cross candidates; all native probes and other gates run."""
    if isinstance(argv, (list, tuple)) and str(argv[0]) in cross:
        hidden.add(str(argv[0]))
        raise FileNotFoundError('compiler-absent validation fixture')
    return real_run(argv, **kwargs)


sys.argv = [str(ROOT / 'sw/builder/test_builder.py')]
with patch.object(subprocess, 'run', side_effect=without_cross):
    result = runpy.run_path(sys.argv[0], run_name='__main__')
assert hidden == cross, hidden
assert any('THREE INSTRUMENTS' in why for _, why, _ in result['SKIPPED'])
print('ABSENT MODE: all three cross candidates hidden; complete bank executed')
Path('/tmp/571-a371/absent-audit.json').write_text(json.dumps({
    'hidden_candidates': sorted(hidden), 'skipped': result['SKIPPED']}, indent=2) + '\n')
