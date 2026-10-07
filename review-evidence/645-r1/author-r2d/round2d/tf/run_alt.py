"""The two remaining directives of the sweep, AltSpreadLogic_high and
ExtraTimingOpt, from the same round-2d synthesis checkpoint, after
ExtraPostPlacementOpt stopped at the IOB-pack check. Same scripts as
run_timing.py (placement directive substituted, bitstream appended); each run
is recorded whatever its rc, so all three directives have a verdict.
Vendor processes run alone under the shared lock, with run_timing.py's guard.
"""
import json
import os
import shutil
import signal
import subprocess
import time
from pathlib import Path

w = Path(__file__).resolve().parent
common = w / 'route/ax7101/gateware'
out = w / 'resume/qualified-routes'
vivado = str(Path.home() / 'Xilinx/2026.1/Vivado/bin/vivado')
cg = Path('/sys/fs/cgroup') / open('/proc/self/cgroup').read().strip().split('::', 1)[1].lstrip('/')
env = os.environ.copy()
env.update(TMPDIR=str(w.parent / 'tmp'), PYTHONDONTWRITEBYTECODE='1')
env['PATH'] = str(Path.home() / 'litex-milan/venv/bin') + ':' + env['PATH']
rows = json.loads((out / 'commands.json').read_text())
impl = (common / 'merged_implementation.tcl').read_text()
assert impl.count('place_design -directive ExtraPostPlacementOpt') == 1
results = {}
for directive in ['AltSpreadLogic_high', 'ExtraTimingOpt']:
    build = w / 'route' / ('ax7101-' + directive)
    gate = build / 'gateware'
    gate.mkdir(parents=True, exist_ok=True)
    script = impl.replace('open_checkpoint alinx_ax7101_synth.dcp',
                          'open_checkpoint {' + str(common / 'alinx_ax7101_synth.dcp') + '}')
    script = script.replace('place_design -directive ExtraPostPlacementOpt', 'place_design -directive ' + directive)
    assert script.endswith('quit\n')
    script = script[:-len('quit\n')] + 'write_bitstream -force alinx_ax7101.bit\nquit\n'
    for relative in ['software/include/generated/soc.h', 'aem_desc.bin']:
        target = build / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(w / 'route/ax7101' / relative, target)
    (gate / 'qualified_implementation.tcl').write_text(script)
    name = directive + '-build'
    argv = ['flock', '$VIVADO_LOCK', vivado, '-mode', 'batch', '-source', 'qualified_implementation.tcl',
            '-nojournal', '-log', 'implementation-vendor.log']
    peak, stopped, t0 = 0, False, time.time()
    print(time.strftime('%FT%T'), 'START', name, flush=True)
    with (out / (name + '.log')).open('w') as log:
        child = subprocess.Popen(argv, cwd=gate, env=env, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
        while child.poll() is None:
            current = int((cg / 'memory.current').read_text())
            peak = max(peak, current)
            if current > 8950000000:
                stopped = True
                os.killpg(child.pid, signal.SIGTERM)
                time.sleep(3)
                if child.poll() is None:
                    os.killpg(child.pid, signal.SIGKILL)
                break
            time.sleep(1)
        rc = child.wait()
    (out / (name + '.rc')).write_text(f'{rc}\n')
    rows.append(dict(name=name, argv=argv, cwd=str(gate), rc=rc, wall_seconds=round(time.time() - t0, 1),
                     peak_memory_bytes=peak, resource_interruption=stopped))
    (out / 'commands.json').write_text(json.dumps(rows, indent=2) + '\n')
    results[directive] = rc
    print(time.strftime('%FT%T'), 'DONE', name, rc, flush=True)
(out / 'alt-results.json').write_text(json.dumps(results, indent=2) + '\n')
