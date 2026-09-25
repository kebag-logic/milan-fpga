import hashlib,json,pathlib,re,subprocess,sys
root=pathlib.Path('$LANES/400-403-declaration-truth')
out=pathlib.Path('$MANAGEMENT/2026-09-23/400-403-a323')
path=root/'tb/verilator/nvm_capture_cpu/measurements.json'
receipt=json.loads(path.read_text()); old=json.loads(path.read_text())
runs=json.loads((out/'measurement-runs.json').read_text())
assert len(runs)==6 and all(r['rc']==0 for r in runs)
hashfile=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
receipt['base']=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
receipt['product_firmware_sha256']=hashfile(root/'sw/firmware/milan_baremetal/milan_baremetal.c')
receipt['remeasurement_assignment']='https://github.com/kebag-logic/milan-fpga/issues/400#issuecomment-5838671391'
receipt['measurements']=[]
for run in runs:
 build=pathlib.Path(run['build_dir'])
 arm=json.loads((build/'measurement.json').read_text())
 spec=json.loads((build/'sources.json').read_text())
 cpus=[pathlib.Path(p) for p in spec['sources'] if 'VexiiRiscvLitex_' in p]
 assert len(cpus)==1
 arm.update(clock_role='contract' if arm['cpu_hz']==50000000 else 'non-contract comparison',
  command=run['command'],cpu_netlist_sha256=hashfile(cpus[0]),
  instrumented_firmware_sha256=hashfile(build/'measurement_firmware/milan_baremetal.c'),
  bios_sha256=hashfile(build/'software/bios/bios.bin'))
 receipt['measurements'].append(arm)
sys.path.insert(0,str(root/'tb/verilator/nvm_capture_cpu'))
import run as capture
receipt['maxima']=[]
for shape,clock in sorted({(a['shape'],a['cpu_hz']) for a in receipt['measurements']}):
 group=[a for a in receipt['measurements'] if (a['shape'],a['cpu_hz'])==(shape,clock)]
 worst=capture.maximum_ms(group)
 assert worst<=24.5, 'STOP: limit exceeded'
 receipt['maxima'].append(dict(shape=shape,cpu_hz=clock,maximum_ms=worst,margin=49/worst))
# Keep capture rows compact, matching the existing receipt layout.
text=json.dumps(receipt,indent=2)+'\n'
text=re.sub(r'        \{\n(.*?)\n        \}',lambda m:'        {'+' '.join(s.strip() for s in m[1].splitlines())+'}',text,flags=re.S)
path.write_text(text)
(out/'previous-measurements.json').write_text(json.dumps(old,indent=2)+'\n')
p=root/'docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md'
s=p.read_text()
for before,after in zip(old['maxima'],receipt['maxima']):
 assert (before['shape'],before['cpu_hz'])==(after['shape'],after['cpu_hz'])
 s=s.replace(f"{before['maximum_ms']:.5f}",f"{after['maximum_ms']:.5f}")
 s=s.replace(f"{before['margin']:.4f}x",f"{after['margin']:.4f}x")
worst=next(a['maximum_ms'] for a in receipt['maxima'] if a['shape'].endswith('8x8') and a['cpu_hz']==50000000)
s=s.replace('0.19546 ms below',f'{24.5-worst:.5f} ms below')
s=s.replace('Product firmware, RTL and builder census lists remain unchanged.',
 'The composed product firmware is pinned in the refreshed receipt.\nFirmware and hold behavior are unchanged by this remeasurement.')
s=s.replace('The [round-2 assignment](https://github.com/kebag-logic/milan-fpga/issues/559#issuecomment-5831090112) governs this measurement.',
 'The [round-2 assignment](https://github.com/kebag-logic/milan-fpga/issues/559#issuecomment-5831090112) governs this measurement.\nThe [composition assignment](https://github.com/kebag-logic/milan-fpga/issues/400#issuecomment-5838671391) requires this firmware remeasurement.')
start=s.index('| 1x1 | 50 / 100, contract | ON |',s.index('## 18.'))
end=s.index('\n\n',start)
rows=[]
for a in sorted(receipt['measurements'],key=lambda a:(a['shape'],a['cpu_hz'],a['traffic']=='off')):
 ticks=[r['sys_cycles'] for r in a['rows']]
 shape='8x8' if a['shape'].endswith('8x8') else '1x1'
 role='contract' if a['cpu_hz']==50000000 else 'non-contract'
 rows.append(f"| {shape} | {a['cpu_hz']//1000000} / 100, {role} | {a['traffic'].upper()} | {min(ticks):,} to {max(ticks):,} | {a['minimum_ms']:.5f} to {a['maximum_ms']:.5f} | {a['margin']:.4f}x |")
s=s[:start]+'\n'.join(rows)+s[end:]
def arm(shape,hz,traffic):return next(a for a in receipt['measurements'] if a['shape'].endswith(shape) and a['cpu_hz']==hz and a['traffic']==traffic)['maximum_ms']
d8=arm('8x8',50000000,'on')-arm('8x8',50000000,'off')
d1=arm('1x1_tdm8',50000000,'on')-arm('1x1_tdm8',50000000,'off')
d100=arm('8x8',100000000,'off')-arm('8x8',100000000,'on')
assert d8>0 and d1>0 and d100>0, 'Revise traffic wording for changed sign'
s=s.replace('0.04300 ms',f'{d8:.5f} ms').replace('0.177%',f"{d8/arm('8x8',50000000,'off')*100:.3f}%")
s=s.replace('0.01785 ms (0.271%)',f"{d1:.5f} ms ({d1/arm('1x1_tdm8',50000000,'off')*100:.3f}%)")
s=s.replace('0.78591 ms',f'{d100:.5f} ms')
s=s.replace('   Each has 16 captures per traffic arm, ON and OFF.\n', '   Each has 16 captures per traffic arm, ON and OFF.\n   The [composition remeasurement](#18-cost) covers the declaration changes.\n')
p.write_text(s)
print(json.dumps(receipt['maxima'],indent=2))
