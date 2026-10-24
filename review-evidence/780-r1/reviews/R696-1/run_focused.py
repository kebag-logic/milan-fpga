#!/usr/bin/env python3
"""Focused adoption review. Run from the exact-head parent checkout.

All disposable checkouts and build products remain under packet/scratch.
No background shell jobs; independent foreground subprocesses are joined.
"""
import concurrent.futures
import difflib
import hashlib
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path.cwd().resolve()
PACKET = Path(__file__).resolve().parent
SCRATCH = PACKET / 'scratch'
CLONE = SCRATCH / 'probe-tree'
HEAD = '25f05752f7e50e3cf7e27008e434ffde930b4b6f'
VERILATOR = os.environ.get('REVIEW_VERILATOR', 'verilator')
ENV = dict(os.environ, TMPDIR=str(SCRATCH), PYTHONDONTWRITEBYTECODE='1',
           VERILATOR=VERILATOR, VERILATOR_JOBS='8')

def run(args, cwd=ROOT):
    return subprocess.run(args, cwd=cwd, env=ENV, check=True, capture_output=True).stdout

def logged(name, args, cwd=ROOT):
    with (PACKET / (name+'.log')).open('wb') as log:
        log.write(('COMMAND '+repr(args)+'\n').encode()); log.flush()
        p = subprocess.run(args, cwd=cwd, env=ENV, stdout=log, stderr=subprocess.STDOUT)
    (PACKET / (name+'.rc')).write_text(str(p.returncode)+'\n')
    return name, p.returncode

def probe():
    return logged('parent-probe', ['make','-j16','-C','tb/verilator/pp_shadow',
                    'run-base',f'VERILATOR={VERILATOR}','VERILATOR_JOBS=8'], CLONE)

def checks():
    cmds = [
        ('boundary', ['python3','docs/diagrams/submodule_boundaries.gen.py','--check']),
        ('submodule-docs',['python3','scripts/check_submodule_docs.py']),
        ('port-contracts',['python3','scripts/check_port_contracts.py']),
        ('integrator-params',['python3','protocol-processor/scripts/check-integrator-params.py']),
        ('resource-baseline',['python3','syn/ooc/pp_resource_gate.py','check-baseline']),
        ('command-model',['python3','-B','protocol-processor/scripts/check_aecp_commands.py']),
    ]
    results = [logged(n,c) for n,c in cmds]
    with (PACKET/'rom-regeneration.log').open('w') as log:
        for image, generator in [('ltn_rom.hex','acmp/rom/gen_ltn_rom.py'),('ucode.hex','aecp/ucode/gen_ucode.py')]:
            output=SCRATCH/image
            run(['python3',str(ROOT/'protocol-processor/hdl'/generator),'-o',str(output)])
            digest=hashlib.sha256(output.read_bytes()).hexdigest()
            ledger=(ROOT/'syn/yosys/rom_digests.tsv').read_text().splitlines()
            for pin in ['ed2118035e4cec76fb1b59cfbf8a053aeacc8af8','93fb0b2d736b36588ea7321e25fba2f8819ea41f']:
                expected=next(x.split()[2] for x in ledger if x.startswith(pin+'\t'+image+'\t'))
                assert digest==expected,(image,pin,digest,expected)
                log.write(f'PASS {pin} {image} {digest}\n')
    return results

def main():
    SCRATCH.mkdir(exist_ok=True)
    assert run(['git','rev-parse','HEAD']).decode().strip()==HEAD
    version=run([VERILATOR,'--version']).decode()
    assert 'Verilator 5.050 ' in version
    (PACKET/'simulator-identity.txt').write_text(version)
    if not CLONE.exists():
        run(['git','clone','--quiet','--shared','--no-checkout',str(ROOT),str(CLONE)])
        run(['git','checkout','--quiet','--detach',HEAD],CLONE)
        for sub in ['protocol-processor','gptp-processor','third_party/verilog-axis']:
            pin=run(['git','rev-parse',f'HEAD:{sub}']).decode().strip()
            run(['git','clone','--quiet','--shared','--no-checkout',str(ROOT/sub),str(CLONE/sub)])
            run(['git','checkout','--quiet','--detach',pin],CLONE/sub)
    file=CLONE/'tb/verilator/pp_shadow/sim_main.cpp'
    before=run(['git','show','HEAD:tb/verilator/pp_shadow/sim_main.cpp']).decode()
    after=before.replace('        grade_unassigned_opcode_echoes();',
                         '        grade_unassigned_opcode_echoes();\n        grade_adoption_probe();',1)
    marker='    // helper: the newest AECP frame at the MAC boundary past `from`'
    assert marker in after
    after=after.replace(marker,(PACKET/'probe.cpp.inc').read_text()+'\n'+marker,1)
    after=after.replace('            grade_the_device_answers_aecp();',
        '            grade_adoption_probe();\n'
        '            printf("adoption probe: %ld checks, %ld failures\\n", checks, fails);\n'
        '            return fails ? 1 : 0;',1)
    file.write_text(after)
    (PACKET/'parent-probe.patch').write_text(''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),
        fromfile='a/tb/verilator/pp_shadow/sim_main.cpp',tofile='b/tb/verilator/pp_shadow/sim_main.cpp')))
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        futures=[pool.submit(probe),pool.submit(checks)]
        results=[f.result() for f in futures]
    print(results)
    outcomes=[results[0],*results[1]]
    return int(any(rc != 0 for _,rc in outcomes))

if __name__=='__main__':
    sys.exit(main())
