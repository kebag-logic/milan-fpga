# SPDX-License-Identifier: Apache-2.0
"""Independently verify public embedded-link and propagation findings."""
import argparse, pathlib, re, subprocess, sys
p = argparse.ArgumentParser()
p.add_argument('--source', type=pathlib.Path, required=True)
p.add_argument('--packet', type=pathlib.Path, required=True)
a = p.parse_args(); source = a.source.resolve(); packet = a.packet.resolve()
runner = [sys.executable, str(packet/'scripts/run.py'), '--source', str(source), '--packet', str(packet)]
def run(label, cmd):
    return subprocess.run([*runner, '--label', label, '--', *map(str, cmd)]).returncode
sources = re.search(r'zephyr_library_sources\((.*?)\)', (source/'CMakeLists.txt').read_text(), re.S).group(1).split()
print('Embedded source list:', ', '.join(sources), flush=True)
flags = ['cc', '-std=c11', '-I'+str(source/'src/include'), '-I'+str(source/'src')]
module = [*flags, packet/'scripts/module_probe.c', *[source/x for x in sources]]
bad = run('module-list-link', [*module, '-o', packet/'scratch/module-list-link'])
good = run('module-list-control', [*module, source/'src/core/switch.c', '-o', packet/'scratch/module-list-control'])
if good == 0:
    good = run('module-list-control-run', [packet/'scratch/module-list-control'])
results = []
for profile in ['default', 'milan']:
    lib = packet/('scratch/build-'+profile); exe = packet/('scratch/map-'+profile)
    compiled = run('map-build-'+profile, [*flags, '-Wall', '-Wextra', '-Werror', packet/'scripts/map_probe.c', '-L'+str(lib), '-lshlan', '-Wl,-rpath,'+str(lib), '-o', exe])
    results.append(run('map-'+profile, [exe]) if compiled == 0 else 2)
print(f'Observed link failure={bad}; link control={good}; map discrepancies={results}')
sys.exit(0 if bad != 0 and good == 0 and results == [1, 1] else 1)
