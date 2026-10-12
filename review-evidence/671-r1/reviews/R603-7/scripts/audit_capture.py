#!/usr/bin/env python3
"""Reconcile six public executed capture arms with the committed receipt."""
import hashlib,json,pathlib,subprocess,sys
R=pathlib.Path(sys.argv[1]).resolve();P=pathlib.Path(__file__).resolve().parents[1]
r=json.loads((R/'tb/verilator/nvm_capture_cpu/measurements.json').read_text())
assert r['base']=='44416838b90c40536a2104ab1f2bd4ff02268bec'
assert r['tree']==subprocess.check_output(['git','rev-parse',r['base']+'^{tree}'],cwd=R,text=True).strip()
assert r['product_firmware_sha256']==hashlib.sha256((R/'sw/firmware/milan_baremetal/milan_baremetal.c').read_bytes()).hexdigest()
old=json.loads(subprocess.check_output(['git','show','c7d0ad63:tb/verilator/nvm_capture_cpu/measurements.json'],cwd=R))
for arm in r['measurements']:
 tag=('1x1' if '1x1' in arm['shape'] else '8x8')+'-'+str(arm['cpu_hz']//1000000)+'-'+arm['traffic']
 raw=json.loads((P/'receipts/public'/f'capture__{tag}__measurement.json').read_text())
 assert all(arm[k]==v for k,v in raw.items()),tag
 log=(P/'receipts/public'/f'capture__run-{tag}.log').read_text()
 decoder=json.JSONDecoder();candidates=[]
 for pos,c in enumerate(log):
  if c=='{':
   try:
    obj,_=decoder.raw_decode(log[pos:])
    if isinstance(obj,dict) and 'rows' in obj:candidates.append(obj)
   except ValueError:pass
 assert raw in candidates,tag
 assert len(arm['rows'])==16
 assert arm['config_sha256']==hashlib.sha256((R/'configs'/(arm['shape']+'.yaml')).read_bytes()).hexdigest()
 previous=next(x for x in old['measurements'] if (x['shape'],x['cpu_hz'],x['traffic'])==(arm['shape'],arm['cpu_hz'],arm['traffic']))
 assert [x['sys_cycles'] for x in arm['rows']]==[x['sys_cycles'] for x in previous['rows']]
 assert arm['instrumented_firmware_sha256']==previous['instrumented_firmware_sha256']
 assert arm['bios_sha256']==previous['bios_sha256']
 print(tag,'16 exact public rows; min/max ms',arm['minimum_ms'],arm['maximum_ms'])
print('Firmware SHA256',r['product_firmware_sha256'])
for x in r['maxima']:print('MAX',x['shape'],x['cpu_hz'],x['maximum_ms'],'margin to 24.5 ms',24.5-x['maximum_ms'],'floor ratio',49/x['maximum_ms'])
print('PASS: all 96 committed rows equal public run summaries; six exact per-arm receipts')
