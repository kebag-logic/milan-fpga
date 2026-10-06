#!/usr/bin/env python3
"""Reproduce focused R491-3 checks. Usage: python3 review_checks.py REPO PACKET."""
import ast
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

sys.dont_write_bytecode = True
REPO = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2]).resolve()
SCRATCH = OUT / 'scratch'
HEAD = '0f3d37dbffc4ca3f0e0f69499de80fc256a7db57'
OLD = '5747a8cb99495cb0331658cdd499b9c44e3eda91'
PRE = 'c79c178e7edc427df347787aff6a2cf03adb13ae'
MOVE = 'e8f7d2470159d28a235a44ffd070e38fb57db182'
BASE = 'e617275074e370cec342af99b929e2588fc8d43f'
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1', PYTHONDONTWRITEBYTECODE='1',
           TMPDIR=str(SCRATCH))

def git(*args, cwd=REPO):
    return subprocess.check_output(['git', *args], cwd=cwd, env=env)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def run(name, args, cwd=REPO, expected=0):
    result = subprocess.run(args, cwd=cwd, env=env, capture_output=True)
    (OUT / (name + '.stdout')).write_bytes(result.stdout)
    (OUT / (name + '.stderr')).write_bytes(result.stderr)
    (OUT / (name + '.rc')).write_text(str(result.returncode) + '\n')
    assert result.returncode == expected, (name, result.returncode, expected)
    return {'name': name, 'command': args, 'expected_rc': expected,
            'actual_rc': result.returncode, 'stdout_sha256': sha(result.stdout),
            'stderr_sha256': sha(result.stderr)}

def table(blob):
    tree = ast.parse(blob)
    node = next(n for n in tree.body if isinstance(n, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == 'DUT_READER_DISPOSITIONS'
                        for t in n.targets))
    raw = b''.join(blob.splitlines(keepends=True)[node.lineno-1:node.end_lineno])
    return raw, ast.literal_eval(node.value), node

def clone_at(name, rev):
    dest = SCRATCH / name
    if not dest.exists():
        run(name + '-clone', ['git', 'clone', '--quiet', '--shared', '--no-checkout',
                              str(REPO), str(dest)])
        run(name + '-checkout', ['git', 'checkout', '--quiet', '--detach', rev], dest)
    assert git('rev-parse', 'HEAD', cwd=dest).decode().strip() == rev
    args = ['git', '-c', 'protocol.file.allow=always']
    for sub in ['protocol-processor', 'gptp-processor']:
        run(name+'-configure-'+sub, ['git', 'config', 'submodule.'+sub+'.url', str(REPO/sub)], dest)
    args += ['submodule', 'update', '--init', '--', 'protocol-processor', 'gptp-processor']
    run(name + '-submodules', args, dest)
    return dest

