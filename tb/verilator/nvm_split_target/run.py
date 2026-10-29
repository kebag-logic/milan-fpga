#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Run the saved-state store's cases on the split CPU at one point, and grade them (#665).

Each case's image is built by the service-budget harness (build.build), with
the flash port on the split SoC's own map, and booted on its test SoC with the
case's journal in the flash (target_cases.py). The `commit` case runs first: the
others boot the journal it wrote, or one the reference codec derives from it.
target_grade.py grades each log. README.md has the cases, the rules and the
figures.

Usage:
    python3 -B tb/verilator/nvm_split_target/run.py --point 8x8 --build-dir DIR [--cases a,b] [--jobs N]
    python3 -B tb/verilator/nvm_split_target/run.py --self-test

Exit 0 = every case passed and every planted control was caught (a step over
T_svc fails the run unless --record-budget-findings); 1 = a case failed or a
control escaped; 2 = a build or an input failed.
"""
from __future__ import annotations

import argparse
import json
import os
import shlex
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import target_cases as cases  # noqa: E402
import target_grade as tg  # noqa: E402

build, scenario = cases.build, cases.scenario
POINTS = {'1x1': ('endstation_ax7101_1x1_tdm8', 1), '8x8': ('endstation_ax7101_8x8', 2)}


def bound_control(obs: object, measured: dict, length: int, cpu_hz: int) -> dict:
    """The capture's bound, planted in the measured commit: its capture lengthened to exactly the bound must
    fit, and lengthened one page of its own measured cost (its cycles a byte, times a page) past the bound
    must be caught."""
    bound = tg.recipe.HOLD_FLOOR_MS * cpu_hz // 2000
    page = -(-measured['cycles'] * cases.PAGE // length)
    at = tg.capture(tg.lengthened(obs, bound - measured['cycles']), measured['latches'], cpu_hz)
    past = tg.capture(tg.lengthened(obs, bound - measured['cycles'] + page), measured['latches'], cpu_hz)
    caught = at['within_bound'] and not past['within_bound']
    words = [f"at the bound {at['ms']:.4f} ms fits; one page ({page:,} cycles) past it, {past['ms']:.4f} ms, "
             f"is over"] if caught else []
    return dict(case='capture-one-page-past', caught=caught, words=words, passed=caught, findings=[],
                page_cycles=page)


def built(root: Path, key: str, point: str, reuse: bool) -> dict:
    """One arm's build at the point: reused when asked and every recorded input still attests, else built."""
    shape, n_if = POINTS[point]
    arm, _, plant = key.partition('+')
    variant, mutation = cases.ARMS[arm], cases.PLANTS[plant] if plant else 'none'
    directory = root / key
    if reuse and (directory / 'build.json').is_file():
        spec = build.reused(directory)
        if (spec['variant'], spec['mutation']) != (build.label(variant), build.label(mutation)):
            raise RuntimeError(f'reused build {key} is of {spec["variant"]} and {spec["mutation"]}')
    else:
        spec = build.build(directory, shape, n_if, mutation, variant, build.Core())
    return dict(spec, build_dir=str(directory))


#: Set by --regrade: boot() reads each case's recorded log and journal instead of running it.
REGRADE = {'on': False}


def boot(spec: dict, out: Path, case: cases.Case, script: str, journal: bytes) -> tuple[str, bytes]:
    """One boot of the case's model on its script, the flash holding journal at the journal: the log and the
    journal it left. A regrade refuses a case whose recorded script, journal or log is not this run's."""
    left = out / f'{case.name}.journal.out'
    if REGRADE['on']:
        recorded = [out / f'{case.name}.{suffix}' for suffix in ('txt', 'journal.in', 'log')]
        if not all(p.is_file() for p in recorded) or recorded[0].read_text() != script or \
                recorded[1].read_bytes() != journal:
            raise RuntimeError(f'regrade: {case.name} has no recorded run of this script and journal')
        return recorded[2].read_text(), left.read_bytes() if left.is_file() else b''
    (out / f'{case.name}.txt').write_text(script)
    (out / f'{case.name}.journal.in').write_bytes(journal)
    left.unlink(missing_ok=True)
    env = dict(os.environ, BUDGET_JOURNAL_IN=str(out / f'{case.name}.journal.in'), BUDGET_JOURNAL_OUT=str(left))
    argv = [str(Path(spec['build_dir']) / 'native/Vsim'), str(out / f'{case.name}.txt'), '-']
    print('COMMAND', shlex.join(argv), flush=True)
    with (out / f'{case.name}.log').open('w') as sink:
        subprocess.run(argv, cwd=Path(spec['build_dir']) / 'gateware', stdout=sink,
                       stderr=subprocess.STDOUT, env=env, check=False)
    return (out / f'{case.name}.log').read_text(), left.read_bytes() if left.is_file() else b''


