"""R219-2 focused review probes. Only output/scratch and in-memory objects mutate."""
import ast
import collections
import contextlib
import copy
import hashlib
import io
import json
import pathlib
import re
import subprocess
import sys
import tempfile
import types

OUT = pathlib.Path(__file__).resolve().parent
ROOT = pathlib.Path.cwd()
BASE = 'b17580b91deb11f3441dfc5d7f9fafe539d929b8'
OLD = '6af65a151663e1301f1983a6c9d22650a0b35da9'
HEAD = 'ad62493186576144f9fa1568babad012bc9ad8ca'
REC = OUT / 'receipts'
SOURCE = ROOT / 'scripts/ci_events.py'

def save(name, value):
    (REC / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + '\n')

def git(*args):
    return subprocess.check_output(['git', '--no-replace-objects', *args])

def module(source, name):
    m = types.ModuleType(name)
    m.__file__ = str(SOURCE)
    sys.modules[name] = m
    exec(compile(source, str(SOURCE), 'exec'), m.__dict__)
    return m

def norm(text):
    # Independently implement the documented space/tab/LF/continuation contract.
    assert all(c in ' \t\n' or c.isprintable() for c in text)
    return [s for line in text.replace('\\\n', '').split('\n')
            if (s := re.sub('[ \t]+', ' ', line).strip(' \t'))]

assert git('rev-parse', 'HEAD').decode().strip() == HEAD
assert not git('status', '--porcelain=v1')
source = SOURCE.read_text()
old_source = git('show', f'{OLD}:scripts/ci_events.py').decode()
base_source = git('show', f'{BASE}:scripts/ci_events.py').decode()
m = module(source, 'r219_head')
old = module(old_source, 'r219_old')
base = module(base_source, 'r219_base')
world = m.parse_world(m.read_tree(ROOT))
assert not m.check(world).findings

def ast_facts(text):
    tree = ast.parse(text)
    funcs = {}
    globals_ = []
    for n in tree.body:
        if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
            n = copy.deepcopy(n)
            for f in ast.walk(n):
                if isinstance(f, (ast.FunctionDef, ast.ClassDef)) and f.body and isinstance(f.body[0], ast.Expr) and isinstance(f.body[0].value, ast.Constant) and isinstance(f.body[0].value.value, str):
                    f.body = f.body[1:]
            funcs[n.name] = ast.dump(n, include_attributes=False)
        elif isinstance(n, (ast.Assign, ast.AnnAssign, ast.Import, ast.ImportFrom)):
            globals_.append(ast.dump(n, include_attributes=False))
    return funcs, globals_

new_f, new_g = ast_facts(source)
old_f, old_g = ast_facts(old_source)
base_f, _ = ast_facts(base_source)
changed = [n for n in old_f if old_f[n] != new_f[n]]
assert changed == ['_carrier_script_edits', '_carrier_script_arms'], changed
assert old_g == new_g
assert old.CARRIER_STEP_LISTS == m.CARRIER_STEP_LISTS
workflow_blobs = {}
for path in m.WORKFLOWS:
    ids = {rev: git('rev-parse', f'{rev}:{path}').decode().strip() for rev in (BASE, OLD, HEAD)}
    assert len(set(ids.values())) == 1
    workflow_blobs[path] = ids
base_changed = [n for n in base_f if base_f[n] != new_f[n]]
assert base_changed == ['check_carrier_steps', '_mutations', '_selftest_whitespace', 'selftest']
assert {k: tuple({a: b for a,b in v.items() if a != 'run'} for v in seq)
        for k, seq in m.CARRIER_STEP_LISTS.items()} == base.CARRIER_STEP_LISTS
save('source-preservation.json', {
    'revision_changed_functions_excluding_docstrings': changed,
    'revision_unchanged_functions_classes': len(old_f) - len(changed),
    'revision_all_top_level_assignments_and_imports_ast_equal': old_g == new_g,
    'base_existing_functions_changed': base_changed,
    'base_existing_unchanged': len(base_f) - len(base_changed),
    'carrier_records_equal_old': True,
    'workflow_blobs': workflow_blobs,
    'diff_names': git('diff', '--name-only', BASE, HEAD).decode().splitlines(),
    'old_policy_current_checker_findings': m.check(dict(world, **{m.POLICY: git('show', f'{OLD}:{m.POLICY}').decode()})).findings,
})

old_arms = old._mutations(world)
base_arms = base._mutations(world)
new_arms = m._mutations(world)
by_name = {n: (fn, want) for n, fn, want in new_arms}
assert len(by_name) == len(new_arms)
for name, fn, want in old_arms:
    nfn, nwant = by_name[name]
    a, b = copy.deepcopy(world), copy.deepcopy(world)
    fn(a)
    nfn(b)
    assert a == b and want == nwant, name
