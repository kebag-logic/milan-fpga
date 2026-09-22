"""Actual CLI checks and source-mutant controls in disposable external fixtures."""
import json
import pathlib
import re
import subprocess
import sys
import tempfile
import time

OUT = pathlib.Path(__file__).resolve().parent
ROOT = pathlib.Path.cwd()
REC = OUT / 'receipts'
SRC = (ROOT/'scripts/ci_events.py').read_text()
OLD = '6af65a151663e1301f1983a6c9d22650a0b35da9'
BASE = 'b17580b91deb11f3441dfc5d7f9fafe539d929b8'
results = (json.loads((REC/'cli-results.json').read_text())
           if '--mutants-only' in sys.argv else [])

def run(label, args, expected):
    previous = next((r for r in results if r['label'] == label), None)
    if previous is not None:
        assert previous['exit_code'] == expected
        return (REC/f'{label}.log').read_text()
    start = time.monotonic()
    p = subprocess.run(args, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                       text=True, timeout=120)
    (REC/f'{label}.log').write_text(p.stdout)
    results.append({'label':label,'argv':list(map(str,args)),'exit_code':p.returncode,
        'expected':expected,'seconds':round(time.monotonic()-start,3),
        'failures':len(re.findall(r'^  FAIL ',p.stdout,re.M)),
        'tail':p.stdout.splitlines()[-3:]})
    (REC/'cli-results.json').write_text(json.dumps(results,indent=2)+'\n')
    assert p.returncode == expected, (label,p.returncode,p.stdout[-1800:])
    print(f'{label}: exit {p.returncode}; {p.stdout.splitlines()[-1] if p.stdout else "(empty)"}',flush=True)
    return p.stdout

for label,args in (
    ('pristine-check',['scripts/ci_events.py','--check']),
    ('pristine-selftest',['scripts/ci_events.py','--selftest']),
    ('docs-check',['scripts/docs_check.py']),
    ('toc-check',['scripts/gen_toc.py','--check']),
    ('doc-paths',['scripts/check_doc_paths.py']),
    ('em-dash',['scripts/check_em_dash.py','--base',BASE]),
    ('python-idiom',['scripts/check_py_idiom.py']),
):
    if '--mutants-only' not in sys.argv:
        expected = 2 if label == 'python-idiom' else 0
        run(label,['python3','-B',*args],expected)

needle = 'c.item(tuple(lines) == canonical, path,'
variants = {
    'M5b': "c.item(len(lines) == len(canonical) and all((re.sub(r' \\|\\| true$', '', a) == re.sub(r' \\|\\| true$', '', b)) if i < len(lines) - 1 else a == b for i, (a, b) in enumerate(zip(lines, canonical))), path,",
    'prefix': 'c.item(tuple(lines[:len(canonical)]) == canonical, path,',
    'unordered': 'c.item(sorted(lines) == sorted(canonical), path,',
    'comparison-removed': 'c.item(True, path,',
}
def change_function(src, replacement, target=needle):
    before, chunk = src.split('def check_carrier_script(',1)
    chunk, after = chunk.split('\n\ndef check_carrier_steps(',1)
    assert chunk.count(target) == 1
    return before+'def check_carrier_script('+chunk.replace(target,replacement)+'\n\ndef check_carrier_steps('+after

