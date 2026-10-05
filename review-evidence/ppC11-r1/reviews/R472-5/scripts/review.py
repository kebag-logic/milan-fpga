#!/usr/bin/env python3
"""Reproduce the merge audit and focused gates; all child commands are awaited."""
import argparse
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import stat
import subprocess
import sys
import time

HEAD = '7124bde172a523179a2788dca825587aa5a2a1e6'
TREE = '6009d72c1ee277ec12e287926b371000be555fba'
PARENT = '5123548eb4de35f24d43eb088c12dab70b06d01d'
PACKET = Path(__file__).resolve().parents[1]
RECEIPTS = PACKET / 'receipts'
SCRATCH = PACKET / 'scratch'


def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args])


def run(repo, name, cmd, env=None, expected=0):
    start = time.time()
    with (RECEIPTS / (name + '.log')).open('wb') as log:
        log.write(('$ ' + shlex.join(map(str, cmd)) + '\n').encode())
        log.flush()
        p = subprocess.run(list(map(str, cmd)), cwd=repo, env=env, stdout=log,
                           stderr=subprocess.STDOUT, timeout=570)
    (RECEIPTS / (name + '.rc')).write_text(str(p.returncode) + '\n')
    print(f'{name}: rc {p.returncode}, expected {expected}, {time.time()-start:.2f}s', flush=True)
    assert p.returncode == expected, name
    return (RECEIPTS / (name + '.log')).read_text()


def audit(repo):
    assert git(repo, 'rev-parse', 'HEAD').decode().strip() == HEAD
    assert git(repo, 'rev-parse', 'HEAD^{tree}').decode().strip() == TREE
    parents = git(repo, 'show', '-s', '--format=%P', HEAD).decode().split()
    assert len(parents) == 2 and parents[0] == PARENT and parents[1].startswith('054d01c7')
    base = git(repo, 'merge-base', *parents).decode().strip()
    changes = [set(git(repo, 'diff', '--name-only', base, p).decode().splitlines()) for p in parents]
    overlap = sorted(changes[0] & changes[1])
    assert overlap == ['docs/architecture/09_verification.md']
    merged = run(repo, 'clean-merge-tree', ['git', 'merge-tree', '--write-tree', *parents])
    assert merged.splitlines()[1] == TREE
    doc = overlap[0]
    sides = []
    for label, rev in [('ours', parents[0]), ('base', base), ('theirs', parents[1])]:
        path = SCRATCH / (label + '-09.md')
        path.write_bytes(git(repo, 'show', rev + ':' + doc))
        sides.append(path)
    m = subprocess.run(['git', 'merge-file', '-p', *map(str, sides)], capture_output=True)
    assert m.returncode == 0 and m.stdout == git(repo, 'show', HEAD + ':' + doc)
    (RECEIPTS / 'merged-09.md').write_bytes(m.stdout)
    rows = []
    for path in sorted(changes[0] | changes[1]):
        owner = 'both: clean text merge' if path in overlap else ('reviewed parent' if path in changes[0] else 'processor main')
        if path not in overlap:
            rev = parents[0] if path in changes[0] else parents[1]
            assert git(repo, 'ls-tree', rev, '--', path) == git(repo, 'ls-tree', HEAD, '--', path), path
        rows.append({'path': path, 'owner': owner})
    # C11 has no behavioral HDL or C++ changes relative to processor main.
    def without_comments(blob):
        return re.sub(rb'\s+', b'', re.sub(rb'/\*.*?\*/|//[^\n]*', b'', blob, flags=re.S))
    code = []
    for path in git(repo, 'diff', '--name-only', parents[1], HEAD, '--', 'hdl', 'tb').decode().splitlines():
        if Path(path).suffix in ['.sv', '.cpp', '.hpp']:
            assert without_comments(git(repo, 'show', parents[1]+':'+path)) == without_comments(git(repo, 'show', HEAD+':'+path)), path
            code.append(path)
    data = {'head': HEAD, 'tree': TREE, 'parents': parents, 'merge_base': base,
            'overlap': overlap, 'clean_merge_tree_matches': True,
            'independent_merge_file_matches': True, 'path_ownership': rows,
            'c11_code_equal_after_comment_and_whitespace_removal': code}
    (RECEIPTS / 'structural-audit.json').write_text(json.dumps(data, indent=2)+'\n')
    old = git(repo, 'show', 'c050d97153dd0480ae741102c1647eeda9b7f273:docs/architecture/02_interfaces.md').decode()
    history = (repo/'docs/history/02-class-a-word-stream.md').read_text()
    start = old.index('Word-oriented stream,')
    end = old.index('\n\nThe RX stream carries', start)
    assert old[start:end] in history
    assert re.findall(r'```wavedrom\n(.*?)\n```', old, re.S)[:2] == re.findall(r'```json\n(.*?)\n```', history, re.S)
    (RECEIPTS/'history-provenance.json').write_text(json.dumps({
        'base': 'c050d97153dd0480ae741102c1647eeda9b7f273',
        'historical_prose_and_table_verbatim': True,
        'historical_wave_sources_verbatim': 2}, indent=2)+'\n')
    print(json.dumps(data, indent=2), flush=True)


