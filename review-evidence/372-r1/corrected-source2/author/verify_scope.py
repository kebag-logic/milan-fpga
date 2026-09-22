"""Prove the four-path correction and unchanged executable harness bytes."""
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent
LANE = Path('$CANDIDATE')
BASE = '60c5225fe5f93209bf313c51b7a722f25f9aaa7d'
ALLOWED = {
    'docs/testing/ASSERTIONS.md', 'docs/testing/TESTING.md',
    'tb/verilator/README.md', 'tb/verilator/ptp_ts/mux_sva_main.cpp',
}


def git(*args):
    return subprocess.check_output(
        ['rtk', 'proxy', 'git', '--no-replace-objects', *args], cwd=LANE
    )


def sha(data):
    return hashlib.sha256(data).hexdigest()


changed = set(git('diff', '--name-only', BASE).decode().splitlines())
assert changed == ALLOWED, changed
initial = json.loads((ROOT / 'initial-integrity.json').read_text())
files = []
for entry in initial['files']:
    path = LANE / entry['path']
    data = str(path.readlink()).encode() if path.is_symlink() else path.read_bytes()
    mode = '120000' if path.is_symlink() else ('100755' if path.stat().st_mode & 0o111 else '100644')
    assert mode == entry['mode'], entry['path']
    if entry['path'] not in ALLOWED:
        assert sha(data) == entry['sha256'], entry['path']
    files.append({'path': entry['path'], 'mode': mode, 'sha256': sha(data)})
pins = {}
for row in git('ls-files', '--stage').decode().splitlines():
    meta, path = row.split('\t')
    mode, oid, stage = meta.split()
    assert stage == '0', row
    if mode == '160000':
        pins[path] = oid
assert pins == initial['gitlinks'], pins
flags = git('ls-files', '-v').decode().splitlines()
assert not [row for row in flags if row[0].islower() or row.startswith('S ')]
path = 'tb/verilator/ptp_ts/mux_sva_main.cpp'
old = git('show', f'{BASE}:{path}')
new = (LANE / path).read_bytes()
marker = b'#include <verilated.h>'
old_index, new_index = old.index(marker), new.index(marker)
old_header, new_header = old[:old_index], new[:new_index]
for header in (old_header, new_header):
    assert all(not line.strip() or line.startswith(b'//') for line in header.splitlines())
    assert not any(line.rstrip().endswith(b'\\') or b'??/' in line for line in header.splitlines())
assert old_header.count(b'\n') == new_header.count(b'\n')
assert old[old_index:] == new[new_index:]
token_receipt = {
    'path': path, 'base': BASE,
    'method': 'Every byte from the first executable/preprocessor token to EOF is identical; both prefixes contain only full-line comments and blanks, no line splicing, and the same newline count.',
    'first_executable_line_before': old_header.count(b'\n') + 1,
    'first_executable_line_after': new_header.count(b'\n') + 1,
    'executable_suffix_bytes': len(old[old_index:]),
    'executable_suffix_sha256_before': sha(old[old_index:]),
    'executable_suffix_sha256_after': sha(new[new_index:]),
    'whole_file_sha256_before': sha(old), 'whole_file_sha256_after': sha(new),
    'equal': True,
}
report = {
    'base': BASE, 'head': git('rev-parse', 'HEAD').decode().strip(),
    'head_tree': git('rev-parse', 'HEAD^{tree}').decode().strip(),
    'index_tree': git('write-tree').decode().strip(),
    'changed_paths': sorted(changed), 'unchanged_ordinary_files': len(files) - len(ALLOWED),
    'all_file_modes_unchanged': True, 'hidden_flags': 0, 'gitlinks': pins,
    'required_submodule_status': git('submodule', 'status', 'third_party/verilog-axis', 'protocol-processor', 'gptp-processor').decode(),
    'harness_executable_token_comparison': token_receipt,
    'working_files': files,
    'status': git('status', '--porcelain=v1').decode(),
}
assert report['required_submodule_status'] == initial['required_submodule_status']
print(json.dumps({key: value for key, value in report.items() if key != 'working_files'}, indent=2))
(ROOT / 'source-scope-and-token-comparison.json').write_text(json.dumps(report, indent=2) + '\n')
