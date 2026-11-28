"""Bind the final local commit to measured inputs and dependency identity."""
import hashlib,json,os,subprocess,sys,time
from pathlib import Path
root=Path.cwd(); packet=Path('$MANAGEMENT/2026-09-23/usbnet-a855/round7/receipts');scratch=Path('$VALIDATION_STORAGE/usbnet-a855/round7')
def git(*args):return subprocess.check_output(['git',*args],cwd=root)
def sha(data):return hashlib.sha256(data).hexdigest()
head=git('rev-parse','HEAD').decode().strip();dependency='640699e6866602b2a5de5d404c43f3bd4df8037c';merge='91252ecf7457287079d5d2f794b8544f0d9d34c4'
assert subprocess.run(['git','merge-base','--is-ancestor',dependency,head],cwd=root).returncode==0
assert not git('status','--porcelain'),git('status','--porcelain')
identity=[]
for row in json.loads((packet/'dependency-identity.json').read_text()):
 path=row['path']; actual=sha((root/path).read_bytes()); wanted=sha(git('show',dependency+':'+path))
 assert actual==wanted,path
 identity.append(dict(path=path,sha256=actual,identical=True))
sys.path.insert(0,str(root/'tb/verilator/ctrl_service_budget'));import build
manifest=json.loads((scratch/'census/manifest.json').read_text())
for variant in manifest['groups']:build.reused(scratch/'census'/variant)
changed=git('diff','--name-only',merge,head).decode().splitlines()
assert all(p.startswith(('tb/verilator/usbnet/','docs/')) or p=='scripts/measure_test_evidence_readers.py' for p in changed),changed
inputs={}
tracked=git('ls-files','-z','tb/verilator/usbnet','sw/firmware/ctrl','hdl/usbnet','sw/litex/usbnet_soc.py').decode().split('\0')
for relative in filter(None,tracked):
 f=root/relative
 if f.is_file():inputs[relative]=sha(f.read_bytes())
for row in json.loads((packet/'firmware-identity.json').read_text()):
 for name,value in row['hashes'].items():
  f=packet/'firmware'/row['tree']/row['recipe']/name;assert sha(f.read_bytes())==value
record=dict(head=head,dependency=dependency,merge=merge,dependency_files=identity,changes_since_measured_merge=changed,firmware_and_product_rtl_unchanged_since_measured_merge=True,all_eight_census_builds_reverified=True,inputs=inputs,pins=git('submodule','status').decode(),status='FAIL evidence retained; no review approval',utc=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()))
(packet/'final-head.json').write_text(json.dumps(record,indent=2)+'\n')
(packet/'round7.patch').write_bytes(git('diff','--binary',merge,head))
(packet/'local-history.txt').write_bytes(git('log','-2','--format=fuller'))
print(head,'dependency and measured inputs verified')
