"""Benchmark native optimization with identical inputs, in one released destination slot.
This is runtime evidence only; it does not qualify firmware or supply CPU costs.
"""
import hashlib,json,os,resource,shutil,subprocess,time
from pathlib import Path
r=Path('$VALIDATION_STORAGE/artysplit-a829/r4');out=r/'native-optimization'
def active():
 rows=[]
 for p in Path('/proc').glob('[0-9]*/cmdline'):
  try:a=p.read_bytes().split(b'\0')
  except OSError:continue
  if a and a[0].startswith(str(r).encode()) and a[0].endswith(b'/native/Vsim'):rows.append(a[0].decode())
 return rows
while True:
 if any((r/n).exists() for n in ('watch-finding.json','remaining-finding.json')):raise SystemExit('A finding takes priority')
 done=True
 for name in ('srp-talker-loss','srp-talker-held'):
  p=r/'arm-valid/results'/(name+'.log')
  if not p.exists():done=False;break
  with p.open('rb') as f:f.seek(max(0,p.stat().st_size-4000));done=done and b'RESULT: PASS' in f.read()
 if done and str(r/'arm-valid/native/Vsim') not in active():break
 time.sleep(5)
# The other released destination slot belongs to measure-full-mrpdus.py.
assert len(active())<=3 and all(n in (str(r/'arm-two/native/Vsim'),str(r/'arm-later/native/Vsim')) for n in active())
out.mkdir(exist_ok=False);native=out/'native'
shutil.copytree(r/'arm-a/native',native)
for pattern in ('*.o','*.a','*.d'):
 for p in native.glob(pattern):p.unlink()
(native/'Vsim').unlink()
argv=['make','-j8','-C',str(native),'-f','Vsim.mk','Vsim','OPT_FAST=-O3','OPT_SLOW=-O3','OPT_GLOBAL=-O3']
with (out/'make.log').open('w') as f:subprocess.run(argv,stdout=f,stderr=subprocess.STDOUT,check=True,timeout=3600)
script=out/'short.txt';script.write_text('wait ready\nwait cycles 800000\nend\n')
records=[]
for sample in range(3):
 for name,exe in [('baseline',r/'arm-a/native/Vsim'),('optimized',native/'Vsim')]:
  log=out/f'{name}-{sample}.log';before=resource.getrusage(resource.RUSAGE_CHILDREN);start=time.monotonic()
  with log.open('w') as f:p=subprocess.run([str(exe),str(script),'-'],cwd=r/'arm-a/gateware',stdout=f,stderr=subprocess.STDOUT,timeout=600)
  after=resource.getrusage(resource.RUSAGE_CHILDREN);raw=log.read_bytes()
  records.append(dict(kind=name,sample=sample,returncode=p.returncode,wall_seconds=time.monotonic()-start,cpu_seconds=after.ru_utime+after.ru_stime-before.ru_utime-before.ru_stime,trace_sha256=hashlib.sha256(raw).hexdigest(),completed=b'RESULT: PASS' in raw[-4000:]))
  print(records[-1],flush=True)
identical=len({row['trace_sha256'] for row in records})==1
ok=identical and all(row['returncode']==0 and row['completed'] for row in records)
means={kind:sum(row['cpu_seconds'] for row in records if row['kind']==kind)/3 for kind in ('baseline','optimized')}
record=dict(status='PASS' if ok else 'FAIL',kind='native runtime benchmark; no firmware qualification',records=records,identical=identical,mean_cpu_seconds=means,speedup=means['baseline']/means['optimized'],build_command=argv)
(out/'result.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record),flush=True)
raise SystemExit(not ok)
