import concurrent.futures
import json
import os
from pathlib import Path
import subprocess

work = Path(__file__).parent
repo = Path(os.environ['REPO'])
env = os.environ.copy()
env.update(PYTHONDONTWRITEBYTECODE='1', PYTHONHASHSEED='0', MAKEFLAGS='-j16',
           VERILATOR_JOBS='2', TMPDIR=str(work / 'tmp'))
commands = {}


def run(name, argv, cwd):
    commands[name] = {'argv': argv, 'cwd': str(cwd)}
    (work / 'commands.json').write_text(json.dumps(commands, indent=2) + '\n')
    assert not (work / (name + '.log')).exists(), name
    print('START', name, flush=True)
    with (work / (name + '.log')).open('w') as log:
        rc = subprocess.run(argv, cwd=cwd, env=env, stdout=log,
                            stderr=subprocess.STDOUT).returncode
    (work / (name + '.rc')).write_text(str(rc) + '\n')
    print('DONE', name, rc, flush=True)
    return rc


def physical():
    dp = work / 'physical/tb/verilator/milan_dp'
    checks = work / 'physical/tb/verilator/milan_dp_gptp'
    jobs = [
        ('physical-build', ['make', '-j16', 'ax1x1gptp-build', 'VERILATOR_JOBS=3'], dp),
        ('physical', ['/usr/bin/time', '-f', 'wall_clock_seconds=%e process_exit_status=%x',
                      './obj_ax1x1gptp/Vmilan_dp_ax1x1gptp'], dp),
        ('accounting', ['python3', '-B', 'verify_abort.py'], checks),
        ('recentre-controls', ['python3', '-B', 'verify_recentres.py', '--jobs', '2'], checks),
    ]
    for name, argv, cwd in jobs:
        rc = run(name, argv, cwd)
        if rc:
            return rc
    return 0


def builder():
    link = repo / 'sw/builder/out'
    target = work / 'builder-out'
    assert not link.exists() and not link.is_symlink()
    target.mkdir(exist_ok=True)
    link.symlink_to(target, target_is_directory=True)
    try:
        return run('builder', ['python3', '-B', 'sw/builder/test_builder.py',
                              '--require-rv32', '--require-elaboration'], repo)
    finally:
        assert link.is_symlink() and link.resolve() == target.resolve()
        link.unlink()


def focused():
    cwd = work / 'focused/tb/verilator/milan_dp_render'
    rc = run('render-pullin', ['make', '-j16', 'tdm8render-pullin',
                             'PULLIN_JOBS=8', 'VERILATOR_JOBS=2'], cwd)
    if rc:
        return rc
    return run('render-boundary', ['python3', '-B', 'tdm8_render_mutants.py',
                                  '--law-boundary', '--jobs', '4'], cwd)


def suite(name, directory, extra=()):
    return lambda: run(name, ['make', '-j16', 'VERILATOR_JOBS=2', *extra],
                       work / 'broad/tb/verilator' / directory)


jobs = [physical, suite('datapath', 'milan_dp', ('SIM_JOBS=2',)),
        suite('render', 'milan_dp_render'), suite('media-clock', 'milan_dp_mclk'),
        suite('pp-shadow', 'pp_shadow'), builder,
        lambda: run('portability', ['bash', 'syn/yosys/run.sh'], repo), focused,
        lambda: run('source-selftest', ['python3', '-B', 'scripts/check_rtl_source_lists.py',
                                       '--selftest'], repo),
        lambda: run('wire-truth-selftest', ['python3', '-B', 'tb/tools/avtp_wire_truth.py',
                                           '--self-test'], repo)]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(lambda job: job(), jobs))
rc = int(any(results))
(work / 'all-functional.rc').write_text(str(rc) + '\n')
print('ALL FUNCTIONAL DONE', rc, flush=True)
raise SystemExit(rc)
