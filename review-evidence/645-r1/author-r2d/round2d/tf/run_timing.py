"""Three-directive AX7101 1x1 TDM8 signoff at the round-2d head 3eee12dc.

Round 2c's driver with round-2d paths: the project was re-elaborated from the
round2d/route-source export (tf/elaboration: the project Tcl is identical to
round 2c's after path normalisation), and round 2c's synthesis-only and
implementation scripts are reused with only their export and project paths
substituted. Vendor work starts only after the functional gates and the
campaign chain have both written their rc files.


Same recipe as the earlier qualified sweep (resume/merged_route.py and
resume/qualify_routes.py): synthesis alone with one synthesis thread, saved
checkpoint, then a fresh 32-thread implementation per placement directive,
the timing-grade hook, bitstream, the rejected-constraint check (#607) and the
flash manifest. Every vendor process runs under the shared lock and only after
the functional gates have finished. The project was re-elaborated at this head
(tf/elaboration); its scripts differ from the earlier project only in paths.
"""
import hashlib
import importlib.util
import json
import os
import shutil
import signal
import subprocess
import time
from pathlib import Path

w = Path(__file__).resolve().parent
round2d = w.parent
round2c = round2d.parent / 'round2c'
src = round2d / 'route-source'
common = w / 'route/ax7101/gateware'
old = round2c / 'tf/route/ax7101/gateware'
out = w / 'resume/qualified-routes'
out.mkdir(parents=True, exist_ok=True)
vivado = str(Path.home() / 'Xilinx/2026.1/Vivado/bin/vivado')
cg = Path('/sys/fs/cgroup') / open('/proc/self/cgroup').read().strip().split('::', 1)[1].lstrip('/')
env = os.environ.copy()
env.update(TMPDIR=str(round2d / 'tmp'), PYTHONDONTWRITEBYTECODE='1')
env['PATH'] = str(Path.home() / 'litex-milan/venv/bin') + ':' + env['PATH']
rows = json.loads((out / 'commands.json').read_text()) if (out / 'commands.json').exists() else []

# Wait for the functional gates: no vendor process beside a heavy build.
gates_rc = round2d / 'functional/full-gates.rc'
chain_rc = round2d / 'campaign-chain.rc'
while not (gates_rc.exists() and chain_rc.exists()):
    time.sleep(20)
print('functional gates finished rc', gates_rc.read_text().strip(), 'campaigns rc', chain_rc.read_text().strip(), flush=True)
statuses = [gates_rc, chain_rc] + [round2d / 'candidate' / f for f in ('campaign.rc', 'quiet-distributions.rc', 'pullin.rc')]
if any(not p.exists() or p.read_text().strip() != '0' for p in statuses):
    out.mkdir(parents=True, exist_ok=True)
    (out / 'all.rc').write_text('99\n')
    raise SystemExit('a functional gate or campaign did not pass: no vendor run at this content')


def anon():
    return int(next(l.split()[1] for l in (cg / 'memory.stat').read_text().splitlines() if l.startswith('anon ')))


# The earlier qualified sweep ran with an 8.75 GB reclaim threshold; restore
# it for the vendor phase only. The guard stops a run above 8.95 GB, under the
# 9 GB working ceiling (an 8.8 GB guard stopped one synthesis on cache overshoot).
subprocess.run(['systemctl', '--user', 'set-property', '--runtime', cg.name, 'MemoryHigh=8750000000'], check=True)


