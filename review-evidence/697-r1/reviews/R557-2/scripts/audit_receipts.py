#!/usr/bin/env python3
"""Audit named mutation results, local links and exact checkout bytes and modes."""
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import xml.etree.ElementTree as ET
repo,packet=map(lambda s:Path(s).resolve(),sys.argv[1:3])
def git(*args):return subprocess.check_output(['git',*args],cwd=repo)
head='ccb4ac30b03682d68a52fe7f1eb375b0c8bfb9d3'
assert git('rev-parse','HEAD').decode().strip()==head
assert git('rev-parse','HEAD^{tree}').decode().strip()=='d8c4f1244d691e84b40a34cb0028b06d068613f3'
index={}
for entry in git('ls-files','--stage','-z').split(b'\0'):
    if not entry:continue
    info,name=entry.split(b'\t');mode,oid,stage=info.decode().split()
    assert stage=='0'
    index[name.decode()]=(mode,oid)
checked=[];links=[]
for entry in git('ls-tree','-r','-z','HEAD').split(b'\0'):
    if not entry:continue
    info,name=entry.split(b'\t');mode,kind,oid=info.decode().split();name=name.decode()
    assert index[name]==(mode,oid),name
    if mode=='160000':links.append({'path':name,'oid':oid});continue
    p=repo/name
    data=os.readlink(p).encode() if mode=='120000' else p.read_bytes()
    actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    actual_mode='120000' if p.is_symlink() else ('100755' if p.stat().st_mode & stat.S_IXUSR else '100644')
    assert actual==oid and actual_mode==mode,(name,actual,oid,mode,actual_mode)
    checked.append({'path':name,'git_blob':oid,'mode':mode,'bytes_verified':True})
assert not git('diff','--exit-code','HEAD')
assert not git('diff','--cached','--exit-code','HEAD')
assert not git('status','--porcelain'),git('status','--porcelain').decode()
base_links=[line for line in git('ls-tree','-r','ae982af85ec97286bd35b39403926d8f0eaec81d').decode().splitlines() if line.startswith('160000')]
assert not links and not base_links
(packet/'receipts/checkout-final.json').write_text(json.dumps({'head':head,'tree':'d8c4f1244d691e84b40a34cb0028b06d068613f3','files':checked,'index_exact':True,'tracked_modes_exact':True,'working_tree_clean':True,'head_gitlinks':links,'base_gitlinks':base_links},indent=2)+'\n')

table=json.loads((repo/'tests/mutations.json').read_text())
audits=[]
for location in ('scratch/runs/mutations','scratch/supplement/mutations-repeat'):
    work=packet/location
    results=json.loads((work/'results.json').read_text())
    assert {x['name'] for x in results}=={x['name'] for x in table}
    assert len(results)==311 and all(x['status']=='CAUGHT' for x in results)
    kills=0
    for plant in table:
        reports={}
        for p in (work/plant['name']).glob('*.xml'):
            root=ET.parse(p).getroot()
            cases=list(root.iter('testcase'))
            assert len(cases)==int(root.get('tests')) and len({(c.get('classname'),c.get('name')) for c in cases})==len(cases)
            assert all(c.get('status')=='run' and c.get('result')=='completed' and not c.findall('skipped') for c in cases)
            reports[p.stem]={c.get('classname')+'.'+c.get('name'):'\n'.join(f.get('message','') for f in c.findall('failure')) for c in cases}
        default='maap_debug' if any(k['test'].startswith('MaapDebug.') for k in plant['kills']) else Path(plant['path']).stem
        for kill in plant['kills']:
            names=reports[kill.get('arm',default)]
            assert kill['needle'].strip()
            assert any((n.startswith(kill['test']) if kill['test'].endswith('/') else n==kill['test']) and kill['needle'] in message for n,message in names.items()),(plant['name'],kill)
            kills+=1
    audits.append({'campaign':location.replace('scratch/',''),'plants':len(results),'required_killers':kills,'all_named_assertions_verified':True})
(packet/'receipts/mutation-audit.json').write_text(json.dumps(audits,indent=2)+'\n')

links=[];errors=[]
for md in [repo/'README.md',repo/'CONTRIBUTING.md',repo/'CHANGELOG.md',repo/'SECURITY.md',*sorted((repo/'docs').glob('*.md'))]:
    for label,url in re.findall(r'\[([^\]]+)\]\(([^)]+)\)',md.read_text()):
        if '://' in url or url.startswith('mailto:'):continue
        path,_,fragment=url.partition('#')
        dest=(md.parent/path).resolve()
        valid=dest.exists()
        if valid and fragment.startswith('L') and re.fullmatch(r'L\d+',fragment):
            valid=1<=int(fragment[1:])<=len(dest.read_text().splitlines())
        links.append({'document':str(md.relative_to(repo)),'target':url,'valid':valid})
        if not valid:errors.append(links[-1])
assert not errors,errors
(packet/'receipts/document-links.json').write_text(json.dumps({'checked':len(links),'invalid':errors},indent=2)+'\n')
print(json.dumps({'tracked_blobs':len(checked),'gitlinks':0,'campaigns':audits,'relative_links':len(links)}))
