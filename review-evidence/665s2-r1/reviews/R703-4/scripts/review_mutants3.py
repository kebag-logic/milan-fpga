#!/usr/bin/env python3
"""Reviewer-owned source mutants for round 3 of the budget harness, each run against the
harness's own self-test (run.py --self-test must exit non-zero to count as caught).

Usage: review_mutants3.py SANDBOX_ROOT
SANDBOX_ROOT holds tb/verilator/ctrl_service_budget.orig (a copy of the head's harness) with
every other path linked to the checkout. S* omit load work from the scenario's source (not
through Group.offer, which the harness's own mutants patch); G* plant defects in the grading
code the round added (service, release, owed responses, never answered, fan-out cost); H* are
further composition defects that lower the composed maximum. Each is one exact-text edit; an
anchor that is not unique is reported, not run.
"""
import shutil
import subprocess
import sys
from pathlib import Path

G, S = 'grade.py', 'scenario.py'
MUTANTS = [
    # Load omission in the scenario's source
    ('S1', S, '        if channel == own:\n            continue\n',
     "        if channel in (own, 'srp'):\n            continue\n", 'load: composed_load omits SRP in every row'),
    ('S2', S, '        if channel == own:\n            continue\n',
     "        if channel in (own, 'maap'):\n            continue\n", 'load: composed_load omits MAAP in every row'),
    ('S3', S, "    behind = admission('acmp', get(0))['at_once'] - OWED_AHEAD - 1\n", '    behind = 0\n',
     'load: the owed row omits the ACMP commands behind its input'),
    ('S4', S, '    for n in range(count - 1):\n        g.offer', '    for n in range(count - 5):\n        g.offer',
     'load: the backlog row omits four of its ACMP commands'),
    ('S5', S, '        if channel == own:\n            continue\n',
     "        if channel == own or (channel == 'srp' and p.interfaces > 1):\n            continue\n",
     'load: SRP omitted at the two-interface point only'),
    ('S6', S, "        composed_load(g, p, own='adp')\n", "        composed_load(g, p, own='adp', counts={'srp': 0})\n",
     'load: SRP omitted in the bound-talker rows only'),
    ('S7', S, "    composed_load(g, p, own='acmp')\n    for n in range(OWED_AHEAD):",
     "    composed_load(g, p, own='acmp', counts={'aecp': 8})\n    for n in range(OWED_AHEAD):",
     'load: the owed row carries half the AECP burst'),
    ('S8', S, "    g.add('gap 1', 'mark composed')\n    gm_run(g, p)\n", "    g.add('gap 1', 'mark composed')\n    gm_run(g, p, 14)\n",
     'load: the event row carries 14 grandmaster changes'),
    # The round's new grading code
    ('G1', G, '        out.append((c, interface, at if released >= end else None))',
     '        out.append((c, interface, at))', 'service: a record is released by any tail write before the run ends'),
    ('G2', G, "            released += (value - last) & 0xFFFF", "            released += value - last",
     'service: the 16-bit tail counter is not taken modulo 2^16'),
    ('G3', G, '(r is None or r > end))', 'r is None)',
     'service: a record released after the window closed counts as released inside it'),
    ('G4', G, '                admission=group.admission, serviced=not left, unreleased=left,',
     '                admission=group.admission, serviced=True, unreleased=left,',
     'service: every window reports its load released'),
    ('G5', G, "        for which, n in (('first', inside[0]), ('last', inside[-1])):",
     "        for which, n in (('first', inside[0]),):", "service: only each channel's first record is graded"),
    ('G6', G, "                                 // max(1, len(cycles) - 1)) if cycles else dict(recipients=0)",
     "                                 // max(1, len(cycles))) if cycles else dict(recipients=0)",
     'fan-out: the per-recipient cost divides by the recipients, not the gaps'),
    ('G7', G, "    if not check and probe.owed and row['owed_ahead'] != owed:",
     "    if not check and probe.owed and len(row['owed_ahead']) != len(owed):",
     'owed: only the number of responses ahead is checked, not their sequence'),
    ('G8', G, '    if missing and probe.may_drop and all(spec.startswith(\'resp\') for spec in missing):',
     '    if missing and all(spec.startswith(\'resp\') for spec in missing):',
     'never answered: every probe may drop its response'),
    ('G9', G, '                       ahead=sum(1 for _, _, r in records[:n] if r is None or r > commit),',
     '                       ahead=sum(1 for _, _, r in records[:n] if r is None),',
     'service: the records ahead count only those never released'),
    ('G10', G, "    load['GM'] = CONTRACT.evt_words // CONTRACT.ev_words - 1",
     "    load['GM'] = CONTRACT.evt_words // CONTRACT.ev_words - 2", 'defined load: one grandmaster change fewer'),
    # Further composition defects that lower the composed maximum
    ('H1', G, '    top = max(inside, key=lambda p: p.cycles)', '    top = inside[-1]',
     "composition: the composed maximum is the window's last pass"),
    ('H2', G, '    top = max(inside, key=lambda p: p.cycles)', '    top = sorted(inside, key=lambda p: p.cycles)[len(inside) // 2]',
     "composition: the composed maximum is the window's median pass"),
    ('H3', G, '    return [p for p in log.passes if start <= p.start_sys <= end]',
     '    return [p for p in log.passes if start <= p.start_sys <= end and p.cycles < 1_000_000]',
     'composition: passes over 1 M cycles are dropped from the window'),
]


def main() -> int:
    root = Path(sys.argv[1]).resolve()
    orig = root / 'tb/verilator/ctrl_service_budget.orig'
    work = root / 'tb/verilator/ctrl_service_budget'
    escaped = 0
    for ident, name, old, new, what in MUTANTS:
        shutil.rmtree(work, ignore_errors=True)
        shutil.copytree(orig, work)
        path = work / name
        text = path.read_text()
        if text.count(old) != 1:
            print(f'{ident} ANCHOR-NOT-UNIQUE ({text.count(old)}) {what}')
            escaped += 1
            continue
        path.write_text(text.replace(old, new))
        result = subprocess.run([sys.executable, '-B', str(work / 'run.py'), '--self-test'],
                                capture_output=True, text=True)
        failed = [line for line in result.stdout.splitlines() if line.startswith(('FAIL', 'MUTANT ESCAPED'))]
        verdict = 'CAUGHT' if result.returncode else 'ESCAPED'
        escaped += verdict == 'ESCAPED'
        print(f'{ident} {verdict} rc={result.returncode} {what}' + (f' :: {failed[0][:160]}' if failed else ''),
              flush=True)
    shutil.rmtree(work, ignore_errors=True)
    shutil.copytree(orig, work)
    print(f'review mutants: {len(MUTANTS)} run, {escaped} escaped the self-test')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
