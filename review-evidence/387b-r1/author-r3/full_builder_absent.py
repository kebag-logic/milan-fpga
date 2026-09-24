import runpy, subprocess, sys
from pathlib import Path
from unittest.mock import patch
root = Path('$LANES/387-media-rebase')
sys.path.insert(0, str(root/'sw/builder'))
from test_firmware_compiler import CompilerAudit
with (Path(__file__).parent/'builder-compiler-audit.jsonl').open('w') as stream:
    audit = CompilerAudit(stream, None)
    with patch.object(subprocess, 'run', side_effect=audit.invoke), patch.object(sys, 'argv', ['sw/builder/test_builder.py']):
        runpy.run_path(str(root/'sw/builder/test_builder.py'), run_name='__main__')
    assert audit.hidden == audit.cross, audit.hidden
    assert audit.compiles == 0
    print('Full builder: all RV32 candidates absent; firmware compiler invocations:',audit.compiles)
