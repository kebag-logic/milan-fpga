"""Restore dependency provenance in the disposable copied RTL fixture."""
import hashlib,json,shutil,subprocess
from pathlib import Path
r=Path('$VALIDATION_STORAGE/artysplit-a829/r4')
source=Path('$LANES/arty-split'); target=r/'rtl-fixture'
records=[]
def run(args,cwd=target):
    return subprocess.run(args,cwd=cwd,check=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True).stdout
for name in ('gptp-processor','third_party/verilog-axis'):
    pin=run(['git','rev-parse','HEAD:'+name],source).strip()
    assert run(['git','rev-parse','HEAD'],source/name).strip()==pin
    directory=target/name
    prior={str(p.relative_to(directory)):hashlib.sha256(p.read_bytes()).hexdigest() for p in directory.rglob('*') if p.is_file()}
    run(['git','rm','-r','--cached','--',name])
    backup=directory.with_name(directory.name+'-flattened-copy')
    assert not backup.exists()
    directory.rename(backup)
    run(['git','clone','--no-hardlinks','--no-checkout',str(source/name),str(directory)])
    run(['git','checkout','--detach',pin],directory)
    tracked=run(['git','ls-files','-z'],directory).split('\0')
    after={n:hashlib.sha256((directory/n).read_bytes()).hexdigest() for n in tracked if n}
    assert prior==after,(name,'dependency bytes differ')
    assert not (directory/'.git/objects/info/alternates').exists()
    run(['git','update-index','--add','--cacheinfo','160000,'+pin+','+name])
    shutil.rmtree(backup)
    records.append(dict(dependency=name,pin=pin,files=len(after),bytes_identical=True,private_objects=True))
run(['git','commit','-m','Preserve pinned dependencies in disposable RTL fixture'])
result=dict(status='PASS',fixture_head=run(['git','rev-parse','HEAD']).strip(),dependencies=records)
(r/'rtl-fixture-gitlinks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result),flush=True)