def integrity(repo, label):
    head = git(repo, 'rev-parse', 'HEAD').decode().strip()
    index = git(repo, 'write-tree').decode().strip()
    assert head == HEAD and index == TREE
    records = git(repo, 'ls-tree', '-rz', '--full-tree', HEAD).split(b'\0')
    rows, links = [], []
    for record in filter(None, records):
        meta, rawpath = record.split(b'\t', 1)
        mode, kind, oid = meta.decode().split()
        path = rawpath.decode()
        file = repo / path
        if kind == 'commit':
            actual = git(file, 'rev-parse', 'HEAD').decode().strip()
            assert actual == oid
            links.append({'path': path, 'gitlink': oid, 'actual': actual})
            continue
        data = os.fsencode(os.readlink(file)) if mode == '120000' else file.read_bytes()
        actual = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        actual_mode = '120000' if file.is_symlink() else ('100755' if file.stat().st_mode & stat.S_IXUSR else '100644')
        assert actual == oid and actual_mode == mode, path
        rows.append({'path': path, 'mode': mode, 'blob': oid, 'sha256': hashlib.sha256(data).hexdigest()})
    status = git(repo, 'status', '--porcelain=v1', '--untracked-files=all').decode()
    assert status == '', status
    d = {'head': head, 'tree': TREE, 'index_tree': index, 'tracked_blobs': len(rows),
         'required_gitlinks': links, 'status': status, 'files': rows}
    (RECEIPTS / ('integrity-'+label+'.json')).write_text(json.dumps(d, indent=2)+'\n')
    print(f'integrity {label}: {len(rows)} blobs and modes match; index matches; {len(links)} gitlinks; clean', flush=True)


def gates(repo):
    env = os.environ.copy()
    env['TMPDIR'] = str(SCRATCH)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    venv = SCRATCH / 'doc-env'
    if not venv.exists():
        run(repo, 'create-doc-env', [sys.executable, '-m', 'venv', venv])
        run(repo, 'install-doc-renderer', [venv/'bin/python', '-m', 'pip', 'install', 'wavedrom==2.0.3.post3'], env)
    env['PATH'] = str(venv/'bin') + os.pathsep + env['PATH']
    run(repo, 'diagram-cli-version', ['mmdc', '--version'], env)
    cmds = [('make-check', ['make', '-j16', 'check']),
            ('make-ids', ['make', '-j16', 'ids']),
            ('ids-selftest', ['python3', 'scripts/check-ids.py', '--selftest'])]
    # One foreground driver waits for all independent gates. No detached jobs.
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        futures = [pool.submit(run, repo, name, cmd, env) for name, cmd in cmds]
        for f in futures:
            f.result()


def probes(repo):
    env = os.environ.copy()
    env.update(TMPDIR=str(SCRATCH), PYTHONDONTWRITEBYTECODE='1')
    target = SCRATCH/'id-probes'
    if not target.exists():
        run(repo, 'probe-clone', ['git', 'clone', '--shared', '--no-checkout', str(repo), str(target)], env)
        run(target, 'probe-checkout', ['git', 'checkout', '--detach', HEAD], env)
    paths = ['docs/architecture/06_aecp_engine.md', 'hdl/aecp/KL_aecp_notify.sv', 'tb/aecp_notify/sim_main.cpp']
    for i, path in enumerate(paths):
        file = target/path
        original = file.read_bytes()
        token = f'T-R472-MERGE-PROBE-{i}'
        try:
            file.write_bytes(original + ('\n// '+token+'\n').encode())
            out = run(target, f'ids-imported-{i}', ['python3', 'scripts/check-ids.py'], env, 1)
            assert token in out and path in out
            out = run(target, f'make-ids-imported-{i}', ['make', '-j16', 'ids'], env, 2)
            assert token in out and path in out
        finally:
            file.write_bytes(original)
    # Compose the historical edge forms against the real merged registries.
    file = target/'tb/r472-id-probe.md'
    cases = [('valid', 'P-RX-SLOTS-1 T-ADP-\n// DELAY(-\n// START) T-NVM-{RS-DEADLINE, RS-AGGREGATE}\n', 0, ''),
             ('missing-minus-base', 'P-R472-MISSING-1\n', 1, 'P-R472-MISSING-1'),
             ('continued-optional', 'T-ADP-\n// DELAY(-\n// STRT)\n', 1, 'T-ADP-DELAY-STRT')]
    try:
        for name, body, expected, token in cases:
            file.write_text(body)
            out = run(target, 'ids-'+name, ['python3', 'scripts/check-ids.py'], env, expected)
            assert token in out
    finally:
        file.unlink(missing_ok=True)
    run(target, 'ids-probe-restored', ['make', '-j16', 'ids'], env)
    assert not git(target, 'status', '--porcelain=v1')
    print('All probes caught; disposable tracked files restored.', flush=True)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('mode', choices=['audit', 'integrity-before', 'integrity-final', 'gates', 'probes'])
    ap.add_argument('--repo', type=Path, default=Path.cwd())
    args = ap.parse_args()
    RECEIPTS.mkdir(exist_ok=True)
    SCRATCH.mkdir(exist_ok=True)
    if args.mode.startswith('integrity-'):
        integrity(args.repo.resolve(), args.mode.split('-')[1])
    else:
        globals()[args.mode](args.repo.resolve())
