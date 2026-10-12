#!/usr/bin/env python3
"""Offline focused reproduction. Run with the hash-locked Markdown interpreter.

Usage: run_review.py REPO AUTHOR_PACKET OUTPUT --jobs 4
All child work is joined before this foreground driver exits. Disposable copies
and unfiltered process logs live under OUTPUT/scratch. No checkout edits.
"""
import argparse
import concurrent.futures
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('repo', type=Path)
    ap.add_argument('packet', type=Path)
    ap.add_argument('output', type=Path)
    ap.add_argument('--jobs', type=int, default=4)
    a = ap.parse_args()
    repo, packet, out = (p.resolve() for p in (a.repo,a.packet,a.output))
    receipts = out/'receipts'; receipts.mkdir(exist_ok=True)
    scratch = out/'scratch'/'campaign'; scratch.mkdir(parents=True,exist_ok=True)
    page = repo/'docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md'
    check = packet/'tools/check_b16_figures.py'
    py = [sys.executable,'-I']
    tasks=[]
    def add(name,args,results=()):tasks.append((name,args,results))
    add('figures',py+[check,page,packet,receipts/'figures-rows.tsv',receipts/'figures-coverage.tsv','--repo',repo])
    for r in range(3,9):
        add(f'controls-r{r}',py+[packet/f'tools/r{r}_check_controls.py',check,page,packet,scratch/f'controls-r{r}',receipts/f'controls-r{r}.json'])
    add('self-probes',py+[packet/'tools/r8_self_probes.py',check,page,packet,scratch/'self-probes',receipts/'self-probes.json'])
    old=sys.argv
    sys.argv=['r8_probe_reruns.py',str(repo),str(packet),str(packet/'tools/review-probes'),str(scratch),'b522bb923fa59581478460b61633bce2cb90ac1d']
    spec=importlib.util.spec_from_file_location('published_probe_driver',packet/'tools/r8_probe_reruns.py')
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);sys.argv=old
    hashes={}
    for name,(file,want,where,argv,res,read) in mod.PROBE.items():
        p=packet/'tools/review-probes'/file
        got=hashlib.sha256(p.read_bytes()).hexdigest();assert got==want
        hashes[name]={'file':file,'sha256':got,'unchanged':True}
        d=scratch/name;(d/'receipts').mkdir(parents=True,exist_ok=True);(d/'scratch').mkdir(exist_ok=True)
        add(name,py+[p,*argv(d)],[(res(d),receipts/(name+'.json'))])
    (receipts/'probe-identities.json').write_text(json.dumps(hashes,indent=2)+'\n')
    for name,args in [('docs-check',['scripts/docs_check.py']),('doc-style',['scripts/check_doc_style.py']),('toc',['scripts/gen_toc.py','--check']),('doc-paths',['scripts/check_doc_paths.py']),('em-dash',['scripts/check_em_dash.py','--base','c20c85bd']),('diff-check',['git','diff','--check','c20c85bd','HEAD'])]:
        add(name,(py+args) if args[0]!='git' else args)
    def safe(t):
        for p,label in sorted([(str(out),'$OUTPUT'),(str(repo),'$REPO'),(str(packet),'$PACKET'),(str(Path(sys.executable).parent.parent),'$ENV')],key=lambda x:-len(x[0])):
            t=t.replace(p,label)
        return t
    def run(task):
        name,args,results=task
        args=list(map(str,args))
        cp=subprocess.run(args,cwd=repo,capture_output=True,text=True,timeout=590)
        (scratch/(name+'.stdout')).write_text(cp.stdout)
        (scratch/(name+'.stderr')).write_text(cp.stderr)
        (receipts/(name+'.log')).write_text(safe(cp.stdout+cp.stderr))
        (receipts/(name+'.rc')).write_text(str(cp.returncode)+'\n')
        for src,dst in results:
            if src.exists():dst.write_text(safe(src.read_text()))
        result={'name':name,'returncode':cp.returncode,'command':safe(' '.join(args))}
        print(json.dumps(result),flush=True)
        return result
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(a.jobs,16)) as pool:
        results=list(pool.map(run,tasks))
    (receipts/'campaign.json').write_text(json.dumps(results,indent=2)+'\n')

if __name__=='__main__':main()
