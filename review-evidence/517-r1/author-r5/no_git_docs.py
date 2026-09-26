import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from run_gate import ROOT, run

with tempfile.TemporaryDirectory(prefix='517-docs-export-') as directory:
    target = Path(directory)
    entries = subprocess.check_output(['git', 'ls-files', '-s', '-z'], cwd=ROOT).split(b'\0')
    for entry in entries:
        if not entry:
            continue
        metadata, raw = entry.split(b'\t', 1)
        if metadata.startswith(b'160000 '):
            (target / os.fsdecode(raw)).mkdir(parents=True, exist_ok=True)
            continue
        relative = Path(os.fsdecode(raw))
        destination = target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / relative, destination, follow_symlinks=False)
    raise SystemExit(run('docs-no-git', ['python3', '-B', 'scripts/docs_check.py'], cwd=target))
