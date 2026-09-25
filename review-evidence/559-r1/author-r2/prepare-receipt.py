from pathlib import Path
import hashlib,json,shutil,subprocess,sys,textwrap
root=Path.cwd()
harness=root/'tb/verilator/nvm_capture_cpu'
sys.path.insert(0,str(root/'scripts'))
import check_nvm_capture as gate
out=Path(__file__).parent
old=json.loads(subprocess.check_output(['git','show','32076148:tb/verilator/nvm_capture_cpu/measurements.json']))
receipt={k:v for k,v in old.items() if k not in ('measurements','harness_sha256','python_hash_seed')}
receipt['assignment']='https://github.com/kebag-logic/milan-fpga/issues/559#issuecomment-5831090112'
receipt['python_hash_seed']='0'
receipt['phase']='CPU rising edges aligned with sys; audio starts at half-period'
receipt['hold_floor_ms']=49
receipt['measured_for']=gate.current_inputs()
receipt['harness_sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(harness.iterdir()) if p.suffix in ('.py','.cpp')}
receipt['measurements']=[]
for name in ['8x8-50-on','8x8-50-off','1x1-50-on','1x1-50-off','8x8-100-on','8x8-100-off']:
 b=Path('$VALIDATION_STORAGE/559-a309-'+name)
 spec=json.loads((b/'sources.json').read_text())
 # Regrade raw logs with the final grader; it verifies all 16 captures.
 gate.capture._grade(b,spec,0)
 item=json.loads((b/'measurement.json').read_text())
 item['clock_role']='contract' if item['cpu_hz']==gate.recipe.CPU_HZ else 'non-contract comparison'
 item['command']=f"python3 tb/verilator/nvm_capture_cpu/run.py --shape {item['shape']} --cpu-hz {item['cpu_hz']} --captures 16 --traffic {item['traffic']} --build-dir /tmp/nvm-capture-{name}"
 cpu=[Path(s) for s in spec['sources'] if 'VexiiRiscvLitex_' in s]
 assert len(cpu)==1
 item['cpu_netlist_sha256']=hashlib.sha256(cpu[0].read_bytes()).hexdigest()
 item['instrumented_firmware_sha256']=hashlib.sha256((b/'measurement_firmware/milan_baremetal.c').read_bytes()).hexdigest()
 item['bios_sha256']=hashlib.sha256((b/'software/bios/bios.bin').read_bytes()).hexdigest()
 receipt['measurements'].append(item)
 for leaf in ('capture.log','measurement.json'):
  shutil.copy2(b/leaf,out/(name+'-'+leaf))
receipt['maxima']=[]
for shape,hz in sorted({(a['shape'],a['cpu_hz']) for a in receipt['measurements']}):
 arms=[a for a in receipt['measurements'] if (a['shape'],a['cpu_hz'])==(shape,hz)]
 worst=gate.capture.maximum_ms(arms)
 receipt['maxima'].append(dict(shape=shape,cpu_hz=hz,maximum_ms=worst,margin=49/worst))
gate.check_receipt(receipt,receipt['measured_for'])
text=json.dumps(receipt,indent=2)
for arm in receipt['measurements']:
 for row in arm['rows']:
  text=text.replace(textwrap.indent(json.dumps(row,indent=2),'        '),'        '+json.dumps(row))
(harness/'measurements.json').write_text(text+'\n')
print('RECEIPT COMPLETE',receipt['maxima'])
