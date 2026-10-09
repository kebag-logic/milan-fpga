import json, os, subprocess, sys, time
from pathlib import Path
w = Path(__file__).resolve().parent
name = sys.argv[1]
spec = json.loads((w / 'jobs' / (name + '.command.json')).read_text())
e = os.environ.copy()
e.update(PYTHONUNBUFFERED='1', PYTHONDONTWRITEBYTECODE='1', PYTHONHASHSEED='0',
         MAKEFLAGS='-j16 --no-print-directory', VERILATOR_JOBS='4',
         VERILATOR=str(w / 'run-simulator-limited'), SWEEP_JOBS='4',
         TMPDIR=str(w / 'tmp'),
         MILAN_LITEX_PYTHON=str(Path.home() / 'litex-milan/venv/bin/python3'),
         LITEX_ENV_CC_TRIPLE='riscv32-linux')
e['PATH'] = str(w / 'shims') + ':$VALIDATION_TOOLS/pinned-verilator-5.050:$VALIDATION_STORAGE/231-a337-sdk/bin:' + e['PATH']
e.update(spec.get('env', {}))
cg = Path('/sys/fs/cgroup' + Path('/proc/self/cgroup').read_text().strip().split(':')[-1])
start = time.monotonic()
peak = 0
with (w / 'jobs' / (name + '.log')).open('w') as log:
    p = subprocess.Popen(spec['argv'], cwd=spec['cwd'], env=e, stdout=log, stderr=subprocess.STDOUT)
    while p.poll() is None:
        peak = max(peak, int((cg / 'memory.current').read_text()))
        time.sleep(1)
    rc = p.wait()
(w / 'jobs' / (name + '.rc')).write_text(str(rc) + '\n')
(w / 'jobs' / (name + '.result.json')).write_text(json.dumps(dict(rc=rc, seconds=round(time.monotonic() - start, 3), peak_memory_bytes=peak), indent=2) + '\n')
raise SystemExit(rc)
