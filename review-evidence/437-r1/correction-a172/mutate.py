"""Isolated exact mutants; require named failing arms in both consumers."""
import concurrent.futures
import ast
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent
LANE = Path('$CANDIDATE')


def main():
    source = (LANE / 'scripts/gen_toc.py').read_text()
    opening = ('            if para == HELD and item_context and not item_context[1] \\\n'
               '                    and _indent_columns(line) >= item_context[0]:\n'
               '                opening_para = PARAGRAPH\n')
    mutants = [
        ('tag-paragraph-reversion', opening, '', ['R238 C01', 'R238 C04', 'R238 P01', 'R238 P04']),
        ('tag-column-too-narrow', '_indent_columns(line) >= item_context[0]',
         '_indent_columns(line) > item_context[0]', ['resumed tag column 2 open', 'first tag column 2 open then fence']),
        ('tag-column-ignored', '_indent_columns(line) >= item_context[0]',
         'True', ['resumed tag column 1 open', 'first tag column 1 open']),
        ('quote-release-removed',
         '    if BLOCK_QUOTE_RE.match(line) or FOOTNOTE_DEFINITION_RE.match(line):\n        return after, None\n',
         '    if FOOTNOTE_DEFINITION_RE.match(line):\n        return after, None\n', ['R238 D01', 'R238 D03']),
        ('footnote-release-removed',
         '    if BLOCK_QUOTE_RE.match(line) or FOOTNOTE_DEFINITION_RE.match(line):\n        return after, None\n',
         '    if BLOCK_QUOTE_RE.match(line):\n        return after, None\n', ['R238 D02', 'R238 D04']),
        ('block-marker-only', 'label == TEXT and after == HELD', 'label != TEXT or after == HELD',
         ['R237 fenced-marker-indented-closer', 'R237 comment-marker-indented-closer', 'R237 HTML-marker-indented-closer']),
    ]
    original_tree = ast.parse((OUT / 'public-archives/author/mutations.py').read_text())
    original_mutants = ast.literal_eval(next(n.value for n in original_tree.body
                                            if isinstance(n, ast.Assign)
                                            and any(isinstance(t, ast.Name) and t.id == 'MUTANTS' for t in n.targets)))
    attribution = {
        'drop-context': ['two spaces'], 'forget-on-blank': ['two spaces'],
        'blanket-indent': ['one space outside item'], 'strict-column': ['two spaces'],
        'fixed-column': ['ordered outside'], 'characters-not-columns': ['tab padding columns'],
        'no-code-padding': ['code padding uses one'], 'four-is-code-padding': ['four padding columns'],
        'empty-never-ends': ['empty item ends at blank'], 'empty-stays-empty': ['empty item gains content'],
        'empty-uses-padding': ['empty item ignores padding'],
        'lose-outer-column': ['nested item retains outer column'],
        'stale-sibling-column': ['sibling replaces column'],
        'stale-context': ['fresh dedented paragraph ends item'], 'no-lazy-hold': ['lazy line retains item'],
        'markers-in-blocks': ['R237 fenced-marker-indented-closer', 'R237 comment-marker-indented-closer',
                              'R237 HTML-marker-indented-closer'],
        'no-ordinal-interruption-check': ['noninterrupting ordinal is no item'],
    }
    mutants += [('prior-' + name, before, after, attribution[name]) for name, before, after in original_mutants]
    originals = {p: p.read_bytes() for p in (LANE / 'scripts').glob('gen_toc*.py')}
    originals[LANE / 'scripts/check_em_dash.py'] = (LANE / 'scripts/check_em_dash.py').read_bytes()
    def one(mutant):
        name, before, after, required = mutant
        assert source.count(before) == 1, (name, source.count(before))
        dest = OUT / 'mutants' / name
        dest.mkdir(parents=True, exist_ok=True)
        for path, data in originals.items():
            (dest / path.name).write_bytes(data)
        altered = source.replace(before, after)
        (dest / 'gen_toc.py').write_text(altered)
        receipts = []
        for script in ('gen_toc.py', 'check_em_dash.py'):
            argv = ['rtk', 'proxy', 'python3', '-B', str(dest / script), '--selftest']
            r = subprocess.run(argv, cwd=LANE, capture_output=True, text=True)
            log = r.stdout + r.stderr
            (dest / (script + '.log')).write_text(log)
            named = {arm: any(arm in line and ('[I437' in line or 'FAIL' in line) for line in log.splitlines())
                     for arm in required}
            receipts.append({'argv': argv, 'exit': r.returncode, 'required_arm_failures': named,
                             'all_failing_lines': [line for line in log.splitlines() if '[I437' in line]})
            assert r.returncode != 0 and all(named.values()), (name, script, named, log)
            if name == 'block-marker-only':
                assert 'thematic break is no item' not in log and 'noninterrupting ordinal is no item' not in log
        return {'name': name, 'before': before, 'after': after, 'required_arms': required,
                'mutated_sha256': hashlib.sha256(altered.encode()).hexdigest(), 'consumers': receipts}
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        rows = list(pool.map(one, mutants))
    assert all(path.read_bytes() == data for path, data in originals.items())
    summary = {'source_sha256': hashlib.sha256(source.encode()).hexdigest(), 'source_bytes_preserved': True,
               'mutants': rows}
    (OUT / 'mutations.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps({'mutants': len(rows), 'both_consumers_fail_named_arms': True, 'source_bytes_preserved': True}))


if __name__ == '__main__':
    main()
