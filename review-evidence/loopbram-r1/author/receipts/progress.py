from pathlib import Path
import json,re,time
p=Path('$SCRATCH/route/endstation_ax7101_1x1_tdm8/gateware')
complete=[]
for x in sorted(p.glob('**/measure_*.log')):
 result=x.with_suffix('.json')
 if result.exists():
  d=json.loads(result.read_text());complete.append(f"{x.parent.name if x.parent!=p else 'synthesis'}: exit {d['exit']}");continue
 lines=x.read_text(errors='replace').splitlines()
 stages=[l for l in lines if re.search(r'^Start |^Finished |^Phase |^Ending |^ERROR:|Exiting Vivado|Design Timing Summary',l)]
 print(str(x.relative_to(p)),f'{x.stat().st_size} bytes; updated {time.time()-x.stat().st_mtime:.0f}s ago')
 print('\n'.join(stages[-3:]))
print('Completed:', '; '.join(complete))
