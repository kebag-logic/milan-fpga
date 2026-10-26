#!/usr/bin/env python3
"""Fetch only the assigned immutable public evidence; verify its published digests."""
import concurrent.futures, hashlib, json, pathlib, subprocess
OUT=pathlib.Path(__file__).resolve().parent
PREFIX='repos/kebag-logic/milan-fpga/contents/review-evidence/pp202-r1/'
REF='51842a7a26d2f6c667175bc187ef801aaa3b89c8'
(OUT/'scratch').mkdir(exist_ok=True)
manifest=subprocess.check_output(['gh','api',PREFIX+'MANIFEST.json?ref='+REF,'-H','Accept: application/vnd.github.raw+json'])
(OUT/'scratch/public-manifest.json').write_bytes(manifest)
MAN=json.loads(manifest)
names={'author/parent-src-stream-id-wiring.patch','author/receipts/INDEX.md',
       'author/receipts/base-head-records.txt','author/receipts/clauses.txt',
       'author/receipts/consumer/PARENT-STATE.txt'}
for item in MAN:
    f=item['file']
    if '/consumer/' in f and (f.endswith(('SUMMARY.txt','HEAD.txt','submodules.txt','verdict.log','.rc','rom_digests.diff','rom_digests_final.diff','ooc_record_final.log','ooc_record_rom_digests.log'))): names.add(f)
    if '/processor/' in f and (f.endswith(('SUMMARY.txt','HEAD.txt','run_suites.log','run_suites.rc','acmp_mutants.log','acmp_mutants.rc','make_check.log','lint_hdl.log','req_tags_exec.log','yosys_run.log'))): names.add(f)
def fetch(item):
    name=item['file']; path=OUT/'scratch/public'/name
    path.parent.mkdir(parents=True,exist_ok=True)
    data=subprocess.check_output(['gh','api',PREFIX+name+'?ref='+REF,'-H','Accept: application/vnd.github.raw+json'])
    digest=hashlib.sha256(data).hexdigest()
    assert digest==item['published_sha256'], name
    path.write_bytes(data)
    return dict(file=name,sha256=digest,bytes=len(data))
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    records=list(pool.map(fetch,[x for x in MAN if x['file'] in names]))
(OUT/'public-evidence-verification.json').write_text(json.dumps(records,indent=2)+'\n')
print('Verified',len(records),'public evidence files at',REF)
