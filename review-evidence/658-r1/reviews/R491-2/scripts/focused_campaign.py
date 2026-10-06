#!/usr/bin/env python3
"""Run independent guard mutations concurrently in a disposable checkout.

Usage: focused_campaign.py SOURCE PACKET VERILATOR [--jobs 2]
The foreground supervisor waits for and reaps every child. Each compile uses
at most floor(16/jobs) children. Build logs stay in private scratch because
compiler installation paths can identify the host. Runtime logs are receipts.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import time

ap = argparse.ArgumentParser()
ap.add_argument('source', type=Path)
ap.add_argument('packet', type=Path)
ap.add_argument('verilator')
ap.add_argument('--jobs', type=int, default=2, choices=(1, 2))
a = ap.parse_args()
scratch = a.packet.resolve() / 'scratch'
receipts = a.packet.resolve() / 'receipts'
repo = scratch / 'source'
env = dict(os.environ, TMPDIR=str(scratch / 'tmp'), GIT_NO_REPLACE_OBJECTS='1')
Path(env['TMPDIR']).mkdir(exist_ok=True)
def command(cmd, cwd, log):
    with log.open('w') as f:
        r = subprocess.run(cmd, cwd=cwd, env=env, stdout=f, stderr=subprocess.STDOUT)
    log.with_suffix('.rc').write_text(str(r.returncode) + '\n')
    return r.returncode
if not repo.exists():
    with (scratch / 'prepare.log').open('w') as f:
        subprocess.run(['git', 'clone', '--shared', '--no-checkout', str(a.source.resolve()), str(repo)], check=True, stdout=f, stderr=f)
        subprocess.run(['git', '-C', str(repo), 'checkout', '--detach', '5747a8cb99495cb0331658cdd499b9c44e3eda91'], check=True, stdout=f, stderr=f)
        for sub in ('protocol-processor', 'gptp-processor', 'third_party/verilog-axis'):
            subprocess.run(['git', '-C', str(repo), 'config', f'submodule.{sub}.url', str(a.source.resolve() / sub)], check=True)
            subprocess.run(['git', '-C', str(repo), '-c', 'protocol.file.allow=always', 'submodule', 'update', '--init', '--', sub], check=True, stdout=f, stderr=f)
suite = repo / 'tb/verilator/milan_dp'
spec = importlib.util.spec_from_file_location('dynmap', suite / 'dynmap_mutants.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
version = subprocess.check_output([a.verilator, '--version'], text=True).strip()
assert version.startswith('Verilator 5.050 '), version
(receipts / 'simulator-version.txt').write_text(version + '\n')

def case(item):
    name, edits, must_fail = item
    build = scratch / name
    build.mkdir(exist_ok=True)
    source = (repo / 'hdl/milan/milan_datapath.sv').read_text()
    for old, new in edits:
        assert source.count(old) == 1, (name, old)
        source = source.replace(old, new)
    rtl = build / 'milan_datapath.sv'
    rtl.write_text(source)
    started = time.monotonic()
    cmd = ['make', '-j16', '-s', 'dynmap-build', 'VERILATOR=' + a.verilator,
           f'VERILATOR_JOBS={16 // a.jobs}', 'DYNMAP_MDIR=' + str(build / 'obj'), 'DP_SRC=' + str(rtl)]
    if name != 'clean':
        cmd += ['-o', 'ltn_rom.hex', '-o', 'ucode.hex']
    rc = command(cmd, suite, build / 'build.log')
    result = dict(case=name, build_rc=rc)
    if rc == 0:
        log = receipts / (name + '.log')
        rc = command([str(build / 'obj/Vmilan_dp_dynmap')], suite, log)
        output = log.read_text()
        answer = module.verdict(rc, output, must_fail)
        result.update(run_rc=rc, verdict=answer, named_check=must_fail)
        result['ok'] = answer == ('caught' if must_fail else 'pass')
    else:
        result['ok'] = False
    result['seconds'] = round(time.monotonic() - started, 3)
    (receipts / (name + '.json')).write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result), flush=True)
    return result

results = [case(('clean', [], None))]
assert results[0]['ok'], 'clean control failed; inspect scratch/clean/build.log'
cases = []
for n in range(5, 12):
    leg, desc, edits, check = module.MUTATIONS[n - 1]
    assert leg == 'dynmap'
    cases.append((f'mutant-{n:02}', edits, check))
# Independent equivalence controls: the two RAM sites separately.
cases += [('capture-ram-only', [module.unheld(module.HOLD_CAPTURE_RAM)], None),
          ('render-ram-only', [module.unheld(module.HOLD_RENDER_RAM)], None)]
with ThreadPoolExecutor(max_workers=a.jobs) as pool:
    results.extend(pool.map(case, cases))
(receipts / 'campaign.json').write_text(json.dumps(results, indent=2) + '\n')
raise SystemExit(0 if all(r['ok'] for r in results) else 1)
