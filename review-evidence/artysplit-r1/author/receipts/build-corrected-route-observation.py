"""Read-only progress evidence for the three foreground implementation attempts."""
import datetime,json,re,subprocess
from pathlib import Path
r=Path('$VALIDATION_STORAGE/artysplit-a829/r4/build-corrected')
rows=[]
for name in ('ExtraPostPlacementOpt','AltSpreadLogic_high','ExtraTimingOpt'):
 p=r/'images'/(name+'.log');result=r/'images'/(name+'.result.json')
 data=p.read_text(errors='replace') if p.exists() else ''
 phase='waiting for its turn'
 for token,label in (('Start RTL','synthesis'),('synth_design','synthesis'),('opt_design','optimization'),
                     ('place_design','placement'),('route_design','routing'),('write_bitstream','bitstream'),
                     ('SIGNOFF','signoff')):
  if token in data:phase=label
 row=dict(directive=name,phase=phase,log_bytes=p.stat().st_size if p.exists() else 0)
 if result.exists():row.update(result=json.loads(result.read_text()))
 row['errors']=[line for line in data.splitlines() if line.startswith('ERROR:')][-4:]
 row['slot_admission']=[line for line in data.splitlines() if line.startswith('vivado-slot: slot')][:1]
 rows.append(row)
 mem=int(re.search(r'^MemAvailable:\s+(\d+)',Path('/proc/meminfo').read_text(),re.M)[1])*1024
 record=dict(time=datetime.datetime.now(datetime.timezone.utc).isoformat(),attempts=rows,mem_available_bytes=mem)
 (r/'route-observation.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record))
