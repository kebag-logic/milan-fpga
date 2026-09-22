"""Bounded original-driver interruption measurements in disposable fixtures."""
from pathlib import Path
import hashlib
import json
import os
import shutil
import signal
import subprocess
import time

M = Path(__file__).resolve().parent
SOURCE = Path('$VALIDATION_STORAGE/lanes/trusted-dev-20260922-512')
OUT = M / '523-readiness'
SCRATCH = Path('$VALIDATION_STORAGE/523-readiness')
assert not OUT.exists() and not SCRATCH.exists()
OUT.mkdir()
SCRATCH.mkdir()
HEAD = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=SOURCE, text=True).strip()
assert HEAD == '483a133ed08867ea0d300d2b4a027b5b48a4282f'


def write(path, text, mode=0o644):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    path.chmod(mode)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def identity(pid):
    try:
        # Fields after the closing command parenthesis begin with state (3).
        fields = Path(f'/proc/{pid}/stat').read_text().rsplit(')', 1)[1].split()
        return dict(pgid=int(fields[2]), session=int(fields[3]), start=fields[19])
    except FileNotFoundError:
        return None


def wait_file(path, process):
    deadline = time.monotonic() + 10
    while time.monotonic() < deadline:
        if path.is_file():
            return json.loads(path.read_text())
        assert process.poll() is None, process.returncode
        time.sleep(0.02)
    raise AssertionError('Mutation/child readiness handshake never arrived')


def run_case(name, kind, sig):
    root = SCRATCH / name
    root.mkdir()
    bin_dir = root / 'bin'
    bin_dir.mkdir()
    ready = root / 'ready.json'
    sentinel = root / 'later-suite'
    env = dict(os.environ, PATH=str(bin_dir) + ':' + os.environ['PATH'],
               PROBE_READY=str(ready), PROBE_SENTINEL=str(sentinel))
    real_make = '''#!/usr/bin/python3
import json,os,subprocess,sys,time
from pathlib import Path
if any(a.endswith('/omega') for a in sys.argv):
    Path(os.environ['PROBE_SENTINEL']).write_text('later suite executed\\n')
    print('1 checks: 1 PASS, 0 FAIL',flush=True)
    raise SystemExit(0)
child=subprocess.Popen(['/usr/bin/python3','-c','import time; time.sleep(120)'])
target=Path.cwd().parents[2]/'hdl/ieee8021as/gptp_plane/KL_gptp_txret.sv'
data=dict(pid=os.getpid(),pgid=os.getpgrp(),grandchild=child.pid,
          mutant_applied=target.exists() and 'if ((epi_done_i || !epi_busy_i)' in target.read_text())
Path(os.environ['PROBE_READY']).write_text(json.dumps(data))
try:
    child.wait()
finally:
    if child.poll() is None:
        child.terminate()
    child.wait()
'''
    write(bin_dir / 'make', real_make, 0o755)
    paths = []
    if kind == 'mutation':
        paths = ['tb/verilator/gptp_shadow/mutants.py'] + [
            'hdl/ieee8021as/gptp_plane/' + x for x in
            ['KL_gptp_txret.sv', 'KL_gptp_gmii_launch.sv', 'KL_gptp_txticket.sv']]
        for name_in_repo in paths:
            target = root / name_in_repo
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(SOURCE / name_in_repo, target)
        for command in [['git','init','-q'], ['git','add','.'],
                        ['git','-c','user.name=Fixture','-c','user.email=fixture@example.invalid',
                         'commit','-qm','Original interruption fixture']]:
            subprocess.run(command, cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        argv = ['/usr/bin/python3', str(root / paths[0])]
    else:
        paths = ['scripts/run_all_suites.sh']
        (root / 'scripts').mkdir()
        shutil.copy2(SOURCE / paths[0], root / paths[0])
        for suite in ['alpha', 'omega']:
            (root / 'tb/verilator' / suite).mkdir(parents=True)
        write(bin_dir / 'python3', '''#!/bin/bash
case "$1" in
  */suite_shards.py) printf 'alpha\\nomega\\n' ;;
esac
exit 0
''', 0o755)
        write(root / 'syn/yosys/check_list_hermetic.sh', '#!/bin/bash\nexit 0\n', 0o755)
        argv = ['/bin/bash', str(root / paths[0]), str(root / 'suite-logs')]
    before = {p: dict(sha256=digest(root / p), mode=(root / p).stat().st_mode & 0o777) for p in paths}
    with (OUT / (name + '.stdout')).open('wb') as stdout, (OUT / (name + '.stderr')).open('wb') as stderr:
        proc = subprocess.Popen(argv, cwd=root, env=env, start_new_session=True, stdout=stdout, stderr=stderr)
        handshake = wait_file(ready, proc)
        assert proc.pid == os.getpgid(proc.pid)
        owned = {pid: identity(pid) for pid in [handshake['pid'], handshake['grandchild']]}
        assert all(info and info['session'] == proc.pid for info in owned.values())
        if kind == 'mutation':
            assert handshake['mutant_applied']
        # The group is exclusively this fixture's new session. No global kill.
        os.killpg(proc.pid, sig)
        if handshake['pgid'] != proc.pid:
            assert owned[handshake['pid']]['pgid'] == handshake['pgid']
            os.killpg(handshake['pgid'], sig)
        try:
            rc = proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid, signal.SIGKILL)
            proc.wait()
            raise
        finally:
            # timeout creates a child process group for the sweep's command.
            # Restrict any final cleanup to the PID/PGID from our handshake.
            for pid in [handshake['pid'], handshake['grandchild']]:
                try:
                    if identity(pid) == owned[pid]:
                        os.kill(pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
    after = {p: dict(sha256=digest(root / p), mode=(root / p).stat().st_mode & 0o777) for p in paths}
    if kind == 'mutation':
        diff = subprocess.run(['git', 'diff', '--', *paths], cwd=root, capture_output=True, check=True)
        (OUT / (name + '.diff')).write_bytes(diff.stdout)
    result = dict(name=name, driver_head=HEAD, kind=kind, signal=sig.name, argv=argv,
                  handshake=handshake, exit_code=rc, before=before, after=after,
                  changed_paths=[p for p in paths if before[p] != after[p]],
                  next_suite_executed=sentinel.exists(),
                  limit='Synthetic make/preflight fixtures exercise original orchestration, not RTL correctness')
    (OUT / (name + '.json')).write_text(json.dumps(result, indent=2) + '\n')
    return result


rows = []
for name, kind, sig in [('mutation-term', 'mutation', signal.SIGTERM),
                        ('mutation-kill', 'mutation', signal.SIGKILL),
                        ('sweep-term', 'sweep', signal.SIGTERM)]:
    rows.append(run_case(name, kind, sig))
(OUT / 'results.json').write_text(json.dumps(rows, indent=2) + '\n')
print(json.dumps([{k: r[k] for k in ('name','exit_code','changed_paths','next_suite_executed')} for r in rows], indent=2))
