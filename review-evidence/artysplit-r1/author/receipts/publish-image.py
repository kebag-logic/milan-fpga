"""Preserve a qualified, routed Arty image and recheck its copied flash-pair inputs.

No hardware operation is present. The original manifest/layout bytes are kept.
Run only after the final source commit and successful grade-images.py.
"""
import datetime,hashlib,json,os,shutil,subprocess,sys
from pathlib import Path

root=Path('$LANES/arty-split')
scratch=Path('$VALIDATION_STORAGE/artysplit-a829/r4')
packet=Path('<home-path>/milan-fpga-management/2026-09-23/artysplit-a829/round4')
def read(path):return json.loads(path.read_text())
def artifact(path):
 return dict(path=str(path),bytes=path.stat().st_size,sha256=hashlib.sha256(path.read_bytes()).hexdigest())
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
assert head!='4a89ddcdb18bdfaafc9e999daeee1e7ba56274a2','No round-4 source commit'
assert subprocess.run(['git','diff','--quiet','HEAD'],cwd=root).returncode==0,'Tracked source is dirty'
qualified=read(scratch/'final-census/qualification.json')
assert qualified['status']=='PASS' and qualified['cpu_hz']==80_000_000 and qualified['groups']==145
assert all(value=='PASS' for value in qualified['checks'].values())
for name in ('final-service-selftest','final-boot-positive-fixedseed','final-boot-controls-fixedseed'):
 assert read(scratch/(name+'.json'))['returncode']==0,name
for row in read(scratch/'final-firmware-results.json'):assert row['returncode']==0
assert len(read(scratch/'final-firmware-results.json'))==4
assert read(scratch/'identity-final-compare.json')['status']=='PASS'
assert read(scratch/'identity-final-export-command.json')['returncode']==0
docs=read(scratch/'docs-final-corrected/results.json')
assert len(docs)==11 and not any(row['rc'] for row in docs)
graded=read(scratch/'images/graded-images.json')
assert graded['status']=='PASS' and len(graded['candidates'])==3
assert read(scratch/'images/inputs.json')['head']==head
best=graded['best']; assert best['status']=='PASS'
assert len(best['corners'])==4
assert min(row['timing']['wns'] for row in best['corners'])>=0.030
assert min(row['timing']['whs'] for row in best['corners'])>=0.0
source=Path(best['layout']['path']).parent
firmware=Path(graded['firmware']['path'])
assert artifact(firmware)==graded['firmware']
dest=packet/'image'
assert not dest.exists(),'Preserve any prior image packet; choose deliberately before retrying'
(dest/'gateware').mkdir(parents=True)
paths=[source/name for name in ('csr.csv','csr.json','flashboot_layout.json',
                               'image_manifest.json','aem_desc.bin','aem_desc.json')]
paths += [path for path in (source/'gateware').iterdir()
          if path.is_file() and path.suffix in ('.bit','.v','.tcl','.init','.xdc')]
copied=[]
for path in paths:
 target=dest/path.relative_to(source)
 shutil.copy2(path,target)
 assert target.read_bytes()==path.read_bytes()
 copied.append(artifact(target))
shutil.copy2(firmware,dest/'ctrl_app.elf')
assert (dest/'ctrl_app.elf').read_bytes()==firmware.read_bytes()
bit=dest/'gateware/digilent_arty.bit'
layout=dest/'flashboot_layout.json'
commands=[]
def command(name,argv,env=None):
 log=dest/(name+'.log')
 with log.open('w') as stream:
  process=subprocess.run(argv,cwd=root,env=env,stdout=stream,stderr=subprocess.STDOUT,timeout=600)
 commands.append(dict(name=name,command=argv,returncode=process.returncode,log=artifact(log)))
 (scratch/'publish-image-commands.json').write_text(json.dumps(commands,indent=2)+'\n')
 assert process.returncode==0,name
command('image-identity',[sys.executable,str(root/'sw/litex/check_image_identity.py'),str(dest),
                          '--firmware',str(dest/'ctrl_app.elf'),'--bitstream',str(bit)])
env=dict(os.environ,BIT=str(bit),LAYOUT=str(layout),AEM=str(dest/'aem_desc.bin'),
         FPGA_PART='xc7a100tcsg324',EXPECTED_GPTP_OWNER='fabric',
         PYTHON='<home-path>/litex-milan/venv/bin/python3',TMPDIR=str(scratch/'work-tmp'))
command('offline-flash-pair-inputs',['bash',str(root/'sw/litex/deploy.sh'),'check-images'],env)
record=dict(status='PASS',head=head,time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            directive=best['directive'],corners=best['corners'],utilization=best['utilization'],
            worst_wns_ns=best['worst_wns_ns'],worst_whs_ns=best['worst_whs_ns'],
            qualification=artifact(scratch/'final-census/qualification.json'),
            route_grading=artifact(scratch/'images/graded-images.json'),
            artifacts={name:artifact(dest/path) for name,path in (
             ('Bitstream','gateware/digilent_arty.bit'),('flashboot_layout.json','flashboot_layout.json'),
             ('Matched image_manifest.json','image_manifest.json'),('AEM image','aem_desc.bin'),
             ('AEM manifest','aem_desc.json'),('Firmware ELF','ctrl_app.elf'))},
            copied= copied,commands=commands,
            note='Offline input validation only. No hardware was accessed.')
(scratch/'image-ready.json').write_text(json.dumps(record,indent=2)+'\n')
(dest/'provenance.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2),flush=True)
