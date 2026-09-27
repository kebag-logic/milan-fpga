"""Update timing prose from the freshly assembled capture receipt."""
import json
from pathlib import Path

receipt=json.loads(Path('tb/verilator/nvm_capture_cpu/measurements.json').read_text())
assert receipt['base']=='499b15f97eb0a469b7cd1308fbba7af3c64d1851'
old=json.loads((Path(__file__).parent/'old-measurements.json').read_text())
p=Path('docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md')
s=p.read_text()
s=s.replace('Timing. MEASURED on 2026-09-26 in the', 'Timing. MEASURED on '+receipt['date']+' in the')
anchor='The [clock assignment](https://github.com/kebag-logic/milan-fpga/issues/565#issuecomment-5848231174) requires this configuration remeasurement.'
assert s.count(anchor)==1
s=s.replace(anchor, '\n'.join([
 'The [clock assignment](https://github.com/kebag-logic/milan-fpga/issues/565#issuecomment-5848231174) set both configurations to the contract clock.',
 'The [pin-adoption assignment](https://github.com/kebag-logic/milan-fpga/issues/580#issuecomment-5857045698) requires this remeasurement.',
 'The measured parent commit is `'+receipt['base']+'`.',
 'Its tree is `'+receipt['tree']+'`.',
 'Its protocol-processor pin is `'+receipt['processor_pins']['protocol-processor']+'`.']))
for before,after in zip(old['maxima'],receipt['maxima']):
 assert (before['shape'],before['cpu_hz'])==(after['shape'],after['cpu_hz'])
 s=s.replace(f"{before['maximum_ms']:.5f}",f"{after['maximum_ms']:.5f}")
 s=s.replace(f"{before['margin']:.4f}x",f"{after['margin']:.4f}x")
peak=next(x['maximum_ms'] for x in receipt['maxima'] if x['shape'].endswith('8x8') and x['cpu_hz']==50000000)
s=s.replace('0.19754 ms below',f'{24.5-peak:.5f} ms below')
start=s.index('| Shape | CPU / system MHz, basis | Traffic | System ticks, minimum to maximum |')
end=s.index('\n\nThe full closed-record census',start)
rows=['| Shape | CPU / system MHz, basis | Traffic | System ticks, minimum to maximum | Elapsed ms, minimum to maximum | 49 ms / arm maximum |','|---|---|---|---|---|---|']
measurements=receipt['measurements']
for shape,clock in [('endstation_ax7101_1x1_tdm8',50000000),('endstation_ax7101_8x8',50000000),('endstation_ax7101_8x8',100000000)]:
 for arm in ('on','off'):
  m=next(x for x in measurements if (x['shape'],x['cpu_hz'],x['traffic'])==(shape,clock,arm))
  label='8x8' if shape.endswith('8x8') else '1x1'
  ticks=[r['sys_cycles'] for r in m['rows']]
  basis='contract' if clock==50000000 else 'non-contract'
  rows.append(f"| {label} | {clock//1000000} / 100, {basis} | {arm.upper()} | {min(ticks):,} to {max(ticks):,} | {m['minimum_ms']:.5f} to {m['maximum_ms']:.5f} | {m['margin']:.4f}x |")
s=s[:start]+'\n'.join(rows)+s[end:]
def maxima(shape,clock):
 return {x['traffic']:x['maximum_ms'] for x in measurements if x['shape']==shape and x['cpu_hz']==clock}
a=maxima('endstation_ax7101_8x8',50000000)
b=maxima('endstation_ax7101_1x1_tdm8',50000000)
c=maxima('endstation_ax7101_8x8',100000000)
assert a['on']>a['off'] and b['on']>b['off'] and c['on']<c['off']
s=s.replace('0.04092 ms',f"{a['on']-a['off']:.5f} ms").replace('0.169%',f"{(a['on']/a['off']-1)*100:.3f}%")
s=s.replace('0.01785 ms (0.271%)',f"{b['on']-b['off']:.5f} ms ({(b['on']/b['off']-1)*100:.3f}%)")
s=s.replace('0.78591 ms',f"{c['off']-c['on']:.5f} ms")
p.write_text(s)
p=Path('CHANGELOG.md');s=p.read_text()
anchor='- The capture receipt refreshes its pin.\n- Measured inputs remain unchanged.'
assert s.count(anchor)==1
s=s.replace(anchor,'- The capture was re-measured at the adopted processor pin.\n- The receipt identifies the measured parent tree and processor pins.\n- All six points contain 16 captures per traffic arm.\n- The 8x8 maximum remains below 24.5 ms.')
s=s.replace('All six points contain 16 captures per traffic arm.', 'Each of the six traffic arms contains 16 captures.')
p.write_text(s)
print('Updated snapshot section 18 and changelog from completed measurements')
