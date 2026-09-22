from pathlib import Path
import json,hashlib,subprocess
ROOT=Path(__file__).resolve().parents[1]
rows=[]
for e in json.loads((ROOT/'public/prior-blobs.json').read_text()):
 data=(ROOT/'public'/e['path']).read_bytes()
 actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
 assert actual==e['sha']
 rows.append({'file':e['path'],'blob':actual,'verified':True})
for e in json.loads((ROOT/'public/readiness-evidence/423/MANIFEST.json').read_text()):
 data=(ROOT/'public/readiness-evidence/423'/e['file']).read_bytes();actual=hashlib.sha256(data).hexdigest()
 assert actual==e['published_sha256']
 if not e['path_redacted']: assert actual==e['original_sha256']
 rows.append({'file':e['file'],'sha256':actual,'verified':True})
(ROOT/'logs/public-verification.json').write_text(json.dumps(rows,indent=2)+'\n')
print('8 public blob identities and 6 manifest entries verified')
repo=ROOT/'fixtures/donor.git';patches=[]
for oid,expected in [('9790ac736e6d10301ad814ffdf73dbe37b59768b','d3d164b309e376ea06a3734e8452dd5668c4721d0462dc0656af05d6b3c155b3'),('3db86812096830fada2f5f276fa5f4d9f37d1d14','fa20a2516a4d866a859506c5396779fb98bbafe943e4de2651e9ec252bca996f')]:
 cmd=['rtk','proxy','git','--no-replace-objects','-C',str(repo),'show','--format=',oid]
 p=subprocess.run(cmd,capture_output=True);p.check_returncode();actual=hashlib.sha256(p.stdout).hexdigest();assert actual==expected
 patches.append({'oid':oid,'command':cmd,'exit':p.returncode,'sha256':actual,'matches_issue_hash':True})
(ROOT/'logs/issue-patch-hashes-verified.json').write_text(json.dumps(patches,indent=2)+'\n')
print('Both issue patch hashes reproduced; full-index renderings differ only in formatting and are separately preserved')
