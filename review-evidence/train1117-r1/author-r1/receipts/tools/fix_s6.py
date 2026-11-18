#!/usr/bin/env python3
"""Step 6's composition fix, applied to a tree (argv[1]):
1. grade.grade: #914's `interfaces` and `shape` are read only as `stated_at = shape or interfaces`; with #938's
   `journal` the union takes 7 parameters, past check_py_idiom's MAX_PARAMETERS (6) and its full ratchet. Fold the two
   into one, `at` (the image's shape, or an interface count at the shipping shape's streams), and pass `shape or
   interfaces` at the four callers that gave both (run.py, selftest_round.py x3). Same values reach every grader.
2. aecp_mutants.py and selftest_mutants.py: each side left them within LONG_MODULE_LINES (1,000), the union is over;
   rewrap comment runs to 120 columns, words unchanged, until each is within it."""
import re
import sys
import textwrap
from pathlib import Path

root = Path(sys.argv[1])
H = root / 'tb/verilator/ctrl_service_budget'


def sub(path: Path, old: str, new: str, count: int = 1) -> None:
    t = path.read_text()
    assert t.count(old) == count, (path, old, t.count(old))
    path.write_text(t.replace(old, new))


sub(H / 'grade.py',
    "def grade(text: str, group: scenario.Group, sys_hz: int, cpu_hz: int, interfaces: int = 2,\n"
    "          shape: shape_costs.Shape | None = None, journal: Path | None = None) -> dict:\n",
    "def grade(text: str, group: scenario.Group, sys_hz: int, cpu_hz: int,\n"
    "          at: int | shape_costs.Shape = 2, journal: Path | None = None) -> dict:\n")
sub(H / 'grade.py',
    "    whole, the polls and the slices are held to the costs stated at the image's shape (shape_costs.py, THE SHAPES), or\n"
    "    with none given at that many interfaces at the shipping shape's streams.\"\"\"\n"
    "    stated_at = shape or interfaces\n",
    "    whole, the polls and the slices are held to the costs stated at `at`, the image's shape (shape_costs.py, THE\n"
    "    SHAPES), or an interface count, that many interfaces at the shipping shape's streams.\"\"\"\n"
    "    stated_at = at\n")
sub(H / 'run.py',
    "spec['cpu_hz'], spec['interfaces'], shape,\n",
    "spec['cpu_hz'], shape or spec['interfaces'],\n")
sub(H / 'selftest_round.py',
    "sys_hz, cpu_hz, shape_costs.interfaces(interfaces),\n                           shape)",
    "sys_hz, cpu_hz,\n                           shape or shape_costs.interfaces(interfaces))", count=2)
sub(H / 'selftest_round.py',
    "sys_hz, cpu_hz, shape_costs.interfaces(given),\n"
    "                            given if isinstance(given, shape_costs.Shape) else None)",
    "sys_hz, cpu_hz,\n"
    "                            given if isinstance(given, shape_costs.Shape) else shape_costs.interfaces(given))")


def rewrap_until(path: Path, limit: int) -> int:
    lines = path.read_text().splitlines(True)
    runs = []
    i = 0
    while i < len(lines):
        m = re.match(r'^(\s*)(#: |# )\S', lines[i])
        if m:
            ind, pre = m.group(1), m.group(2)
            j = i
            while j < len(lines) and lines[j].startswith(ind + pre) and lines[j][len(ind + pre):].strip():
                j += 1
            if j - i >= 2:
                words = ' '.join(l[len(ind + pre):].strip() for l in lines[i:j])
                w = textwrap.wrap(words, width=120 - len(ind + pre), break_long_words=False, break_on_hyphens=False)
                if len(w) < j - i:
                    runs.append((j - i - len(w), i, j, [ind + pre + x + '\n' for x in w]))
            i = j
        else:
            i += 1
    over = len(lines) - limit
    chosen, saved = [], 0
    for gain, i, j, new in sorted(runs, key=lambda r: (-r[0], r[1])):
        if saved >= over:
            break
        chosen.append((i, j, new))
        saved += gain
    for i, j, new in sorted(chosen, reverse=True):
        old = ''.join(lines[i:j])
        assert ' '.join(old.replace('#:', ' ').replace('#', ' ').split()) == \
            ' '.join(''.join(new).replace('#:', ' ').replace('#', ' ').split())
        lines[i:j] = new
    path.write_text(''.join(lines))
    return len(lines)


for f in (root / 'sw/firmware/ctrl/test/aecp_mutants.py', H / 'selftest_mutants.py'):
    print(f.relative_to(root), rewrap_until(f, 1000))
print('applied')
