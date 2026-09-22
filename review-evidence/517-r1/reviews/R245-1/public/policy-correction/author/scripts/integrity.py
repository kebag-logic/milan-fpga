#!/usr/bin/env python3
"""Prove tracked bytes, modes, index and required submodules against Git objects."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import stat
import subprocess

SOURCE = Path('$CANDIDATE')
EVIDENCE = Path(__file__).resolve().parents[1]
BASE = '7ab1c8d0ad073fbc1977c455dea89b7b318d4e52'
GATE = 'scripts/check_baremetal_only.py'
REQUIRED = ('protocol-processor', 'gptp-processor', 'third_party/verilog-axis')
BENCHMARKED = ('sim_pool.py', 'test_sim_pool.py', 'Makefile', 'sim_nxn.cpp', 'README.md')
ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
ENV['GIT_NO_REPLACE_OBJECTS'] = '1'


def git(root, *args):
    return subprocess.check_output(['rtk', 'proxy', 'git', '-C', str(root), *args], env=ENV)


def entries(root, ref):
    result = {}
    for row in git(root, 'ls-tree', '-rz', ref).split(b'\0'):
        if row:
            meta, path = row.split(b'\t', 1)
            mode, kind, oid = meta.decode().split()
            result[os.fsdecode(path)] = dict(mode=mode, kind=kind, oid=oid)
    return result


def verify(root, ref, changed=()):
    expected = entries(root, ref)
    actual_index = {}
    for row in git(root, 'ls-files', '-sz').split(b'\0'):
        if row:
            meta, path = row.split(b'\t', 1)
            mode, oid, stage = meta.decode().split()
            assert stage == '0', (path, stage)
            actual_index[os.fsdecode(path)] = dict(mode=mode, oid=oid)
    assert actual_index == {p: dict(mode=v['mode'], oid=v['oid']) for p, v in expected.items()}
    files = {}
    for path, entry in expected.items():
        if entry['kind'] == 'commit':
            continue
        file = root / path
        info = file.lstat()
        if entry['mode'] == '120000':
            assert stat.S_ISLNK(info.st_mode), path
            data = os.fsencode(os.readlink(file))
        else:
            assert stat.S_ISREG(info.st_mode), path
            assert bool(info.st_mode & 0o111) == (entry['mode'] == '100755'), path
            data = file.read_bytes()
        oid = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        if path not in changed:
            assert oid == entry['oid'], (path, oid, entry['oid'])
        files[path] = dict(**entry, disk_oid=oid, sha256=hashlib.sha256(data).hexdigest(), size=len(data))
    # Index flags cannot conceal a different source from the byte proof above.
    flags = git(root, 'ls-files', '-v').decode().splitlines()
    assert all(line.startswith('H ') for line in flags), [s for s in flags if not s.startswith('H ')]
    return dict(ref=ref, tree=git(root, 'rev-parse', ref + '^{tree}').decode().strip(),
                files=files, gitlinks={p: e['oid'] for p, e in expected.items() if e['kind'] == 'commit'},
                index_exact=True, tracked_bytes_modes_exact=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('label')
    parser.add_argument('--working', action='store_true')
    args = parser.parse_args()
    head = git(SOURCE, 'rev-parse', 'HEAD').decode().strip()
    result = dict(head=head, base=BASE)
    result['source'] = verify(SOURCE, head, (GATE,) if args.working else ())
    result['submodules'] = {}
    for path in REQUIRED:
        root = SOURCE / path
        pin = result['source']['gitlinks'][path]
        assert not root.is_symlink()
        assert git(root, 'rev-parse', 'HEAD').decode().strip() == pin
        assert Path(git(root, 'rev-parse', '--show-superproject-working-tree').decode().strip()).resolve() == SOURCE
        result['submodules'][path] = verify(root, pin)
    result['external'] = dict(pin=result['source']['gitlinks']['external'],
                              status='uninitialized; not required by focused gates; not validated')
    assert not (SOURCE / 'external' / '.git').exists()
    base_entries = entries(SOURCE, BASE)
    current_entries = entries(SOURCE, head)
    changed_paths = [p for p in sorted(set(base_entries) | set(current_entries))
                     if base_entries.get(p) != current_entries.get(p)]
    assert changed_paths == ([] if args.working else [GATE]), changed_paths
    result['changed_paths_from_base'] = changed_paths
    result['benchmarked_artifacts'] = {}
    for name in BENCHMARKED:
        path = 'tb/verilator/milan_dp/' + name
        data = (SOURCE / path).read_bytes()
        assert data == git(SOURCE, 'show', BASE + ':' + path)
        result['benchmarked_artifacts'][path] = result['source']['files'][path]
    budgets = {p: item for p, item in result['source']['files'].items() if p.endswith('.budget')}
    assert all(item['disk_oid'] == base_entries[p]['oid'] for p, item in budgets.items())
    result['unchanged_budget_files'] = budgets
    spec = importlib.util.spec_from_file_location('checked_gate', SOURCE / GATE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    fixtures = module._sim_pool_host_fixtures()
    for path, lines in fixtures.items():
        actual = git(SOURCE, 'show', BASE + ':' + path).decode().splitlines()
        assert all(line in actual for line in lines), path
    result['literal_fixtures_in_original_source'] = sum(map(len, fixtures.values()))
    target = EVIDENCE / (args.label + '.json')
    assert not target.exists(), target
    target.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(dict(head=head, tree=result['source']['tree'], changed_paths=changed_paths,
                         source_files=len(result['source']['files']), budgets=len(budgets),
                         submodules={p: {'pin': v['ref'], 'files': len(v['files'])}
                                     for p, v in result['submodules'].items()},
                         literal_fixtures=result['literal_fixtures_in_original_source'],
                         external=result['external'], verdict='PASS'), indent=2))


if __name__ == '__main__':
    main()
