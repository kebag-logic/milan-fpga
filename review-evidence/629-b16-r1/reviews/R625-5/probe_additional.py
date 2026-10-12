#!/usr/bin/env python3
"""Additional numeric-coverage probes on disposable page copies; no source-tree edits."""
import concurrent.futures,json,pathlib,subprocess,sys
repo,packet,out=map(lambda x:pathlib.Path(x).resolve(),sys.argv[1:4])
page=repo/'docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md'
text=page.read_text();readme=(page.parent/'README.md').read_text()
anchor="| Attribution | No loss in the network or the DUT | Every stage at the path's floor."
assert text.count(anchor)==1
line=text[:text.index(anchor)].count('\n')+1
cases=[]
for number in ['26','+26','-26','.5','-.25','7e2','7E-2','７','²','⅔','7.']:
 for unit in ['s','ppm','dB']:
  cases.append((f'plain-{len(cases):02d}',f'The residual was {number}{unit}.'))
for sep in ['','  ','\t','\u00a0','\u202f','\u200b','\u2060','-','\u00ad','\u2010','\u2011','\ufe63','\uff0d','**','`','&nbsp;','&#160;','<i></i>','<!-- safe -->']:
 # Decode just the explicit escape sequences used in the table.
 sep=sep.encode().decode('unicode_escape') if sep.startswith('\\') else sep
 cases.append((f'descriptor-{len(cases):02d}',f'The residual was CLOCK_DOMAIN 7{sep}ppm.'))
for form in ['CLOCK_DOMAIN 7. ppm','CLOCK_DOMAIN 7.0 ppm','channels 7 to 8. ppm','CLOCK_DOMAIN 7&#x20;ppm','CLOCK_DOMAIN 7&#xA0;ppm','CLOCK_DOMAIN 7\' ppm','CLOCK_DOMAIN 7) ppm','[7 ppm](#b16c-attribution)','"7 ppm"','`7 ppm`','arbitrary7suffix','CLOCK_DOMAIN 7—ppm']:
 cases.append((f'additional-{len(cases):02d}',f'The residual was {form}.'))
def run(case):
 name,insert=case; d=out/'scratch/own-probes'/name;d.mkdir(parents=True,exist_ok=True)
 (d/page.name).write_text(text.replace(anchor,anchor.replace('Every stage',insert+' Every stage')))
 (d/'README.md').write_text(readme)
 cmd=[sys.executable,'-I',str(packet/'tools/check_b16_figures.py'),str(d/page.name),str(packet),str(d/'rows.tsv'),str(d/'coverage.tsv'),'--repo',str(repo),'--show','100']
 r=subprocess.run(cmd,capture_output=True,text=True,timeout=120)
 head=json.loads(r.stdout.splitlines()[0]) if r.stdout.startswith('{') else {}
 assert not r.stderr, r.stderr
 return dict(name=name,insert=insert,line=line,rc=r.returncode,summary=head,diagnostics=r.stdout.splitlines()[1:])
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool: results=list(pool.map(run,cases))
(out/'receipts/own-probes.json').write_text(json.dumps(results,indent=2,ensure_ascii=True)+'\n')
print('probes',len(results),'detected',sum(x['rc']==1 for x in results))
for x in results:
 if x['rc']!=1: print('ACCEPTED',x['name'],x['insert'],x['summary'])
