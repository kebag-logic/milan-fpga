"""Fresh synthetic-only oracle receipts; reruns use the exact request cache."""
import concurrent.futures
import datetime
import hashlib
import html
import json
import re
import subprocess
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent
LANE = Path('$CANDIDATE')
sys.dont_write_bytecode = True
sys.path.insert(0, str(LANE / 'scripts'))
import gen_toc as toc
import gen_toc_container_cases as cases


def fixtures():
    rows = [{'id': name, 'page': f'{prefix}\n<{tag}>\n## Old\n</{tag}>\n\n## Real\n',
             'visible': visible, 'source': 'published-description reconstruction or boundary'}
            for name, prefix, tag, visible in cases.probe_rows()]
    rows += [{'id': name, 'page': page, 'visible': visible, 'source': 'correction_rows'}
             for name, page, visible in cases.correction_rows()]
    public = OUT / 'public-archives'
    # All independent R237 pages, and all R238 probes, are kept byte-exact.
    rows += [{'id': 'R237 archive ' + r['id'], 'page': r['page'], 'source': 'R237 public archive'}
             for r in json.loads((public / 'R237-1/renderer-inputs.json').read_text())]
    rows += [{'id': 'R238 archive ' + r['id'], 'page': r['page'], 'source': 'R238 public archive',
              'prior_github': r['github']}
             for r in map(json.loads, (public / 'R238-1/receipts/probes.jsonl').read_text().splitlines())]
    rows += [{'id': name, 'page': page, 'source': 'selected omission'}
             for name, page, _ in cases.container_arms() if 'limitation' in name]
    rows += [{'id': name, 'page': page, 'source': 'optional item HTML termination residue'}
             for name, page in [
                 ('empty item opens HTML', '-\n  <span>\n## Old\n</span>\n\n## Real\n'),
                 ('empty sibling opens HTML', '- item\n-\n  <span>\n## Old\n</span>\n\n## Real\n')]]
    return rows


def render(page):
    request = {'text': page, 'mode': 'gfm', 'context': 'kebag-logic/milan-fpga'}
    data = json.dumps(request).encode()
    key = hashlib.sha256(data).hexdigest()
    path = OUT / 'renderer' / (key + '.json')
    if path.exists():
        return json.loads(path.read_text())
    argv = ['rtk', 'proxy', 'gh', 'api', 'markdown', '--input', '-']
    utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
    result = subprocess.run(argv, input=data, capture_output=True)
    row = {'argv': argv, 'utc': utc, 'request': request, 'request_bytes': data.decode(),
           'exit': result.returncode, 'html': result.stdout.decode(), 'stderr': result.stderr.decode()}
    if result.returncode:
        raise RuntimeError(row)
    row['github_all'] = [html.unescape(re.sub('<[^>]+>', '', value))
                         for value in re.findall(r'<h[1-6]\b[^>]*>(.*?)</h[1-6]>', row['html'], re.S)]
    row['response_sha256'] = hashlib.sha256(result.stdout).hexdigest()
    path.write_text(json.dumps(row, indent=2) + '\n')
    return row


def main():
    rows = fixtures()
    (OUT / 'renderer').mkdir(exist_ok=True)
    pages = list(dict.fromkeys(r['page'] for r in rows))
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        responses = dict(zip(pages, pool.map(render, pages)))
    failures = []
    for row in rows:
        response = responses[row['page']]
        row['request_sha256'] = hashlib.sha256(response['request_bytes'].encode()).hexdigest()
        row['github_all'] = response['github_all']
        row['head_all'] = [h[1] for h in toc.headings(row['page'])]
        row['github'] = [h for h in row['github_all'] if h in ('Old', 'Real')]
        row['head'] = [h for h in row['head_all'] if h in ('Old', 'Real')]
        row['agreement'] = row['github'] == row['head']
        if 'visible' in row and ('Old' in row['github']) != row['visible']:
            failures.append(row['id'])
        if row['source'] == 'correction_rows' and not row['agreement']:
            failures.append(row['id'])
    (OUT / 'renderer-results.json').write_text(json.dumps(rows, indent=2) + '\n')
    print(json.dumps({'rows': len(rows), 'unique_requests': len(pages), 'expected_failures': failures,
                      'remaining_disagreements': [r['id'] for r in rows if not r['agreement']]}, indent=2))
    return bool(failures)


if __name__ == '__main__':
    sys.exit(main())
