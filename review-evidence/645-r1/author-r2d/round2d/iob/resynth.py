"""Synthesis controls for the eth0_rx_dv IOB-pack failure, run alone today.

  r2c: round 2c's timing synthesis inputs as they are (f6bd415f content, the
       pre-fix pop_dup_w term), from round 2c's own script, sources and
       elaborated top, in a fresh directory: does today's run reproduce round
       2c's netlist (eth_rx_rst on the flop's R pin)?
  r2d: round 2d's inputs (3eee12dc content) again: is the LUT-on-D mapping
       reproducible?
Each run writes its own synthesis checkpoint here, then probe.tcl reads the
eth0_rx_dv register's pins from it. Nothing in either source tree is written.
"""
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

here = Path(__file__).resolve().parent
root = Path('$VALIDATION_STORAGE/645-a531')
vivado = str(Path.home() / 'Xilinx/2026.1/Vivado/bin/vivado')
env = os.environ.copy()
env.update(TMPDIR=str(root / 'round2d/tmp'))
cg = Path('/sys/fs/cgroup') / open('/proc/self/cgroup').read().strip().split('::', 1)[1].lstrip('/')
results = {}
for tag in sys.argv[1:]:
    src = root / ('round2c' if tag == 'r2c' else 'round2d') / 'tf/route/ax7101/gateware'
    work = here / ('resynth-' + tag)
    if work.exists():
        shutil.rmtree(work)
    work.mkdir()
    for f in ['alinx_ax7101.xdc', 'alinx_ax7101_rom.init', 'alinx_ax7101_sram.init', 'alinx_ax7101_mem.init',
              'merged_synth_only.tcl']:
        shutil.copy2(src / f, work / f)
    t0 = time.time()
    peak = 0
    with (work / 'run.log').open('w') as log:
        child = subprocess.Popen(['flock', '$VIVADO_LOCK', vivado, '-mode', 'batch', '-source',
                                  'merged_synth_only.tcl', '-nojournal', '-log', 'synthesis-vendor.log'],
                                 cwd=work, env=env, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
        while child.poll() is None:
            peak = max(peak, int((cg / 'memory.current').read_text()))
            if peak > 8950000000:
                os.killpg(child.pid, 15)
            time.sleep(1)
        rc = child.wait()
    probe = subprocess.run(['flock', '$VIVADO_LOCK', vivado, '-mode', 'batch', '-nojournal', '-nolog',
                            '-notrace', '-source', str(here / 'probe2.tcl'), '-tclargs',
                            str(work / 'alinx_ax7101_synth.dcp')], cwd=work, env=env, capture_output=True, text=True)
    (work / 'probe.log').write_text(probe.stdout + probe.stderr)
    lines = [l for l in probe.stdout.splitlines() if l.startswith('PROBE')]
    results[tag] = dict(synthesis_rc=rc, wall_seconds=round(time.time() - t0, 1), peak_memory_bytes=peak,
                        probe_rc=probe.returncode, probe=lines)
    (here / 'resynth-results.json').write_text(json.dumps(results, indent=2) + '\n')
    print(tag, rc, *lines, sep='\n  ', flush=True)
