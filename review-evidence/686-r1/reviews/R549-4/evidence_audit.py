#!/usr/bin/env python3
"""Read only public archived evidence and verify its identity and receipts."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

SOURCE_ARCHIVE = '84add8ed571d376f8a1b39c3c6f71c4e80eed32a'
ARCHIVE = '319f3567ed693bc5dffd422164a768c142485a2d'
HEAD = '9c601b5983acfd60fb269b9a88c27b48cab7cf65'
CANDIDATE = '1351f398f9e0c246888b9ac5286db8370a3bc1f3'
TREE = '140c3b838ef3a1f72e2669744871a48b83911311'
PREFIX = 'review-evidence/686-r1/'

def main():
    p = argparse.ArgumentParser()
    p.add_argument('repo', type=Path)
    a = p.parse_args()
    out = Path(__file__).resolve().parent
    selected = out / 'public-receipts'
    selected.mkdir(exist_ok=True)
    index = []
    def git(*args):
        return subprocess.check_output(['git', '-C', str(a.repo), *args],
                                       env=__import__('os').environ | {'GIT_NO_REPLACE_OBJECTS': '1'})
    def read(path, archive=ARCHIVE, save=False):
        raw = git('show', archive + ':' + PREFIX + path)
        index.append({'archive': archive, 'path': PREFIX + path,
                      'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)})
        if save:
            dst = selected / path
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes(raw)
        return raw
    summary = {'source_head': HEAD, 'source_archive': SOURCE_ARCHIVE,
               'candidate_archive': ARCHIVE, 'candidate_head': CANDIDATE,
               'candidate_tree': TREE, 'manager_source_bank': 'NOT RUN'}
    for bank, count in [('manager-builder', 48), ('full-native', 5)]:
        stem = 'manager-candidate/'
        results = json.loads(read(stem + bank + '/results.json', save=True))
        complete = json.loads(read(stem + bank + '/complete.json', save=True))
        integrity = json.loads(read(stem + bank + '-initial-integrity.json', save=True))
        assert results['head'] == complete['head'] == integrity['parent']['head'] == CANDIDATE
        assert integrity['parent']['tree'] == TREE and integrity['result'] == 'PASS'
        assert len(results['results']) == count and complete['exit_code'] == 0
        lines = []
        for i, r in enumerate(results['results'], 1):
            assert r['exit_code'] == 0
            raw = read(stem + bank + f'/{i:02}.log')
            lines.append({'number': i, 'exit_code': r['exit_code'], 'bytes': len(raw)})
        summary[bank] = {'count': count, 'all_exits_zero': True, 'logs': lines}
    read('manager-candidate/pinned-tool-identity.json', save=True)
    for f in ['full-native/01.log', 'full-native/05.log', 'full-suite-logs/maap.log']:
        read('manager-candidate/' + f, save=True)
    resource = 'author-r2/resource-receipts/'
    manifest = read(resource + 'MANIFEST.sha256', save=True).decode()
    checked = []
    for line in manifest.splitlines():
        digest, path = line.split(maxsplit=1)
        path = path.lstrip('*')
        assert not path.startswith('/') and '..' not in Path(path).parts
        raw = read(resource + path)
        assert hashlib.sha256(raw).hexdigest() == digest, path
        checked.append(path)
    summary['resource_manifest'] = {'checked': len(checked), 'mismatches': 0}
    baseline = json.loads(git('show', HEAD + ':syn/ooc/pp_resource_baseline.json'))
    prior = json.loads(git('show', '291710b180ca9196780a6d17f2517957c9bcb89c:syn/ooc/pp_resource_baseline.json'))
    summary['resource_records_equal'] = []
    for endpoint in ['route-1x1', 'ooc-1x1', 'ooc-8x8']:
        for name in ['record.json', 'regen.log']:
            read(resource + 'r2-48f12dc1/' + endpoint + '/' + name, save=True)
        record = json.loads((selected / resource / 'r2-48f12dc1' / endpoint / 'record.json').read_text())
        assert record == baseline['endpoints'][endpoint]['record']
        for key in ['tolerance', 'floor', 'ceiling']:
            assert baseline['endpoints'][endpoint].get(key) == prior['endpoints'][endpoint].get(key)
        summary['resource_records_equal'].append(endpoint)
        for name in ['check_' + endpoint + '.log', 'check_' + endpoint + '.rc']:
            read(resource + 'r2-48f12dc1/gate/' + name, save=True)
    handoff = read('author-r2/HANDOFF.md', SOURCE_ARCHIVE).decode()
    begin = handoff.index('### Round 2 gate table, final')
    end = handoff.index('### Area (Part A)', begin)
    (out / 'author-source-gate-table.md').write_text(handoff[begin:end])
    changed = git('diff', '--name-only', '48f12dc14099a3630a98eb07e9ec790695a72bfb', HEAD).decode().splitlines()
    assert changed == ['docs/design/MAAP_FABRIC.md'], changed
    summary['after_author_gate_head'] = {'head': '48f12dc14099a3630a98eb07e9ec790695a72bfb',
                                       'changed_paths_to_review_head': changed}
    (out / 'evidence-audit.json').write_text(json.dumps(summary, indent=2) + '\n')
    (out / 'examined-public-blobs.json').write_text(json.dumps(index, indent=2) + '\n')
    print('PASS: builder 48/48, native 5/5; candidate head/tree matched')
    print('PASS: all 53 numbered logs present; no source-bank execution inferred')
    print(f'PASS: resource manifest {len(checked)} published files, zero mismatches')
    print('PASS: only MAAP_FABRIC.md changed after the author source gate head')
    print('PASS: three resource records equal source HEAD; tolerances, floors and ceilings unchanged')

if __name__ == '__main__':
    main()
