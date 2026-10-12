#!/usr/bin/env python3
"""Independent parser-boundary probes; only disposable copies are changed.
Usage: parser-python probe_constructs.py REPO PACKET OUTPUT
"""
from pathlib import Path
import json
import shutil
import subprocess
import sys

repo,packet,out=map(lambda x:Path(x).resolve(),sys.argv[1:])
page=repo/'docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md'
base=page.read_text(); index=(page.parent/'README.md').read_text()
scratch=out/'scratch'/'own-probes';scratch.mkdir(parents=True,exist_ok=True)
forms={
    'strike-in-index':('index',' ~~evidence~~'),
    'image-in-index':('index',' ![evidence](x.png)'),
    'footnote-in-index':('index',' note[^own]'),
    'task-list-end':('end','- [x] evidence'),
    'reference-image-end':('end','![label][picture]\n\n[picture]: x.png'),
    'raw-processing-instruction':('end','<?evidence?>'),
    'raw-declaration':('end','<!DOCTYPE evidence>'),
    'raw-cdata':('end','<![CDATA[evidence]]>'),
    'empty-strike':('end','~~evidence~~'),
    'reference-footnote':('end','Evidence[^n].\n\n[^n]: text.'),
    'indented-code':('end','    evidence'),
    'block-html-multiline':('end','<div>\nevidence\n</div>'),
    'numeric-character-reference':('end','CLOCK_DOMAIN &#55; ppm.'),
    'numeric-character-reference-newline':('end','CLOCK_DOMAIN &#55;\nppm.'),
    'code-split-unknown-unit':('end','CLOCK_DOMAIN `7`furlongs.'),
    'emphasis-split-unknown-unit':('end','CLOCK_DOMAIN *7*furlongs.'),
    'nested-link-emphasis':('end','CLOCK_DOMAIN [**7**](#b16c-attribution)ppm.'),
    'hardbreak-in-quote':('end','> CLOCK_DOMAIN 7\\\n> furlongs.'),
    'unicode-zero-width':('end','CLOCK_DOMAIN 7\u200bfurlongs.'),
    'tab-in-number-unit':('end','CLOCK_DOMAIN 7\tppm.'),
    'math-block':('end','$$\n7 ppm\n$$'),
    'marked-generator-extra-line':('end','<!-- solution-cpu-contract:start -->\n<!--extra-->'),
    'blank-generator-padding':('end',' <!-- solution-cpu-contract:start -->'),
    'autolink-no-number':('end','<https://example.com/evidence>'),
    'generator-exact':('end','<!-- solution-cpu-contract:start -->'),
}
rows=[]
for name,(where,addition) in forms.items():
    d=scratch/name;d.mkdir(exist_ok=True)
    text=base;idx=index
    if where=='index':
        lines=idx.splitlines();lines[14]=lines[14].rstrip()[:-1]+addition+' |';idx='\n'.join(lines)+'\n';ln=15
        if name=='footnote-in-index':idx+='\n[^own]: evidence.\n'
    else:
        text+='\n'+addition+'\n';ln=len(base.splitlines())+2
    (d/page.name).write_text(text);(d/'README.md').write_text(idx)
    cp=subprocess.run([sys.executable,'-I',str(packet/'tools/check_b16_figures.py'),str(d/page.name),str(packet),str(d/'rows.tsv'),str(d/'coverage.tsv'),'--repo',str(repo),'--show','100'],capture_output=True,text=True,timeout=60)
    rows.append(dict(name=name,where=where,line=ln,added=addition,rc=cp.returncode,stdout=cp.stdout,stderr=cp.stderr.replace(str(repo),'$REPO').replace(str(out),'$OUTPUT'),receipts=(d/'rows.tsv').exists() and (d/'coverage.tsv').exists()))
    print(name,cp.returncode,flush=True)
(out/'receipts'/'own-constructs.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False)+'\n')
