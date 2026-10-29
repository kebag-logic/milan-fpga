#!/usr/bin/env python3
"""Exercise the real boot driver and grader with a controlled native-process result."""
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
root = Path.cwd()
packet = Path(__file__).resolve().parent
scratch = packet / 'scratch' / 'boot-exit'
scratch.mkdir(parents=True, exist_ok=True)
spec = importlib.util.spec_from_file_location('review_boot_run', root / 'tb/verilator/ctrl_split_boot/run.py')
run = importlib.util.module_from_spec(spec)
spec.loader.exec_module(run)
shape = 'endstation_ax7101_1x1_tdm8'
soc = {'sys_hz':100000000, 'cpu_hz':50000000, 'shape':shape, 'interfaces':1}
writes = run.expected_writes(shape, scratch / 'oracle')
banner = 'Milan split control firmware: boot\r\nMilan split control firmware: ready\r\n'
status = ('ID=4d494c4e VERSION=00020060 PTP_CTRL=00000001 ADP_CTRL=00000000 PP_CTRL=00000000 '
          'PP_STAT=00000000 AEM=loaded\r\n'
          'GPTP_GM=001bc5fffe001122 GPTP_PARENT=001bc5fffe334455 PDELAY_NS=600 AS_PATH_COUNT=3 '
          'AS_PATH_GEN=7 CLKV_STAT=00010002 SYNC=1 ASCAPABLE=1 TU=0 GPTP_LAT=029000db\r\n'
          'TAI_NS=0x0000000000001000\r\n')
answers = [status, 'TAI_NS=0x0000000000002000\r\n', 'TAI_NS=0x0000000000003000\r\n']
rows = [f'CSRW {i+1} {o:03x} {v:08x}' for i,(o,v) in enumerate(writes)] + ['READY 10000']
for i, answer in enumerate(answers):
    start = 20000 + 100000*i
    name = 'milan_status' if i == 0 else 'milan_gettime'
    rows += [f'IN {start} {name}']
    rows += [f'UART {start+100*(j+1)} {b:02x}' for j,b in enumerate(answer.encode())]
transcript = banner + ''.join(answers)
baseline = '\n'.join(rows) + '\n'

def execute(rc):
    out = scratch / f'exit-{rc}'
    (out / 'soc/gateware').mkdir(parents=True, exist_ok=True)
    executable = out / 'native-fixture'
    ending = ('== ctrl_split_boot: checks: 1   failures: 0 ==\nRESULT: PASS\n' if rc == 0 else
              'FAIL: simulation exceeded its time limit\n'
              '== ctrl_split_boot: checks: 1   failures: 1 ==\nRESULT: FAIL\n')
    executable.write_text('#!' + sys.executable + '\nimport pathlib,sys\n'
                          + 'pathlib.Path(sys.argv[1]).write_bytes(' + repr(transcript.encode()) + ')\n'
                          + 'print(' + repr(baseline+ending) + ', end="")\n'
                          + 'sys.exit(' + str(rc) + ')\n')
    executable.chmod(0o755)
    (out / 'soc/soc.json').write_text(json.dumps(soc))
    # Replace only expensive build(); point(), subprocess execution, grade(), and main() remain unchanged.
    run.build = lambda *args: (executable, soc)
    sys.argv = ['run.py', '--build-dir', str(out)]
    verdict = run.main()
    print(f'PROBE native exit={rc}, top-level gate exit={verdict}')
    sys.argv = ['run.py', '--build-dir', str(out), '--regrade']
    regraded = run.main()
    print(f'PROBE native exit={rc}, regrade gate exit={regraded}')
    if rc == 0:
        assert regraded == 0
    return verdict

assert execute(0) == 0, 'positive control must pass'
bad = execute(1)
print('DEFECT REPRODUCED' if bad == 0 else 'DEFECT REJECTED')
raise SystemExit(1 if bad == 0 else 0)
