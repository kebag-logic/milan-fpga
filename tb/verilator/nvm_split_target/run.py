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

Exit 0 = every case passed (no service step over T_svc among them) and every
planted control was caught; 1 = a case failed or a control escaped; 2 = a
build or an input failed. The capture's CPU and elapsed times are recorded and
graded against no bound of their own (#665 owner decision 2026-10-29, option
(c)).

Every figure is converted and graded at the CPU and bus clocks the builds
recorded (their build.json, from the shape's constraints). results.json keeps
those clocks beside the results, and table.md names them beside every table; a
record with a clock missing, a figure not converted at its CPU clock, or clocks
that are not its builds' is refused (#665, the timing figures name their
clocks).
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


def clocks(specs: dict[str, dict]) -> dict[str, int]:
    """The CPU and bus clocks every arm's build recorded. One conversion and one T_svc in cycles serve every
    case, so builds that record different clocks, or no whole positive number of hertz, are refused."""
    seen = {key: (spec.get('cpu_hz'), spec.get('sys_hz')) for key, spec in specs.items()}
    if len(set(seen.values())) != 1:
        raise RuntimeError(f'the builds record different clocks (CPU Hz, bus Hz): {seen}')
    cpu_hz, sys_hz = next(iter(seen.values()))
    if not all(type(hz) is int and hz > 0 for hz in (cpu_hz, sys_hz)):
        raise RuntimeError(f'the builds record no usable clocks (CPU Hz, bus Hz): {seen}')
    return dict(cpu_hz=cpu_hz, sys_hz=sys_hz)


