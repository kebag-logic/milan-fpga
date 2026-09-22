from pathlib import Path
import hashlib,json,sys
out=Path(sys.argv[1]).resolve();lane=Path(sys.argv[2]).resolve()
sys.path.insert(0,str(out/'bench'));from analyze import ORDINARY
sys.path.insert(0,str(lane/'scripts'));from suite_tally import scan,log_reports_failure
names=['cold-sequential','warm-sequential','cold-pooled','warm-pooled'];runs=[out/'runs'/name for name in names]
load=lambda p:json.loads(p.read_text())
head=load(out/'candidate.json')['head'];identities=[load(r/'identity.json') for r in runs]
for field in ['head','tree','version','tool','tool_files','affinity','limits','cgroup','cgroup_ancestry','host_boot_id','submodules']:
 assert all(i[field]==identities[0][field] for i in identities),field
assert all(i['head']==head for i in identities)
inputs=[load(r/'inputs-after.json') for r in runs];exes=[load(r/'executables.json') for r in runs]
assert all(x==inputs[0] for x in inputs);assert all(x==exes[0] for x in exes)
rows=[];canonical=None;phases=None
for run,identity in zip(runs,identities):
 raw=(run/'milan_dp.log').read_bytes();text=raw.decode();tally=scan(text)
 assert (tally[0],tally[1],len(tally[2]),tally[3])==(9324,0,13,[])
 assert not log_reports_failure(text)[1]
 assert load(run/'exit.json')==dict(make=0,verdict=0,tally=0,clean=True,same_head=True)
 captures={};checks={}
 for pos,exe in enumerate(ORDINARY,1):
  data=(run/'legs'/f'{pos:02d}-{Path(exe).name}.log').read_bytes();assert raw.count(data)==1,exe
  captures[exe]=hashlib.sha256(data).hexdigest();checks[exe]=scan(data.decode())[0]
 assert list(checks.values())==[230,135,1633,1635,3061,1633,230,33,227,139]
 disk=(run/'legs/replay.log').read_bytes();assert raw.count(disk)==1
 if canonical is None:canonical=captures
 else:assert captures==canonical
 records=[json.loads(x[len('RENDER-PHASE '):]) for x in text.splitlines() if x.startswith('RENDER-PHASE ')]
 assert len(records)==23
 semantic=[{k:v for k,v in record.items() if k not in ('t_s','elapsed_s','idle_s')} for record in records]
 if phases is None:phases=semantic
 else:assert phases==semantic
 jobs=int(identity['environment']['SIM_JOBS']);group=set(ORDINARY[1:6]);pids={};peak=group_peak=overlap=0
 for line in (run/'samples.jsonl').read_text().splitlines():
  sample=json.loads(line);alive=[]
  for proc in sample['procs']:
   if proc['argv'] and proc['argv'][0] in ORDINARY:
    assert len(proc['argv'])==1
    pids.setdefault(proc['argv'][0],set()).add(proc['pid'])
    if proc['state']!='Z':alive.append(proc)
  g=sum(proc['argv'][0] in group for proc in alive)
  peak=max(peak,len(alive));group_peak=max(group_peak,g);overlap+=int(g>0 and len(alive)>g)
  assert len(alive)<=jobs and g<=1
 assert set(pids)==set(ORDINARY) and all(len(p)==1 for p in pids.values())
 assert peak==jobs and group_peak==1 and bool(overlap)==(jobs==2)
 assert {p.name:p.read_bytes() for p in (run/'headers-before').iterdir()}=={p.name:p.read_bytes() for p in (run/'headers-after').iterdir()}
 analysis=load(run/'analysis.json');rows.append({'run':run.name,'head':identity['head'],'whole_checks':tally[0],'whole_failures':tally[1],'tallies':len(tally[2]),'render_phase_records':len(records),'per_leg_checks':checks,'per_leg_sha256':captures,'sampled_ordinary_peak':peak,'sampled_group_peak':group_peak,'overlap_samples':overlap,'leg_phase':analysis['leg_phase'],'resources':analysis['summary'],'disk_transcript_sha256':hashlib.sha256(disk).hexdigest()})
result={'same_head':head,'all_input_executable_and_per_leg_bytes_equal':True,'all_23_render_identities_equal':True,'checks':rows}
(out/'measurement-verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'same_head':head,'runs':len(rows),'checks_each':9324,'tallies_each':13,'render_identities_each':23,'equal_bytes':True}))
