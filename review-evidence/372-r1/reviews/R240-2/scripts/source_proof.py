#!/usr/bin/env python3
"""Check correction extent/suffix and export exact focused inputs to scratch."""
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import zipfile

repo = Path(sys.argv[1]).resolve()
out = Path(__file__).resolve().parents[1]
head = '059c3a60b8290873ed9fd14673f9981e8af754ce'
old = '60c5225fe5f93209bf313c51b7a722f25f9aaa7d'
base = '52711029f374650dc93830d5ea28e81cb5c8f410'
def git(*args):
    return subprocess.check_output(['rtk', 'proxy', 'git', '-C', str(repo), *args])

changes = git('diff', '--name-only', old, head).decode().splitlines()
assert changes == ['docs/testing/ASSERTIONS.md', 'docs/testing/TESTING.md',
                   'tb/verilator/README.md', 'tb/verilator/ptp_ts/mux_sva_main.cpp']
name = 'tb/verilator/ptp_ts/mux_sva_main.cpp'
before, after = [git('show', rev + ':' + name) for rev in [old, head]]
before_lines, after_lines = before.splitlines(keepends=True), after.splitlines(keepends=True)
assert before_lines[35:] == after_lines[35:]
assert after_lines[35] == b'#include <verilated.h>\n'
suffix = b''.join(after_lines[35:])
assert len(suffix) == 39374
pr_changes = git('diff', '--name-only', base, head).decode().splitlines()
assert not any(n.startswith(('hdl/', 'sw/', 'syn/', 'third_party/', 'protocol-processor',
                             'gptp-processor', '.github/')) for n in pr_changes)
for name in ['tb/verilator/ptp_ts/sim_main.cpp', 'scripts/run_all_suites.sh',
             'scripts/suite_tally.py', 'scripts/suite_shards.py']:
    assert git('rev-parse', base + ':' + name) == git('rev-parse', head + ':' + name), name
for name, args in [('source.diff', ['diff', base, head]),
                   ('correction.diff', ['diff', old, head]),
                   ('history.txt', ['log', '--format=fuller', '--parents', base+'..'+head])]:
    (out / 'raw' / name).write_bytes(git(*args))
archive = git('archive', '--format=zip', head, 'tb/common', 'tb/verilator/ptp_ts',
              'hdl/common', 'hdl/ieee8021as/ptp_timestamp', 'scripts/suite_tally.py')
scratch = out / 'scratch'
assert not scratch.exists(), 'scratch must be new'
with zipfile.ZipFile(io.BytesIO(archive)) as files:
    files.extractall(scratch)
print(json.dumps(dict(head=head, base=base, correction_parent=old, correction_paths=changes,
                     original_scope=pr_changes, suffix_start_line=36, suffix_bytes=len(suffix),
                     suffix_sha256=hashlib.sha256(suffix).hexdigest(),
                     scratch=str(scratch), focused_archive_sha256=hashlib.sha256(archive).hexdigest()),
                 indent=2))