def run_cases(selected: list[cases.Case], specs: dict[str, dict], point: str, out: Path, jobs: int,
              clk: dict[str, int]) -> list[dict]:
    """The commit case, then the others on the journals it leaves, graded at the builds' clocks clk."""
    shape = POINTS[point][0]
    cpu_hz, sys_hz = clk['cpu_hz'], clk['sys_hz']
    bench, records, length = cases.shape_bench(shape, out / 'shape')
    pages = -(-length // cases.PAGE)
    any_spec = next(iter(specs.values()))
    target = scenario.point(point, any_spec)
    slot = json.loads((Path(any_spec['flash_map']) / 'flash_port.json').read_text())['journal']['size'] // 2
    commit = next(c for c in cases.CASES if c.commit)
    log, saved = boot(specs[cases.build_key(commit)], out, commit, cases.script(commit, target, records, pages),
                      b'\xff' * 2 * slot)
    obs = tg.observe(log, sys_hz, cpu_hz)
    plens = cases.payload_lengths(bench)
    base = tg.Context(cpu_hz, records, pages, b'\xff' * 2 * slot, saved, {}, [], plens)
    results = [tg.grade_case(commit, obs, base, bench)]
    if tg.service(obs):
        results.append(tg.step_control(obs, cpu_hz))
    journals = cases.journals(saved, bench, slot)
    applied = bench.decode(saved[:int.from_bytes(saved[16:20], 'little')])[1]
    applies = tg.expected_applies(applied, bench.expect, bench.donor.base)

    def one(case: cases.Case) -> dict:
        """Boot and grade one case on its journal."""
        log, left = boot(specs[cases.build_key(case)], out, case, cases.script(case, target, records, pages),
                         journals[case.journal])
        ctx = tg.Context(cpu_hz, records, pages, journals[case.journal], left, applied, applies)
        return tg.grade_case(case, tg.observe(log, sys_hz, cpu_hz), ctx, bench)

    with ThreadPoolExecutor(max_workers=jobs) as pool:
        results += list(pool.map(one, [c for c in selected if not c.commit]))
    return results


def record(results: list[dict], point: str, clk: dict[str, int]) -> dict:
    """results.json: the point and its shape, the clocks every figure was converted and graded at, T_svc, and
    the results."""
    return dict(point=point, shape=POINTS[point][0], cpu_hz=clk['cpu_hz'], sys_hz=clk['sys_hz'],
                t_svc_ms=scenario.T_SVC_MS, results=results)


def missing_clocks(rec: dict) -> list[str]:
    """A finding for each clock the record does not carry as a whole positive number of hertz."""
    return [f'no {key} recorded' for key in ('cpu_hz', 'sys_hz')
            if type(rec.get(key)) is not int or rec[key] <= 0]


def figures(result: dict) -> list[tuple[str, int, float]]:
    """A result's times in ms, each with the CPU cycles it was converted from."""
    rows = [('longest step', result['longest_step_cycles'], result['longest_step_ms'])] \
        if 'longest_step_cycles' in result else []
    if 'capture' in result:
        c = result['capture']
        rows += [('capture CPU time', c['cycles'], c['ms']), ('capture elapsed', c['elapsed_cycles'], c['elapsed_ms']),
                 ('capture longest step', c['longest_cycles'], c['longest_ms'])]
    rows += [(f'{phase} longest step', row['longest_cycles'], row['longest_ms'])
             for phase, row in sorted(result.get('phases', {}).items())]
    return rows


def misconverted(rec: dict) -> list[str]:
    """A finding for each figure not converted or graded at the record's CPU clock: a time in ms, a phase's
    verdict against T_svc, the step control's T_svc in cycles."""
    cpu_hz, found = rec['cpu_hz'], []
    for r in rec['results']:
        found += [f"{r['case']}: {label} {value} ms is not {cycles:,} CPU cycles at {cpu_hz:,} Hz"
                  for label, cycles, value in figures(r) if value != tg.ms(cycles, cpu_hz)]
        found += [f"{r['case']}: {phase}'s T_svc verdict is not its longest step's at {cpu_hz:,} Hz"
                  for phase, row in sorted(r.get('phases', {}).items())
                  if row['within_t_svc'] != tg.within_t_svc(row['longest_cycles'], cpu_hz)]
        if 'limit_cycles' in r and r['limit_cycles'] != int(scenario.T_SVC_MS * cpu_hz // 1000):
            found.append(f"{r['case']}: T_svc of {r['limit_cycles']:,} cycles is not T_svc at {cpu_hz:,} Hz")
    return found


def provenance(rec: dict) -> list[str]:
    """What is wrong with the record's clocks: one missing, or a figure not converted at its CPU clock."""
    return missing_clocks(rec) or misconverted(rec)


def against_build(rec: dict, specs: dict[str, dict]) -> list[str]:
    """A finding for each arm whose build.json records other clocks than the record's."""
    return [f"{key}: the build records CPU {spec.get('cpu_hz')} Hz and bus {spec.get('sys_hz')} Hz, the results "
            f"{rec.get('cpu_hz')} Hz and {rec.get('sys_hz')} Hz" for key, spec in specs.items()
            if (spec.get('cpu_hz'), spec.get('sys_hz')) != (rec.get('cpu_hz'), rec.get('sys_hz'))]


def mhz(hz: int) -> str:
    """A clock in MHz, to six significant digits; the clock line gives its exact hertz beside it."""
    return f'{hz / 1e6:g} MHz'


def clock_line(rec: dict) -> str:
    """The clocks a table's figures were measured, converted and graded at, as the run's builds recorded them."""
    return (f"Clocks, as this run's builds recorded them: CPU {mhz(rec['cpu_hz'])} ({rec['cpu_hz']:,} Hz), "
            f"bus {mhz(rec['sys_hz'])} ({rec['sys_hz']:,} Hz).")


def table(rec: dict) -> str:
    """The run's record as Markdown: each case's verdict, then the steps against T_svc, then the commit's
    capture and phases, each table beside the clocks it was measured at. A record without its clocks, or
    whose figures are not at them, is refused."""
    wrong = provenance(rec)
    if wrong:
        raise ValueError('the results carry no sound clock provenance: ' + '; '.join(wrong))
    results, clock = rec['results'], clock_line(rec)
    lines = [f"# Saved-state cases on the split CPU, {rec['point']}", '', clock, '', '| Case | Verdict | Detail |',
             '|---|---|---|']
    for r in results:
        verdict = ('caught' if r['caught'] else 'ESCAPED') if 'caught' in r else 'pass' if r['passed'] else 'FAIL'
        detail = '; '.join(r.get('words') or r['findings']) or (
            f"{r['applies']} apply entries, boot {r['boot_cycles']:,} CPU cycles" if 'applies' in r else '')
        lines.append(f"| {r['case']} | {verdict} | {detail} |")
    lines += ['', f'Every service step is graded against T_svc = {scenario.T_SVC_MS} ms of CPU time.', '', clock, '',
              '| Case | Service steps | Longest step, CPU cycles | Longest, ms |', '|---|---:|---:|---:|']
    lines += [f"| {r['case']} | {r['service_steps']} | {r['longest_step_cycles']:,} | {r['longest_step_ms']:.3f} |"
              for r in results if 'service_steps' in r]
    for r in results:
        if 'capture' in r:
            c = r['capture']
            lines += ['', f"Capture, measured (no bound of its own): {c['latches']} records in {c['steps']} steps; "
                      f"CPU time {c['cycles']:,} cycles, {c['ms']:.3f} ms; elapsed {c['elapsed_cycles']:,} cycles, "
                      f"{c['elapsed_ms']:.3f} ms; longest step {c['longest_cycles']:,} cycles, "
                      f"{c['longest_ms']:.3f} ms.", '', clock, '',
                      '| Phase | Steps | Longest step, CPU cycles | Longest, ms | Within T_svc | Total, CPU cycles |',
                      '|---|---:|---:|---:|---|---:|']
            lines += [f"| {p} | {row['steps']} | {row['longest_cycles']:,} | {row['longest_ms']:.3f} | "
                      f"{'yes' if row['within_t_svc'] else '**no**'} | {row['cycles']:,} |"
                      for p, row in sorted(r['phases'].items())]
    return '\n'.join(lines) + '\n'


def exit_status(results: list[dict]) -> int:
    """0 when every case passed, no step over T_svc among them, and every control was caught."""
    for r in results:
        if 'caught' in r:
            print(f"CONTROL {r['case']} {'caught' if r['caught'] else 'ESCAPED'}: {'; '.join(r['words'])}")
        else:
            print(f"CASE {r['case']} {'pass' if r['passed'] else 'FAIL'}: {'; '.join(r['findings'])}")
    return 1 if any(not r['passed'] for r in results) else 0


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
        clk = clocks(specs)
        rec = record(run_cases(selected, specs, args.point, out, args.jobs, clk), args.point, clk)
        (out / 'results.json').write_text(json.dumps(rec, indent=1, default=str) + '\n')
        wrong = against_build(rec, specs)
        if wrong:
            raise RuntimeError('; '.join(wrong))
        text = table(rec)
    except (RuntimeError, OSError, ValueError) as error:
        print(f'REFUSED: {error}')
        return 2
    (out / 'table.md').write_text(text)
    print(text)
    return exit_status(rec['results'])


if __name__ == '__main__':
    os.environ.setdefault('PYTHONHASHSEED', '0')
    sys.exit(main())
