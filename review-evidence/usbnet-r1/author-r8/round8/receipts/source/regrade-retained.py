"""Regrade only the complete retained census; never invoke a native model."""
import concurrent.futures
import contextlib
import hashlib
import json
import multiprocessing
import os
from pathlib import Path
import shutil
import sys
import time

ROOT = Path.cwd()
OLD = Path('$MANAGEMENT/2026-09-23/usbnet-a855/round7/receipts')
OUT = OLD.parent.parent / 'round8/receipts'
BUILDS = Path('$VALIDATION_STORAGE/usbnet-a855/round7/census')
RESULTS = Path('$VALIDATION_STORAGE/usbnet-a855/round8/census')
sys.path.insert(0, str(ROOT / 'tb/verilator/ctrl_service_budget'))
import build
import run

original = run.graded
expected_grades = json.loads((OLD / 'pre-parallel-grade-hashes.json').read_text())

def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()

def one(job):
    group, log, spec, out = job
    result = original([group], [log], spec, out)
    key = out.parent.name + '/' + group.name
    digest = sha(out / (group.name + '.json'))
    assert digest == expected_grades[key], ('a measured grade changed', key)
    print('REGRADED', key, digest, flush=True)
    return result

def parallel(groups, logs, spec, out):
    assert len({g.name for g in groups}) == len(groups)
    with concurrent.futures.ProcessPoolExecutor(max_workers=4,
            mp_context=multiprocessing.get_context('fork')) as pool:
        parts = list(pool.map(one, [(g, log, spec, out) for g, log in zip(groups, logs)]))
    return tuple([item for part in parts for item in part[i]] for i in range(3))

def main():
    manifest = json.loads((OLD / 'census/manifest.json').read_text())
    archive = json.loads((OLD / 'census/ARCHIVE.json').read_text())['cases']
    completed = json.loads((OLD / 'census/completed.json').read_text())
    expected = {(v, g) for v, gs in manifest['groups'].items() for g in gs}
    assert len(expected) == 159 and len(manifest['groups']) == 8
    assert {tuple(r['case'].split('/', 1)) for r in archive} == expected
    records = {(r['variant'], r['group']): r for r in completed}
    assert set(records) == expected and all(r['native_status'] == 0 for r in completed)
    traces = []
    for entry in archive:
        variant, group = entry['case'].split('/', 1)
        src = BUILDS / variant / 'results'
        dest = RESULTS / variant / 'results'
        dest.mkdir(parents=True, exist_ok=True)
        log = src / (group + '.log')
        digest = sha(log)
        assert digest == entry['raw_sha256'] == records[variant, group]['trace_sha256']
        assert log.stat().st_size == entry['raw_bytes']
        link = dest / log.name
        if not link.exists():
            link.symlink_to(log)
        assert link.resolve() == log.resolve()
        for suffix in ('.txt', '.status'):
            source = src / (group + suffix)
            assert source.read_bytes() == (OLD / 'census' / variant / 'results' / source.name).read_bytes()
            shutil.copyfile(source, dest / source.name)
        traces.append(dict(case=entry['case'], sha256=digest, raw_bytes=entry['raw_bytes']))
    for variant in manifest['groups']:
        shutil.copyfile(BUILDS / variant / 'build.json', RESULTS / variant / 'build.json')
        for journal in (BUILDS / variant / 'results').glob('*journal*'):
            if journal.is_file():
                shutil.copyfile(journal, RESULTS / variant / 'results' / journal.name)
    (OUT / 'retained-trace-identity.json').write_text(json.dumps(traces, indent=2) + '\n')
    run.graded = parallel
    commands = []
    for variant, groups in manifest['groups'].items():
        argv = ['--point', 'arty-1x1', '--build-dir', str(BUILDS / variant), '--variant', variant,
                '--out', str(RESULTS / variant / 'results'), '--regrade', '--record-budget-findings']
        if variant == 'answering-ports':
            argv += ['--groups', ','.join(groups)]
        sys.argv = [str(ROOT / 'tb/verilator/ctrl_service_budget/run.py'), *argv]
        started = time.monotonic()
        with (OUT / ('regrade-' + variant + '.log')).open('w') as stream:
            with contextlib.redirect_stdout(stream), contextlib.redirect_stderr(stream):
                rc = run.main()
        commands.append(dict(command=sys.argv, returncode=rc, seconds=time.monotonic() - started))
        (OUT / 'regrade-commands.json').write_text(json.dumps(commands, indent=2) + '\n')
        print('VARIANT', variant, 'rc', rc, 'seconds', commands[-1]['seconds'], flush=True)
        assert rc == 0, ('regrade refused', variant)
    identity = []
    for variant, group in sorted(expected):
        path = RESULTS / variant / 'results' / (group + '.json')
        digest = sha(path)
        assert digest == expected_grades[variant + '/' + group]
        identity.append(dict(case=variant + '/' + group, grade_sha256=digest))
    (OUT / 'regraded-identity.json').write_text(json.dumps(identity, indent=2) + '\n')
    print('PASS: 159 retained traces regraded; all grades identical; eight variants; no native execution', flush=True)

if __name__ == '__main__':
    main()