orig_checker = m.check_carrier_script
m.check_carrier_script = lambda *args: None
for name, fn, want in base_arms:
    w = copy.deepcopy(world)
    fn(w)
    assert any(want in f for f in m.check(w).findings), name
m.check_carrier_script = orig_checker

inventory, probes, check_calls = [], [], []
run_count = collections.Counter()
line_count = 0
carrier_arms = m._carrier_script_arms(world)
carrier_by_name = {name:(fn,want) for name,fn,want in carrier_arms}
for path,jid in ((m.DOCS,'docs-check'),(m.DOCS,'wire-accountability'),
                 (m.DOCS,'docs-check-no-git'),(m.ELABORATE,'elaborate')):
    for at, step in enumerate(world[path]['jobs'][jid]['steps']):
        if 'run' not in step:
            continue
        lines = norm(step['run'])
        record = m.CARRIER_STEP_LISTS[(path,jid)][at]
        assert tuple(lines) == record['run']
        run_count[jid] += 1
        inventory.append({'path':path,'job':jid,'step':at+1,'name':step['name'],'lines':lines})
        what = f"job `{jid}` step {at+1} (`{step['name']}`)"
        for n,line in enumerate(lines):
            line_count += 1
            w = copy.deepcopy(world)
            edited = list(lines)
            edited[n] += ' || true'
            w[path]['jobs'][jid]['steps'][at]['run'] = '\n'.join(edited)
            findings = m.check(w).findings
            want = f'{what} script is not the canonical form: line {n+1} must be {line!r}'
            assert any(want in f for f in findings), (what,n,findings)
            label = f'carrier-script-407 {jid} step {at+1} ' + ('or-true' if n == len(lines)-1 else f'or-true-line-{n+1}')
            fn, reason = carrier_by_name[label]
            actual = copy.deepcopy(world)
            fn(actual)
            assert actual == w and reason == want, label
            probes.append({'label':label,'expected':want,'findings':findings})
            if re.search(r' --check(?: |$)',line):
                check_calls.append({'job':jid,'step':at+1,'name':step['name'],'line':n+1,'call':line,'arm':label})
        for invalid in ('', 'true', '\n'.join(lines)+'\necho extra', '\n# comment\n'+step['run'], None, [], 4):
            w = copy.deepcopy(world)
            w[path]['jobs'][jid]['steps'][at]['run'] = invalid
            assert m.check(w).findings, (what, invalid)
        for bad in (None, (), [], 'true', (1,), ('true',)):
            key = (path,jid)
            saved = m.STEP_LISTS[key]
            spec = copy.deepcopy(saved)
            spec[at]['run'] = bad
            m.STEP_LISTS[key] = spec
            try:
                assert any(what in f for f in m.check(world).findings), (what,bad)
            finally:
                m.STEP_LISTS[key] = saved
        for char in ('\u00a0', '\u2028', '\r', '\x00'):
            w = copy.deepcopy(world)
            w[path]['jobs'][jid]['steps'][at]['run'] = char + step['run']
            assert any(what in f for f in m.check(w).findings), (what,char)

assert sum(run_count.values()) == 56 and line_count == 173
assert len(carrier_arms) == 456
for name,fn,want in carrier_arms:
    w = copy.deepcopy(world)
    fn(w)
    assert any(want in f for f in m.check(w).findings), name
    assert want

# Run the retained positive and missing-record controls without trusting output alone.
with contextlib.redirect_stdout(io.StringIO()) as buf:
    problems, nrecord = m._selftest_carrier_script_pins(world)
    assert not problems
    problems, nwhite = m._selftest_whitespace(world)
    assert not problems
(REC/'positive-controls.log').write_text(buf.getvalue())
save('inventory.json', inventory)
save('line-swallowing.json', probes)
save('check-calls.json', check_calls)
save('mutation-population.json', {'carrier_counts':dict(run_count), 'lines':line_count,
    'prior_mutations_retained_same_edits_and_reasons':len(old_arms),
    'base_specialized_arms_pass_with_new_helper_disabled':len(base_arms),
    'current_workflow_arms':len(new_arms),'carrier_arms':len(carrier_arms),
    'carrier_levers':dict(collections.Counter(n.split(' ',4)[4].split('-line-')[0] for n,_,_ in carrier_arms)),
    'missing_record_plus_maintenance':nrecord,'whitespace_controls':nwhite})
print(json.dumps({'bodies':dict(run_count),'lines':line_count,
    'old_controls_retained':len(old_arms),'specialized_controls_retained':len(base_arms),
    'workflow_mutations':len(new_arms),'carrier_mutations':len(carrier_arms),
    'revision_executable_changes':changed},indent=2))
