#!/usr/bin/env python3
"""R240 independent bounded probes. Mutants are outside the source checkout."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

ROOT = Path('$VALIDATION_STORAGE/reviews/r240-372-r1')
OUT = Path(__file__).resolve().parent
WORK = OUT / 'independent-controls'
HERE = ROOT / 'tb/verilator/ptp_ts'
TOOL = '$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator'
WORK.mkdir(exist_ok=True)
results = []
env = dict(os.environ, MAKEFLAGS='-j1', PYTHONDONTWRITEBYTECODE='1')

def command(name, argv):
    start = time.monotonic()
    with (WORK/(name+'.log')).open('wb') as f:
        run = subprocess.run(['rtk','proxy',*map(str,argv)],cwd=ROOT,env=env,stdout=f,stderr=subprocess.STDOUT)
    text = (WORK/(name+'.log')).read_text(errors='replace')
    results.append(dict(name=name,argv=['rtk','proxy',*map(str,argv)],exit=run.returncode,seconds=time.monotonic()-start))
    print(name, 'exit',run.returncode,flush=True)
    (WORK/'commands.json').write_text(json.dumps(results,indent=2)+'\n')
    return run.returncode,text

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec)
    sys.modules[name]=mod
    spec.loader.exec_module(mod)
    return mod

sys.path.insert(0,str(ROOT/'scripts'))
campaign=load('r240_campaign',HERE/'sva_campaign.py')
tally=load('r240_tally',ROOT/'scripts/suite_tally.py')
path=campaign.CHECKER+'.u_s0_stimulus.ap_tvalid_held_until_handshake'
named=f'[6000] %Error: checker.sv:1: Assertion failed in {path}: injected\n'
assert campaign.detection(3,named,'u_s0_stimulus.ap_tvalid_held_until_handshake').ok
parser_cases=[]
for status,text,why in [(0,named,'zero exit'),(1,named,'scoreboard exit'),(2,named,'usage exit'),
                        (-11,named,'signal'),(124,named,'timeout'),(3,'','unnamed stop'),
                        (3,named.replace('u_s0_stimulus','u_s1_stimulus'),'wrong instance'),
                        (3,named.replace('handshake:','handshake_extra:'),'property prefix collision')]:
    verdict=campaign.detection(status,text,'u_s0_stimulus.ap_tvalid_held_until_handshake')
    assert not verdict.ok,why
    parser_cases.append(dict(case=why,verdict=verdict._asdict()))
(WORK/'parser-rejections.json').write_text(json.dumps(parser_cases,indent=2)+'\n')

for width in (8,64):
    binary=HERE/f'obj_dir_mux_sva_w{width}/Vmux_sva'
    for seed in (0,1,2,4294967295,18446744073709551615):
        status,text=command(f'seed-w{width}-{seed}',[binary,f'+seed={seed}'])
        assert status==0 and 'failures: 0' in text and not campaign.fired(text)
    for seed in (1,17):
        status,text=command(f'random-initial-state-w{width}-{seed}',
                            [binary,'+verilator+rand+reset+2',f'+verilator+seed+{seed}'])
        assert status==0 and 'failures: 0' in text
    for idx,arg in enumerate(('+scenario=absent','+stimulus_fault=s2_flip_tdata',
                              '+seed=-1','+seed=18446744073709551616','+seed=1x')):
        status,text=command(f'bad-argument-w{width}-{idx}',[binary,arg])
        assert status==2 and not campaign.fired(text)

def build(name, width, *, source_text=None, stream_text=None, assertions='--assert'):
    row=WORK/name
    row.mkdir(exist_ok=True)
    sva=row/'sva'
    sva.mkdir(exist_ok=True)
    for p in (ROOT/'tb/common/sva').glob('*.sv'):
        shutil.copyfile(p,sva/p.name)
    if stream_text is not None:
        (sva/'axis_stream_source_sva.sv').write_text(stream_text)
    dut=ROOT/'hdl/common/axis_mux_rr_2in_1out.sv'
    if source_text is not None:
        dut=row/dut.name
        dut.write_text(source_text)
    status,text=command(name+'-build',['make','--no-print-directory','-C',HERE,'mux-sva-build',
                         f'VERILATOR={TOOL}',f'MUX_SVA_WIDTH={width}',f'MUX_SVA_OBJ={row}/obj',
                         f'SVA_DIR={sva}',f'MUX_SVA_DUT={dut}',f'MUX_SVA_ASSERT={assertions}'])
    assert status==0,(name,text[-2000:])
    return row/'obj/Vmux_sva'

stream=(ROOT/'tb/common/sva/axis_stream_source_sva.sv').read_text()
old='axis_sva_witness("ap_tkeep_stable_until_handshake", $past(rst_n && stalled_w));'
assert stream.count(old)==1
binary=build('one-witness-lost',64,stream_text=stream.replace(old,'axis_sva_witness("ap_tkeep_stable_until_handshake", 1\'b0);'))
status,text=command('one-witness-lost-run',[binary])
assert status==1 and not campaign.fired(text)
assert all('is elaborated with its assertions' not in line for line in campaign.fail_lines(text))
assert sum('ap_tkeep_stable_until_handshake' in line for line in campaign.fail_lines(text))==3

assert stream.count(' disable iff (!rst_n)')==4
binary=build('reset-guard-removed',64,stream_text=stream.replace(' disable iff (!rst_n)',''))
status,text=command('reset-guard-removed-run',[binary,campaign.ERROR_LIMIT,'+scenario=reset_while_stalled'])
assert status==3 and any('ap_tvalid_held_until_handshake' in p for p in campaign.fired(text))

dut=(ROOT/'hdl/common/axis_mux_rr_2in_1out.sv').read_text()
old='m_tdata  = s1_tdata;'
assert dut.count(old)==1
binary=build('scoreboard-high-bit',64,source_text=dut.replace(old,"m_tdata  = s1_tdata ^ 64'h8000000000000000;"),assertions='--no-assert')
status,text=command('scoreboard-high-bit-run',[binary,'+scenario=multi_beats'])
assert status==1 and not campaign.fired(text)
assert any('a beat that no source handed over' in l for l in campaign.fail_lines(text))
assert any('every accepted beat left the mux' in l for l in campaign.fail_lines(text))

print('R240 independent controls PASS: 8 parser rejections, 14 positive runs, 10 malformed-argument refusals, 3 successfully built scratch controls')
