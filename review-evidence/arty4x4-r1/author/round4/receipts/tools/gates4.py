"""The 1x1 lane's firmware, native and memory gates, at the 4x4 shape (and the 1x1's boot beside it), two at a time,
resumable by command and head. usage: gates.py (cwd = checkout root)"""
import concurrent.futures, json, os, subprocess, sys, threading
from pathlib import Path
R = Path('$VALIDATION_STORAGE/arty4x4-a863/gates4'); ROOT = Path('$LANES/arty-4x4')
env = dict(os.environ, PYTHONHASHSEED='0', PYTHONDONTWRITEBYTECODE='1', TMPDIR='$VALIDATION_STORAGE/arty4x4-a863/work-tmp',
           COURSIER_MODE='offline', SBT_OPTS='-Dsbt.offline=true')
HEAD = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
saved = R / 'gates-results.json'
records = json.loads(saved.read_text()) if saved.exists() else []
lock = threading.Lock()
def one(name, argv):
    if any(r['name'] == name and r['command'] == argv and r['returncode'] == 0 and r['head'] == HEAD for r in records):
        print('KEPT', name, flush=True); return 0
    print('START', name, flush=True)
    with (R / (name + '.log')).open('w') as log:
        rc = subprocess.run(argv, cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT).returncode
    with lock:
        records[:] = [r for r in records if r['name'] != name]
        records.append(dict(name=name, command=argv, returncode=rc, head=HEAD))
        saved.write_text(json.dumps(records, indent=2) + '\n')
    print('DONE', name, rc, flush=True); return rc
py = sys.executable
boot = 'import sys; sys.path.insert(0, "tb/verilator/ctrl_split_boot"); import run; run.JOBS=4; raise SystemExit(run.main())'
region = 'import sys; sys.path.insert(0, "tb/verilator/ctrl_region_decode"); import run; run.JOBS=4; raise SystemExit(run.main())'
jobs = [(f'firmware-{n}', [py, '-B', 'sw/firmware/ctrl/test/test_ctrl_firmware.py', '--self-test', '--require-rv32',
         '--shard', f'{n}/4', '--jobs', '2', '--build-dir', str(R / 'firmware' / str(n))]) for n in range(4)]
jobs += [('boot-4x4', [py, '-B', '-c', boot, '--shape', 'endstation_arty_split_4x4', '--interfaces', '1',
          '--build-dir', str(R / 'boot-4x4')]),
         ('boot-native-controls-4x4', [py, '-B', 'tb/verilator/ctrl_split_boot/run.py', '--native-controls', '--shape',
          'endstation_arty_split_4x4', '--interfaces', '1', '--build-dir', str(R / 'boot-controls-4x4')]),
         ('region-4x4', [py, '-B', '-c', region, '--shape', 'endstation_arty_split_4x4', '--self-test',
          '--build-dir', str(R / 'region-4x4')]),
         ('boot-1x1', [py, '-B', '-c', boot, '--shape', 'endstation_arty_split', '--interfaces', '1',
          '--build-dir', str(R / 'boot-1x1')]),
         ('ctrl-memory', [py, '-B', 'sw/litex/test_ctrl_memory.py']),
         ('host-arms', [py, '-B', '$VALIDATION_STORAGE/arty4x4-a863/tools/host-tests.py'])]
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    rcs = list(pool.map(lambda j: one(*j), jobs))
print('GATES', 'PASS' if not any(rcs) else 'FAIL', HEAD, dict(zip([j[0] for j in jobs], rcs)), flush=True)