def run_cases(selected: list[cases.Case], specs: dict[str, dict], point: str, out: Path, jobs: int) -> list[dict]:
    """The commit case, then the others on the journals it leaves, graded."""
    shape = POINTS[point][0]
    bench, records, length = cases.shape_bench(shape, out / 'shape')
    pages = -(-length // cases.PAGE)
    any_spec = next(iter(specs.values()))
    target = scenario.point(point, any_spec)
    slot = json.loads((Path(any_spec['flash_map']) / 'flash_port.json').read_text())['journal']['size'] // 2
    commit = next(c for c in cases.CASES if c.commit)
    log, saved = boot(specs[cases.build_key(commit)], out, commit, cases.script(commit, target, records, pages),
                      b'\xff' * 2 * slot)
    obs = tg.observe(log, any_spec['sys_hz'], any_spec['cpu_hz'])
    plens = cases.payload_lengths(bench)
    base = tg.Context(any_spec['cpu_hz'], records, pages, b'\xff' * 2 * slot, saved, {}, [], plens)
    results = [tg.grade_case(commit, obs, base, bench)]
    if 'capture' in results[0] and results[0]['capture']['latches']:
        results.append(bound_control(obs, results[0]['capture'], length, any_spec['cpu_hz']))
    journals = cases.journals(saved, bench, slot)
    applied = bench.decode(saved[:int.from_bytes(saved[16:20], 'little')])[1]
    applies = tg.expected_applies(applied, bench.expect, bench.donor.base)

    def one(case: cases.Case) -> dict:
        """Boot and grade one case on its journal."""
        log, left = boot(specs[cases.build_key(case)], out, case, cases.script(case, target, records, pages),
                         journals[case.journal])
        ctx = tg.Context(any_spec['cpu_hz'], records, pages, journals[case.journal], left, applied, applies)
        return tg.grade_case(case, tg.observe(log, any_spec['sys_hz'], any_spec['cpu_hz']), ctx, bench)

    with ThreadPoolExecutor(max_workers=jobs) as pool:
        results += list(pool.map(one, [c for c in selected if not c.commit]))
    return results


def table(results: list[dict], point: str) -> str:
    """The run's results as Markdown: each case's verdict, then the commit's capture and phases."""
    lines = [f'# Saved-state cases on the split CPU, {point}', '', '| Case | Verdict | Detail |', '|---|---|---|']
    for r in results:
        verdict = ('caught' if r['caught'] else 'ESCAPED') if 'caught' in r else 'pass' if r['passed'] else 'FAIL'
        detail = '; '.join(r.get('words') or r['findings']) or (
            f"{r['applies']} apply entries, boot {r['boot_cycles']:,} CPU cycles" if 'applies' in r else '')
        lines.append(f"| {r['case']} | {verdict} | {detail} |")
    for r in results:
        if 'capture' in r:
            c = r['capture']
            lines += ['', f"Capture: {c['latches']} records in {c['steps']} steps, {c['cycles']:,} CPU cycles, "
                      f"{c['ms']:.3f} ms against {c['bound_ms']} ms; longest step {c['longest_cycles']:,} cycles.", '',
                      '| Phase | Steps | Longest step, CPU cycles | Longest, ms | Total, CPU cycles |',
                      '|---|---:|---:|---:|---:|']
            lines += [f"| {p} | {row['steps']} | {row['longest_cycles']:,} | {row['longest_ms']:.3f} | {row['cycles']:,} |"
                      for p, row in sorted(r['phases'].items())]
    return '\n'.join(lines) + '\n'


def exit_status(results: list[dict], record: bool) -> int:
    """0 when every case passed and every control was caught; a T_svc miss fails unless recorded."""
    failed = [r['case'] for r in results if not r['passed']]
    misses = [f"{r['case']}: {p}" for r in results for p in r.get('t_svc_misses', [])]
    for r in results:
        if 'caught' in r:
            print(f"CONTROL {r['case']} {'caught' if r['caught'] else 'ESCAPED'}: {'; '.join(r['words'])}")
        else:
            print(f"CASE {r['case']} {'pass' if r['passed'] else 'FAIL'}: {'; '.join(r['findings'])}")
    for m in misses:
        print(f'T_SVC {m} has a step over T_svc')
    return 1 if failed or (misses and not record) else 0


def main(argv: list[str] | None = None) -> int:
    """Build the selected cases' arms at the point, run them and grade them, or run the self-test."""
    ap = argparse.ArgumentParser(description=__doc__.split('\n', 1)[0])
    ap.add_argument('--point', choices=sorted(POINTS))
    ap.add_argument('--build-dir', type=Path)
    ap.add_argument('--cases', help='comma-separated case names; default every case (the commit always runs)')
    ap.add_argument('--out', type=Path, help='results directory; default <build-dir>/results')
    ap.add_argument('--jobs', type=int, default=4)
    ap.add_argument('--reuse-build', action='store_true')
    ap.add_argument('--regrade', action='store_true', help='grade the runs recorded in --out on a reused build')
    ap.add_argument('--record-budget-findings', action='store_true')
    ap.add_argument('--self-test', action='store_true')
    args = ap.parse_args(argv)
    if args.self_test:
        import target_selftest
        return target_selftest.main()
    if not args.point or not args.build_dir:
        ap.error('--point and --build-dir are required')
    names = args.cases.split(',') if args.cases else [c.name for c in cases.CASES]
    unknown = set(names) - {c.name for c in cases.CASES}
    if unknown:
        ap.error(f'unknown cases {sorted(unknown)}')
    selected = [c for c in cases.CASES if c.name in names or c.commit]
    REGRADE['on'] = args.regrade
    args.reuse_build |= args.regrade
    root = args.build_dir.resolve()
    out = (args.out or root / 'results').resolve()
    out.mkdir(parents=True, exist_ok=True)
    try:
        specs = {key: built(root, key, args.point, args.reuse_build)
                 for key in dict.fromkeys(cases.build_key(c) for c in selected)}
        results = run_cases(selected, specs, args.point, out, args.jobs)
    except (RuntimeError, OSError, ValueError) as error:
        print(f'REFUSED: {error}')
        return 2
    (out / 'results.json').write_text(json.dumps(results, indent=1, default=str) + '\n')
    (out / 'table.md').write_text(table(results, args.point))
    print(table(results, args.point))
    return exit_status(results, args.record_budget_findings)


if __name__ == '__main__':
    os.environ.setdefault('PYTHONHASHSEED', '0')
    sys.exit(main())
