#!/usr/bin/env python3
"""Independent visible-number and cross-boundary construct probes.

Arguments: repository author-packet output-root. Requires locked docs interpreter.
The original checkout is read only. Every altered document is under scratch.
"""
import concurrent.futures
import json
import pathlib
import shutil
import subprocess
import sys

repo, packet, out = map(lambda x:pathlib.Path(x).resolve(),sys.argv[1:4])
page = repo/'docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md'
base = page.read_text().split('\n')
intro = next(i for i,s in enumerate(base) if s.startswith('In lane B16, the operator tried'))
cases = []
def case(name, edits, target=None, expect='refused'):
    cases.append((name,edits,target or intro+1,expect))
for n,(opening,closing) in enumerate([
    ('`','`'), ('`  ','  `'), ('``','``'), ('`` `x','` ``'),
    ('`\t','\t`'), ('` x',' `'), ('`   x','   `'),
    ('``   `x','`   ``'), ('` &amp;',' `'), ('` \\x',' `')]):
    case(f'multiline-code-{n}',[(intro-1,base[intro-1]+' '+opening),
                              (intro,base[intro]+' 7.25 ppm'+closing)])
for n,(opening,closing) in enumerate([
    ('<PRE class="x">','</PRE>'), ('<ScRiPt>','</sCrIpT>'),
    ('<!--\t','-->'), ('<?x','?>'), ('<!DOCTYPE x','>'),
    ('<![CDATA[',']]>'), ('> <pre>','</pre>'), ('- <pre>','</pre>'),
    ('~~start','end~~'), ('![a','b](x.png)'),
    ('[a','b](#b16c-attribution)'), ('*a','b*'), ('**a','b**')]):
    case(f'boundary-{n}',[(intro-1,opening),(intro,base[intro]+' 7.25 ppm '+closing)])
for n,s in enumerate(['7.25ppm','-.25 ppm','7e2 ppm','CLOCK_DOMAIN 7\u00a0\u00a0furlongs',
                      'CLOCK_DOMAIN 7\u200bppm','CLOCK_DOMAIN 7&#x20;ppm',
                      'CLOCK_DOMAIN **7**ppm','CLOCK_DOMAIN [7](#b16c-attribution)ppm',
                      'CLOCK_DOMAIN 7![](x.png)ppm', 'CLOCK_DOMAIN 7&#xfeff;furlongs',
                      'CLOCK_DOMAIN ７furlongs','CLOCK_DOMAIN 7\u2066ppm',
                      'CLOCK_DOMAIN 7<em></em>ppm']):
    case(f'number-{n}',[(intro,base[intro]+' '+s)])
case('clean',[],expect='pass')
case('permitted-hard-break',[(intro-1,base[intro-1]+'  ')],expect='pass')

def run(c):
    name,edits,target,expect=c
    d=out/'scratch/independent'/name/'docs/findings';d.mkdir(parents=True,exist_ok=True)
    lines=base.copy()
    for i,s in edits:lines[i]=s
    p=d/page.name;p.write_text('\n'.join(lines));shutil.copyfile(page.parent/'README.md',d/'README.md')
    r=subprocess.run([sys.executable,'-I',str(packet/'tools/check_b16_figures.py'),str(p),str(packet),
                      str(d/'rows.tsv'),str(d/'coverage.tsv'),'--repo',str(repo),'--show','200'],
                     capture_output=True,text=True,timeout=300)
    named=[s for s in r.stdout.splitlines() if s.startswith(('MARKUP ','UNCOVERED '))]
    at_line=any(f'{page.name}:{target} ' in s for s in named)
    result=dict(name=name,edits=[{'line':i+1,'text':s} for i,s in edits],expected=expect,
                target_line=target,rc=r.returncode,detected_at_line=at_line,
                rows_written=(d/'rows.tsv').exists(),coverage_written=(d/'coverage.tsv').exists(),
                stdout=r.stdout,stderr=r.stderr,
                meets=(r.returncode==0 if expect=='pass' else r.returncode==1 and at_line))
    return result
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results=list(pool.map(run,cases))
(out/'receipts/independent-probes.json').write_text(json.dumps(results,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(dict(cases=len(results),met=sum(x['meets'] for x in results),
                     unexpected=[dict(name=x['name'],rc=x['rc'],named=x['detected_at_line']) for x in results if not x['meets']]),indent=2))
