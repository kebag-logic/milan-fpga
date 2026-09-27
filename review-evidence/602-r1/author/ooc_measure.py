"""Measure the two AX shapes using the repository OOC flow and shaped defaults."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path('$LANES/602-phc-step-mr')
WORK = Path('$VALIDATION_STORAGE/602-a383-work')
OUT = Path(__file__).resolve().parent
phase = sys.argv[1]
assert phase in ('before', 'after', 'neutral')
head = subprocess.check_output(['rtk', 'proxy', 'git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
base = '6d5ebd7357c1e468e446f18a61527c5be6118a04'
base_source = subprocess.check_output(['rtk', 'proxy', 'git', 'show', base + ':hdl/milan/milan_datapath.sv'], cwd=ROOT, text=True)
assert (WORK/'base-datapath.sv').read_text() == base_source
source = base_source if phase in ('before', 'neutral') else (ROOT/'hdl/milan/milan_datapath.sv').read_text()
control = None
if phase == 'neutral':
    old, new = 'tkd_crflk_q_r', 'tkd_crf_lock_prev_r'
    assert new not in source
    source, count = re.subn(r'\b' + old + r'\b', new, source)
    assert count == 4, count
    assert re.sub(r'\b' + new + r'\b', old, source) == base_source
    control = dict(kind='local wire/register identifier rename only', old=old, new=new, references=count,
                   inverse_rename_byte_identical=True)

common = dict(MILAN_CLK_FREQ_HZ=50000000, TALKER_WIRE_CHANS_P=8,
              AUDIO_IF_MASTER_P=1, GPTP_INGRESS_LAT_NS_P=656, GPTP_EGRESS_LAT_NS_P=219,
              I2SPB_P=0, LPF_P=0)
shapes = {
    'endstation_ax7101_1x1_tdm8': dict(N_STREAMS=1, AUDIO_IF_SLOTS_P=8,
        AUDIO_IF_CLK_HZ_P=24576000, AUDIO_IF_RENDER_SLOTS_P=8, LOOPBACK_P=1),
    'endstation_ax7101_8x8': dict(N_STREAMS=8, AUDIO_IF_SLOTS_P=32,
        AUDIO_IF_CLK_HZ_P=98304000, AUDIO_IF_RENDER_SLOTS_P=0, LOOPBACK_P=0,
        LTAP_P=0, DPROBES_P=0),
}
for shape, params in shapes.items():
    params = common | params
    work = WORK / f'ooc-{phase}-{shape}'
    work.mkdir(exist_ok=True)
    shaped = source
    for key, value in params.items():
        shaped, count = re.subn(r'(parameter (?:int|bit)(?: unsigned)? '+key+r'\s*= )[^,\n]+',
                                lambda m: m[1]+str(value), shaped)
        assert count == 1, (key, count)
    dp = work/'milan_datapath.sv'
    dp.write_text(shaped)
    script = (ROOT/'syn/yosys/ooc.sh').read_text()
    script = script.replace('. "$(dirname "$0")/malloc.sh"', '. "'+str(ROOT/'syn/yosys/malloc.sh')+'"')
    script = script.replace('R="$(cd "$(dirname "$0")/../.." && pwd)"', 'R="'+str(ROOT)+'"')
    assert script.count('$R/hdl/milan/milan_datapath.sv') == 1
    script = script.replace('$R/hdl/milan/milan_datapath.sv', str(dp))
    runner = work/'ooc.sh'
    runner.write_text(script)
    env = dict(os.environ, OOC_SHAPE=str(ROOT/'configs/generated'/shape), OOC_TMP=str(work/'artifacts'))
    result = subprocess.run(['rtk', 'proxy', 'timeout', '--kill-after=60', '5400', 'bash', str(runner), 'milan_datapath'],
                            cwd=ROOT, env=env, check=False)
    records = {'head':head, 'base':base, 'neutral_control':control, 'phase':phase, 'shape':shape, 'parameters':params, 'rc':result.returncode,
               'source_sha256':hashlib.sha256(source.encode()).hexdigest(), 'artifacts':{}}
    for p in sorted(work.rglob('*')):
        if p.is_file():
            data = p.read_bytes()
            records['artifacts'][str(p)] = dict(bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
            if p.name.endswith('.ooc.log'):
                text = data.decode()
                start = text.rfind('=== milan_datapath ===')
                (OUT/f'ooc-{phase}-{shape}-stat.txt').write_text(text[start:start+10000])
    (OUT/f'ooc-{phase}-{shape}.json').write_text(json.dumps(records,indent=2)+'\n')
    if result.returncode:
        sys.exit(result.returncode)
