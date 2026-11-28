"""Finish resource accounting, link checks and file integrity after all work."""
import hashlib,json,os,re,shutil,subprocess,time
from pathlib import Path
base=Path('$MANAGEMENT/2026-09-23/usbnet-a855/round7');p=base/'receipts';scratch=Path('$VALIDATION_STORAGE/usbnet-a855')
unit=Path('/proc/self/cgroup').read_text().strip().split(':',2)[2]
cg=Path('/sys/fs/cgroup')/unit.lstrip('/')
ours=[];jobs=[]
job_names={'qualify-census.py','run-census.py','run-supplemental.py','collect-egress.py','census7.py','after-qualification.py','archive-census.py','native-slots.py','parallel-regrade.py'}
for d in Path('/proc').glob('[0-9]*'):
 try:
  if (d/'cgroup').read_text().strip().split(':',2)[2]!=unit:continue
  args=(d/'cmdline').read_bytes().split(b'\0');exe=args[0].decode()
  if any(Path(a.decode()).name in job_names for a in args if a):jobs.append(int(d.name))
  if exe.startswith(str(scratch/'round7')) and exe.endswith('/native/Vsim'):ours.append(dict(pid=int(d.name),state=(d/'stat').read_text().split()[2]))
 except OSError:pass
assert not ours,ours
assert not jobs,jobs
used=int(subprocess.check_output(['du','-sx','--block-size=1',str(scratch)]).split()[0]);free=shutil.disk_usage('/data').free
assert used<=25_000_000_000 and free>=18_000_000_000,(used,free)
resources=dict(utc=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),unit=unit,cpu_weight=(cg/'cpu.weight').read_text().strip(),cpu_max=(cg/'cpu.max').read_text().strip(),cpu_affinity=sorted(os.sched_getaffinity(0)),scratch_bytes=used,data_free_bytes=free,native_children=ours,active_measurement_jobs=jobs,cleanup_log='$MANAGEMENT/2026-09-23/disk-cleanup.log',shared_ccache=os.environ.get('CCACHE_DIR'),no_push=True,no_post=True,no_bench=True)
assert resources['cpu_weight']=='200';assert resources['shared_ccache']=='$VALIDATION_STORAGE/ccache'
(p/'resources-final.json').write_text(json.dumps(resources,indent=2)+'\n')
links=[]
for name in ('HANDOFF-r7.md','REVIEW-READY.md','PR-BODY.md','receipts/INDEX.md'):
 f=base/name
 for target in re.findall(r'\]\(([^)]+)\)',f.read_text()):
  if '://' in target or target.startswith('#'):continue
  resolved=(f.parent/target.split('#')[0]).resolve();assert resolved.exists() or resolved==p/'MANIFEST.sha256',(name,target);links.append(dict(file=name,target=target))
(p/'packet-links.json').write_text(json.dumps(links,indent=2)+'\n')
lines=[]
for f in sorted(p.rglob('*')):
 if f.is_file() and f.name!='MANIFEST.sha256':
  digest=hashlib.file_digest(f.open('rb'),'sha256').hexdigest();lines.append(digest+'  '+str(f.relative_to(p)))
(p/'MANIFEST.sha256').write_text('\n'.join(lines)+'\n')
assert (p/'MANIFEST.sha256').is_file()
print('Final receipt files:',len(lines),'scratch:',used,'free:',free,'all links valid')
