#!/usr/bin/env python3
"""Reviewer probes for PR #898 (issue #897): GET_AS_PATH through the AECP face.

Plants each named defect into a disposable copy of sw/firmware/ctrl (never the
checkout) and requires the named GoogleTest test to fail on its own words, with
the repository's own arms and diagnostic readers. Also runs the unmutated arms
as a baseline.

usage:
  probe_898.py --repo <clone> --out <dir> baseline-aecp        # app-mode suite at 1 and 2 interfaces
  probe_898.py --repo <clone> --out <dir> baseline-plat        # plat, platboot1, platboot2 arms
  probe_898.py --repo <clone> --out <dir> aecp NAME [NAME...]  # author plants (aecp_mutants) or reviewer plants
  probe_898.py --repo <clone> --out <dir> plat NAME [NAME...]  # author plat plants (ctrl_mutants) or reviewer plants
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

FACE = 'aecp_face.c'
COUNT = 'if (!gsi(f, interface, 2u, AVB_INTERFACE, index, 0u, 0u, 0u, &n) || n > capacity) {'
ENTRY = 'if (!gsi(f, interface, 2u, AVB_INTERFACE, index, 8u, k, 0u, &out[k])) {'
T1 = 'Face.AsPathIsTheDatapathsSequenceThroughItsOwnWindow'
T2 = 'Face.AsPathCarriesItsWholeBoundAndFailsACountPastIt'
T3 = 'Face.AnUnansweredAsPathWordFailsItsPortThere'
T4 = 'AppFace.AnAsPathChangeNotifiesTheDatapathsSequence'

#: Reviewer plants, independent of the author's table: (name, file under ctrl/, old, new, ((test, words), ...)).
REVIEWER_AECP = (
    ('rv-count-never-reported', 'aecp/' + FACE, '\t*count = (size_t)n;\n', '\t*count = 0u;\n',
     ((T1, "the count, the datapath's"),)),
    ('rv-caller-capacity-ignored', 'aecp/' + FACE, COUNT, COUNT.replace('n > capacity', 'n > (capacity | AECP_PATH_ITEMS)'),
     ((T2, 'one past the capacity fails the port'),)),
    ('rv-entry-ordinal-plus-one', 'aecp/' + FACE, ENTRY, ENTRY.replace('8u, k, 0u', '8u, k + 1u, 0u'),
     ((T1, 'in order'),)),
    ('rv-last-entry-not-read', 'aecp/' + FACE, 'for (unsigned k = 0; k < (unsigned)n; ++k) {',
     'for (unsigned k = 1; k < (unsigned)n; ++k) {', ((T1, 'the count, then each entry once'),)),
    ('rv-entry-byte-order-swapped', 'aecp/' + FACE, ENTRY + '\n\t\t\treturn false;\n\t\t}\n',
     ENTRY + '\n\t\t\treturn false;\n\t\t}\n\t\tout[k] = __builtin_bswap64(out[k]);\n',
     ((T1, 'in order'),)),
    ('rv-entry-index-zero', 'aecp/' + FACE, ENTRY, ENTRY.replace('AVB_INTERFACE, index, 8u', 'AVB_INTERFACE, 0u, 8u'),
     ((T1, 'of its AVB_INTERFACE'),)),
    ('rv-count-type-zero', 'aecp/' + FACE, COUNT, COUNT.replace('2u, AVB_INTERFACE, index, 0u', '2u, 0u, index, 0u'),
     ((T1, 'of its AVB_INTERFACE'),)),
    ('rv-entry-through-first-window', 'aecp/' + FACE, ENTRY, ENTRY.replace('gsi(f, interface, 2u', 'gsi(f, 0u, 2u'),
     ((T1, "read through its own interface's window"),)),
    ('rv-as-path-event-dropped', 'app/ctrl_app_aecp.c', 'ctrl_app_aecp_changed(c, 9u, e->interface, 4u);',
     '(void)c;', ((T4, 'an AS_PATH change notifies GET_AS_PATH'),)),
    ('rv-path-not-in-face-ports', 'aecp/' + FACE, '.avb = avb, .path = path,', '.avb = avb,',
     ((T1, 'its descriptor_index'),)),
)

#: Reviewer platform plants: (name, file under ctrl/, old, new, arm, test, words, also)
REVIEWER_PLAT = (
    ('rv-plat-entries-dropped', 'aecp/' + FACE, '\t*count = (size_t)n;\n', '\t*count = n != 0u ? 1u : 0u;\n',
     'platboot1', 'Boot.B11GetAsPathAnswersTheDatapathsSequence', 'B11 the count the datapath serves',
     (('platboot2', 'Boot.B11GetAsPathAnswersTheDatapathsSequence', 'B11 the count the datapath serves'),)),
)


def setup(repo: Path) -> None:
    sys.path[:0] = [str(repo / 'sw/firmware/ctrl/test'), str(repo / 'sw/firmware/gtest')]


def copy_tree(repo: Path, dest: Path) -> Path:
    ctrl = repo / 'sw/firmware/ctrl'
    if dest.exists():
        shutil.rmtree(dest)
    src = dest / 'ctrl'
    shutil.copytree(ctrl, src, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    shutil.copytree(ctrl.parent / 'ctrl_nvm', dest / 'ctrl_nvm', ignore=shutil.ignore_patterns('test', '__pycache__'))
    return src


def plant(src: Path, path: str, old: str, new: str) -> None:
    target = src / path
    text = target.read_text()
    if text.count(old) != 1:
        raise SystemExit(f'REFUSED: fixture occurs {text.count(old)} times in {path}')
    target.write_text(text.replace(old, new))


def run_aecp(repo: Path, out: Path, names: list[str], jobs: int) -> list[dict]:
    import aecp_arms, aecp_mutants, fw_gtest
    from ctrl_build import Tree, Refusal
    config = repo / 'configs/endstation_ax7101_1x1_tdm8.yaml'
    # the author's table: defect() already prefixes aecp/ to a bare file name
    author = {d.name: (d.path, d.old, d.new, d.checks) for d in aecp_mutants.DEFECTS}
    mine = {n: (p, o, w, c) for n, p, o, w, c in REVIEWER_AECP}
    results = []
    build = fw_gtest.Build(jobs=jobs)
    for name in names:
        path, old, new, checks = author.get(name) or mine[name]
        work = out / ('work-' + name)
        src = copy_tree(repo, work)
        plant(src, path, old, new)
        tree = Tree(src, work / 'build', work / 'reuse', build, aecp_mutants.STACK)
        selected = ':'.join(t for t, _ in checks)
        try:
            outcome = aecp_arms.core_arm(tree, config, 2, 'app', selected)
        except Refusal as error:
            outcome = None
            log = f'refused: {error}'
        log = outcome.log if outcome else log
        ok = outcome is not None and all(aecp_mutants.caught(t, w, outcome) for t, w in checks)
        (out / (name + '.log')).write_text(log)
        results.append({'name': name, 'origin': 'author' if name in author else 'reviewer', 'file': path,
                        'checks': checks, 'rc': outcome.rc if outcome else 2, 'caught': ok})
        print(f"[{'ok' if ok else 'ESCAPED'}] {name}: {selected}", flush=True)
        shutil.rmtree(work, ignore_errors=True)
    return results


def run_plat(repo: Path, out: Path, names: list[str], jobs: int) -> list[dict]:
    import ctrl_mutants, plat_arms, fw_gtest
    from ctrl_build import Tree, Refusal, Outcome
    from ctrl_mutant import Mutant
    arms = {'platboot1': lambda t: plat_arms.arm_platboot(t, 1), 'platboot2': lambda t: plat_arms.arm_platboot(t, 2)}
    author = {m.name: m for m in ctrl_mutants.MUTANTS}
    mine = {r[0]: Mutant(*r) for r in REVIEWER_PLAT}
    results = []
    for name in names:
        m = author.get(name) or mine[name]
        root = out / ('work-' + name)
        ctrl, stack = ctrl_mutants.plant(m, root)
        tree = Tree(ctrl, root / 'work' / 'build', root / 'reuse', fw_gtest.Build(jobs=jobs), stack)
        missed, logs = [], []
        for arm, test, needle in m.kills():
            try:
                outcome = arms[arm](tree)
            except Refusal as exc:
                outcome = Outcome(arm, 2, f'refused: {exc}')
            logs.append(f'==== {arm}\n{outcome.log}')
            if not ctrl_mutants.caught(test, needle, outcome):
                missed.append(f'{arm}: {test} on {needle!r}')
        (out / (name + '.log')).write_text('\n'.join(logs))
        results.append({'name': name, 'origin': 'author' if name in author else 'reviewer', 'file': m.path,
                        'kills': m.kills(), 'caught': not missed, 'missed': missed})
        print(f"[{'ok' if not missed else 'ESCAPED'}] {name}: {', '.join(k[0] for k in m.kills())} {missed}", flush=True)
        shutil.rmtree(root, ignore_errors=True)
    return results


def baseline(repo: Path, out: Path, which: str, jobs: int) -> list[dict]:
    import fw_gtest
    from ctrl_build import Tree, STACK
    work = out / ('work-baseline-' + which)
    src = copy_tree(repo, work)
    tree = Tree(src, work / 'build', work / 'reuse', fw_gtest.Build(jobs=jobs), STACK)
    results = []
    if which == 'aecp':
        import aecp_arms
        config = repo / 'configs/endstation_ax7101_1x1_tdm8.yaml'
        runs = [(f'app-if{i}', lambda i=i: aecp_arms.core_arm(tree, config, i, 'app', '*')) for i in (1, 2)]
    else:
        import plat_arms
        runs = [('plat', lambda: plat_arms.arm_plat(tree)),
                ('platboot1', lambda: plat_arms.arm_platboot(tree, 1)),
                ('platboot2', lambda: plat_arms.arm_platboot(tree, 2))]
    for label, fn in runs:
        outcome = fn()
        (out / f'baseline-{label}.log').write_text(outcome.log)
        results.append({'arm': label, 'rc': outcome.rc})
        print(f'[baseline] {label} rc={outcome.rc}', flush=True)
    return results


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--repo', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--jobs', type=int, default=2)
    ap.add_argument('mode', choices=('baseline-aecp', 'baseline-plat', 'aecp', 'plat', 'list'))
    ap.add_argument('names', nargs='*')
    args = ap.parse_args()
    repo = args.repo.resolve()
    setup(repo)
    args.out.mkdir(parents=True, exist_ok=True)
    if args.mode == 'list':
        print('\n'.join(r[0] for r in REVIEWER_AECP + REVIEWER_PLAT))
        return 0
    if args.mode.startswith('baseline'):
        res = baseline(repo, args.out, args.mode.split('-')[1], args.jobs)
        bad = any(r['rc'] != 0 for r in res)
    elif args.mode == 'aecp':
        res = run_aecp(repo, args.out, args.names, args.jobs)
        bad = any(not r['caught'] for r in res)
    else:
        res = run_plat(repo, args.out, args.names, args.jobs)
        bad = any(not r['caught'] for r in res)
    (args.out / 'results.json').write_text(json.dumps(res, indent=2, default=list) + '\n')
    return int(bad)


if __name__ == '__main__':
    raise SystemExit(main())
