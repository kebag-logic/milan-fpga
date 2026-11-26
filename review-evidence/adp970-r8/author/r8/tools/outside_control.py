"""Scratch control of ctrl_configs.held's by-text classification: model_counts.py with and without its OUTSIDE entry,
and a planted unclassified program naming the firmware's tree. Argument: the checkout root."""
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / 'sw/firmware/ctrl/test'))
import ctrl_configs  # noqa: E402
from ctrl_build import Refusal  # noqa: E402
from ctrl_capture import Capture  # noqa: E402

NAME = 'tb/verilator/ctrl_service_budget/model_counts.py'
PLANT = root / 'tb/verilator/ctrl_service_budget/planted_counts.py'
EMPTY = Capture((), (), (), ())


def reasons(planted=None):
    try:
        ctrl_configs.held(EMPTY, ctrl_configs.Scope(frozenset({'verilator'})), planted, known=())
    except Refusal as e:
        return str(e).split('; ')
    return []


def about(rs, name):
    return [r for r in rs if r.startswith(name + ' names the firmware')]


rc = 0
print(f'{NAME} in OUTSIDE: {NAME in ctrl_configs.OUTSIDE}')
r = about(reasons(), NAME)
print(f'  with the entry: {len(r)} refusal(s) of it'); rc |= bool(r)
saved = ctrl_configs.OUTSIDE.pop(NAME)
r = about(reasons(), NAME)
print(f'  entry removed in memory: {len(r)} refusal(s) of it'); rc |= not r
for line in r:
    print(f'    REFUSED: {line}')
ctrl_configs.OUTSIDE[NAME] = saved
text = "TREE = 'sw/firmware/ctrl'\n\nif __name__ == '__main__':\n    print(TREE)\n"
r = about(reasons({PLANT: text}), 'tb/verilator/ctrl_service_budget/planted_counts.py')
print(f'  planted unclassified program naming the tree: {len(r)} refusal(s) of it'); rc |= not r
for line in r:
    print(f'    REFUSED: {line}')
print(f'rc={int(rc)}')
sys.exit(int(rc))
