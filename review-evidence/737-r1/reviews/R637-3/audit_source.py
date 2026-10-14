#!/usr/bin/env python3
"""Read-only source identity, pin, resource and public evidence checks."""
import ast
from collections import Counter
import hashlib
import json
from pathlib import Path
import stat
import subprocess
import sys

HEAD = '84ee9ea119b548b4982d2c0988d8753a2ce4d0cf'
TREE = '4d44778bb1074178effb49e07480a33d95e8fd6d'
RUNNER = 'f968f67655ac386ea703248b724c3781b95ec379d3a5287b378e470df81f895c'

def main():
    root = Path(sys.argv[1]).resolve()
    out = Path(__file__).resolve().parent
    def git(*args):
        return subprocess.check_output(['git', '--no-replace-objects', '-C', str(root), *args])
    assert git('rev-parse', 'HEAD').decode().strip() == HEAD
    assert git('rev-parse', 'HEAD^{tree}').decode().strip() == TREE
    assert git('diff', '--cached', '--raw', HEAD) == b''
    index = {}
    for row in git('ls-files', '--stage', '-z').split(b'\0'):
        if row:
            meta, path = row.split(b'\t', 1)
            mode, oid, stage = meta.decode().split()
            assert stage == '0'
            index[path.decode()] = (mode, oid)
    checked = 0
    links = []
    tracked = {}
    for row in git('ls-tree', '-rz', HEAD).split(b'\0'):
        if not row:
            continue
        meta, path = row.split(b'\t', 1)
        mode, kind, oid = meta.decode().split()
        name = path.decode()
        tracked[name] = (mode, oid)
        target = root / name
        if kind == 'commit':
            if name == 'external':
                links.append({'path': name, 'pin': oid, 'initialized': False})
                continue
            actual = subprocess.check_output(['git', '-C', str(target), 'rev-parse', 'HEAD']).decode().strip()
            assert actual == oid, name
            status = subprocess.check_output(['git', '-C', str(target), 'status', '--porcelain'])
            assert not status, name
            links.append({'path': name, 'pin': oid, 'initialized': True, 'clean': True})
        else:
            info = target.lstat()
            assert stat.S_ISREG(info.st_mode), name
            assert ('100755' if info.st_mode & 0o111 else '100644') == mode, name
            raw = target.read_bytes()
            actual = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
            assert actual == oid, name
            checked += 1
    assert index == tracked
    assert not git('status', '--porcelain=v1', '--untracked-files=all')
    raw = (root / 'scripts/act_ci.py').read_bytes()
    assert hashlib.sha256(raw).hexdigest() == RUNNER
    syntax = ast.parse(raw)
    pins = ast.literal_eval(next(n for n in syntax.body if isinstance(n, ast.Assign)
                          and any(isinstance(t, ast.Name) and t.id == 'EVIDENCE_HELPERS' for t in n.targets)).value)
    for name, want in pins.items():
        assert hashlib.sha256((root / 'scripts' / name).read_bytes()).hexdigest() == want
    def without_pins(source):
        tree = ast.parse(source)
        tree.body = [n for n in tree.body if not (isinstance(n, ast.Assign) and
                     any(isinstance(t, ast.Name) and t.id == 'EVIDENCE_HELPERS' for t in n.targets))]
        return ast.dump(tree)
    assert without_pins(raw) == without_pins(git('show', '2658a64c:scripts/act_ci.py'))
    assert git('diff', '2658a64c..HEAD', '--', 'scripts/check_baremetal_only.py') == b''
    before = ast.parse(git('show', '2658a64c:scripts/build_ci_act.py'))
    after = ast.parse((root / 'scripts/build_ci_act.py').read_text())
    def assignment(tree, name):
        return ast.literal_eval(next(n for n in tree.body if isinstance(n, ast.Assign) and
                         any(isinstance(t, ast.Name) and t.id == name for t in n.targets)).value)
    assert assignment(before, 'GO_SHA256') == assignment(after, 'GO_SHA256')
    assert assignment(after, 'GO_ARCHIVE').format(sys.platform) == 'go1.25.0.linux-amd64.tar.gz'
    public = out / 'scratch/public-evidence'
    resource = json.loads((public / 'round3-source-sizing.json').read_text())
    accepted = []
    for row in resource['accepted']:
        for name, want in row['recipe']['worktree_inputs'].items():
            assert hashlib.sha256((root / name).read_bytes()).hexdigest() == want
        reserve = (row['memory_cap_bytes'] - row['memory_peak_bytes']) / row['memory_cap_bytes']
        assert reserve >= 0.25 and row['rc'] == 0 and not any(row['memory_events'].values())
        assert row['recipe']['compiler_jobs'] == 8
        accepted.append({'class': row['tool'], 'cpus': row['cpu_width'], 'peak_bytes': row['memory_peak_bytes'],
                         'reserve_percent': round(reserve * 100, 3), 'recipe_matches_head': True})
    intervals = sorted((r['state']['StartedAt'], r['state']['FinishedAt']) for r in resource['accepted'])
    assert all(a[1] <= b[0] for a, b in zip(intervals, intervals[1:]))
    banks = json.loads((public / 'round3-committed-gates.json').read_text())
    assert banks['head'] == HEAD
    assert all(r['head'] == HEAD and r['returncode'] == 0 for r in banks['steps'])
    projections = json.loads((public / 'round3-worker-projections.json').read_text())
    assert all(r['seconds'] <= r['bound_seconds'] and r['margin_seconds'] == r['bound_seconds'] - r['seconds']
               for r in projections['workers'])
    result = {'head': HEAD, 'tree': TREE, 'tracked_blobs_byte_and_mode_checked': checked,
              'index_matches_tree': True, 'gitlinks': links, 'status_clean': True,
              'runner_sha256': RUNNER, 'runner_ast_unchanged_except_helper_pins': True,
              'helper_pins': pins, 'baremetal_gate_unchanged': True, 'go_digest_unchanged': True,
              'go_archive_at_review_host': assignment(after, 'GO_ARCHIVE').format(sys.platform),
              'source_builds': accepted, 'source_build_measurements_nonoverlapping': True,
              'author_exact_head_bank_steps': dict(Counter(r['workflow'] for r in banks['steps'])),
              'worker_projections_within_own_bounds': len(projections['workers']),
              'docs_base_arithmetic_seconds': 2039 - 1065 - 37 - 99 + 23.699 + 60,
              'docs_contract_worker_seconds': 316.686 + 113.654 + 2 + 120,
              'docs_workflow_projection_seconds': 1506 + 60 + 60 + 120 + 30,
              'limits': 'Static runner audit only; author source measurements and gate receipts are public evidence, not independent reruns or a manager source bank.'}
    (out / 'source-audit.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
