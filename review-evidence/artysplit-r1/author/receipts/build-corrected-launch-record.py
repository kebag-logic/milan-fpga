"""Record this source candidate and start the fresh phase in the handoff."""
import datetime,hashlib,json,re,subprocess
from pathlib import Path
root=Path.cwd();out=Path('$VALIDATION_STORAGE/artysplit-a829/r4/build-corrected')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
refinement=json.loads((out/'refinement.json').read_text())
paths=subprocess.check_output(['git','diff','--name-only','-z'],cwd=root).decode().split('\0')
paths+=subprocess.check_output(['git','ls-files','--others','--exclude-standard','-z'],cwd=root).decode().split('\0')
paths=sorted({p for p in paths if p and not p.startswith('dispatch-build/')})
patch=subprocess.check_output(['git','diff','--binary'],cwd=root)
for p in paths:
 if subprocess.run(['git','ls-files','--error-unmatch',p],cwd=root,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode:
  diff=subprocess.run(['git','diff','--no-index','--binary','/dev/null',p],cwd=root,stdout=subprocess.PIPE)
  assert diff.returncode==1;patch+=diff.stdout
files=[dict(file=p,bytes=(root/p).stat().st_size,sha256=hashlib.sha256((root/p).read_bytes()).hexdigest()) for p in paths]
(out/'source-before-qualification.patch').write_bytes(patch)
record=dict(time=now,head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
 base='854bd7236792ce1adbd10c43b13a6a5002ad3bb6',files=files,
 patch_sha256=hashlib.sha256(patch).hexdigest(),firmware_tree=refinement['firmware_tree'])
(out/'source-before-qualification.json').write_text(json.dumps(record,indent=2)+'\n')
(out.parent/'active-phase.json').write_text(json.dumps(dict(root=str(out),time=now,reason='Complete 145-case calibration closed; measured build and accounting costs applied'),indent=2)+'\n')
(out/'pipeline-launch.json').write_text(json.dumps(dict(time=now,status='FRESH QUALIFICATION LAUNCH',firmware_tree=refinement['firmware_tree'],max_harness_legs=4),indent=2)+'\n')
packet=Path('<home-path>/milan-fpga-management/2026-09-23/artysplit-a829/round4')
handoff=packet/'HANDOFF-r4.md';s=handoff.read_text()
s=re.sub(r'^Status: .*$', 'Status: IN PROGRESS. All 145 calibration cases are closed. The measured build and event-cost corrections are applied; complete fresh firmware, service, boot, identity and docs qualification is starting before routing.',s,count=1,flags=re.M)
s=re.sub(r'^ETA: .*$', 'ETA: approximately 8–14 hours from 2026-11-24 04:45 UTC for fresh qualification, three routing attempts and packaging; host contention or a new finding can extend this.',s,count=1,flags=re.M)
note=('Build-correction checkpoint: firmware tree `'+refinement['firmware_tree']+'`. '
      'The complete calibration measured load 0.4966771140, txL 48.74 ms, last notice 121.84 ms, ACMP 28.82 ms and maximum pass 141157 cycles (1.7644625 ms). '
      'Both-MRPDU build statement 1035 us now selects one MRPDU per 950 us slice; ordinary transmit statement is 30 ms, with pace 9 ms and queued bound 125 ms. '
      'GM 40 us, tick 45 us and transmit notice 205 us are installed. The four original shape blocks and old cost rows remain byte-identical. '
      'These are calibration and source-model results; fresh qualification and routing remain pending.')
s=s.replace('\nIN PROGRESS; no qualified image yet.','\n'+note+'\n\nIN PROGRESS; no qualified image yet.')
handoff.write_text(s)
with (packet/'REPORT.md').open('a') as stream:stream.write('\n\n'+now+'\n\n'+note+'\n')
print(json.dumps(dict(status='RECORDED',files=len(files),firmware_tree=refinement['firmware_tree'],phase=str(out)),indent=2))
