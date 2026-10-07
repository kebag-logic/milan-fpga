"""Every functional gate touched by the dev 6a05347d merge (f6bd415f), three lanes.

Default shard 1/2 (milan_dp, 12,064 checks) completed rc 0 in merged-gates/;
everything else is run here. Two lanes of at most one heavy job each:
  lane 1 (tree export):     shard 0/2 -> render pull-in -> LAW boundary -> portability
  lane 2 (physical/builder): physical gPTP -> builder -> source and wire selftests
then the vendor parser under the shared lock once both lanes are idle.
Each command keeps its own log and rc; a resource guard stops everything.
"""
from pathlib import Path
import json, os, signal, subprocess, threading, time

work = Path(__file__).resolve().parent
out = work / 'merged-gates-f'
out.mkdir(exist_ok=True)
e = os.environ.copy()
e.update(PYTHONDONTWRITEBYTECODE='1', PYTHONHASHSEED='0', MAKEFLAGS='-j8', VERILATOR_JOBS='2',
         VERILATOR=str(work / 'run-simulator-limited'), SWEEP_JOBS='4', SIM_JOBS='2', PULLIN_JOBS='4',
         TMPDIR=str(work.parent / 'tmp'), MILAN_LITEX_PYTHON=str(Path.home() / 'litex-milan/venv/bin/python3'),
         LITEX_ENV_CC_TRIPLE='riscv32-linux', SUITE_TIMEOUT='14400')
e['PATH'] = str(work / 'shims') + ':$VALIDATION_TOOLS/pinned-verilator-5.050:$VALIDATION_STORAGE/231-a337-sdk/bin:' + e['PATH']
cg = Path('/sys/fs/cgroup') / open('/proc/self/cgroup').read().strip().split('::', 1)[1].lstrip('/')
rows = []
lock = threading.Lock()
abort = threading.Event()


def run(name, argv, cwd, env=e):
    if abort.is_set():
        return 125
    print(time.strftime('%FT%T'), 'START', name, int((cg / 'memory.current').read_text()), flush=True)
    peak = 0
    interrupted = False
    t0 = time.time()
    with (out / (name + '.log')).open('w') as log:
        child = subprocess.Popen(argv, cwd=cwd, env=env, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
        while child.poll() is None:
            current = int((cg / 'memory.current').read_text())
            peak = max(peak, current)
            if current > 8800000000 or abort.is_set():
                interrupted = True
                abort.set()
                os.killpg(child.pid, signal.SIGTERM)
                time.sleep(3)
                if child.poll() is None:
                    os.killpg(child.pid, signal.SIGKILL)
                break
            time.sleep(1)
        rc = child.wait()
    (out / (name + '.rc')).write_text(str(rc) + '\n')
    with lock:
        rows.append({'name': name, 'argv': argv, 'cwd': str(cwd), 'rc': rc, 'wall_seconds': round(time.time() - t0, 1),
                     'peak_memory_bytes': peak, 'resource_interruption': interrupted})
        (out / 'commands.json').write_text(json.dumps(rows, indent=2) + '\n')
    print(time.strftime('%FT%T'), 'DONE', name, rc, flush=True)
    return rc


results = {}


def lane1():
    root = work / 'physical'
    results['sweep-0'] = run('sweep-0', ['bash', 'scripts/run_all_suites.sh', str(out / 'sweep-0'), '--shard', '0/2'], root)
    results['sweep-1'] = run('sweep-1', ['bash', 'scripts/run_all_suites.sh', str(out / 'sweep-1'), '--shard', '1/2'], root)


def lane2():
    root = work / 'builder'
    results['physical'] = run('physical', ['bash', 'scripts/run_all_suites.sh', str(out / 'physical'), '--physical-gptp'], root)
    results['builder'] = run('builder', ['python3', '-B', 'sw/builder/test_builder.py', '--require-rv32', '--require-elaboration'], root)
    results['source-controls'] = run('source-controls', ['python3', '-B', 'scripts/check_rtl_source_lists.py', '--selftest'], root)
    results['wire-controls'] = run('wire-controls', ['python3', '-B', 'tb/tools/avtp_wire_truth.py', '--self-test'], root)


def lane3():
    tree = work / 'tree'
    render = tree / 'tb/verilator/milan_dp_render'
    results['render-pullin'] = run('render-pullin', ['make', '-j8', 'tdm8render-pullin', 'PULLIN_JOBS=4', 'VERILATOR_JOBS=2'], render)
    results['render-boundary'] = run('render-boundary', ['make', '-j8', 'tdm8render-law-boundary', 'LAW_BOUNDARY_JOBS=2', 'VERILATOR_JOBS=2'], render)
    results['portability'] = run('portability', ['bash', 'syn/yosys/run.sh'], tree)


threads = [threading.Thread(target=f) for f in (lane1, lane2, lane3)]
for t in threads:
    t.start()
for t in threads:
    t.join()
rc = int(any(results.values()))
(out / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
(out / 'all.rc').write_text(str(rc) + '\n')
raise SystemExit(rc)