def run(name, argv, cwd):
    done = out / (name + '.rc')
    if done.exists() and done.read_text().strip() == '0':
        print(time.strftime('%FT%T'), 'SKIP (rc 0 recorded)', name, flush=True)
        return
    while anon() > 2000000000:
        time.sleep(10)
    peak = 0
    stopped = False
    print(time.strftime('%FT%T'), 'START', name, flush=True)
    t0 = time.time()
    with (out / (name + '.log')).open('w') as log:
        child = subprocess.Popen(argv, cwd=cwd, env=env, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
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
    rows.append(dict(name=name, argv=argv, cwd=str(cwd), rc=rc, wall_seconds=round(time.time() - t0, 1),
                     peak_memory_bytes=peak, resource_interruption=stopped))
    (out / 'commands.json').write_text(json.dumps(rows, indent=2) + '\n')
    print(time.strftime('%FT%T'), 'DONE', name, rc, flush=True)
    if rc:
        (out / 'all.rc').write_text(f'{rc}\n')
        raise SystemExit(rc)


def lock(argv):
    return ['flock', '$VIVADO_LOCK', vivado, '-mode', 'batch', '-source', *argv]


# Scripts: the earlier ones with the project path moved to this work root.
def moved(text):
    text = text.replace(str(round2c / 'route-source'), str(src)).replace(str(old.parent), str(common.parent))
    assert 'round2c' not in text
    return text


synth = (old / 'merged_synth_only.tcl').read_text()
assert synth.count(str(old.parent)) == 1
(common / 'merged_synth_only.tcl').write_text(moved(synth))
impl = (old / 'merged_implementation.tcl').read_text()
(common / 'merged_implementation.tcl').write_text(moved(impl))

run('synthesis', lock(['merged_synth_only.tcl', '-nojournal', '-log', 'synthesis-vendor.log']), common)
run('ExtraPostPlacementOpt-implementation', lock(['merged_implementation.tcl', '-nojournal', '-log', 'implementation-vendor.log']), common)

spec = importlib.util.spec_from_file_location('constraints', src / 'sw/litex/clock_constraints.py')
constraints = importlib.util.module_from_spec(spec)
spec.loader.exec_module(constraints)
settings = ('set_property BITSTREAM.CONFIG.SPI_BUSWIDTH 4 [current_design]\nset_property CONFIG_MODE SPIx4 [current_design]\n'
            'set_property BITSTREAM.CONFIG.CONFIGRATE 50 [current_design]\nset_property CFGBVS VCCO [current_design]\n'
            'set_property CONFIG_VOLTAGE 3.3 [current_design]\n')
for directive in ['ExtraPostPlacementOpt', 'AltSpreadLogic_high', 'ExtraTimingOpt']:
    build = w / 'route' / ('ax7101' if directive == 'ExtraPostPlacementOpt' else 'ax7101-' + directive)
    gate = common if directive == 'ExtraPostPlacementOpt' else build / 'gateware'
    gate.mkdir(parents=True, exist_ok=True)
    if directive == 'ExtraPostPlacementOpt':
        declaration = (common / 'alinx_ax7101_signoff_grade.txt').read_text().splitlines()[0]
        hook = ('source {' + str(src / 'sw/litex/timing_grade.tcl') + '}\nset ::kl_timing_grade {' + declaration
                + '}\nkl_timing_grade_check\n')
        script = 'set_param general.maxThreads 32\nopen_checkpoint alinx_ax7101_route.dcp\n' + hook + settings + \
            'write_bitstream -force alinx_ax7101.bit\nquit\n'
        log_name = 'bitstream-vendor.log'
        logs = [common / 'synthesis-vendor.log', common / 'implementation-vendor.log', gate / log_name]
    else:
        assert impl.count('place_design -directive ExtraPostPlacementOpt') == 1
        script = impl.replace('open_checkpoint alinx_ax7101_synth.dcp',
                              'open_checkpoint {' + str(common / 'alinx_ax7101_synth.dcp') + '}')
        script = script.replace('place_design -directive ExtraPostPlacementOpt', 'place_design -directive ' + directive)
        assert script.endswith('quit\n')
        script = script[:-len('quit\n')] + 'write_bitstream -force alinx_ax7101.bit\nquit\n'
        for relative in ['software/include/generated/soc.h', 'aem_desc.bin']:
            target = build / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(w / 'route/ax7101' / relative, target)
        log_name = 'implementation-vendor.log'
        logs = [common / 'synthesis-vendor.log', gate / log_name]
    (gate / 'qualified_implementation.tcl').write_text(script)
    run(directive + '-build', lock(['qualified_implementation.tcl', '-nojournal', '-log', log_name]), gate)
    combined = gate / 'vivado.log'
    combined.write_text('\n'.join(p.read_text(errors='replace') for p in logs))
    try:
        constraints.check_implementation_log(combined)
    except BaseException:
        for bit in gate.glob('*.bit'):
            bit.rename(bit.with_suffix('.bit.rejected'))
        (out / (directive + '-constraint-check.rc')).write_text('1\n')
        raise
    (out / (directive + '-constraint-check.rc')).write_text('0\n')
    bit = gate / 'alinx_ax7101.bit'
    assert bit.is_file()
    run(directive + '-manifest', ['python3', '-B', str(src / 'sw/litex/layout_from_soch.py'), str(build), '--bit', str(bit)], src)
    provenance = {str(p.relative_to(w)): {'sha256': hashlib.sha256(p.read_bytes()).hexdigest(), 'bytes': p.stat().st_size}
                  for p in logs + [bit, build / 'flashboot_layout.json', build / 'software/include/generated/soc.h',
                                   build / 'aem_desc.bin']}
    (out / (directive + '-artifacts.json')).write_text(json.dumps(provenance, indent=2) + '\n')
(out / 'all.rc').write_text('0\n')
subprocess.run(['systemctl', '--user', 'set-property', '--runtime', cg.name, 'MemoryHigh=7500000000'], check=True)
