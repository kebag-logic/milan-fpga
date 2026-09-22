"""Render only the synthetic real-Git pages and bind oracle answers to gate receipts."""
import concurrent.futures
import json
from render import OUT, render


def main():
    rows = json.loads((OUT / 'consumers-corrected.json').read_text())
    pages = list(dict.fromkeys(r['base_page'] for r in rows))
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        answers = dict(zip(pages, pool.map(render, pages)))
    receipts = []
    for row in rows:
        response = answers[row['base_page']]
        visible = 'Old \u2014 heading' in response['github_all']
        receipts.append({'id': row['id'], 'expected': row['visible'], 'github_visible': visible,
                         'request_bytes': response['request_bytes'], 'html': response['html'],
                         'utc': response['utc'], 'exit': response['exit']})
    (OUT / 'renderer-consumers.json').write_text(json.dumps(receipts, indent=2) + '\n')
    failed = [r['id'] for r in receipts if r['expected'] != r['github_visible']]
    print(json.dumps({'real_git_rows': len(rows), 'unique_synthetic_requests': len(pages), 'failed': failed}))
    assert not failed


if __name__ == '__main__':
    main()
