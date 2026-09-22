#!/usr/bin/env python3
"""Index the factual command receipts and verify the complete handoff manifest."""
import hashlib
import json
from pathlib import Path
import shlex
import subprocess

OUT = Path(__file__).resolve().parents[1]
SOURCE = Path('$CANDIDATE')
BASE = '7ab1c8d0ad073fbc1977c455dea89b7b318d4e52'
HEAD = '5874895eb817ed41c0f8be4eb427ad3315c29844'


def git(*args):
    return subprocess.check_output(['rtk', 'proxy', 'git', *args], cwd=SOURCE)


def main():
    assert git('rev-parse', 'HEAD').decode().strip() == HEAD
    assert git('status', '--porcelain=v1') == b''
    assert git('rev-parse', 'HEAD^').decode().strip() == BASE
    assert len(git('show', '-s', '--format=%B', 'HEAD').decode().strip().splitlines()) == 1
    (OUT / 'correction.patch').write_bytes(git('diff', '--binary', BASE, HEAD))
    gate_hash = hashlib.sha256((SOURCE / 'scripts/check_baremetal_only.py').read_bytes()).hexdigest()
    mutations = json.loads((OUT / 'mutations/receipts.json').read_text())
    assert all(row['source_sha256'] == gate_hash and row['detected'] for row in mutations)
    rows = []
    receipts = sorted((OUT / 'raw').glob('*.json'), key=lambda p: json.loads(p.read_text())['started_utc'])
    for path in receipts:
        receipt = json.loads(path.read_text())
        expected = {'baseline-check': 1, 'preliminary-boundary-probe': 2}.get(path.stem, 0)
        assert receipt['exit'] == expected, (path, receipt['exit'])
        argv = shlex.join(receipt['argv'])
        status = receipt.get('worktree_status', 'not captured by initial recorder')
        rows.append(dict(label=path.stem, **receipt))
    (OUT / 'command-ledger.json').write_text(json.dumps(rows, indent=2) + '\n')
    lines = ['# Factual command ledger', '',
             'Each row links the raw combined output and its argv/exit receipt.',
             'Precommit tests name the then-current parent HEAD; they are not clean-head runs.',
             'The final gate check/selftest and byte proof name the correction commit.', '',
             '| Label | Exit | Exact argv |', '|---|---:|---|']
    for row in rows:
        label = row['label']
        lines.append(f"| [{label}](raw/{label}.log) ([receipt](raw/{label}.json)) | {row['exit']} | "
                     + '`' + shlex.join(row['argv']) + '` |')
    lines += ['', 'The baseline exit 1 and preliminary boundary exit 2 are preserved failures.',
              'Mutation exits are separately recorded in mutations/receipts.json and are expected refusals.', '']
    (OUT / 'COMMANDS.md').write_text('\n'.join(lines))
    files = sorted(path for path in OUT.rglob('*') if path.is_file() and path.name != 'MANIFEST.sha256')
    manifest = ''.join(hashlib.sha256(path.read_bytes()).hexdigest() + '  ' +
                       path.relative_to(OUT).as_posix() + '\n' for path in files)
    (OUT / 'MANIFEST.sha256').write_text(manifest)
    for line in manifest.splitlines():
        digest, name = line.split('  ', 1)
        assert hashlib.sha256((OUT / name).read_bytes()).hexdigest() == digest, name
    print(json.dumps(dict(head=HEAD, tree=git('rev-parse', 'HEAD^{tree}').decode().strip(),
                          clean=True, recorded_commands=len(rows),
                          manifest_files=len(files), manifest_verified=True), indent=2))


if __name__ == '__main__':
    main()
