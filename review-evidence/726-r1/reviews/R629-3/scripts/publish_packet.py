#!/usr/bin/env python3
"""Build an explicit allowlist without publishing fetch snapshots or scratch trees."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

def main():
    ap=argparse.ArgumentParser();ap.add_argument('packet',type=Path);a=ap.parse_args();p=a.packet.resolve();r=p/'receipts'
    checks=json.loads((r/'hosted-checks-final.json').read_text())
    job=json.loads((r/'hosted-docs-job.json').read_text())
    summary=dict(format='Selected fields from raw hosted API responses; no status inferred.',
        assembled_at_utc=datetime.now(timezone.utc).isoformat(),
        raw_sha256={n:hashlib.sha256((r/n).read_bytes()).hexdigest()
                    for n in ('hosted-checks-final.json','hosted-docs-job.json')},
        checks=[{k:c[k] for k in ('id','name','head_sha','status','conclusion','started_at','completed_at','html_url')}
                for c in checks['check_runs']],
        docs_job={k:job[k] for k in ('id','head_sha','status','conclusion','html_url','steps')})
    (r/'hosted-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    pr=json.loads((r/'pr-729.json').read_text())
    body=pr['body'];sentence='The new commits remain local pending authorized publication.'
    assert sentence in body
    residue=dict(artifact='PR #729 body',format='Verbatim selected Status sentences from captured PR body.',
                 raw_sha256=hashlib.sha256((r/'pr-729.json').read_bytes()).hexdigest(),
                 text=[line for line in body.splitlines() if line.startswith('Local source head:') or line==sentence])
    (r/'pr-status-residue.json').write_text(json.dumps(residue,indent=2)+'\n')
    excluded={'full.diff','dependencies.log','pinned-dependencies.log','issue-726.json','issue-comments.json',
              'pr-729.json','pr-comments.json','hosted-checks.json','hosted-checks-final.json',
              'hosted-runs.json','hosted-docs-job.json'}
    files=[p/'REPORT.md']
    files.extend(f for f in (p/'scripts').iterdir() if f.is_file())
    files.extend(f for f in r.iterdir() if f.is_file() and f.name not in excluded and not f.name.endswith('build.log'))
    public=r/'public'
    files.extend(public/'review-round3'/name for name in (
        'docs-35-recovered.json','pinned-builder-all.log','docs-67.json','docs-67.log',
        'standing-before-1__run.log','standing-before-8__run.log'))
    files.append(public/'ROUND3-GATES.tsv')
    files.extend((public/'evidence').glob('*'))
    assert all(f.is_file() for f in files)
    report=(p/'REPORT.md').read_text()
    assert report.startswith('[R629] POSITIVE - exact head e893e4d13d99eb5ba00745f0f5cf74ee847972c2\n')
    assert report.rstrip().endswith('R629-3 FINISHED') and 'SKELETON' not in report
    files=sorted(set(files));lines=[]
    for f in files:
        rel=f.relative_to(p).as_posix();assert not rel.startswith('scratch/')
        lines.append(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+rel)
    (p/'MANIFEST.sha256').write_text('\n'.join(lines)+'\n')
    print(json.dumps(dict(files=len(files),bytes=sum(f.stat().st_size for f in files),
                         manifest='MANIFEST.sha256',report='REPORT.md'),indent=2))

if __name__=='__main__':main()
