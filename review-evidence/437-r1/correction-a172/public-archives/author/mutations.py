#!/usr/bin/env python3
"""Bounded exact-text mutants in disposable copies, never the checkout."""
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from receipt import HERE, identity

MUTANTS = [
    ("drop-context", 'after = _paragraph_after(line, label, para, prev)',
     'after = _paragraph_after(line, label, para, prev)\n    return after, None'),
    ("forget-on-blank", 'return after, None if context and context[1] else context', 'return after, None'),
    ("blanket-indent", '_indent_columns(line) >= context[0]', '_indent_columns(line) >= 1'),
    ("strict-column", '_indent_columns(line) >= context[0]', '_indent_columns(line) > context[0]'),
    ("fixed-column", 'column = len(prefix.expandtabs(4))', 'column = 2'),
    ("characters-not-columns", 'column = len(prefix.expandtabs(4))', 'column = len(prefix)'),
    ("no-code-padding", 'or column - marker_end > 4', 'or False'),
    ("four-is-code-padding", 'column - marker_end > 4', 'column - marker_end >= 4'),
    ("empty-never-ends", 'return after, None if context and context[1] else context', 'return after, context'),
    ("empty-stays-empty", '(context[0], False)', 'context'),
    ("empty-uses-padding", 'if not item.group(2) or column - marker_end > 4:', 'if column - marker_end > 4:'),
    ("lose-outer-column", 'if context and _indent_columns(line) >= context[0]:',
     'if context and _indent_columns(line) >= context[0] and not LIST_ITEM_RE.match(line):'),
    ("stale-sibling-column", 'return after, (column, not bool(item.group(2)))',
     'return after, context or (column, not bool(item.group(2)))'),
    ("stale-context", '    return after, None\n\n\ndef _comment_after',
     '    return after, context\n\n\ndef _comment_after'),
    ("no-lazy-hold", 'if para == HELD and after == HELD:', 'if False:'),
    ("markers-in-blocks", 'LIST_ITEM_RE.match(line) if label == TEXT and after == HELD else None',
     'LIST_ITEM_RE.match(line)'),
    ("no-ordinal-interruption-check", 'LIST_ITEM_RE.match(line) if label == TEXT and after == HELD else None',
     'LIST_ITEM_RE.match(line) if label == TEXT else None'),
]


def main():
    source = Path('scripts/gen_toc.py').read_text()
    before = hashlib.sha256(source.encode()).hexdigest()
    stamp = sys.argv[1]
    destination = HERE / f'mutations-{stamp}'
    destination.mkdir(exist_ok=True)
    results = []
    with tempfile.TemporaryDirectory(prefix='copies-', dir=destination) as tmp:
        root = Path(tmp)
        scripts = root / 'scripts'
        scripts.mkdir()
        for name in ('gen_toc.py', 'gen_toc_cases.py', 'gen_toc_guards.py',
                     'gen_toc_closer_cases.py', 'gen_toc_container_cases.py', 'check_em_dash.py'):
            shutil.copyfile(Path('scripts', name), scripts / name)
        for name, old, new in MUTANTS:
            assert source.count(old) == 1, (name, source.count(old))
            (scripts / 'gen_toc.py').write_text(source.replace(old, new))
            row = {'mutant': name, 'replace': old, 'with': new, 'checks': []}
            for gate in ('gen_toc.py', 'check_em_dash.py'):
                args = ['rtk', 'proxy', 'python3', '-B', str(scripts / gate), '--selftest']
                result = subprocess.run(args, text=True, capture_output=True, timeout=45)
                output = result.stdout + result.stderr
                (destination / f'{name}-{gate}.log').write_text(output)
                failing = [line for line in output.splitlines() if 'I437' in line]
                row['checks'].append({'gate': gate, 'command': args, 'exit': result.returncode,
                                      'named_failures': failing})
            assert all(x['exit'] != 0 and x['named_failures'] for x in row['checks']), row
            results.append(row)
            print(name, [(x['gate'], x['exit'], len(x['named_failures'])) for x in row['checks']], flush=True)
    assert hashlib.sha256(Path('scripts/gen_toc.py').read_bytes()).hexdigest() == before
    report = {**identity(), 'source_sha256': before, 'results': results}
    (HERE / f'mutations-{stamp}.json').write_text(json.dumps(report, indent=2) + '\n')
    print(f'PASS: {len(results)} mutants killed by both shipped selftests; checkout bytes unchanged')


if __name__ == '__main__':
    main()
