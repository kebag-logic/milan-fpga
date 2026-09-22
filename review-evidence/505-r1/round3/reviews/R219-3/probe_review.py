#!/usr/bin/env python3
"""Bounded identity, F1/F2/F3 and historical AC5 retention probes."""
import ast
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path('$VALIDATION_STORAGE/reviews/r219-505-r3')
OUT = Path(__file__).resolve().parent
BASE = 'b17580b91deb11f3441dfc5d7f9fafe539d929b8'
FIRST = '6af65a151663e1301f1983a6c9d22650a0b35da9'
PRIOR = 'ad62493186576144f9fa1568babad012bc9ad8ca'
HEAD = '5d45ecc0cf2dc572d538cbc534b5d9f95c8688e7'
POLICY = 'docs/testing/CI_WORKFLOWS.md'

def git(*args):
    return subprocess.check_output(['rtk', 'proxy', 'git', '--no-replace-objects',
                                    *args], cwd=ROOT, text=True)

def load_module(source, name):
    import types
    module = types.ModuleType(name)
    module.__file__ = str(ROOT / 'scripts/ci_events.py')
    sys.modules[name] = module
    exec(compile(source, module.__file__, 'exec'), module.__dict__)
    return module

def tree(rev):
    return dict(line.split('\t', 1)[::-1]
                for line in git('ls-tree', '-r', rev).splitlines())

trees = {rev: tree(rev) for rev in (BASE, FIRST, PRIOR, HEAD)}
assert git('rev-parse', 'HEAD').strip() == HEAD
assert git('rev-parse', HEAD + '^').strip() == PRIOR
assert git('merge-base', BASE, HEAD).strip() == BASE
changed = [path for path in trees[HEAD]
           if trees[HEAD].get(path) != trees[PRIOR].get(path)]
assert set(trees[HEAD]) == set(trees[PRIOR]) and changed == [POLICY]
blob_paths = ['scripts/ci_events.py', 'scripts/act_ci.py', POLICY,
              '.github/workflows/docs.yml', '.github/workflows/elaborate.yml',
              '.github/workflows/rtl.yml', '.github/workflows/rtl-fast.yml']
identity = {'head': HEAD, 'parent': PRIOR, 'merge_base': BASE,
            'tree': git('rev-parse', HEAD + '^{tree}').strip(),
            'changed_since_prior': changed,
            'total_tracked_entries': len(trees[HEAD]),
            'unchanged_non_gitlinks': sum(trees[HEAD][p] == trees[PRIOR][p]
                and not trees[HEAD][p].startswith('160000') for p in trees[HEAD]),
            'gitlinks': {p: x for p, x in trees[HEAD].items() if x.startswith('160000')},
            'blobs': {p: {rev: trees[rev][p] for rev in trees} for p in blob_paths}}
(OUT / 'scope-identity.json').write_text(json.dumps(identity, indent=2) + '\n')

def ast_parts(rev):
    parsed = ast.parse(git('show', f'{rev}:scripts/ci_events.py'))
    result = {}
    for node in parsed.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if node.body and isinstance(node.body[0], ast.Expr) and isinstance(
                    node.body[0].value, ast.Constant) and isinstance(node.body[0].value.value, str):
                node.body.pop(0)
            key = node.name
        else:
            key = ast.dump(node, include_attributes=False).split('=', 1)[0] + ':' + str(len(result))
        result[key] = ast.dump(node, include_attributes=False)
    return result

old_ast, new_ast = ast_parts(FIRST), ast_parts(HEAD)
ast_changes = [name for name in old_ast if old_ast[name] != new_ast.get(name)]
assert ast_changes == ['_carrier_script_edits', '_carrier_script_arms'], ast_changes
assert set(old_ast) == set(new_ast)
(OUT / 'historical-executable-identity.json').write_text(json.dumps({
    'from': FIRST, 'to': HEAD, 'changed_ast_definitions_ignoring_docstrings': ast_changes,
    'unchanged_top_level_nodes': len(old_ast) - len(ast_changes),
    'all_workflows_and_act_runner_unchanged': all(trees[FIRST][p] == trees[HEAD][p]
        for p in blob_paths if p not in ('scripts/ci_events.py', POLICY))}, indent=2) + '\n')

source = git('show', HEAD + ':scripts/ci_events.py')
c = load_module(source, 'r219_ci')
world = c.parse_world(c.read_tree(ROOT))
assert not c.check(world).findings
prior_world = copy.deepcopy(world)
prior_world[c.POLICY] = git('show', PRIOR + ':' + c.POLICY)
prior_arms = c._mutations(prior_world)
head_arms = c._mutations(world)
assert [(a[0], a[2]) for a in prior_arms] == [(a[0], a[2]) for a in head_arms]
assert len(head_arms) == 1046
pop = []
for label, mutate, reason in head_arms:
    mutated = copy.deepcopy(world)
    mutate(mutated)
    # The only changed input is policy prose. Workflow mutation payloads are identical.
    pop.append([label, reason, {p: mutated[p] for p in c.WORKFLOWS}])
