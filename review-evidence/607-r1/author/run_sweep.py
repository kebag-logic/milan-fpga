"""Run all three canonical AX7101 place directives sequentially in the foreground."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

root = Path('$LANES/607-xdc-clock-names')
out = Path(__file__).resolve().parent
work = Path('$VALIDATION_STORAGE/607-a408-work')
head = subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
expected = '350af5dcf0aab9fc8ad8d6c6cde3552c63e26a75'
assert head == expected
assert not subprocess.check_output(['git','status','--porcelain'],cwd=root,text=True).strip()
python = '$WORKSPACE_HOME/litex-milan/venv/bin/python'
vivado = '$WORKSPACE_HOME/Xilinx2/2026.1/Vivado/bin/vivado'
env = dict(os.environ, PYTHONHASHSEED='0', PYTHON_CPU_COUNT='16', TMPDIR=str(work),
           LITEX_ENV_CC_TRIPLE='riscv32-linux', GIT_CONFIG_COUNT='1',
           GIT_CONFIG_KEY_0='core.commitGraph', GIT_CONFIG_VALUE_0='false')
env['PATH'] = '$WORKSPACE_HOME/litex-milan/venv/bin:/usr/bin:$WORKSPACE_HOME/br-milan-rv32/host/bin:$WORKSPACE_HOME/Xilinx2/2026.1/Vivado/bin:' + env['PATH']
subprocess.run(['meson','--version'],cwd=root,env=env,check=True,timeout=30)
subprocess.run([python,'sw/builder/endstation_builder.py','configs/endstation_ax7101_1x1_tdm8.yaml'],
               cwd=root,env=env,check=True,timeout=120)
params = json.loads((root/'sw/builder/out/endstation_ax7101_1x1_tdm8/soc_params.json').read_text())
rows = []
for seed,directive in [('asl','AltSpreadLogic_high'),('eto','ExtraTimingOpt'),('eppo','ExtraPostPlacementOpt')]:
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip() == expected
    directory = work / ('build_ax7101_' + seed + '_350af5dcf')
    assert not directory.exists(), 'fresh output required: ' + str(directory)
    command = [python,str(root/'sw/litex/milan_soc.py'),*params['argv'],
               '--entity-gen-dir',str(root/'configs/generated/endstation_ax7101_1x1_tdm8'),
               '--synth-directive','AreaOptimized_high','--opt-directive','ExploreArea',
               '--place-directive',directive,'--vivado-max-threads','16',
               '--build','--output-dir',str(directory)]
    log = work / ('sweep-' + seed + '.log')
    print('START',seed,directive,flush=True)
    started = time.monotonic()
    with log.open('w') as stream:
        result = subprocess.run(command,cwd=root/'sw/litex',env=env,stdout=stream,
                                stderr=subprocess.STDOUT,timeout=14400)
    row = dict(seed=seed,directive=directive,head=head,command=command,rc=result.returncode,
               elapsed_s=round(time.monotonic()-started,2),directory=str(directory),log=str(log))
    rows.append(row)
    (out/'sweep-results.json').write_text(json.dumps(rows,indent=2)+'\n')
    print('BUILD FINISH',seed,'rc='+str(result.returncode),'seconds='+str(row['elapsed_s']),flush=True)
    if result.returncode != 0:
        continue
    reports = directory / 'acceptance'
    reports.mkdir()
    report_command = [vivado,'-mode','batch','-source',str(out/'report_seed.tcl'),
                      '-log','report.log','-journal','report.jou','-tclargs',
                      str(directory/'gateware/alinx_ax7101_route.dcp'),str(reports/'seed')]
    with (reports/'stdout.log').open('w') as stream:
        report_result = subprocess.run(report_command,cwd=reports,env=env,stdout=stream,
                                       stderr=subprocess.STDOUT,timeout=1200)
    row.update(report_rc=report_result.returncode,report_command=report_command)
    (out/'sweep-results.json').write_text(json.dumps(rows,indent=2)+'\n')
    print('REPORT FINISH',seed,'rc='+str(report_result.returncode),flush=True)
assert all(row['rc'] == 0 and row.get('report_rc') == 0 for row in rows)
