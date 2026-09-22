"""Real Git provenance and generated navigation with exact synthetic fixture bytes."""
import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

OUT = Path(__file__).resolve().parent
LANE = Path('$CANDIDATE')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--scripts', type=Path, default=LANE / 'scripts')
    parser.add_argument('--label', default='corrected')
    parser.add_argument('--assert-correct', action='store_true')
    args = parser.parse_args()
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(args.scripts))
    import gen_toc as toc
    import check_em_dash as gate
    rows = json.loads((OUT / 'consumer-inputs.json').read_text())
    heading = '## Old \u2014 heading\n'
    tail = '\n## Alpha\n\nBody.\n\n## Beta\n\nBody.\n\n## Gamma\n\nBody.\n'
    navigation = ('## Contents\n\n- **[Old \u2014 heading](#old--heading)** -- Copied.\n'
                  '- **[Alpha](#alpha)** -- What alpha holds.\n'
                  '- **[Beta](#beta)** -- What beta holds.\n'
                  '- **[Gamma](#gamma)** -- What gamma holds.\n\n')
    head_page = '# Page\n\n' + navigation + heading + tail
    assert toc.generated_block(head_page, 'page.md') and toc.apply(Path('page.md'), head_page) is None
    with tempfile.TemporaryDirectory(prefix='a172-git-', dir=OUT) as tmp:
        repo = Path(tmp)
        gate._fixture_git(repo, 'init', '-q', '--initial-branch=main')
        for i, row in enumerate(rows):
            row['base_page'] = '# Page\n\n' + row['page'].replace('## Old\n', heading).replace('\n## Real\n', '') + tail
            (repo / f'page{i}.md').write_text(row['base_page'])
        base = gate._commit(repo, 'Synthetic base')
        for i in range(len(rows)):
            (repo / f'page{i}.md').write_text(head_page)
        head = gate._commit(repo, 'Synthetic head')
        for i, row in enumerate(rows):
            name = f'page{i}.md'
            verdict = gate.Verdict()
            gate.judge_page(repo, base, gate.Change(name, name), verdict)
            # The empty navigation placeholder precedes the fixture so the
            # insertion site is a real top-level block even for hidden Old.
            nav_page = '# Page\n\n## Contents\n\n' + row['base_page'].split('# Page\n\n', 1)[1]
            generated = toc.apply(Path(name), nav_page) or nav_page
            block = toc.generated_block(generated, name)
            listed = bool(block and any('#old--heading)' in line for line in block[1]))
            row.update({'head_page': head_page, 'base_commit': base, 'head_commit': head,
                        'base_headings': toc.headings(row['base_page']),
                        'navigation_page': generated, 'navigation_provenance': block,
                        'navigation_lists_old': listed, 'head_provenance': toc.generated_block(head_page, name),
                        'findings': verdict.findings, 'exempt': verdict.exempt,
                        'diff': gate._fixture_git(repo, 'diff', '--unified=0', base, head, '--', name)})
            row['correct'] = ((len(verdict.findings), verdict.exempt) == ((0, 1) if row['visible'] else (1, 0))
                              and listed == row['visible']
                              and (row['visible'] or any('mirrors no heading' in f for f in verdict.findings)))
    (OUT / f'consumers-{args.label}.json').write_text(json.dumps(rows, indent=2) + '\n')
    print(json.dumps({'label': args.label, 'rows': len(rows), 'failed': [r['id'] for r in rows if not r['correct']]}, indent=2))
    return int(args.assert_correct and any(not r['correct'] for r in rows))


if __name__ == '__main__':
    sys.exit(main())