with tempfile.TemporaryDirectory(prefix='r219-505-r2-') as tmp:
    scratch = pathlib.Path(tmp)
    (REC/'mutant-patches').mkdir(exist_ok=True)
    for label,replacement in variants.items():
        src = change_function(SRC,replacement)
        path = scratch/f'{label}.py'
        path.write_text(src)
        (REC/'mutant-patches'/f'{label}.txt').write_text(needle+'\n=>\n'+replacement+'\n')
        run(f'{label}-check',['python3','-B',str(path),'--root',str(ROOT),'--check'],0)
        output = run(f'{label}-selftest',['python3','-B',str(path),'--root',str(ROOT),'--selftest'],1)
        if label == 'M5b':
            assert 'FAIL mutation not caught: [carrier-script-407 docs-check step 34 or-true-line-1]' in output
    # Remove only the diagnostic for a missing record, preserving its early return.
    needle_record = 'c.item(recorded, path,'
    missing = scratch/'record-enforcement-removed.py'
    missing.write_text(change_function(SRC,'c.item(True, path,',needle_record))
    (REC/'mutant-patches/record-enforcement-removed.txt').write_text(needle_record+'\n=>\nc.item(True, path,\n')
    run('record-enforcement-removed-check',['python3','-B',str(missing),'--root',str(ROOT),'--check'],0)
    run('record-enforcement-removed-selftest',['python3','-B',str(missing),'--root',str(ROOT),'--selftest'],1)

    # Copy only inputs; no live checkout byte is changed.
    fixture = scratch/'inputs'
    paths = [str(p.relative_to(ROOT)) for p in (ROOT/'.github/workflows').iterdir() if p.suffix in ('.yml','.yaml')]
    paths += ['docs/testing/CI_WORKFLOWS.md']
    for rel in paths:
        target = fixture/rel
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes((ROOT/rel).read_bytes())
    docs = fixture/'.github/workflows/docs.yml'
    original = docs.read_text()
    command = 'python3 scripts/check_py_idiom.py\n'
    assert original.count(command) == 1
    docs.write_text(original.replace(command,'python3 scripts/check_py_idiom.py || true\n'))
    refusal = run('native-ac5-head',['python3','-B',str(ROOT/'scripts/ci_events.py'),'--root',str(fixture),'--check'],1)
    assert 'step 34 (`Python idiom gate`) script is not the canonical form: line 1' in refusal
    base = scratch/'base.py'
    base.write_bytes(subprocess.check_output(['git','show',f'{BASE}:scripts/ci_events.py']))
    run('native-ac5-base',['python3','-B',str(base),'--root',str(fixture),'--check'],0)
    run('native-ac5-M5b',['python3','-B',str(scratch/'M5b.py'),'--root',str(fixture),'--check'],0)

    # Reproduce the old self-test's sensitivity hole using the old source and policy.
    old_source = subprocess.check_output(['git','show',f'{OLD}:scripts/ci_events.py']).decode()
    docs.write_text(original)
    (fixture/'docs/testing/CI_WORKFLOWS.md').write_bytes(subprocess.check_output(['git','show',f'{OLD}:docs/testing/CI_WORKFLOWS.md']))
    old_mutant = scratch/'old-M5b.py'
    old_mutant.write_text(change_function(old_source,variants['M5b']))
    run('old-M5b-selftest',['python3','-B',str(old_mutant),'--root',str(fixture),'--selftest'],0)

    # Full CLI maintenance proof: workflow edit alone refuses; matching constant passes.
    (fixture/'docs/testing/CI_WORKFLOWS.md').write_bytes((ROOT/'docs/testing/CI_WORKFLOWS.md').read_bytes())
    docs.write_text(original.replace('python3 scripts/check_py_idiom.py --selftest\n',
                                   'python3 scripts/check_py_idiom.py --selftest\n          echo reviewed\n'))
    run('maintenance-workflow-only',['python3','-B',str(ROOT/'scripts/ci_events.py'),'--root',str(fixture),'--check'],1)
    record_line = "             'python3 scripts/check_py_idiom.py --selftest',\n"
    assert SRC.count(record_line) == 1
    maint = scratch/'maintenance.py'
    maint.write_text(SRC.replace(record_line,record_line+"             'echo reviewed',\n"))
    run('maintenance-matching-check',['python3','-B',str(maint),'--root',str(fixture),'--check'],0)
    run('maintenance-matching-selftest',['python3','-B',str(maint),'--root',str(fixture),'--selftest'],0)

print('All actual CLI probes completed.',flush=True)
