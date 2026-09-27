"""Run the complete builder entry while hiding only its RV32 candidates."""
from pathlib import Path
import runpy
import subprocess
import sys
from unittest.mock import patch

ROOT = Path.cwd().resolve()
sys.path.insert(0, str(ROOT / 'sw/builder'))
from test_firmware_compiler import CompilerAudit

with (Path('/tmp/573-a352') / 'absent-candidates.jsonl').open('w') as stream:
    audit = CompilerAudit(stream, None)
    original = subprocess.run

    def invoke(argv, **kwargs):
        if str(argv[0]) in audit.cross:
            return audit.invoke(argv, **kwargs)
        return original(argv, **kwargs)

    with patch.object(subprocess, 'run', side_effect=invoke), \
            patch.object(sys, 'argv', [str(ROOT / 'sw/builder/test_builder.py')]):
        runpy.run_path(str(ROOT / 'sw/builder/test_builder.py'), run_name='__main__')
    assert audit.hidden == audit.cross, audit.hidden
    print('ABSENT MODE: all three RV32 candidates hidden; full builder entry completed')
