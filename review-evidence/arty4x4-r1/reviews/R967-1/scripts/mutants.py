"""Disposable mutation probes of the lane's 4x4 delta, each in its own copy of the reviewed tree.

Each mutant edits one file in its copy (an exact, unique text replacement), then runs the named checks there.
A mutant is CAUGHT when at least one check exits non-zero; otherwise it SURVIVED. The clean copy runs the same
checks first and must pass them all. Nothing in the source clone is written.

usage: python3 -I mutants.py CLONE WORKDIR OUT_JSON [--jobs N]
"""
import concurrent.futures
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

H = 'tb/verilator/ctrl_service_budget'
CHECKS = {
    'arty-4x4': ['python3', '-B', f'{H}/arty_grade.py', '--point', 'arty-4x4'],
    'arty-selftest': ['python3', '-I', '-B', f'{H}/arty_grade.py', '--selftest'],
    'ledger-selftest': ['python3', '-I', '-B', f'{H}/egress_ledger.py', '--selftest'],
    'mii-selftest': ['python3', '-I', '-B', f'{H}/egress_mii.py', '--selftest'],
    'record-selftest': ['python3', '-I', '-B', f'{H}/record_classes.py', '--selftest'],
    'shape-check': ['python3', '-I', '-B', f'{H}/shape_costs.py', '--check'],
    'load-check': ['python3', '-I', '-B', f'{H}/load_grade.py', '--check'],
}
LOOP = 'sw/firmware/ctrl/loop/ctrl_loop.h'
ROW = '#elif CTRL_LOOP_SHAPE(1u, 5u, 5u)'
MUTANTS = {
    'crf-frame-not-counted': (f'{H}/egress_mii.py', '    return aaf + crf\n', '    return aaf\n', None),
    'crf-avtpdu-zero': (f'{H}/egress_mii.py', 'CRF_AVTPDU = 28\n', 'CRF_AVTPDU = 0\n', None),
    'row-tx-28': (LOOP, '#define CTRL_LOOP_TX_MS 29u\n', '#define CTRL_LOOP_TX_MS 28u\n', None),
    'row-queued-130': (LOOP, '#define CTRL_LOOP_QUEUED_MS 125u\n#define CTRL_LOOP_TX_MS 29u\n',
                       '#define CTRL_LOOP_QUEUED_MS 130u\n#define CTRL_LOOP_TX_MS 29u\n', None),
    'row-slice-1000': (LOOP, ROW + '      // Arty FPGA 4x4: one interface, four AAF and the CRF each way, 100 MHz\n'
                       '#define CTRL_LOOP_SLICE_US 1250u\n',
                       ROW + '      // Arty FPGA 4x4: one interface, four AAF and the CRF each way, 100 MHz\n'
                       '#define CTRL_LOOP_SLICE_US 1000u\n', None),
    'row-pace-10': (LOOP, '#define AECP_NOTICE_US 195u\n#define AECP_PACE_MS 5u\n',
                    '#define AECP_NOTICE_US 195u\n#define AECP_PACE_MS 10u\n', None),
    'config-sys-80mhz': ('configs/endstation_arty_split_4x4.yaml', 'sys_clk_hz: 100000000 ',
                         'sys_clk_hz: 80000000  ', None),
    'grade-clock-80mhz': (f'{H}/arty_grade.py', "CLOCKS = {POINT: CLOCK_HZ, 'arty-4x4': 100_000_000}",
                          "CLOCKS = {POINT: CLOCK_HZ, 'arty-4x4': 80_000_000}", None),
    'record-clock-80mhz': (f'{H}/record_classes.py', "ARTY_CLOCKS = {'arty-1x1': 80_000_000, 'arty-4x4': 100_000_000}",
                           "ARTY_CLOCKS = {'arty-1x1': 80_000_000, 'arty-4x4': 80_000_000}", None),
    'doc-ledger-63.49': ('docs/design/SPLIT_CONTROL_MEMORY.md', '| `backlog.owed_behind3.if0` | 63.32736 | 63.50 |',
                         '| `backlog.owed_behind3.if0` | 63.32736 | 63.49 |', None),
    'measured-behind3-up': (f'{H}/egress_ledger.py', "'backlog.owed_behind3.if0': 63.32736",
                            "'backlog.owed_behind3.if0': 63.33736", None),
    'ledger-4x4-cycle-12.5ns': (f'{H}/egress_ledger.py', "'arty-4x4': 100_000}", "'arty-4x4': 80_000}", None),
    'poll-base-under': (f'{H}/poll_grade.py', "    'base': 230, 'withdraw': 100, 'rebuild': 185,",
                        "    'base': 200, 'withdraw': 100, 'rebuild': 185,", None),
    'arty-shapes-drop-155': (f'{H}/shape_costs.py', 'ARTY_SHAPES = ((1, 1, 2), (1, 5, 5))',
                             'ARTY_SHAPES = ((1, 1, 2),)', None),
}


def copy_tree(clone: Path, dst: Path) -> None:
    shutil.copytree(clone, dst, symlinks=True, ignore=shutil.ignore_patterns('.git'))


def run_checks(tree: Path) -> dict:
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONHASHSEED='0')
    out = {}
    for name, cmd in CHECKS.items():
        r = subprocess.run(cmd, cwd=tree, env=env, capture_output=True, text=True, timeout=900)
        tail = (r.stdout + r.stderr).strip().splitlines()[-6:]
        refused = [ln for ln in (r.stdout + r.stderr).splitlines() if ln.startswith(('REFUSED', 'FAIL', 'MISSED', '- '))]
        out[name] = dict(rc=r.returncode, refused=refused[:6], tail=tail)
    return out


def one(name: str, clone: Path, work: Path) -> dict:
    tree = work / name
    if tree.exists():
        shutil.rmtree(tree)
    copy_tree(clone, tree)
    if name != 'clean':
        path, old, new, _ = MUTANTS[name]
        text = (tree / path).read_text()
        if text.count(old) != 1:
            return dict(name=name, error=f'{path}: the anchor occurs {text.count(old)} times')
        (tree / path).write_text(text.replace(old, new))
    res = run_checks(tree)
    shutil.rmtree(tree)
    caught = [c for c, r in res.items() if r['rc'] != 0]
    return dict(name=name, mutation=None if name == 'clean' else dict(zip(('file', 'old', 'new'), MUTANTS[name][:3])),
                caught_by=caught, verdict=('CLEAN-PASS' if not caught else 'CLEAN-FAIL') if name == 'clean'
                else ('CAUGHT' if caught else 'SURVIVED'), checks=res)


def main(argv: list[str]) -> int:
    clone, work, out = Path(argv[0]), Path(argv[1]), Path(argv[2])
    jobs = int(argv[4]) if len(argv) > 4 and argv[3] == '--jobs' else 8
    work.mkdir(parents=True, exist_ok=True)
    names = ['clean', *MUTANTS]
    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as pool:
        rows = list(pool.map(lambda n: one(n, clone, work), names))
    out.write_text(json.dumps(rows, indent=1) + '\n')
    for r in rows:
        print(f"{r['name']}: {r.get('verdict', r.get('error'))} {r.get('caught_by', '')}")
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
