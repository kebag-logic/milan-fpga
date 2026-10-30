#!/usr/bin/env python3
"""Plant the removal of the current flash writer's 24.5 ms check in a scratch export of the checkout's
HEAD and run that writer's gate, scripts/check_nvm_capture.py, on it; then the same gate on an unplanted
export as the control. Prints each run's rc and output; exit 0 when the planted run fails with
'OFF timing limit was ignored' and the unplanted run passes.

Usage: plant_d5_removed.py CHECKOUT SCRATCH
"""
import subprocess
import sys
from pathlib import Path

checkout, scratch = Path(sys.argv[1]), Path(sys.argv[2])
CHECK = ("        if (spec.get('mutation', 'none') == 'none'\n"
         "                and row['sys_cycles'] * 2000 > HOLD_FLOOR_MS * spec['sys_hz']):\n"
         "            raise RuntimeError('worst measured copy exceeds half the 49 ms hold floor')\n")


#: The submodules the builder reads: nvm_shape.build loads a config, whose gPTP dataset the
#: gptp-processor generator derives, and builds the AEM image from protocol-processor.
SUBMODULES = ('gptp-processor', 'protocol-processor')


def git(*args: str, cwd: Path) -> str:
    """One git command's output; it must succeed."""
    return subprocess.run(['git', *args], cwd=cwd, capture_output=True, text=True, check=True).stdout.strip()


def export(name: str) -> Path:
    """A shared local clone of the checkout at HEAD in scratch/name, with the builder's submodules cloned
    the same way at the commits HEAD records; each submodule is checked to be its own toplevel first.
    Nothing is written to the checkout."""
    tree = scratch / name
    subprocess.run(['rm', '-rf', str(tree)], check=True)
    git('clone', '-q', '--shared', '--no-checkout', str(checkout), str(tree), cwd=scratch)
    git('checkout', '-q', '--detach', git('rev-parse', 'HEAD', cwd=checkout), cwd=tree)
    for sub in SUBMODULES:
        if Path(git('rev-parse', '--show-toplevel', cwd=checkout / sub)) != checkout / sub:
            raise SystemExit(f'{sub} is not its own repository')
        pinned = git('rev-parse', f'HEAD:{sub}', cwd=checkout)
        subprocess.run(['rm', '-rf', str(tree / sub)], check=True)
        git('clone', '-q', '--shared', '--no-checkout', str(checkout / sub), str(tree / sub), cwd=scratch)
        git('checkout', '-q', '--detach', pinned, cwd=tree / sub)
    return tree


def gate(tree: Path) -> tuple[int, str]:
    """check_nvm_capture.py in tree: its rc and output."""
    run = subprocess.run([sys.executable, 'scripts/check_nvm_capture.py'], cwd=tree, capture_output=True, text=True)
    return run.returncode, run.stdout + run.stderr


head = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=checkout, capture_output=True, text=True,
                      check=True).stdout.strip()
print(f'head {head}')
control = export('d5-control')
rc_control, out_control = gate(control)
print(f'== unplanted: rc={rc_control}\n{out_control}')
planted = export('d5-planted')
grader = planted / 'tb/verilator/nvm_capture_cpu/run.py'
source = grader.read_text()
if source.count(CHECK) != 1:
    raise SystemExit("the current writer's 24.5 ms check is not in its grader once")
grader.write_text(source.replace(CHECK, ''))
rc_planted, out_planted = gate(planted)
print(f'== planted (the 24.5 ms check removed from grade_rows): rc={rc_planted}\n{out_planted}')
ok = rc_control == 0 and rc_planted != 0 and 'OFF timing limit was ignored' in out_planted
print('PLANT CAUGHT' if ok else 'PLANT ESCAPED OR CONTROL FAILED')
sys.exit(0 if ok else 1)
