"""Assemble a receipt from completed, independently graded capture runs."""
from datetime import datetime, timezone
import hashlib
import json
import re
from pathlib import Path
import subprocess
import sys

OUT = Path(__file__).resolve().parent
ROOT = Path.cwd()
HARNESS = ROOT/'tb/verilator/nvm_capture_cpu'
sys.path[:0] = [str(ROOT/'scripts'), str(HARNESS)]
import check_nvm_capture as checker
import run as capture

old = json.loads((OUT/'old-measurements.json').read_text())
identity = json.loads((OUT/'measured-tree.json').read_text())
environment = json.loads((OUT/'environment.json').read_text())
assert subprocess.check_output(['rtk','proxy','git','rev-parse','HEAD'],text=True).strip() == identity['base']
assert subprocess.check_output(['rtk','proxy','git','rev-parse',identity['base']+'^{tree}'],text=True).strip() == identity['tree']
for name,pin in identity['processor_pins'].items():
    assert subprocess.check_output(['rtk','proxy','git','rev-parse',identity['base']+':'+name],text=True).strip() == pin

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

receipt = dict(old)
receipt.update(date=datetime.now(timezone.utc).date().isoformat(),
               base=identity['base'], tree=identity['tree'],
               processor_pins=identity['processor_pins'],
               product_firmware_sha256=digest(ROOT/'sw/firmware/milan_baremetal/milan_baremetal.c'),
               harness_sha256={p.name:digest(p) for p in HARNESS.iterdir() if p.suffix in ('.py','.cpp')},
               measured_for=checker.current_inputs(),
               remeasurement_assignment='https://github.com/kebag-logic/milan-fpga/issues/580#issuecomment-5857045698')
receipt['soc_component_revisions']={name:environment[name] for name in
    ['litex','migen','litedram','liteeth','litespi','litex-boards','pythondata-cpu-vexiiriscv']}
receipt['cpu_generator_revision']=environment['cpu_generator_revision']
receipt['reproduction_environment']={
    'LITEX_ENV_CC_TRIPLE':'SDK compiler prefix, without -gcc; compiler recorded above', 'PYTHONHASHSEED':'0',
    'COURSIER_MODE':'offline', 'SBT_OPTS':'-Dsbt.offline=true',
    'PATH':'SDK bin first, then product environment and host utilities',
    'PRODUCT_PYTHON':'absolute path to the product environment interpreter',
    'PYTHON':'same interpreter as PRODUCT_PYTHON, used for BIOS post-processing'}
receipt['provenance']='base, tree and processor_pins identify the source measured by all six runs.'
receipt['measurements']=[]
artifacts={}
for shape,mhz,arm in [('8x8',50,'on'),('8x8',50,'off'),('1x1',50,'on'),('1x1',50,'off'),('8x8',100,'on'),('8x8',100,'off')]:
    name=f'capture-{shape}-{mhz}-{arm}'
    gate=json.loads((OUT/(name+'.json')).read_text())
    assert gate['rc']==0,gate
    build=Path(gate['command'][gate['command'].index('--build-dir')+1])
    summary=json.loads((build/'measurement.json').read_text())
    spec=json.loads((build/'sources.json').read_text())
    assert capture.grade_rows(summary['rows'],spec)==summary
    assert summary['captures']==16
    netlists=[Path(p) for p in spec['sources'] if Path(p).name.startswith('VexiiRiscvLitex_')]
    assert len(netlists)==1
    summary.update(clock_role='contract' if mhz==50 else 'non-contract comparison',
        command=f'unshare -Urn "$PRODUCT_PYTHON" -B tb/verilator/nvm_capture_cpu/run.py --shape {summary["shape"]} --cpu-hz {summary["cpu_hz"]} --captures 16 --traffic {arm} --build-dir {build}',
        cpu_netlist_sha256=digest(netlists[0]),
        instrumented_firmware_sha256=digest(build/'measurement_firmware/milan_baremetal.c'),
        bios_sha256=digest(build/'software/bios/bios.bin'),
        gptp_ucode_sha256=digest(build/'generated'/summary['shape']/'gptp_ucode.hex'),
        config_sha256=digest(ROOT/'configs'/(summary['shape']+'.yaml')))
    receipt['measurements'].append(summary)
    small = ['capture.log','measurement.json','sources.json']
    large = ['gateware/sim.v','native/Vsim','software/bios/bios.bin','measurement_firmware/milan_baremetal.c']
    for leaf in small+large:
        p=build/leaf
        artifacts[name+'/'+leaf]=dict(bytes=p.stat().st_size,sha256=digest(p))
        if leaf in small and p.stat().st_size<=200000:
            (OUT/(name+'-'+p.name)).write_bytes(p.read_bytes())
receipt['maxima']=[]
for shape,clock in sorted({(x['shape'],x['cpu_hz']) for x in receipt['measurements']}):
    group=[x for x in receipt['measurements'] if (x['shape'],x['cpu_hz'])==(shape,clock)]
    worst=capture.maximum_ms(group)
    assert worst<=24.5, 'STOP: report timing limit on issue #580'
    receipt['maxima'].append(dict(shape=shape,cpu_hz=clock,maximum_ms=worst,margin=49/worst))
checker.check_receipt(receipt,checker.current_inputs())
(OUT/'capture-artifacts.json').write_text(json.dumps(artifacts,indent=2)+'\n')
encoded=json.dumps(receipt,indent=2)
encoded=re.sub(r'\{\n\s+"index":.*?\n\s+\}', lambda match: json.dumps(json.loads(match.group(0))), encoded, flags=re.S)
(HARNESS/'measurements.json').write_text(encoded+'\n')
print(json.dumps(receipt['maxima'],indent=2))
