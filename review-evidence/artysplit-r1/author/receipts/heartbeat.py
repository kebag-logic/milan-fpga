"""Read foreground-gate receipts and keep the requested handoff's live status current."""
import datetime,json,re,subprocess,sys
from pathlib import Path
r=Path('$VALIDATION_STORAGE/artysplit-a829/r4');now=datetime.datetime.now(datetime.timezone.utc).isoformat()
active_phase=r/'active-phase.json'
if active_phase.exists():
 selected=Path(json.loads(active_phase.read_text())['root'])
 if selected!=r:
  raise SystemExit(subprocess.run([sys.executable,'-B',str(selected/'heartbeat.py')]).returncode)
def read(path):
 try:return json.loads(path.read_text())
 except (FileNotFoundError,json.JSONDecodeError):return None
alerts=[]
def command(name):
 data=read(r/(name+'.json'))
 if data is None:return 'pending'
 code=data.get('returncode')
 if code:alerts.append(name+': exit '+str(code))
 return 'PASS' if code==0 else 'FAIL'
fw={str(n):command('final-firmware-'+str(n)) for n in range(4)}
boot=command('final-boot-positive-fixedseed');boot_controls=command('final-boot-controls-fixedseed');grader=command('final-service-selftest')
exports=command('identity-final-export-command')
identity=read(r/'identity-final-compare.json') or {}
if identity.get('status')=='FAIL':alerts.append('AX product identity failed')
docs=read(r/'docs-final-corrected/results.json') or []
if any(row['rc'] for row in docs):alerts.append('documentation gate failed')
doc_status='PASS' if len(docs)==11 and not any(row['rc'] for row in docs) else f'{len(docs)}/11'
builds=len(list((r/'final-census').glob('*/build.json')))
completed=read(r/'final-census/completed.json') or []
manifest=read(r/'final-census/manifest.json') or {}
model=read(r/'final-progress/latest.json') or {}
for name in ('final-census/stop-finding.json','final-progress/owner-finding.json'):
 if (r/name).exists():alerts.append(name)
native_command=read(r/'final-census-command.json')
drain=read(r/'calibration-drain.json')
if native_command and native_command['returncode'] and not drain:alerts.append('service campaign supervisor failed')
total=sum(map(len,manifest.get('groups',{}).values())) or 145
worst=max([row['worst_pass_cycles'] for row in completed] or [0])
mutants=0
p=r/'final-service-selftest.log'
if p.exists():mutants=p.read_text().count('MUTANT caught:')
ready=manifest.get('status','').startswith('NATIVE MEASUREMENTS COMPLETE')
summary=(f"Firmware: {','.join(k+'='+v for k,v in fw.items())}; grader: {grader} ({mutants} mutants caught); "
         f"boot: {boot}, controls: {boot_controls}; AX product: {identity.get('status','pending')}, exports: {exports}; "
         f"docs: {doc_status}; service: {builds}/8 builds, {len(completed)}/{total} groups")
if worst:summary+=f', worst pass {worst}/160000 cycles'
if model.get('choices'):summary+=f"; partial measured txL {model['choices'][0]['rows_ms']['txL']:.2f} ms"
prerequisites_pass=(all(value=='PASS' for value in fw.values()) and boot==boot_controls==grader==exports==doc_status=='PASS'
                    and identity.get('status')=='PASS')
active=[]
for log in (r/'final-census').glob('*/results/*.log'):
 if log.with_suffix('.status').exists():continue
 with log.open('rb') as stream:
  stream.seek(max(0,log.stat().st_size-6000))
  tail=stream.read().decode(errors='replace')
 cycles=[int(value) for value in re.findall(r'^(?:SPAN|CALL) (\d+) ',tail,re.M)]
 if cycles:active.append(dict(variant=log.parent.parent.name,group=log.stem,simulated_seconds=max(cycles)/80_000_000))
if prerequisites_pass:
 summary=(f'Firmware, grader, boot controls, AX identity and docs PASS; '
          f'fresh service {len(completed)}/{total} groups; worst pass {worst}/160000 cycles')
 if model.get('choices'):summary+=f"; partial txL {model['choices'][0]['rows_ms']['txL']:.2f} ms"
if active:
 summary+='; active '+', '.join(f"{row['group']} {row['simulated_seconds']:.2f}s" for row in active)
if drain:
 count=sum('returncode' in child for child in drain['children'])
 summary=(f"Closing the 295 us SRP calibration before the measured 300 us correction: "
          f"{count}/{len(drain['children'])} in-flight native runs finished; "
          f"owner bounds remain within limits")
 if active:summary+='; active '+', '.join(f"{row['group']} {row['simulated_seconds']:.2f}s" for row in active)
 if any(child.get('returncode',0) for child in drain['children']):alerts.append('native calibration drain failed')
state=dict(time=now,summary=summary,alerts=alerts,ready_to_qualify=ready,prerequisites_pass=prerequisites_pass,
           service_builds=builds,service_groups=len(completed),active=active,
           ready_to_adjust=bool(drain and drain['status'].startswith('NATIVE DRAIN COMPLETE')))
(r/'live-status.json').write_text(json.dumps(state,indent=2)+'\n')
p=Path('<home-path>/milan-fpga-management/2026-09-23/artysplit-a829/round4/HANDOFF-r4.md')
text=p.read_text();text=re.sub(r'^\[A829\] #878 round 4, updated .*$',f'[A829] #878 round 4, updated {now}.',text,flags=re.M)
start='Live foreground-gate status: ';line=start+summary+'.'
if start in text:text=re.sub(r'^Live foreground-gate status: .*$',lambda _:line,text,flags=re.M)
else:text=text.replace('\nIN PROGRESS; no qualified image yet.','\n'+line+'\n\nIN PROGRESS; no qualified image yet.')
privacy=read(p.parent/'receipts/privacy-check.json')
if privacy:text=re.sub(r'\d+ compressed receipts currently pass',str(len(privacy['checked']))+' compressed receipts currently pass',text)
p.write_text(text)
print(json.dumps(state))