serialized = json.dumps(pop).encode()
prior_pop = []
for label, mutate, reason in prior_arms:
    mutated = copy.deepcopy(prior_world)
    mutate(mutated)
    prior_pop.append([label, reason, {p: mutated[p] for p in c.WORKFLOWS}])
assert pop == prior_pop
carrier = list(c._carrier_run_steps(world))
arms407 = c._carrier_script_arms(world)
swallow = [a for a in arms407 if 'or-true' in a[0]]
assert len(carrier) == 56 and len(swallow) == 173
assert sum(len(c.normalize_script(step['run'])) for _, _, _, step in carrier) == 173
arms_record = {'prior': PRIOR, 'head': HEAD, 'workflow_arms': len(head_arms),
               'workflow_mutation_payloads_labels_reasons_equal': True,
               'payload_sha256': hashlib.sha256(serialized).hexdigest(),
               'carrier_bodies': len(carrier), 'normalized_lines': len(swallow),
               'swallow_labels': [a[0] for a in swallow]}
(OUT / 'arm-population.json').write_text(json.dumps(arms_record, indent=2) + '\n')

focused = []
for label, mutate, reason in arms407:
    if ('docs-check step 34 or-true-line-1' in label or
        any(f'docs-check step {n} drop-flag' in label for n in (41, 42, 43))):
        mutant = copy.deepcopy(world)
        mutate(mutant)
        findings = c.check(mutant).findings
        assert any(reason in f for f in findings), (label, findings)
        focused.append({'label': label, 'expected_reason': reason, 'findings': findings})
assert len(focused) == 4
(OUT / 'f1-f2-focused.json').write_text(json.dumps(focused, indent=2) + '\n')

pin_name = 'Print the event and pin the one SHA this run validates'
ss = world[c.RTL_FULL]['jobs']['full-ci-gate']['steps']
pin_index = next(i for i, step in enumerate(ss) if step.get('name') == pin_name)
pin_script = ss[pin_index]['run']
pin_lines = c.normalize_script(pin_script)
assert len(pin_lines) == 8
start = pin_script.index('if [ "$head" != "$GITHUB_SHA" ]; then')
end = pin_script.index('fi\n', start) + len('fi\n')
changes = {'delete-mismatch-assertion': pin_script[:start] + pin_script[end:],
           'replace-exit-1-with-true': pin_script.replace('exit 1', 'true')}
for i in range(len(pin_lines)):
    altered = list(pin_lines)
    altered[i] += ' || true'
    changes[f'swallow-normalized-line-{i + 1}'] = '\n'.join(altered)
gap_results = []
for label, altered in changes.items():
    mutant = copy.deepcopy(world)
    mutant[c.RTL_FULL]['jobs']['full-ci-gate']['steps'][pin_index]['run'] = altered
    result = c.check(mutant)
    assert not result.findings, (label, result.findings)
    gap_results.append({'label': label, 'script': altered, 'checked': result.checked,
                        'findings': result.findings})
(OUT / 'f3-disclosed-gap.json').write_text(json.dumps(gap_results, indent=2) + '\n')

# Only execute the checker in a minimal external scratch root; no workflow runs.
with tempfile.TemporaryDirectory(prefix='r219-3-ac5-') as name:
    scratch = Path(name)
    cli_results = []
    for rev in (FIRST, PRIOR, HEAD):
        root = scratch / rev
        for path in (*c.FILES, 'scripts/ci_events.py'):
            dest = root / path
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(git('show', rev + ':' + path))
        docs = root / c.DOCS
        text = docs.read_text()
        needle = '          python3 scripts/check_py_idiom.py\n'
        assert text.count(needle) == 1
        docs.write_text(text.replace(needle, needle.rstrip('\n') + ' || true\n'))
        argv = ['rtk', 'proxy', 'python3', '-B', 'scripts/ci_events.py', '--check']
        p = subprocess.run(argv, cwd=root, text=True, capture_output=True)
        assert p.returncode == 1
        assert 'job `docs-check` step 34 (`Python idiom gate`)' in p.stdout
        assert "line 1 must be 'python3 scripts/check_py_idiom.py'" in p.stdout
        cli_results.append({'head': rev, 'argv': argv,
                            'scratch_recipe': 'copy FILES and checker from this revision; append || true to the Python idiom call',
                            'exit': p.returncode, 'stdout': p.stdout, 'stderr': p.stderr})
    assert len({r['stdout'] for r in cli_results}) == 1
(OUT / 'ac5-native-diagnostic-comparison.json').write_text(json.dumps(cli_results, indent=2) + '\n')
print(json.dumps({'identity': identity['changed_since_prior'],
                  'unchanged_non_gitlinks': identity['unchanged_non_gitlinks'],
                  'historical_ast_changes': ast_changes,
                  'workflow_arms': len(head_arms), 'swallow_arms': len(swallow),
                  'focused_prior_finding_controls': len(focused),
                  'disclosed_gap_controls_accepted': len(gap_results),
                  'AC5_native_diagnostics_equal_at_three_heads': True}, indent=2))
