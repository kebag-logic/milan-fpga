"""Compare the public and new synthetic bytes across all three walk revisions."""
import json
from preserve import OUT, load


def main():
    walks = {name: load(name, OUT / 'snapshots' / name / 'scripts/gen_toc.py')
             for name in ('baseline', 'starting', 'corrected')}
    rows = json.loads((OUT / 'renderer-results.json').read_text())
    for row in rows:
        row['walks'] = {name: [h[1] for h in module.headings(row['page'])] for name, module in walks.items()}
    (OUT / 'three-revision-probes.json').write_text(json.dumps(rows, indent=2) + '\n')
    fixed = [r for r in rows if r['source'] == 'correction_rows']
    assert all([h for h in r['walks']['corrected'] if h in ('Old', 'Real')] == r['github'] for r in fixed)
    optional = [r for r in rows if not r['agreement']]
    assert all(r['walks']['baseline'] == r['walks']['starting'] == r['walks']['corrected'] for r in optional)
    # Retain the rejected exploratory unclosed-comment expectation. These
    # are not correction passes; compare rather than assuming baseline identity.
    exploratory = []
    for path in (OUT / 'renderer').glob('*.json'):
        receipt = json.loads(path.read_text())
        page = receipt['request']['text']
        if '<!--\n\n## Old' in page and '-->' not in page:
            exploratory.append({'page': page, 'github': receipt['github_all'],
                                'walks': {name: [h[1] for h in module.headings(page)] for name, module in walks.items()},
                                'receipt': str(path.relative_to(OUT))})
    (OUT / 'exploratory-unclosed-comments.json').write_text(json.dumps(exploratory, indent=2) + '\n')
    assert all(r['walks']['starting'] == r['walks']['corrected'] for r in exploratory)
    print(json.dumps({'in_scope_correction_rows': len(fixed), 'all_agree': True,
                      'optional_residues_unchanged': [r['id'] for r in optional],
                      'exploratory_unclosed_comments_unchanged_by_correction': len(exploratory),
                      'exploratory_unclosed_comments_differ_from_original_base':
                          sum(r['walks']['baseline'] != r['walks']['corrected'] for r in exploratory),
                      'first_paragraph_counterparts': [r for r in fixed if r['id'] in ('R238 P01', 'R238 P04')]}, indent=2))


if __name__ == '__main__':
    main()