def main():
    assert git('rev-parse', 'HEAD').decode().strip() == HEAD
    (OUT / 'source-diff.patch').write_bytes(git('diff', '--no-ext-diff', '--no-textconv', BASE, HEAD))
    (OUT / 'lane-diff.patch').write_bytes(git('diff', '--no-ext-diff', '--no-textconv', '423ac5d9', HEAD))
    (OUT / 'history.txt').write_bytes(git('log', '--first-parent', '--format=%H %P %s', BASE+'..'+HEAD))
    lane = set(git('diff', '--name-only', '510fae60', OLD).decode().splitlines())
    merge_results = []
    for rev in [PRE, HEAD]:
        parents = git('show', '-s', '--format=%P', rev).decode().split()
        assert len(parents) == 2
        result = subprocess.run(['git', 'merge-tree', '--write-tree', *parents],
                                cwd=REPO, env=env, capture_output=True)
        tree = git('rev-parse', rev+'^{tree}').strip()
        assert result.returncode == 0 and result.stdout.splitlines()[0] == tree
        changed = set(git('diff', '--name-only', parents[0], rev).decode().splitlines())
        overlap = sorted(changed & lane)
        assert overlap == (['scripts/measure_test_evidence.py'] if rev == PRE else [])
        (OUT / ('merge-'+rev[:8]+'.patch')).write_bytes(git('diff', parents[0], rev))
        merge_results.append({'commit': rev, 'parents': parents, 'tree': tree.decode(),
                              'clean_remerge_matches': True, 'lane_path_overlap': overlap})
    before = git('show', PRE+':scripts/measure_test_evidence.py')
    after = git('show', MOVE+':scripts/measure_test_evidence_readers.py')
    braw, btable, _ = table(before)
    araw, atable, _ = table(after)
    assert braw == araw and list(btable.items()) == list(atable.items())
    assert len(ast.parse(after).body) == 2  # docstring + data assignment only
    oldmain = ast.parse(before)
    oldmain.body = [n for n in oldmain.body if not (isinstance(n, ast.Assign)
                  and any(isinstance(t, ast.Name) and t.id == 'DUT_READER_DISPOSITIONS'
                          for t in n.targets))]
    newmain = ast.parse(git('show', MOVE+':scripts/measure_test_evidence.py'))
    newmain.body = [n for n in newmain.body if not (isinstance(n, ast.ImportFrom)
                  and n.module == 'measure_test_evidence_readers')]
    assert ast.dump(oldmain) == ast.dump(newmain)
    budget = git('show', OLD+':scripts/py_idiom.budget')
    for rev in [BASE, PRE, MOVE, HEAD]:
        assert git('show', rev+':scripts/py_idiom.budget') == budget
    info = {'head': HEAD, 'tree': git('rev-parse', 'HEAD^{tree}').decode().strip(),
            'merges': merge_results, 'table_bytes': len(braw), 'table_entries': len(btable),
            'table_sha256_before': sha(braw), 'table_sha256_after': sha(araw),
            'identical_item_order': True, 'remaining_main_ast_identical': True,
            'py_idiom_budget_sha256': sha(budget),
            'line_counts': {'before': len(before.splitlines()),
                            'after': len(git('show', MOVE+':scripts/measure_test_evidence.py').splitlines()),
                            'new_module': len(after.splitlines())}}
    (OUT/'structure.json').write_text(json.dumps(info, indent=2)+'\n')
    cases = [('py-idiom-check', ['python3', 'scripts/check_py_idiom.py']),
             ('py-idiom-selftest', ['python3', 'scripts/check_py_idiom.py', '--selftest']),
             ('ci-scope-selftest', ['python3', 'scripts/ci_scope.py', '--selftest']),
             ('head-default', ['python3', 'scripts/measure_test_evidence.py']),
             ('head-check', ['python3', 'scripts/measure_test_evidence.py', '--check']),
             ('head-selftest', ['python3', 'scripts/measure_test_evidence.py', '--selftest'])]
    with ThreadPoolExecutor(max_workers=6) as pool:
        receipts = list(pool.map(lambda c: run(*c), cases))
    sys.path.insert(0, str(REPO/'scripts'))
    import ci_scope
    import check_py_idiom
    module_path = 'scripts/measure_test_evidence_readers.py'
    assert ci_scope.is_rtl_relevant([module_path])
    counts, sites = check_py_idiom.scan(after.decode(), module_path)
    assert not any(counts.values()), (counts, sites)
    assert module_path in check_py_idiom.sources()
    (OUT/'new-module.json').write_text(json.dumps({'rtl_relevant': True,
         'in_idiom_population': True, 'idiom_counts': counts, 'idiom_sites': sites}, indent=2)+'\n')
    before_dir = clone_at('before', PRE)
    after_dir = clone_at('after', MOVE)
    pairs = [(label, directory, mode) for label, directory in [('before', before_dir), ('after', after_dir)]
             for mode in ['default', 'check', 'selftest']]
    def compare_run(case):
        label, directory, mode = case
        return run(label+'-'+mode, ['python3', 'scripts/measure_test_evidence.py']
                   + ([] if mode == 'default' else ['--'+mode]), directory)
    with ThreadPoolExecutor(max_workers=6) as pool:
        receipts += list(pool.map(compare_run, pairs))
    for mode in ['default', 'check', 'selftest']:
        for suffix in ['stdout', 'stderr', 'rc']:
            raw = (OUT/f'before-{mode}.{suffix}').read_bytes()
            assert raw == (OUT/f'after-{mode}.{suffix}').read_bytes()
            assert raw == (OUT/f'head-{mode}.{suffix}').read_bytes()
    # Sensitivity controls mutate only the disposable extracted module.
    target = after_dir / module_path
    original = target.read_bytes()
    mutation_results = []
    try:
        missing = dict(atable)
        del missing['tb/verilator/milan_dp/dynmap_mutants.py']
        target.write_text('DUT_READER_DISPOSITIONS = '+repr(missing)+'\n')
        mutation_results.append(run('missing-reader', ['python3', 'scripts/measure_test_evidence.py', '--check'], after_dir, 1))
        assert b'tb/verilator/milan_dp/dynmap_mutants.py: UNEXPLAINED' in (OUT/'missing-reader.stdout').read_bytes()
        stale = dict(atable, **{'tb/reviewer_nonexistent_reader.py': 'negative control'})
        target.write_text('DUT_READER_DISPOSITIONS = '+repr(stale)+'\n')
        mutation_results.append(run('stale-reader', ['python3', 'scripts/measure_test_evidence.py', '--check'], after_dir, 1))
        assert b"stale dispositions: ['tb/reviewer_nonexistent_reader.py']" in (OUT/'stale-reader.stdout').read_bytes()
    finally:
        target.write_bytes(original)
    receipts += mutation_results
    (OUT/'commands.json').write_text(json.dumps(receipts, indent=2)+'\n')
    print(json.dumps(info, indent=2))
    print('PASS: all default/check/selftest stdout, stderr and rc bytes equal before, after and final head.')
    print('PASS: exact-head idiom/check and classifier selftests; new module has no idiom violations.')
    print('PASS: missing and stale disposition controls fail for the intended reason.')

if __name__ == '__main__':
    main()
