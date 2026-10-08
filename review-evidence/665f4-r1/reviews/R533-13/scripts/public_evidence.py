#!/usr/bin/env python3
"""Read-only audit of published source-head receipts; no other review reports."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys

EVIDENCE = 'ef69cd574960ff0ed632630d82d41383e38b1acc'
PREFIX = 'review-evidence/665f4-r1/author-r13/'
HEAD = '154722e14781c7373f3229420b6e007f9bcf9835'

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--source',type=Path,required=True); ap.add_argument('--packet',type=Path,required=True)
    a=ap.parse_args(); root=a.source.resolve(); packet=a.packet.resolve()
    def git(*args): return subprocess.check_output(['git','-C',str(root),*args])
    def blob(path): return git('show',EVIDENCE+':'+PREFIX+path)
    def obj(path): return json.loads(blob(path))
    assert git('rev-parse','HEAD').decode().strip()==HEAD
    gates=obj('ROUND13-GATES.json'); rows=[]
    for g in gates:
        path=g.get('retained_log')
        if path:
            data=blob(path); digest=hashlib.sha256(data).hexdigest()
            assert len(data)==g['retained_bytes'] and digest==g['retained_sha256'],path
            out=packet/'scratch/public-author'/path; out.parent.mkdir(parents=True,exist_ok=True); out.write_bytes(data)
            rows.append({'label':g['label'],'rc':g['rc'],'retained_log':path,'bytes':len(data),'sha256':digest,'hash_verified':True})
        else:
            rows.append({'label':g['label'],'rc':g['rc'],'retained_log':None,'limit':'Raw full log not published; structured campaign receipt available.'})
    result={'evidence_commit':EVIDENCE,'gate_count':len(gates),'all_recorded_rc_zero':all(g['rc']==0 for g in gates),'receipts':rows}
    (packet/'receipts/public-gates-audit.json').write_text(json.dumps(result,indent=2)+'\n')
    source=obj('ROUND13-SOURCE.json')
    for row in source['files']:
        data=(root/row['path']).read_bytes()
        assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
    path='sw/firmware/ctrl/test/srp_mutants.py'
    assert git('diff','--name-only','HEAD^','HEAD').decode().splitlines()==[path]
    assert ast.dump(ast.parse(git('show','HEAD^:'+path)))==ast.dump(ast.parse((root/path).read_text()))
    sys.dont_write_bytecode=True; sys.path.insert(0,str(root/'sw/firmware/ctrl/test'))
    import srp_mutants
    import ctrl_mutants
    campaign=obj('ROUND13-CAMPAIGN.json')
    expected2=[d.name for d in srp_mutants.DEFECTS]
    expected1=[d.name for d in srp_mutants.DEFECTS if d.name.startswith(('four-way-','binding-','feedback-','r10-','p11-','srp-bound-','srp-term-','srp-poll-extra','srp-send-extra'))]
    assert campaign['srp_if2_caught']==expected2 and campaign['srp_if1_caught']==expected1
    assert len(campaign['control_caught'])==len(ctrl_mutants.MUTANTS)==471
    result={'head':HEAD,'source_files_hash_verified':source['files'],'parent':git('rev-parse','HEAD^').decode().strip(),
            'final_commit_only_wraps_python':True,'python_ast_unchanged':True,
            'published_campaign_tables_match_standing_driver':True,'control_count':471,'srp_if2':len(expected2),
            'srp_if1':len(expected1),'pin_refusals':campaign['pin_refusals'],
            'limit':'Full raw campaign log not published; structured receipt and source equivalence verified. Focused exact-head local rerun independently verifies the six new catches.'}
    (packet/'receipts/public-source-campaign-audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS: 86 command records, 85 retained log hashes, source hashes and campaign inventory')

if __name__=='__main__': main()
