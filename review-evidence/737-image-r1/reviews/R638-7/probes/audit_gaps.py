"""Run planted steps through the head's exec audit (imported from the clone) and print each judgment.

usage: python3 audit_gaps.py CLONE WORKDIR   (python3 on PATH must be a CPython 3.12 with pip)
"""
import json, os, shutil, subprocess, sys, zipfile
from pathlib import Path
clone, work = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(clone / 'ci/image'))
import exec_audit
names = exec_audit.allowlist()
env = {'PATH': os.environ['PATH'], 'HOME': str(work), 'LC_ALL': 'C.UTF-8', 'LANG': 'C.UTF-8'}
if work.exists():
    shutil.rmtree(work)
(work / 'bin').mkdir(parents=True)
wheel = work / 'zz_probe_pkg-0.1-py3-none-any.whl'
with zipfile.ZipFile(wheel, 'w') as archive:
    archive.writestr('zz_probe_pkg/__init__.py', '')
    archive.writestr('zz_probe_pkg-0.1.dist-info/METADATA', 'Metadata-Version: 2.1\nName: zz-probe-pkg\nVersion: 0.1\n')
    archive.writestr('zz_probe_pkg-0.1.dist-info/WHEEL', 'Wheel-Version: 1.0\nGenerator: fixture\nRoot-Is-Purelib: true\nTag: py3-none-any\n')
    archive.writestr('zz_probe_pkg-0.1.dist-info/RECORD', '')
shutil.copy('/usr/bin/true', work / 'bin/zz_hidden')   # an unlisted program copied from the system: no provenance
source = Path(__file__).with_name('compat_exec.c')
build = f"cc -O0 -o {work}/bin/zz_compat {source} && "  # built inside the traced step, so it has provenance
pip = f"['pip','install','--no-index','--no-deps','--disable-pip-version-check','--target','{work}/inst-%s','{wheel}']"
runpy = "import runpy,sys; sys.argv=%s; runpy.run_module('pip', run_name='__main__')"
cases = [
 ('control: -m pip local-wheel install', f"python3 -m pip install --no-index --no-deps --disable-pip-version-check --target {work}/inst-m {wheel} && test -f {work}/inst-m/zz_probe_pkg/__init__.py"),
 ('control: copied unlisted program, direct exec', f"{work}/bin/zz_hidden"),
 ('inline python program installs the wheel', f"python3 -c \"{runpy % (pip % 'c')}\" && test -f {work}/inst-c/zz_probe_pkg/__init__.py"),
 ('streamed python program (not from a fetcher) installs the wheel', f"printf '%s\\n' \"{runpy % (pip % 's')}\" | python3 - && test -f {work}/inst-s/zz_probe_pkg/__init__.py"),
 ('memfd exec (fexecve) of the copied unlisted program', f"python3 -c \"import ctypes,os; fd=ctypes.CDLL(None,use_errno=True).syscall(319, b'zz', 0); os.write(fd, open('{work}/bin/zz_hidden','rb').read()); os.execve(fd, ['zz_hidden'], {{}})\""),
 ('int 0x80 (i386 entry) exec of the copied unlisted program', build + f"{work}/bin/zz_compat i {work}/bin/zz_hidden"),
 ('x32 entry exec of the copied unlisted program', build + f"{work}/bin/zz_compat x {work}/bin/zz_hidden"),
]
out = []
for label, command in cases:
    report = exec_audit.audit_step({'job': 'probe', 'label': label, 'argv': ['bash', '-e', '-c', command]}, names, work, env)
    reasons = [f['reason'] for f in report['findings'] if 'python3.12' not in f['reason'] or 'installer' in f['reason']]
    pops = [(p['kind'], p['invocation'], p['provenance']) for p in report['population']]
    row = {'case': label, 'exit_status': report['exit_status'], 'instances': report['instances'],
           'findings': reasons, 'population': pops}
    out.append(row)
    print(json.dumps(row))
