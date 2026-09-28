"""Reconstruct retained evidence bytes, then run exact-head service regrades."""
from pathlib import Path
import gzip
import hashlib
import json
import subprocess
import time

out=Path(__file__).parent
root=Path('$LANES/590-592-599-firmware')
head=subprocess.check_output(['rtk','proxy','git','rev-parse','HEAD'],cwd=root,text=True).strip()
artifacts=json.loads((out/'native-artifacts.json').read_text())
commands=json.loads((out/'native-commands.json').read_text())
results=[]


def restore(name, destination):
    matches=[item for item in artifacts if item['name'] in (name,name+'.gz')]
    assert len(matches)==1,(name,len(matches))
    item=matches[0]
    parts=[]
    for part in item['stored']:
        raw=(out/part['path']).read_bytes()
        assert len(raw)==part['size'] and hashlib.sha256(raw).hexdigest()==part['sha256']
        parts.append(raw)
    raw=b''.join(parts)
    if item['name'].endswith('.gz'):
        raw=gzip.decompress(raw)
    assert len(raw)==item['raw_size'] and hashlib.sha256(raw).hexdigest()==item['raw_sha256']
    destination.write_bytes(raw)


for entry in commands:
    name=entry['name']
    if not name.startswith('service-') or name.startswith('service-no-publish'):
        continue
    args=entry['command']
    directory=Path(args[args.index('--build-dir')+1])
    plan=args[args.index('--plan')+1]
    waits='3000000-5000' if plan=='device-wait' else '0-0'
    stem='service-'+plan+'-1-'+waits
    restore(name+'-raw.log',directory/(stem+'.log'))
    restore(name+'-receipt.json',directory/(stem+'.json'))
    log=Path('$VALIDATION_STORAGE/590-a411')/('final-regrade-'+name+'.log')
    command=args+['--regrade']
    started=time.monotonic()
    with log.open('w') as stream:
        result=subprocess.run(command,cwd=root,stdout=stream,stderr=subprocess.STDOUT,timeout=29000)
    raw=log.read_bytes()
    body=gzip.compress(raw,mtime=0) if len(raw)>200000 else raw
    filename=log.name+('.gz' if len(raw)>200000 else '')
    stored=[]
    for index,start in enumerate(range(0,len(body),190000)):
        part=body[start:start+190000]
        target=out/'logs'/(filename+(f'.part{index:02d}' if len(body)>190000 else ''))
        target.write_bytes(part)
        stored.append(dict(path=str(target.relative_to(out)),size=len(part),sha256=hashlib.sha256(part).hexdigest()))
    results.append(dict(name=name,head=head,command=command,rc=result.returncode,
                        stored=stored,seconds=round(time.monotonic()-started,3),size=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
    (out/'final-target-gates.json').write_text(json.dumps(results,indent=2)+'\n')
    print(name,result.returncode,flush=True)
    assert result.returncode==0,log.read_text()[-2000:]
assert subprocess.check_output(['rtk','proxy','git','rev-parse','HEAD'],cwd=root,text=True).strip()==head
print('PASS: all kept service logs regraded at '+head)
