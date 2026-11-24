"""Apply the complete 80 MHz census after closing all frozen calibration inputs."""
import datetime,hashlib,json,math,re,shutil,subprocess,sys
from pathlib import Path
root=Path.cwd();old=Path('$VALIDATION_STORAGE/artysplit-a829/r4/refined');out=old.parent/'build-corrected'
assert root==Path('$LANES/arty-split') and not (out/'refinement.json').exists()
closure=json.loads((old/'calibration-complete-closure.json').read_text())
assert closure['groups']==145 and closure['status'].startswith('COMPLETE CALIBRATION INPUTS CLOSED')
sys.path.insert(0,str(root/'tb/verilator/ctrl_service_budget'))
import build
assert build.tree_digest([root/p for p in build.FIRMWARE_TREES])==closure['firmware_tree']
for path in Path('/proc').glob('[0-9]*/cmdline'):
 try:exe=path.read_bytes().split(b'\0')[0]
 except OSError:continue
 assert not (exe.startswith(b'$VALIDATION_STORAGE/artysplit-a829/') and exe.endswith(b'/native/Vsim')),exe
model=json.loads((old/'calibration-complete-model.json').read_text())
choice=model['choices'][0];costs=model['costs']
assert not choice['owner_findings'] and model['cpu_hz']==80_000_000
assert (choice['slice_us'],choice['pace_ms'],choice['queued_ms'])==(950,9,125)
assert model['retry_us']==[125,30,230]
assert costs['build']==1035 and costs['build_one']==660 and costs['record.srp']==300
assert costs['event.GM']==40 and costs['event.TICK']==45 and costs['item.aecp.notice']==205
assert costs['step']==1060 and costs['centisecond']==150
changes={};before={};after={}
def write(name,transform):
 p=root/name;s=p.read_text();before[name]=hashlib.sha256(p.read_bytes()).hexdigest()
 text=transform(s);assert text!=s,name;p.write_text(text)
 after[name]=hashlib.sha256(p.read_bytes()).hexdigest()
def header(s):
 start=s.index('#elif CTRL_LOOP_SHAPE(1u, 1u, 2u)');end=s.index('#else',start)
 own=s[start:end]
 for name,prior,wanted in [('CTRL_LOOP_BUILD_PASS_US',830,costs['build']),
                           ('CTRL_LOOP_TX_MS',34,math.ceil(choice['rows_ms']['tx']-1e-9))]:
  a=f'#define {name} {prior}u';b=f'#define {name} {wanted}u';assert own.count(a)==1
  own=own.replace(a,b);changes[name]={'old':prior,'new':wanted}
 text=s[:start]+own+s[end:]
 before='// harness; 100 cycles a microsecond). A pass given whole to an aged step, to a'
 after='// harness; 100 cycles a microsecond on AX7101, 80 on Arty). A pass given whole\n// to an aged step, to a'
 assert text.count(before)==1
 return text.replace(before,after)
write('sw/firmware/ctrl/loop/ctrl_loop.h',header)
def load(s):
 lines=s.splitlines(keepends=True);hits=0
 for i,line in enumerate(lines):
  if line.startswith("    'arty-1x1': {'record.srp':"):
   for key,prior in [('event.GM',35),('event.TICK',35),('item.aecp.notice',200)]:
    a=f"'{key}': {prior}";b=f"'{key}': {costs[key]}";assert line.count(a)==1
    line=line.replace(a,b);changes[key]={'old':prior,'new':costs[key]}
   lines[i]=line;hits+=1
 assert hits==2;return ''.join(lines)
write('tb/verilator/ctrl_service_budget/load_grade.py',load)
def docs(s):
 before,section=s.split('## 15. Arty split at 80 MHz\n',1)
 section=section.replace('bound and a 34 ms ordinary transmit bound.',
                         f"bound and a {math.ceil(choice['rows_ms']['tx']-1e-9)} ms ordinary transmit bound.")
 section=section.replace('| Both MRPDU builds | 830 |',f"| Both MRPDU builds | {costs['build']} |")
 section=section.replace('| Transmit notice | 200 |',f"| Transmit notice | {costs['tx.aecp.notice']} |")
 section=section.replace('Its 80 MHz calibration gives the following statements; fresh images',
                         'The complete 80 MHz calibration gives the following statements; fresh images')
 section=section.replace('with these constants must pass the complete measurement campaign.',
  'with these constants must pass the complete measurement campaign.\n'
  'The measured build of both MRPDUs exceeds the slice, so the existing scheduler\n'
  'builds one MRPDU per pass at this point.')
 cold,attempt,notice=model['retry_raw_cycles']
 section=re.sub(r'The retry fit measures .*? before applying the cost rule\.',
  f'The retry fit measures {cold:g} cycles cold, {attempt:g} cycles per refused attempt and\n'
  f'{notice:g} cycles per notice before applying the cost rule.',section,flags=re.S,count=1)
 section=re.sub(r'The slice and pace rules give load .*? ms at 80 MHz\.',
  f"The slice and pace rules give load {model['load']:.10f}, txL {choice['rows_ms']['txL']:.2f} ms, last notice\n"
  f"{choice['rows_ms']['last']:.2f} ms and ACMP {choice['rows_ms']['ACMP']:.2f} ms.\n"
  f"The observed maximum whole pass in the calibration is {closure['worst_pass']['worst_pass_cycles']} cycles,\n"
  f"or {closure['worst_pass']['worst_pass_cycles']/80000:.7f} ms at 80 MHz.",section,flags=re.S,count=1)
 return before+'## 15. Arty split at 80 MHz\n'+section
write('docs/design/SPLIT_CONTROL_MEMORY.md',docs)
for src,dst in [('calibration-complete-census.json','census-preliminary-complete.json'),
                ('calibration-complete-model.json','model-calibration.json')]:
 shutil.copy2(old/src,out/dst)
import arty_grade
installed,findings=arty_grade.inspect(root);assert not findings,findings
assert abs(installed['load']-model['load'])<=1e-12
assert all(abs(installed['rows_ms'][key]-value)<=1e-12 for key,value in choice['rows_ms'].items())
subprocess.run([sys.executable,'-B',str(out/'check-old-rows.py')],check=True,cwd=root)
record=dict(status='APPLIED; FRESH QUALIFICATION REQUIRED',time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
 changes=changes,before=before,after=after,firmware_tree=build.tree_digest([root/p for p in build.FIRMWARE_TREES]),
 model=installed,calibration=str(old/'calibration-complete-closure.json'))
(out/'refinement.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
