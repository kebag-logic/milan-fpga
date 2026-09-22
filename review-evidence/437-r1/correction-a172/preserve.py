"""Compare identical corpus/old-arm inputs under baseline, starting and corrected walks."""
import ast
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent
LANE = Path('$CANDIDATE')
BASE = '88e9276b2a220c716f64a843f7e1eb8f9265e896'
START = '65df1df50a80cd5f540a93d8f0cfabc97da3da75'
sys.dont_write_bytecode = True


def git(*args):
    return subprocess.check_output(['rtk', 'proxy', 'git', *args], cwd=LANE)


def snapshot(label, rev=None):
    dest = OUT / 'snapshots' / label / 'scripts'
    dest.mkdir(parents=True, exist_ok=True)
    paths = list((LANE / 'scripts').glob('gen_toc*.py')) + [LANE / 'scripts/check_em_dash.py']
    for path in paths:
        if rev:
            r = subprocess.run(['rtk', 'proxy', 'git', 'show', rev + ':scripts/' + path.name],
                               cwd=LANE, capture_output=True)
            if r.returncode:
                continue
            data = r.stdout
        else:
            data = path.read_bytes()
        (dest / path.name).write_bytes(data)
    return dest


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def answer(module, name, page):
    return {'blocks': module.blocks(page), 'kinds': module.line_kinds(page),
            'headings': module.headings(page), 'plan': module.plan(page),
            'generated': module.generated_block(page, name), 'owns': module.owns(name, page),
            'refusals': module.refusals(page)}


def tree_pages(rev):
    paths = git('ls-tree', '-r', '--name-only', rev).decode().splitlines()
    return {p: git('show', rev + ':' + p).decode() for p in paths if p.endswith('.md')}


def main():
    paths = {name: snapshot(name, rev) for name, rev in [('baseline', BASE), ('starting', START), ('corrected', None)]}
    walks = {name: load(name, path / 'gen_toc.py') for name, path in paths.items()}
    current = {p: (LANE / p).read_text() for p in git('ls-files', '*.md').decode().splitlines()}
    reports = []
    for population, pages in [('baseline', tree_pages(BASE)), ('starting', tree_pages(START)), ('corrected', current)]:
        dumps = {name: {p: answer(walk, p, text) for p, text in pages.items()} for name, walk in walks.items()}
        diffs = {name: [p for p in pages if dumps[name][p] != dumps['baseline'][p]] for name in walks}
        report = {'population': population, 'pages': len(pages), 'lines': sum(len(p.split('\n')) for p in pages.values()),
                  'differences_vs_baseline': diffs,
                  'digests': {name: hashlib.sha256(json.dumps(d, sort_keys=True).encode()).hexdigest()
                              for name, d in dumps.items()}}
        (OUT / ('corpus-' + population + '.json')).write_text(json.dumps(dumps['corrected'], indent=1) + '\n')
        reports.append(report)
    sys.modules['gen_toc'] = walks['baseline']
    sys.path.insert(0, str(paths['baseline']))
    cases = load('base_cases', paths['baseline'] / 'gen_toc_cases.py')
    closers = load('base_closers', paths['baseline'] / 'gen_toc_closer_cases.py')
    arms = []
    for family in ('walk', 'tag', 'guard', 'heading', 'predecessor', 'provenance', 'refusal'):
        arms += getattr(cases, family + '_arms')()
    arms += closers.closer_arms()
    changed = [name for name, page, _ in arms if isinstance(page, str)
               and answer(walks['baseline'], 'page.md', page) != answer(walks['corrected'], 'page.md', page)]
    unchanged_files = {name: (paths['baseline'] / name).read_bytes() == (paths['corrected'] / name).read_bytes()
                       for name in ('gen_toc_closer_cases.py', 'gen_toc_guards.py')}
    def functions(label, file):
        tree = ast.parse((paths[label] / file).read_text())
        return {n.name: ast.dump(n, include_attributes=False) for n in tree.body
                if isinstance(n, (ast.FunctionDef, ast.ClassDef))}
    policy = {}
    for file, names in [('check_em_dash.py', ['base_labels', 'judge_page']),
                        ('gen_toc.py', ['generated_block', 'refusals', 'owns'])]:
        a, b = functions('baseline', file), functions('corrected', file)
        policy.update({name: a[name] == b[name] for name in names})
    old_probe_rows_unchanged = (functions('starting', 'gen_toc_container_cases.py')['probe_rows'] ==
                                functions('corrected', 'gen_toc_container_cases.py')['probe_rows'])
    summary = {'corpus': reports, 'prior_arm_count': len(arms), 'prior_differences': changed,
               'closer_arms': len(closers.closer_arms()), 'unchanged_files': unchanged_files,
               'unchanged_policy_functions': policy, 'old_I437_probe_rows_unchanged': old_probe_rows_unchanged}
    (OUT / 'preservation.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary, indent=2))
    assert len(arms) == 707 and not changed and all(unchanged_files.values()) and all(policy.values())
    assert old_probe_rows_unchanged and not any(v for r in reports for v in r['differences_vs_baseline'].values())


if __name__ == '__main__':
    main()
