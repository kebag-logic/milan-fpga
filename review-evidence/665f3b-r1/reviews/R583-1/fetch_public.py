#!/usr/bin/env python3
"""Read-only capture of public evidence and review metadata."""
import concurrent.futures
import json
from pathlib import Path
import subprocess
import sys

p = Path(sys.argv[1]).resolve()
rows = json.loads((p / "public-evidence-tree.json").read_text())
prefix = "review-evidence/665f3b-r1/"
def fetch(row):
    name = row['path'].removeprefix(prefix)
    if row['type'] != 'blob' or 'resume-work-history' in name:
        return
    target = p / "public" / name
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open('wb') as out:
        subprocess.run(['gh','api','-H','Accept: application/vnd.github.raw+json',
                        'repos/kebag-logic/milan-fpga/git/blobs/'+row['sha']], stdout=out,check=True)
    return name
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
    downloaded = [x for x in pool.map(fetch, rows) if x]
print('Captured', len(downloaded), 'public artifacts; work-history material excluded.')
queries = {
  'pr-736.json': 'repos/kebag-logic/milan-fpga/pulls/736',
  'pr-736-comments.json': 'repos/kebag-logic/milan-fpga/issues/736/comments?per_page=100',
  'pr-736-reviews.json': 'repos/kebag-logic/milan-fpga/pulls/736/reviews?per_page=100',
  'pr-736-inline.json': 'repos/kebag-logic/milan-fpga/pulls/736/comments?per_page=100',
  'head-checks.json': 'repos/kebag-logic/milan-fpga/commits/db29bdd07529fbc697b7956827092f64b1241714/check-runs?per_page=100',
  'head-runs.json': 'repos/kebag-logic/milan-fpga/actions/runs?head_sha=db29bdd07529fbc697b7956827092f64b1241714&per_page=100',
}
for n in [19,20,23,25]:
    queries[f'stack-pr-{n}.json'] = f'repos/kebag-logic/tsn-c-stack/pulls/{n}'
    queries[f'stack-pr-{n}-reviews.json'] = f'repos/kebag-logic/tsn-c-stack/pulls/{n}/reviews?per_page=100'
    queries[f'stack-pr-{n}-comments.json'] = f'repos/kebag-logic/tsn-c-stack/issues/{n}/comments?per_page=100'
def api(item):
    name, url = item
    with (p / name).open('wb') as out:
        subprocess.run(['gh','api',url],stdout=out,check=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
    list(pool.map(api,queries.items()))
print('Captured public PR, stack provenance, and exact-head checks.')
# Portable audit inputs contain merge metadata and verdict headers only.
(p/'metadata').mkdir(exist_ok=True)
for n in [19,20,23,25]:
    d=json.loads((p/f'stack-pr-{n}.json').read_text())
    summary={k:d[k] for k in ['merged','merged_at','merge_commit_sha','head']}
    summary['head']={'sha':d['head']['sha']}
    (p/'metadata'/f'stack-pr-{n}.json').write_text(json.dumps(summary,indent=2)+'\n')
    cs=json.loads((p/f'stack-pr-{n}-comments.json').read_text())
    headers=[{'html_url':c['html_url'],'body':c['body'].splitlines()[0]} for c in cs
             if c['body'].startswith('[R') and 'POSITIVE' in c['body'].splitlines()[0]]
    (p/'metadata'/f'stack-pr-{n}-comments.json').write_text(json.dumps(headers,indent=2)+'\n')
