#!/usr/bin/env python3
"""Audit already-published artifacts and live read-only merge metadata."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
p=argparse.ArgumentParser()
p.add_argument('--repo',type=Path,required=True)
p.add_argument('--packet',type=Path,required=True)
args=p.parse_args()
repo,packet=args.repo.resolve(),args.packet.resolve()
pub=packet/'public'
rows=json.loads((pub/'MANIFEST.json').read_text())
checked=[]
for row in rows:
    f=pub/row['file']
    if f.exists():
        assert hashlib.sha256(f.read_bytes()).hexdigest()==row['published_sha256'],str(f)
        checked.append(row['file'])
files=json.loads((pub/'author/candidate-files.json').read_text())
for row in files:
    assert hashlib.sha256((repo/row['path']).read_bytes()).hexdigest()==row['sha256'],row['path']
sys.path.insert(0,str(repo/'sw/firmware/ctrl/test'))
import ctrl_mutants
controls=list(csv.DictReader((pub/'author/mutations-control.csv').open()))
names=[re.search(r'mutant ([^ ]+) ',r['executed_control']).group(1) for r in controls]
assert len(names)==len(set(names))==519
assert set(names)=={m.name for m in ctrl_mutants.MUTANTS}
assert all(r['result']=='CAUGHT' for r in controls)
images=json.loads((pub/'author/image-hashes.json').read_text())
assert all(r['release_growth']==r['after']['load']-r['before']['load']<=2048 for r in images)
record={'public_digest_matches':len(checked),'candidate_file_hash_matches':len(files),
        'control_names_match_live_table':len(names),'all_controls_caught':True,
        'public_packet_commit':'52d6b147486ec5561b5862790727b27fb030108a',
        'image_rows':len(images),'image_max_growth':max(r['release_growth'] for r in images)}
(packet/'evidence-audit.json').write_text(json.dumps(record,indent=2)+'\n')
stack=repo/'third_party/tsn-c-stack'
def git(*argv):
    return subprocess.check_output(['git','-C',str(stack),*argv],text=True).strip()
authorized=set()
pr_rows=[]
for n in [19,20,23,25]:
    d=json.loads((packet/'metadata'/f'stack-pr-{n}.json').read_text())
    row={'pr':n,'merged':d['merged'],'merged_at':d['merged_at'],'merge':d['merge_commit_sha'],
         'head':d['head']['sha'],'head_tree':git('rev-parse',d['head']['sha']+'^{tree}'),
         'merge_tree':git('rev-parse',d['merge_commit_sha']+'^{tree}')}
    assert row['merged'] and row['head_tree']==row['merge_tree']
    cs=json.loads((packet/'metadata'/f'stack-pr-{n}-comments.json').read_text())
    row['review_headers']=[{'url':c['html_url'],'line':c['body'].splitlines()[0]} for c in cs
                           if c['body'].startswith('[R') and 'POSITIVE' in c['body'].splitlines()[0]]
    if n!=23:
        raw=subprocess.check_output(['gh','api',f'repos/kebag-logic/tsn-c-stack/pulls/{n}/files?per_page=100'])
        changes=json.loads(raw)
        row['files']=[c['filename'] for c in changes]
        authorized.update(row['files'])
    pr_rows.append(row)
delta=git('diff','--name-only','405dc683','70936b77').splitlines()
assert set(delta)<=authorized
proof={'prs':pr_rows,'changed_paths':delta,'all_paths_in_authorized_pr_file_sets':True,
       'pre_f3b_source_header_delta':git('diff','--name-only','405dc683','1ba27354','--','src','include').splitlines(),
       'same_pre_f3b_acmp_source':git('rev-parse','405dc683:src/acmp.c')==git('rev-parse','1ba27354:src/acmp.c'),
       'same_pre_f3b_acmp_header':git('rev-parse','405dc683:include/acmp.h')==git('rev-parse','1ba27354:include/acmp.h'),
       'head_parent':subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD^'],text=True).strip()}
(packet/'pin-audit.json').write_text(json.dumps(proof,indent=2)+'\n')
print(json.dumps(record,indent=2))
print('Pin audit: merged reviewed trees match; all',len(delta),'changed paths in authorized PRs.')
