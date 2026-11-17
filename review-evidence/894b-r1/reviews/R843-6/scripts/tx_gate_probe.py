#!/usr/bin/env python3
"""Mutation probe of the 8x8/1if THE TRANSMIT figure gate (flip_grade.tx_held) and of the inputs its tx row derives
from. Each mutant is applied to its own copy of a clean exact-head tree; the graders are run there and their rc and
key lines recorded. usage: python3 -I tx_gate_probe.py CLEAN_TREE WORK_DIR OUT_FILE"""
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

B = 'tb/verilator/ctrl_service_budget'
LOOP = 'sw/firmware/ctrl/loop/ctrl_loop.h'
MUTANTS = {
    'M0-none': [],
    'M1-tx74': [(LOOP, '#define CTRL_LOOP_TX_MS 75u', '#define CTRL_LOOP_TX_MS 74u')],
    'M2-tx70': [(LOOP, '#define CTRL_LOOP_TX_MS 75u', '#define CTRL_LOOP_TX_MS 70u')],
    'M3-tx60': [(LOOP, '#define CTRL_LOOP_TX_MS 75u', '#define CTRL_LOOP_TX_MS 60u')],
    'M4-tx76': [(LOOP, '#define CTRL_LOOP_TX_MS 75u', '#define CTRL_LOOP_TX_MS 76u')],
    'M5-polls-at-n_if': [(f'{B}/rows_grade.py', 'polls = poll_grade.stated_us(shape_costs.of_point(point, root))',
                          "polls = poll_grade.stated_us(load_grade.POINTS[point]['n_if'])")],
    'M6-notices-header': [(f'{B}/rows_grade.py',
                           "    h['AECP_NOTICES_MOST'] = shape_costs.notices_most(root / 'configs' / f'{config}.yaml', "
                           "n_if, root, texts)\n", '')],
    'M7-link-own-175': [(f'{B}/rows_grade.py', "'8x8/1if': {'event.LINK': 300}", "'8x8/1if': {'event.LINK': 175}")],
    'M8-long-at-n_if': [(f'{B}/rows_tiers.py',
                         "LONG_NOTICE_US = {p: poll_grade.stated_us(shape_costs.of_point(p))[poll_grade.LONG] for p in "
                         "(*POINTS, '8x8/1if')}",
                         "LONG_NOTICE_US = {p: poll_grade.stated_us(load_grade.POINTS[p]['n_if'])[poll_grade.LONG] for "
                         "p in (*POINTS, '8x8/1if')}")],
    'M9-gate-dropped-from-check': [(f'{B}/flip_grade.py', 'rows_grade.rule_findings(ROOT, rowed) + tx_held(ROOT, points)'
                                    ' + shape_costs.findings(ROOT)',
                                    'rows_grade.rule_findings(ROOT, rowed) + shape_costs.findings(ROOT)')],
    'M10-gate-filter-empty': [(f'{B}/flip_grade.py', 'tuple(p for p in points if p in REPORTED), texts)',
                               'tuple(p for p in points if p in ()), texts)')],
    'M11-M2-and-M9': [(LOOP, '#define CTRL_LOOP_TX_MS 75u', '#define CTRL_LOOP_TX_MS 70u'),
                      (f'{B}/flip_grade.py', 'rows_grade.rule_findings(ROOT, rowed) + tx_held(ROOT, points)'
                       ' + shape_costs.findings(ROOT)', 'rows_grade.rule_findings(ROOT, rowed) + shape_costs.findings(ROOT)')],
}
RUNS = {
    'flip_8x8_1if': ['python3', '-B', f'{B}/flip_grade.py', '--check', '--point', '8x8/1if'],
    'flip_all': ['python3', '-B', f'{B}/flip_grade.py', '--check'],
    'flip_selftest': ['python3', '-B', f'{B}/flip_grade.py', '--selftest'],
    'rows_tiers_selftest': ['python3', '-B', f'{B}/rows_tiers.py', '--selftest'],
    'shape_costs': ['python3', '-B', f'{B}/shape_costs.py', '--check', '--selftest'],
}


def key(text: str) -> str:
    keep = [ln for ln in text.splitlines() if ln.startswith(('HELD', 'OVER 8x8/1if', 'RESULT', 'flip check', 'rows_tiers:',
                                                            'Traceback', 'ESCAPED', 'escaped'))
            or 'Error' in ln or 'refused' in ln]
    return ' | '.join(keep[-6:])


def one(name: str, clean: Path, work: Path) -> str:
    tree = work / name
    if not tree.exists():
        shutil.copytree(clean, tree, symlinks=True)
    for rel, old, new in MUTANTS[name]:
        p = tree / rel
        t = p.read_text()
        assert t.count(old) == 1, (name, rel, old)
        p.write_text(t.replace(old, new))
    out = [f'## {name}: ' + '; '.join(f'{r}: {o!r} -> {n!r}' for r, o, n in MUTANTS[name])]
    for run, cmd in RUNS.items():
        r = subprocess.run(cmd, cwd=tree, capture_output=True, text=True, timeout=1200)
        out.append(f'{run} rc={r.returncode}: {key(r.stdout + r.stderr)}')
    return '\n'.join(out)


def main() -> int:
    clean, work, dst = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    work.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=12) as ex:
        res = list(ex.map(lambda n: one(n, clean, work), MUTANTS))
    dst.write_text('\n\n'.join(res) + '\n')
    print(dst.read_text())
    return 0


if __name__ == '__main__':
    sys.exit(main())
