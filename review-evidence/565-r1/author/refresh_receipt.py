import hashlib,json,sys,re,subprocess
from pathlib import Path
root=Path('$LANES/565-8x8-clock')
work=Path('$VALIDATION_STORAGE/565-a344')
harness=root/'tb/verilator/nvm_capture_cpu'
sys.path[:0]=[str(root/'scripts'),str(harness)]
import check_nvm_capture as gate
import run as capture
import recipe
path=harness/'measurements.json'
receipt=json.loads(path.read_text())
def sha(p):
    with p.open('rb') as stream:
        return hashlib.file_digest(stream,'sha256').hexdigest()
measurements=[]
for shape,clock in ((recipe.SHAPES[0],recipe.CPU_HZ),(recipe.SHAPES[1],recipe.CPU_HZ),(recipe.SHAPES[0],100_000_000)):
    for traffic in ('on','off'):
        short=shape.removeprefix('endstation_ax7101_')
        build=work/f'capture-{short}-{clock//1000000}-{traffic}'
        arm=json.loads((build/'measurement.json').read_text())
        spec=json.loads((build/'sources.json').read_text())
        assert arm['captures']==16 and arm['cpu_hz']==clock and arm['traffic']==traffic
        assert 'CAPTURE_DONE' in (build/'capture.log').read_text()
        assert capture.grade_rows(arm['rows'],arm)==arm
        if clock==recipe.CPU_HZ and short=='8x8' and arm['maximum_ms']>24.5:
            raise SystemExit('STOP: 8x8 exceeds 24.5 ms')
        netlists=[Path(s) for s in spec['sources'] if Path(s).name.startswith('VexiiRiscvLitex_')]
        assert len(netlists)==1
        generated=build/'generated'/shape
        arm.update(clock_role='contract' if clock==recipe.CPU_HZ else 'non-contract comparison',
            command=f'unshare -Urn python3 -B tb/verilator/nvm_capture_cpu/run.py --shape {shape} --cpu-hz {clock} --captures 16 --traffic {traffic} --build-dir {build}',
            cpu_netlist_sha256=sha(netlists[0]),
            instrumented_firmware_sha256=sha(build/'measurement_firmware/milan_baremetal.c'),
            bios_sha256=sha(build/'software/bios/bios.bin'),
            gptp_ucode_sha256=sha(generated/'gptp_ucode.hex'),
            config_sha256=sha(root/'configs'/f'{shape}.yaml'))
        measurements.append(arm)
receipt.update(date='2026-09-26',base=subprocess.run(['git','rev-parse','HEAD'],cwd=root,check=True,text=True,capture_output=True).stdout.strip(),
    remeasurement_assignment='https://github.com/kebag-logic/milan-fpga/issues/565#issuecomment-5848231174',
    measured_for=gate.current_inputs(),
    harness_sha256={p.name:sha(p) for p in sorted(harness.iterdir()) if p.suffix in ('.py','.cpp')},
    product_firmware_sha256=sha(root/'sw/firmware/milan_baremetal/milan_baremetal.c'),measurements=measurements)
receipt['maxima']=[]
for shape,clock in sorted({(a['shape'],a['cpu_hz']) for a in measurements}):
    arms=[a for a in measurements if (a['shape'],a['cpu_hz'])==(shape,clock)]
    maximum=capture.maximum_ms(arms)
    receipt['maxima'].append(dict(shape=shape,cpu_hz=clock,maximum_ms=maximum,margin=recipe.HOLD_FLOOR_MS/maximum))
receipt['processor_pins']={n:subprocess.run(['git','rev-parse',f'HEAD:{n}'],cwd=root,check=True,text=True,capture_output=True).stdout.strip() for n in ('protocol-processor','gptp-processor','third_party/verilog-axis')}
gate.check_receipt(receipt,gate.current_inputs())
text=json.dumps(receipt,indent=2)+'\n'
text=re.sub(r'        \{\n          "index":.*?\n        \}',lambda m:'        '+json.dumps(json.loads(m.group(0))),text,flags=re.S)
path.write_text(text)
for a in measurements:
    print(a['shape'],a['cpu_hz'],a['traffic'],min(r['sys_cycles'] for r in a['rows']),max(r['sys_cycles'] for r in a['rows']),a['minimum_ms'],a['maximum_ms'],a['margin'])
print(json.dumps(receipt['maxima'],indent=2))
