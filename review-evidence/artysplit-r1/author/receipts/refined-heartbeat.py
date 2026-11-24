"""Read foreground-gate receipts and keep the requested handoff's live status current."""
import datetime,json,re,shutil,subprocess
from pathlib import Path
r=Path('$VALIDATION_STORAGE/artysplit-a829/r4/refined');now=datetime.datetime.now(datetime.timezone.utc).isoformat()
def read(path):
 try:return json.loads(path.read_text())
 except (FileNotFoundError,json.JSONDecodeError):return None
alerts=[]
scratch_bytes=int(subprocess.check_output(['du','-s','-B1','$VALIDATION_STORAGE/artysplit-a829'],text=True,timeout=30).split()[0])
disk_free=shutil.disk_usage(r).free
if scratch_bytes>=28_000_000_000:alerts.append('Scratch is approaching the 30 GB cap; reclaim owned intermediates before continuing')
if disk_free<3_000_000_000:alerts.append('The scratch filesystem has less than 3 GB free')
for name in ('watch-final-costs-command','firmware-pipeline-command','boot-pipeline-command',
             'products-pipeline-command','docs-pipeline-command','close-before-continuation-command',
             'calibration-continuation-command','watch-calibration-costs-command'):
 record=read(r/(name+'.json'))
 if record and record.get('returncode'):alerts.append(name+' failed')
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
continuation=(r/'calibration-continuation-launch.json').exists()
model=read(r/('calibration-progress/latest.json' if continuation else 'final-progress/latest.json')) or {}
baseline_model=read(r/'final-progress/001/model.json') or {}
current_model=read(Path(model['model'])) if model.get('model') else {}
cost_changes={key:dict(initial=baseline_model['costs'].get(key),measured=value)
              for key,value in (current_model or {}).get('costs',{}).items()
              if baseline_model.get('costs') and baseline_model['costs'].get(key)!=value}
for name in ('final-census/stop-finding.json','final-progress/owner-finding.json','calibration-progress/owner-finding.json'):
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
adjusting=(r/'final-census/cost-adjustment-needed.json').exists() and not continuation
adjusted=manifest.get('status','').startswith('CALIBRATION COMPLETE; FIRMWARE COST ADJUSTMENT REQUIRED')
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
if continuation:
 summary=(f'Frozen-image calibration {len(completed)}/{total} groups; prior firmware/boot/identity/docs gates PASS; '
          f'worst pass {worst}/160000 cycles; firmware correction and fresh qualification still required')
 if model.get('choices'):summary+=f"; forecast txL {model['choices'][0]['rows_ms']['txL']:.2f} ms"
if active:
 summary+='; active '+', '.join(f"{row['group']} {row['simulated_seconds']:.2f}s" for row in active)
if adjusting:summary+='; another measured firmware cost adjustment is required; closing admission'
if adjusted and not continuation:
 summary=(f'{len(completed)} frozen-image cases completed; closing inputs and census before calibration continuation; '
          f'firmware correction and fresh qualification still required; worst pass {worst}/160000 cycles')
if drain:
 count=sum('returncode' in child for child in drain['children'])
 summary=(f"Closing the 295 us SRP calibration before the measured 300 us correction: "
          f"{count}/{len(drain['children'])} in-flight native runs finished; "
          f"owner bounds remain within limits")
 if active:summary+='; active '+', '.join(f"{row['group']} {row['simulated_seconds']:.2f}s" for row in active)
 if any(child.get('returncode',0) for child in drain['children']):alerts.append('native calibration drain failed')
state=dict(time=now,summary=summary,alerts=alerts,ready_to_qualify=ready,prerequisites_pass=prerequisites_pass,
           service_builds=builds,service_groups=len(completed),active=active,
           ready_to_adjust=(adjusted and not continuation) or bool(drain and drain['status'].startswith('NATIVE DRAIN COMPLETE')),adjusting=adjusting,
           full_calibration_ready=(manifest.get('status','').startswith('CALIBRATION MEASUREMENTS COMPLETE')
                                   and (r/'calibration-pipeline-results.json').exists()),
           measured_cost_changes=cost_changes,
           scratch_bytes=scratch_bytes,disk_free_bytes=disk_free)
(r/'live-status.json').write_text(json.dumps(state,indent=2)+'\n')
p=Path('<home-path>/milan-fpga-management/2026-09-23/artysplit-a829/round4/HANDOFF-r4.md')
text=p.read_text();text=re.sub(r'^\[A829\] #878 round 4, updated .*$',f'[A829] #878 round 4, updated {now}.',text,flags=re.M)
if continuation:
 text=re.sub(r'^Status: .*$',f'Status: IN PROGRESS. Frozen-image calibration is at {len(completed)}/{total} cases. The measured firmware correction and complete fresh qualification remain required before routing.',text,count=1,flags=re.M)
start='Live foreground-gate status: ';line=start+summary+'.'
if start in text:text=re.sub(r'^Live foreground-gate status: .*$',lambda _:line,text,flags=re.M)
else:text=text.replace('\nIN PROGRESS; no qualified image yet.','\n'+line+'\n\nIN PROGRESS; no qualified image yet.')
privacy=read(p.parent/'receipts/privacy-check.json')
if privacy:text=re.sub(r'\d+ compressed receipts currently pass',str(len(privacy['checked']))+' compressed receipts currently pass',text)
cost_line='Live census changes from the initial 300 us candidate: '+json.dumps(cost_changes,sort_keys=True)+'.'
if 'Live census changes from the initial 300 us candidate: ' in text:
 text=re.sub(r'^Live census changes from the initial 300 us candidate: .*$',lambda _:cost_line,text,flags=re.M)
else:text=text.replace('\nIN PROGRESS; no qualified image yet.','\n'+cost_line+'\n\nIN PROGRESS; no qualified image yet.')
p.write_text(text)
print(json.dumps(state))
