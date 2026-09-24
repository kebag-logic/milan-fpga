from pathlib import Path
import runpy, sys
from unittest.mock import patch
sys.path.insert(0, str(Path.cwd() / 'sw/builder'))
from test_firmware_compiler import CompilerAudit
records = Path(__file__).with_name('full-builder-absent-argv.jsonl')
assert not records.exists()
with records.open('w') as stream:
    audit = CompilerAudit(stream, None)
    sys.argv = ['sw/builder/test_builder.py']
    with patch('subprocess.run', side_effect=audit.invoke):
        state = runpy.run_path('sw/builder/test_builder.py', run_name='__main__')
    assert audit.hidden == audit.cross, audit.hidden
    assert audit.compiles == 0, audit.compiles
    assert any('THREE INSTRUMENTS' in why for _, why, _ in state['SKIPPED'])
    print(f'ABSENT AUDIT PASS: {len(audit.hidden)} cross candidates hidden; {audit.compiles} firmware compiles')
