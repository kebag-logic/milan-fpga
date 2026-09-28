"""AX7101 1x1 TDM8 three-seed sweep at the merge head, sequential, 16 threads, fresh outputs.

The round-1 recipe (the builder-emitted shipping argv, AreaOptimized_high synthesis,
ExploreArea optimization, the three canonical place directives) is unchanged; only the
head and the output directories differ. After each build, report_seed.tcl (byte-identical
to the round-1 script) writes per-corner Ethernet crossing and clock-interaction reports
from the routed checkpoint. Resumable: a seed with a recorded rc 0 build and report is kept.
"""
import json
import os
from pathlib import Path
import subprocess
import time

root = Path('$LANES/607-xdc-clock-names')
out = Path(__file__).resolve().parent
work = Path('$VALIDATION_STORAGE/607-a427-work')
expected = 'c7ee5cbd4ed6215b988f3811d5e9156e21aa55c5'
pin = 'c951a9ff0cb5851fb159d33e966e5a2a9a188fe3'
git_env = dict(GIT_CONFIG_COUNT='1', GIT_CONFIG_KEY_0='core.commitGraph', GIT_CONFIG_VALUE_0='false')


def git(*args, cwd=root):
    return subprocess.check_output(['git', *args], cwd=cwd, text=True, env=dict(os.environ, **git_env)).strip()


def check_tree():
    assert git('rev-parse', 'HEAD') == expected
    assert not git('status', '--porcelain')
    assert git('rev-parse', '--show-toplevel', cwd=root / 'protocol-processor') == str(root / 'protocol-processor')
    assert git('rev-parse', 'HEAD:protocol-processor') == pin
    assert git('rev-parse', 'HEAD', cwd=root / 'protocol-processor') == pin


check_tree()
python = '$WORKSPACE_HOME/litex-milan/venv/bin/python'
vivado = '$WORKSPACE_HOME/Xilinx2/2026.1/Vivado/bin/vivado'
taskset = ['taskset', '-c', '0-15']
env = dict(os.environ, PYTHONHASHSEED='0', PYTHON_CPU_COUNT='16', TMPDIR=str(work),
           LITEX_ENV_CC_TRIPLE='riscv32-linux', **git_env)
env['PATH'] = ('$WORKSPACE_HOME/litex-milan/venv/bin:/usr/bin:$WORKSPACE_HOME/br-milan-rv32/host/bin:'
               '$WORKSPACE_HOME/Xilinx2/2026.1/Vivado/bin:' + env['PATH'])
subprocess.run(['meson', '--version'], cwd=root, env=env, check=True, timeout=30)
builder_log = work / 'endstation-builder.log'
with builder_log.open('w') as stream:
    subprocess.run([python, 'sw/builder/endstation_builder.py', 'configs/endstation_ax7101_1x1_tdm8.yaml'],
                   cwd=root, env=env, check=True, timeout=600, stdout=stream, stderr=subprocess.STDOUT)
check_tree()
params = json.loads((root / 'sw/builder/out/endstation_ax7101_1x1_tdm8/soc_params.json').read_text())
receipt = out / 'sweep-results.json'
rows = json.loads(receipt.read_text()) if receipt.exists() else []
rows = [row for row in rows if row['head'] == expected and row['rc'] == 0 and row.get('report_rc') == 0]
done = {row['seed'] for row in rows}
for seed, directive in [('asl', 'AltSpreadLogic_high'), ('eto', 'ExtraTimingOpt'), ('eppo', 'ExtraPostPlacementOpt')]:
    if seed in done:
        print('KEEP', seed, flush=True)
        continue
    check_tree()
    directory = work / ('build_ax7101_' + seed + '_' + expected[:9])
    assert not directory.exists(), 'fresh output required: ' + str(directory)
    command = [*taskset, python, str(root / 'sw/litex/milan_soc.py'), *params['argv'],
               '--entity-gen-dir', str(root / 'configs/generated/endstation_ax7101_1x1_tdm8'),
               '--synth-directive', 'AreaOptimized_high', '--opt-directive', 'ExploreArea',
               '--place-directive', directive, '--vivado-max-threads', '16',
               '--build', '--output-dir', str(directory)]
    log = work / ('sweep-' + seed + '.log')
    print('START', seed, directive, time.strftime('%H:%M:%S'), flush=True)
    started = time.monotonic()
    with log.open('w') as stream:
        result = subprocess.run(command, cwd=root / 'sw/litex', env=env, stdout=stream,
                                stderr=subprocess.STDOUT, timeout=14400)
    row = dict(seed=seed, directive=directive, head=expected, command=command, rc=result.returncode,
               elapsed_s=round(time.monotonic() - started, 2), directory=str(directory), log=str(log))
    rows.append(row)
    receipt.write_text(json.dumps(rows, indent=2) + '\n')
    print('BUILD FINISH', seed, 'rc=' + str(result.returncode), 'seconds=' + str(row['elapsed_s']), flush=True)
    if result.returncode != 0:
        continue
    reports = directory / 'acceptance'
    reports.mkdir()
    report_command = [*taskset, vivado, '-mode', 'batch', '-source', str(out / 'report_seed.tcl'),
                      '-log', 'report.log', '-journal', 'report.jou', '-tclargs',
                      str(directory / 'gateware/alinx_ax7101_route.dcp'), str(reports / 'seed')]
    with (reports / 'stdout.log').open('w') as stream:
        report_result = subprocess.run(report_command, cwd=reports, env=env, stdout=stream,
                                       stderr=subprocess.STDOUT, timeout=1800)
    row.update(report_rc=report_result.returncode, report_command=report_command)
    receipt.write_text(json.dumps(rows, indent=2) + '\n')
    print('REPORT FINISH', seed, 'rc=' + str(report_result.returncode), flush=True)
check_tree()
assert len(rows) == 3 and all(row['rc'] == 0 and row.get('report_rc') == 0 for row in rows)
print('SWEEP COMPLETE', flush=True)
