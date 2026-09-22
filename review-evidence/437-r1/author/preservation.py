#!/usr/bin/env python3
"""Prove prior arm data, #507 controls, policy functions, and tree scope."""
import ast
import hashlib
import json
import sys
from pathlib import Path
from receipt import HERE, BASE, command, identity, parser


def functions(source):
    return {node.name: ast.dump(node, include_attributes=False)
            for node in ast.parse(source).body if isinstance(node, ast.FunctionDef)}


def main():
    old = functions((HERE / 'base-scripts/gen_toc_cases.py').read_text())
    new = functions(Path('scripts/gen_toc_cases.py').read_text())
    changed = [name for name in old if old[name] != new.get(name)]
    assert changed == ['guard_arms', '_class_guard_arms'] and set(old) == set(new), changed
    closer = Path('scripts/gen_toc_closer_cases.py').read_bytes()
    assert (HERE / 'base-scripts/gen_toc_closer_cases.py').read_bytes() == closer
    old = functions((HERE / 'base-scripts/check_em_dash.py').read_text())
    new = functions(Path('scripts/check_em_dash.py').read_text())
    assert [name for name in old if old[name] != new.get(name)] == ['selftest']
    sys.path.insert(0, str(Path.cwd() / 'scripts'))
    import gen_toc as current
    import gen_toc_cases as cases
    import gen_toc_closer_cases as closers
    baseline = parser(HERE / 'base-scripts/gen_toc.py')
    arms = sum((getattr(cases, name + '_arms')() for name in
                ('walk', 'tag', 'guard', 'heading', 'predecessor', 'provenance', 'refusal')), [])
    arms += closers.closer_arms()
    assert len(arms) == 707
    differences = []
    for name, page, _ in arms:
        for method in ('blocks', 'headings', 'generated_block', 'refusals'):
            if getattr(current, method)(page) != getattr(baseline, method)(page):
                differences.append((name, method))
    assert not differences, differences
    paths = command(['git', 'diff', '--name-only', BASE, 'HEAD']).stdout.splitlines()
    assert paths == ['CONTRIBUTING.md', 'scripts/check_em_dash.py', 'scripts/gen_toc.py',
                     'scripts/gen_toc_cases.py', 'scripts/gen_toc_container_cases.py'], paths
    submodules = command(['git', 'submodule', 'status']).stdout
    assert submodules == (HERE / 'submodules-base.txt').read_text()
    report = {**identity(), 'prior_arms': len(arms), 'classification_differences': differences,
              'expanded_guard_functions': changed,
              'guard_name_update': 'eight families -> nine families',
              'closer_module_sha256': hashlib.sha256(closer).hexdigest(),
              'gate_changed_functions': ['selftest'], 'changed_files': paths,
              'submodules_identical': submodules}
    (HERE / 'preservation-head.json').write_text(json.dumps(report, indent=2) + '\n')
    print('PASS: all 707 prior arm inputs classify identically; #507 module byte-identical; '
          'policy functions unchanged; exactly five scoped files; public submodules preserved')


if __name__ == '__main__':
    main()
