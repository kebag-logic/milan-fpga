"""Publish the complete service result in the repository, then gate those docs.

Run only after the full fresh qualification succeeds. No firmware is changed.
"""
import datetime,hashlib,json,os,re,subprocess,sys,time
from pathlib import Path
root=Path.cwd();r=Path('$VALIDATION_STORAGE/artysplit-a829/r4/build-corrected')
qualified=json.loads((r/'final-census/qualification.json').read_text())
assert qualified['status']=='PASS' and qualified['groups']==145
assert all(value=='PASS' for value in qualified['checks'].values())
measured=json.loads((r/'final-census/derived-model.json').read_text())
assert measured['choices'] and not measured['choices'][0]['owner_findings']
sys.path.insert(0,str(root/'tb/verilator/ctrl_service_budget'));import build
firmware_tree=build.tree_digest([root/p for p in build.FIRMWARE_TREES])
assert firmware_tree==json.loads((r/'refinement.json').read_text())['firmware_tree']
out=r/'docs-after-service';assert not out.exists();out.mkdir()
changes=[]
def write(name,transform):
 path=root/name;before=path.read_bytes();after=transform(before.decode()).encode()
 assert before!=after,name;path.write_bytes(after)
 changes.append(dict(file=name,before_sha256=hashlib.sha256(before).hexdigest(),after_sha256=hashlib.sha256(after).hexdigest()))
def design(text):
 before,section=text.split('## 15. Arty split at 80 MHz\n',1)
 a=('The complete 80 MHz calibration gives the following statements; fresh images\n'
    'with these constants must pass the complete measurement campaign.')
 b=('The complete 80 MHz campaign qualifies these statements over 145 native cases\n'
    'across eight image variants. The seven held-egress misses remain recorded\n'
    'under their ledger; every other service row meets its bound.')
 assert section.count(a)==1;section=section.replace(a,b)
 cold,attempt,notice=measured['retry_raw_cycles'];choice=measured['choices'][0]
 section=re.sub(r'The retry fit measures .*? before applying the cost rule\.',
  f'The retry fit measures {cold:g} cycles cold, {attempt:g} cycles per refused attempt and\n'
  f'{notice:g} cycles per notice before applying the cost rule.',section,flags=re.S,count=1)
 cycles=qualified['worst_pass']['worst_pass_cycles']
 section=re.sub(r'The slice and pace rules give load .*? ms at 80 MHz\.',
  f"The slice and pace rules give load {measured['load']:.10f}, txL {choice['rows_ms']['txL']:.2f} ms, last notice\n"
  f"{choice['rows_ms']['last']:.2f} ms and ACMP {choice['rows_ms']['ACMP']:.2f} ms.\n"
  f'The observed maximum whole pass in the fresh qualification is {cycles} cycles,\n'
  f'or {cycles/80000:.7f} ms at 80 MHz.',section,flags=re.S,count=1)
 return before+'## 15. Arty split at 80 MHz\n'+section
write('docs/design/SPLIT_CONTROL_MEMORY.md',design)
def builder(text):
 a='The 80 MHz costs, slice and pace remain under qualification.'
 assert text.count(a)==1
 return text.replace(a,'The 80 MHz costs, slice and pace pass the complete service campaign.\n'
                       '[Section 15](design/SPLIT_CONTROL_MEMORY.md#15-arty-split-at-80-mhz) records their measured basis and memory ledger.')
write('docs/ENDSTATION_BUILDER.md',builder)
def integration(text):
 a='The scheduler costs, slice and pace remain under qualification.\nNo routed image or flash layout is qualified yet.'
 b=('The scheduler costs, slice and pace pass the complete 80 MHz service campaign.\n'
    '[Section 15](../design/SPLIT_CONTROL_MEMORY.md#15-arty-split-at-80-mhz) records the measurements and the Arty memory ledger.\n'
    'Each routed image needs its own timing and identity evidence.\n'
    'For this split image, #878 applies the #818 floor: WNS at least +0.030 ns\n'
    'and WHS at least zero in all four signoff reports.\n'
    'Select the best worst-corner WNS from three placement directives.\n'
    'Hardware checks follow image qualification.')
 assert text.count(a)==1;text=text.replace(a,b)
 a='   The retired Arty recipe retains its WNS >= 0 rule.'
 b=('   The retired all-fabric Arty recipe retains its WNS >= 0 rule.\n'
    '   The Arty split image in #878 uses the +0.030 ns WNS and nonnegative WHS\n'
    '   floor at all four signoff reports, with the same best-of-three selection.')
 assert text.count(a)==1;return text.replace(a,b)
write('docs/integration/BUILDING.md',integration)
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(r/'work-tmp'))
records=[]
commands=[row['command'] for row in json.loads((r/'docs/results.json').read_text())]
for number,argv in enumerate(commands):
 log=out/f'{number:02d}-{Path(argv[1]).stem}.log';start=time.monotonic()
 with log.open('w') as stream:process=subprocess.run(argv,cwd=root,env=env,stdout=stream,stderr=subprocess.STDOUT,timeout=3600)
 records.append(dict(command=argv,rc=process.returncode,seconds=round(time.monotonic()-start,3),log=log.name))
 (out/'results.json').write_text(json.dumps(records,indent=2)+'\n')
 print('DOC',number,process.returncode,flush=True)
assert build.tree_digest([root/p for p in build.FIRMWARE_TREES])==firmware_tree
record=dict(status='PASS' if not any(row['rc'] for row in records) else 'FAIL',
 time=datetime.datetime.now(datetime.timezone.utc).isoformat(),firmware_tree=firmware_tree,changes=changes,results=records,
 qualification_sha256=hashlib.sha256((r/'final-census/qualification.json').read_bytes()).hexdigest())
(r/'final-service-documentation.json').write_text(json.dumps(record,indent=2)+'\n')
raise SystemExit(record['status']!='PASS')
