# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The saved-state cases' portable self-test (#665): Python and PyYAML only, no LiteX or simulator.

It runs the graders on synthetic logs and the case builders on the shipping
1x1 shape, then replaces each grading rule in turn with a weaker one (MUTANTS)
and requires a named check to fail. Run it through run.py --self-test.

It holds the run's clock provenance: results.json carries the builds'
recorded clocks, the report names them beside every table, a synthetic run at
other clocks renders those clocks and its figures at them, and a record with
a clock missing, misconverted or not its builds' is refused (#665).

It also holds D5 on the current flash writer unchanged (#665 owner decision
2026-10-29, option (c)): that writer's own grader, nvm_capture_cpu/run.py,
must still refuse a capture over 24.5 ms, and the check is planted away from
its source to prove the self-test notices.
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import struct
import sys
import tempfile
import types
from collections.abc import Iterator
from pathlib import Path
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import target_cases as cases  # noqa: E402
import target_grade as tg  # noqa: E402

CPU_HZ, SYS_HZ = 50_000_000, 100_000_000
#: A differently clocked synthetic input: the report and the record must follow it, not the product's clocks.
OTHER_CPU_HZ, OTHER_SYS_HZ = 62_500_000, 125_000_000
Check = tuple[str, bool, str]


def _run_module() -> types.ModuleType:
    """run.py under a module name of its own, so the mutants can replace its functions."""
    spec = importlib.util.spec_from_file_location('nvm_split_target_run', HERE / 'run.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


RUN = _run_module()


def span(cpu: int, cycles: int, name: str = 'nvm_store_service') -> str:
    """A SPAN line as sim_main.cpp prints it."""
    return f'SPAN {2 * cpu} {cpu} {cycles} 00000fd4 {name}'


def call(cpu: int, name: str) -> str:
    """A CALL line as sim_main.cpp prints it."""
    return f'CALL {2 * cpu} {cpu} {name}'


#: The first latch step's start in commit_log, and the gap between one step's end and the next's start.
FIRST, GAP = 1000, 10_000
#: T_svc in CPU cycles at the self-test's CPU clock.
LIMIT = int(tg.scenario.T_SVC_MS * CPU_HZ // 1000)


def commit_log(records: int, step: int, closing: int, other: int = 300) -> str:
    """A commit's service steps: an idle step, a latch step per record of `step` cycles, the step that ends the
    capture of `closing` cycles, then two seal steps, the erase and its poll, a program and its read-back,
    each of `other` cycles."""
    lines, cpu = [span(100, 50)], FIRST
    for _ in range(records):
        lines += [span(cpu, step), call(cpu + 1, 'acmp_nvm:latch'), call(cpu + 2, 'aecp_value_latch')]
        cpu += step + GAP
    lines.append(span(cpu, closing))
    cpu += closing + GAP
    for phase in ('nvm_crc32_update', 'nvm_crc32_update', 'nvm_flash_litespi:ls_erase', 'nvm_flash_litespi:ls_busy',
                  'nvm_flash_litespi:ls_program', 'nvm_flash_litespi:ls_read'):
        lines += [span(cpu, other), call(cpu + 1, phase)]
        cpu += other + GAP
    return '\n'.join([*lines, 'RESULT: PASS']) + '\n'


def capture_checks() -> list[Check]:
    """The capture measured with no bound of its own: its CPU time, its elapsed time and its steps; a capture
    far past the current writer's 24.5 ms, every step within T_svc, is no finding; a capture missing a
    record is refused."""
    records, step, closing = 4, 40_000, 1000
    got = tg.capture(tg.observe(commit_log(records, step, closing), SYS_HZ, CPU_HZ), records, CPU_HZ)
    elapsed = records * (step + GAP) + closing
    out = [("the capture's CPU time is its steps' cycles, its elapsed time its first step's start to its last "
            "step's end", (got['cycles'], got['elapsed_cycles'], got['steps'], got['findings']) ==
            (records * step + closing, elapsed, records + 1, []), str(got))]
    long = int(0.9 * LIMIT)
    slow = tg.observe(commit_log(6, long, long), SYS_HZ, CPU_HZ)
    measured = tg.capture(slow, 6, CPU_HZ)
    out.append(('a capture of twice 24.5 ms of CPU time, every step within T_svc, is no finding',
                measured['ms'] > 49 and not measured['findings'] and not tg.over_t_svc(slow, CPU_HZ), str(measured)))
    short = tg.capture(tg.observe(commit_log(records - 1, step, closing), SYS_HZ, CPU_HZ), records, CPU_HZ)
    out.append(('a capture that latched one record fewer than the shape is refused',
                any('latched 3 records' in f for f in short['findings']), str(short['findings'])))
    phases = tg.phases(tg.observe(commit_log(records, step, closing), SYS_HZ, CPU_HZ), CPU_HZ)
    out.append(('every service step is classified by its calls, the closing step as the capture\'s',
                {p: r['steps'] for p, r in phases.items()} == dict(idle=1, capture=records + 1, seal=2, erase=1,
                                                                  poll=1, program=1, read=1), str(phases)))
    return out


def t_svc_checks() -> list[Check]:
    """Every service step held to T_svc, in every phase: at T_svc a step passes, one CPU cycle over it is a
    finding naming the step and its phase, the finding fails its case, and the measured commit's step
    control is caught in every phase."""
    at = tg.observe(commit_log(2, LIMIT, LIMIT, other=LIMIT), SYS_HZ, CPU_HZ)
    over = tg.observe(commit_log(2, LIMIT + 1, LIMIT + 1, other=LIMIT + 1), SYS_HZ, CPU_HZ)
    named = [f.split(' takes ')[0] for f in tg.over_t_svc(over, CPU_HZ)]
    want = ['step 1 (capture)', 'step 2 (capture)', 'step 3 (capture)', 'step 4 (seal)', 'step 5 (seal)',
            'step 6 (erase)', 'step 7 (poll)', 'step 8 (program)', 'step 9 (read)']
    out = [('a step of exactly T_svc passes, in the capture, seal, erase, poll, program and read phases',
            not tg.over_t_svc(at, CPU_HZ), str(tg.over_t_svc(at, CPU_HZ))),
           ('a step one CPU cycle over T_svc is a finding naming it and its phase, in the capture, seal, erase, '
            'poll, program and read phases', named == want, str(named))]
    obs = tg.observe(commit_log(4, 40_000, 1000), SYS_HZ, CPU_HZ)
    phases = [s.phase for s in tg.service(obs)]
    stretched = {i: [f.split(' takes ')[0] for f in tg.over_t_svc(tg.stretched(obs, i, LIMIT + 1), CPU_HZ)]
                 for i in range(len(phases))}
    out.append(('any one step stretched one cycle over T_svc, the idle step among them, is that step alone, its '
                'phase kept', all(v == [f'step {i} ({phases[i]})'] for i, v in stretched.items()) and
                'idle' in phases, str(stretched)))
    control = tg.step_control(obs, CPU_HZ)
    out.append(("the step control: each phase's longest step at T_svc passes and one cycle past it is caught",
                control['caught'] and control['limit_cycles'] == LIMIT and not control['escaped'] and
                control['words'][0].endswith('capture, erase, idle, poll, program, read, seal'), str(control)))
    absent = cases.Case('absent', 'fixture', 'none', 'blank')
    ctx = tg.Context(CPU_HZ, 1, 1, b'', b'', {}, [])
    graded = {cycles: tg.grade_case(absent, tg.observe(service_log(cycles), SYS_HZ, CPU_HZ), ctx, None)
              for cycles in (LIMIT, LIMIT + 1)}
    verdicts = {cycles: [f for f in r['findings'] if 'over T_svc' in f] for cycles, r in graded.items()}
    out.append(('a service step over T_svc fails its case, one at T_svc does not',
                not verdicts[LIMIT] and len(verdicts[LIMIT + 1]) == 1, str(verdicts)))
    return out


def graded_commit(cpu_hz: int, sys_hz: int) -> list[dict]:
    """A synthetic commit's results and its step control, graded at the clocks given."""
    obs = tg.observe(commit_log(4, 40_000, 1000), sys_hz, cpu_hz)
    capture = dict(tg.capture(obs, 4, cpu_hz), decomposed={})
    capture.pop('findings')
    result = dict(case='commit', findings=[], passed=True, service_steps=11, longest_step_cycles=40_000,
                  longest_step_ms=tg.ms(40_000, cpu_hz), capture=capture, phases=tg.phases(obs, cpu_hz))
    return [result, tg.step_control(obs, cpu_hz)]


def graded_record(cpu_hz: int, sys_hz: int) -> dict:
    """graded_commit's record at 1x1, as run.py writes it to results.json."""
    return RUN.record(graded_commit(cpu_hz, sys_hz), '1x1', dict(cpu_hz=cpu_hz, sys_hz=sys_hz))


def report_checks() -> list[Check]:
    """The run's report presents T_svc as F1's only timing bound and 24.5 ms as no bound of F1's."""
    text = rendered(graded_record(CPU_HZ, SYS_HZ))
    return [('the report grades every step against T_svc and gives the capture no bound',
             f'T_svc = {tg.scenario.T_SVC_MS} ms' in text and 'no bound of its own' in text and '24.5' not in text
             and 'elapsed' in text, text[:400])]


def rendered(rec: dict) -> str:
    """run.table's report of the record, or the words it refuses it with (a mutant may fail it otherwise)."""
    try:
        return RUN.table(rec)
    except (ValueError, KeyError, TypeError) as error:
        return f'REFUSED {type(error).__name__}: {error}'


def refusal(rec: dict) -> str:
    """The words run.table refuses the record with, or '' when it renders it."""
    text = rendered(rec)
    return text if text.startswith('REFUSED ') else ''


def unclocked_tables(text: str, words: str) -> list[str]:
    """Each table header of the report not preceded, one blank line above, by a clock line holding words."""
    lines = text.splitlines()
    return [lines[i] for i in range(len(lines) - 1) if lines[i].startswith('| ') and lines[i + 1].startswith('|---')
            and not (i >= 2 and lines[i - 1] == '' and lines[i - 2].startswith('Clocks, ') and words in lines[i - 2])]


def main_run(cpu_hz: int, sys_hz: int, graded_at: int = 0, planted: dict | None = None) -> tuple[int, dict, str]:
    """run.py's main on builds recording cpu_hz and sys_hz, its cases graded at the clocks main passes them:
    its exit status, results.json and table.md. graded_at plants a CPU clock for the grading, and planted the
    run's clocks, other than the builds'."""
    def built(root: Path, key: str, point: str, reuse: bool) -> dict:
        """A build that records only its clocks."""
        return dict(cpu_hz=cpu_hz, sys_hz=sys_hz, build_dir=str(root / key))

    def run_cases(selected: list, specs: dict, point: str, out: Path, jobs: int, clk: dict) -> list[dict]:
        """The synthetic commit, graded at the clocks main passes, or at graded_at."""
        return graded_commit(graded_at or clk['cpu_hz'], clk['sys_hz'])
    with tempfile.TemporaryDirectory() as tmp, replaced(RUN, 'built', built), \
            replaced(RUN, 'run_cases', run_cases), contextlib.redirect_stdout(io.StringIO()), \
            replaced(RUN, 'clocks', (lambda specs: planted) if planted else RUN.clocks):
        status = RUN.main(['--point', '1x1', '--build-dir', tmp, '--cases', 'valid'])
        out = Path(tmp) / 'results'
        saved = json.loads((out / 'results.json').read_text()) if (out / 'results.json').is_file() else {}
        text = (out / 'table.md').read_text() if (out / 'table.md').is_file() else ''
    return status, saved, text


def clock_checks() -> list[Check]:
    """The clocks every figure was converted and graded at travel with the results: the builds' recorded
    clocks in results.json and beside every table, a differently clocked input rendered at its own clocks, and
    a record with a clock missing, a figure misconverted or clocks not its builds' refused."""
    other = f'CPU 62.5 MHz ({OTHER_CPU_HZ:,} Hz), bus 125 MHz ({OTHER_SYS_HZ:,} Hz)'
    product = f'CPU 50 MHz ({CPU_HZ:,} Hz), bus 100 MHz ({SYS_HZ:,} Hz)'
    specs = {'a': dict(cpu_hz=OTHER_CPU_HZ, sys_hz=OTHER_SYS_HZ), 'b': dict(cpu_hz=OTHER_CPU_HZ, sys_hz=OTHER_SYS_HZ)}
    rec = RUN.record(graded_commit(OTHER_CPU_HZ, OTHER_SYS_HZ), '1x1', RUN.clocks(specs))
    back = json.loads(json.dumps(rec, default=str))
    out = [('the results record carries the clocks its builds recorded, through JSON',
            (back.get('cpu_hz'), back.get('sys_hz')) == (OTHER_CPU_HZ, OTHER_SYS_HZ) and not refusal(back) and
            not RUN.against_build(back, specs), str({k: back.get(k) for k in ('cpu_hz', 'sys_hz')}))]
    text = rendered(rec)
    out.append(('a run at other clocks is reported at them: its clocks named, its figures converted at its CPU '
                'clock', other in text and '50 MHz' not in text and '| 0.640 |' in text and '| 0.800 |' not in text,
                text[:600]))
    out.append(('every table of the report has the clocks beside it', not unclocked_tables(text, other) and
                not unclocked_tables(rendered(graded_record(CPU_HZ, SYS_HZ)), product) and text.count('\n| ') >= 3,
                str(unclocked_tables(text, other))))
    for key in ('cpu_hz', 'sys_hz'):
        words = refusal({k: v for k, v in rec.items() if k != key})
        out.append((f'a record without its {key} is refused', f'no {key} recorded' in words, words))
    out.append(('a record whose clock is not a whole positive number of hertz is refused',
                'no cpu_hz recorded' in refusal(dict(rec, cpu_hz=62.5e6)) and
                'no sys_hz recorded' in refusal(dict(rec, sys_hz=0)), ''))
    relabelled = refusal(dict(graded_record(CPU_HZ, SYS_HZ), cpu_hz=OTHER_CPU_HZ))
    out.append(("a record whose CPU clock is not the one its figures were converted at is refused",
                'is not 40,000 CPU cycles at 62,500,000 Hz' in relabelled and "T_svc verdict" not in relabelled
                and 'T_svc of 500,000 cycles' in relabelled, relabelled))
    wrong = RUN.against_build(rec, {'a': dict(cpu_hz=CPU_HZ, sys_hz=SYS_HZ), 'b': specs['b']})
    out.append(("a record whose clocks are not its builds' is refused, naming the build", len(wrong) == 1 and
                wrong[0].startswith('a: the build records CPU 50000000 Hz'), str(wrong)))
    refused = []
    for label, bad in (('disagree', {'a': specs['a'], 'b': dict(cpu_hz=CPU_HZ, sys_hz=OTHER_SYS_HZ)}),
                       ('lack one', {'a': dict(sys_hz=SYS_HZ)}), ('are none', {})):
        try:
            RUN.clocks(bad)
        except RuntimeError as error:
            refused.append(label if 'clocks' in str(error) else f'{label}: {error}')
    out.append(('builds that disagree on their clocks, lack one or are none are refused',
                refused == ['disagree', 'lack one', 'are none'], str(refused)))
    status, saved, report = main_run(OTHER_CPU_HZ, OTHER_SYS_HZ)
    out.append(("run.py writes its builds' clocks to results.json and beside every table of table.md",
                status == 0 and (saved.get('cpu_hz'), saved.get('sys_hz')) == (OTHER_CPU_HZ, OTHER_SYS_HZ) and
                other in report and not unclocked_tables(report, other), f'{status} {str(saved)[:200]}'))
    status, saved, report = main_run(OTHER_CPU_HZ, OTHER_SYS_HZ, graded_at=CPU_HZ)
    out.append(('run.py refuses results graded at another CPU clock than their record names, writing no table',
                status == 2 and not report, f'{status} {report[:200]}'))
    status, saved, report = main_run(OTHER_CPU_HZ, OTHER_SYS_HZ, planted=dict(cpu_hz=CPU_HZ, sys_hz=SYS_HZ))
    out.append(("run.py refuses a run whose clocks are not its builds', writing no table",
                status == 2 and not report and saved.get('cpu_hz') == CPU_HZ, f'{status} {report[:200]}'))
    return out


def boot_log(applies: list[str], service: int = 50) -> str:
    """One boot span holding the owners' apply entries in order, then a service step of `service` cycles."""
    lines = [span(100, 90_000, 'nvm_store_boot')]
    lines += [call(200 + 10 * i, name) for i, name in enumerate(applies)]
    return '\n'.join([*lines, span(200_000, service), 'RESULT: PASS']) + '\n'


def service_log(cycles: int) -> str:
    """A boot with nothing to apply, then one service step of `cycles` cycles."""
    return boot_log([], cycles)


#: A container's records as the reference decode returns them, out of order on purpose.
RECORDS = {('NAME', 1): b'n', ('MAPS_IN', 0): b'm', ('BINDING', 1): b'b', ('FMT_IN', 0): b'f', ('CFG_IDX', 0): b'c',
           ('BINDING', 0): b'b', ('NAME', 0): b'n', ('MAPS_OUT', 2): b'o'}
ORDER = ['acmp_restore_binding', 'acmp_restore_binding', 'aecp_value_restore', 'aecp_value_restore',
         'aecp_map_restore', 'aecp_map_restore', 'aecp_restore_settle', 'aecp_value_restore', 'aecp_value_restore']


def order_checks() -> list[Check]:
    """The apply order the container needs, and every departure from it caught."""
    sys.path.insert(0, str(cases.ROOT / 'scripts'))
    from nvm_klj2 import id_blocks
    base = next(b for g, b, _ in id_blocks(0x20) if g == 'BINDING')
    want = tg.expected_applies(RECORDS, {}, base)
    out = [('the bindings first, then the D3 records in ascending id, settle before the first name', want == ORDER,
            str(want)),
           ('a container with no name settles last', tg.expected_applies({('FMT_IN', 0): b'f'}, {}, base) ==
            ['aecp_value_restore', 'aecp_restore_settle'], '')]
    plants = {'the settle after the names': [*ORDER[:6], *ORDER[7:], ORDER[6]],
              'a binding after the D3 walk': [*ORDER[1:], ORDER[0]],
              'a name before a map': [*ORDER[:5], ORDER[7], ORDER[6], ORDER[5], ORDER[8]],
              'one apply missing': ORDER[:-1], 'one apply too many': [*ORDER, 'aecp_value_restore']}
    seen, found = tg.apply_order(tg.observe(boot_log(ORDER), SYS_HZ, CPU_HZ), want)
    out.append(('the container\'s own order passes', seen == ORDER and not found, str(found)))
    for label, order in plants.items():
        found = tg.apply_order(tg.observe(boot_log(order), SYS_HZ, CPU_HZ), want)[1]
        out.append((f'{label} is caught', bool(found) and found[0].startswith('apply order'), str(found)))
    twice = boot_log(ORDER) + boot_log(ORDER)
    out.append(('two boots are refused', 'boots traced' in str(tg.apply_order(tg.observe(twice, SYS_HZ, CPU_HZ),
                                                                              want)[1]), ''))
    return out


def wire_line(ch: int, frame: bytes) -> str:
    """A WIRE line as sim_main.cpp prints it."""
    return f'WIRE 1000 0 {ch} {frame.hex()}'


def answer_checks() -> list[Check]:
    """The entity_name and sink 0's talker read off the AECP and ACMP responses, by sequence_id."""
    f, scenario = cases.f, cases.scenario
    response = bytearray(f.read_descriptor(f.Aem(1, 2, 3, 4, cases.SEQ['read_entity']), 0, 0).ljust(160, b'\0'))
    response[15] = (response[15] & 0xF0) | tg.AECP_RESPONSE
    response[90:154] = cases.SAVED_NAME
    state = bytearray(f.acmp(f.ACMP['GET_RX_STATE_RESPONSE'], 5, f.Acmp(talker=scenario.TALKER_A,
                                                                         sequence=cases.SEQ['rx_state'])))
    other = bytearray(state)
    struct.pack_into('>H', other, 62, cases.SEQ['rx_state'] + 1)
    struct.pack_into('>Q', other, 34, 7)
    text = '\n'.join([wire_line(scenario.CH['aecp'], bytes(response)), wire_line(scenario.CH['acmp'], bytes(other)),
                      wire_line(scenario.CH['acmp'], bytes(state)), 'RESULT: PASS']) + '\n'
    got = tg.answers(tg.observe(text, SYS_HZ, CPU_HZ))
    return [('the answers are read by sequence_id: the name and the talker',
             got == dict(entity_status=0, entity_name=cases.SAVED_NAME, rx_status=0, rx_talker=scenario.TALKER_A),
             str(got))]


def journal_checks() -> list[Check]:
    """The journals derived from a committed container, judged by the reference codec: saved accepted, the
    torn newer slot refused beside it, the wrong major version refused."""
    sys.path.insert(0, str(cases.ROOT / 'scripts'))
    from nvm_contract import VD_OK, VD_VER
    from nvm_klj2 import frame_record, rid_of_key
    with tempfile.TemporaryDirectory() as tmp:
        bench, records, length = cases.shape_bench('endstation_ax7101_1x1_tdm8', Path(tmp))
    pages = -(-length // cases.PAGE)
    rid = rid_of_key(('NAME', 0), bench.donor.base)
    container = bench.assemble({**bench.frames, rid: frame_record(rid, cases.SAVED_NAME, bench.donor.layout)}, 1)
    slot = 0x1_0000
    journals = cases.journals(container.ljust(2 * slot, b'\xff'), bench, slot)
    verdicts = {name: [bench.decode(j[s:s + slot][:struct.unpack_from('<I', j, s + 16)[0]])[0]
                       if j[s:s + 4] != b'\xff' * 4 else 'blank' for s in (0, slot)] for name, j in journals.items()}
    torn_b = verdicts['torn'][1]
    return [('the shape\'s records and pages', (records, pages) == (54, 14), str((records, pages))),
            ('saved: slot A accepted, slot B blank', verdicts['saved'] == [VD_OK, 'blank'], str(verdicts['saved'])),
            ('torn: slot A accepted, the newer slot B refused', verdicts['torn'][0] == VD_OK and torn_b not in
             (VD_OK, 'blank'), str(verdicts['torn'])),
            ('version: slot A refused for its version, slot B blank', verdicts['version'] == [VD_VER, 'blank'],
             str(verdicts['version'])),
            ('torn: the newer slot is the next sequence, its last page erased',
             struct.unpack_from('<I', journals['torn'], slot + 8)[0] == 2 and
             journals['torn'][slot + len(container) - 1] == 0xFF, '')]


def plant_checks() -> list[Check]:
    """Every arm and planted defect applies to the checkout's sources, each a scratch copy."""
    failed = []
    with tempfile.TemporaryDirectory() as tmp:
        for name, plant in cases.PLANTS.items():
            try:
                cases.build.mutated_source(Path(tmp) / name, plant)
            except RuntimeError as error:
                failed.append(str(error))
        for name, arm in cases.ARMS.items():
            if arm != 'none':
                try:
                    cases.build.variant_fixture(Path(tmp) / name, arm)
                except RuntimeError as error:
                    failed.append(str(error))
    return [('every arm and planted defect applies to the checkout\'s sources', not failed, '; '.join(failed))]


def control_checks() -> list[Check]:
    """A control passes only when its planted defect is caught by its words."""
    ctx = tg.Context(CPU_HZ, 1, 1, b'', b'', {}, ORDER)
    reorder = cases.Case('r', 'fixture', 'x', 'saved', control='apply order')
    escape = cases.Case('g', 'guard-probe', 'x', 'blank', control='flash write escaped the journal')
    slow = cases.Case('s', 'fixture', 'x', 'blank', control='over T_svc')
    graded = {name: tg.grade_case(case, tg.observe(text, SYS_HZ, CPU_HZ), ctx, None)['caught'] for name, case, text in (
        ('reordered', reorder, boot_log([*ORDER[1:], ORDER[0]])), ('in order', reorder, boot_log(ORDER)),
        ('escaped write', escape, 'FAIL: flash write escaped the journal\nRESULT: FAIL\n'),
        ('no write', escape, 'RESULT: PASS\n'), ('slow step', slow, service_log(LIMIT + 1)),
        ('step at T_svc', slow, service_log(LIMIT)))}
    return [('a control is caught by its words and escapes without them',
             graded == {'reordered': True, 'in order': False, 'escaped write': True, 'no write': False,
                        'slow step': True, 'step at T_svc': False}, str(graded))]


#: The current flash writer's capture grader (#559): check_nvm_capture.py regrades its receipt through it.
CAPTURE_CPU = cases.ROOT / 'tb/verilator/nvm_capture_cpu'
#: Its 24.5 ms check, as the removal plant deletes it from grade_rows.
SHIPPING_CHECK = ("        if (spec.get('mutation', 'none') == 'none'\n"
                  "                and row['sys_cycles'] * 2000 > HOLD_FLOOR_MS * spec['sys_hz']):\n"
                  "            raise RuntimeError('worst measured copy exceeds half the 49 ms hold floor')\n")


def shipping_source(text: str) -> str:
    """The current writer's grader source, as the checkout has it."""
    return text


def _shipping_check_removed(text: str) -> str:
    """The removal plant: the current writer's grader with its 24.5 ms check deleted."""
    return text.replace(SHIPPING_CHECK, '')


def shipping_grader(scratch: Path) -> types.ModuleType:
    """nvm_capture_cpu/run.py as shipping_source leaves it, written to the same place under scratch (its
    ROOT is three directories up) and imported from there under a module name of its own; the checkout's
    file is only read. Its recipe is the checkout's."""
    copy = scratch / CAPTURE_CPU.relative_to(cases.ROOT) / 'run.py'
    copy.parent.mkdir(parents=True)
    copy.write_text(shipping_source((CAPTURE_CPU / 'run.py').read_text()))
    if str(CAPTURE_CPU) not in sys.path:
        sys.path.append(str(CAPTURE_CPU))
    spec = importlib.util.spec_from_file_location('nvm_capture_cpu_run', copy)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def d5_checks() -> list[Check]:
    """D5 on the current flash writer, unchanged: its own grader holds its capture to half its 49 ms hold
    floor, 24.5 ms. A capture of exactly 24.5 ms passes and one system tick more is refused."""
    source = (CAPTURE_CPU / 'run.py').read_text()
    with tempfile.TemporaryDirectory() as tmp:
        grader = shipping_grader(Path(tmp))
    sys_hz = 100_000_000
    limit = grader.HOLD_FLOOR_MS * sys_hz // 2000
    row = dict(index=0, ok=1, sys_cycles=limit, raw=4, records=1, mismatches=0, open=0, requests=1, responses=1,
               reads=1)
    spec = dict(shape=grader.SHAPES[0], captures=1, sys_hz=sys_hz, cpu_hz=grader.CPU_HZ,
                configured_cpu_hz=grader.CPU_HZ, phase='aligned rising edges', traffic='on', raw_bytes=4, records=1)
    at = grader.grade_rows([row], spec)['maximum_ms']
    try:
        grader.grade_rows([dict(row, sys_cycles=limit + 1)], spec)
        refused = ''
    except RuntimeError as error:
        refused = str(error)
    return [("the removal plant applies to the current writer's grader: its 24.5 ms check is there once",
             source.count(SHIPPING_CHECK) == 1, str(source.count(SHIPPING_CHECK))),
            ("the current flash writer's capture is held to 24.5 ms: exactly 24.5 ms passes, one system tick more "
             "is refused", grader.HOLD_FLOOR_MS / 2 == 24.5 and at == 24.5 and 'half the 49 ms' in refused,
             f'{at} {refused!r}')]


def checks() -> list[Check]:
    """Every check."""
    return [*capture_checks(), *t_svc_checks(), *report_checks(), *clock_checks(), *order_checks(), *answer_checks(),
            *journal_checks(), *plant_checks(), *control_checks(), *d5_checks()]


@contextlib.contextmanager
def replaced(owner: object, name: str, value: object) -> Iterator[None]:
    """owner's `name` replaced for the block."""
    with patch.object(owner, name, value):
        yield


_OVER, _CAPTURE = tg.over_t_svc, tg.capture
SELF = sys.modules[__name__]


def _unstretched(obs: tg.Observed, index: int, cycles: int) -> tg.Observed:
    """stretched, but the step left as it was."""
    return obs


def _elapsed_is_cpu(obs: tg.Observed, records: int, cpu_hz: int) -> dict:
    """capture, its elapsed time reported as its CPU time."""
    got = _CAPTURE(obs, records, cpu_hz)
    return dict(got, elapsed_cycles=got['cycles'], elapsed_ms=got['ms'])


def _bound_reimposed(obs: tg.Observed, records: int, cpu_hz: int) -> dict:
    """capture, with the current writer's 24.5 ms bound imposed on F1 again."""
    got = _CAPTURE(obs, records, cpu_hz)
    return dict(got, findings=[*got['findings'], *(['over 24.5 ms'] if got['ms'] > 24.5 else [])])


_TABLE = RUN.table


def _fixed_clock_line(rec: dict) -> str:
    """clock_line, naming the product's clocks whatever the record holds."""
    return f"Clocks, as this run's builds recorded them: CPU 50 MHz ({CPU_HZ:,} Hz), bus 100 MHz ({SYS_HZ:,} Hz)."


def _unclocked_record(results: list[dict], point: str, clk: dict[str, int]) -> dict:
    """record, without its clocks."""
    return dict(point=point, shape=RUN.POINTS[point][0], t_svc_ms=tg.scenario.T_SVC_MS, results=results)


def _first_build_clocks(specs: dict[str, dict]) -> dict:
    """clocks, the first build's taken for every build and never refused."""
    first = next(iter(specs.values()), {})
    return dict(cpu_hz=first.get('cpu_hz'), sys_hz=first.get('sys_hz'))


def _last_table_unclocked(rec: dict) -> str:
    """table, the clock line beside its last table dropped."""
    text, line = _TABLE(rec), RUN.clock_line(rec) + '\n\n'
    at = text.rfind(line)
    return text[:at] + text[at + len(line):]


#: Each grading rule replaced by a weaker one, and the check that must then fail.
MUTANTS: tuple[tuple[str, object, str, object, str], ...] = (
    ('steps: strictly below T_svc', tg, 'within_t_svc',
     lambda cycles, cpu_hz: cycles * 1000 < tg.scenario.T_SVC_MS * cpu_hz,
     'a step of exactly T_svc passes, in the capture, seal, erase, poll, program and read phases'),
    ('steps: only the capture\'s steps graded', tg, 'over_t_svc',
     lambda obs, cpu_hz: [f for f in _OVER(obs, cpu_hz) if '(capture)' in f],
     'a step one CPU cycle over T_svc is a finding naming it and its phase, in the capture, seal, erase, poll, '
     'program and read phases'),
    ('steps: the idle step not graded', tg, 'over_t_svc',
     lambda obs, cpu_hz: [f for f in _OVER(obs, cpu_hz) if '(idle)' not in f],
     'any one step stretched one cycle over T_svc, the idle step among them, is that step alone, its phase kept'),
    ('steps: no step graded against T_svc', tg, 'over_t_svc', lambda obs, cpu_hz: [],
     'a service step over T_svc fails its case, one at T_svc does not'),
    ('step control: the planted cycle not added', tg, 'stretched', _unstretched,
     "the step control: each phase's longest step at T_svc passes and one cycle past it is caught"),
    ('capture: the closing step is not the capture\'s', tg, 'service',
     lambda obs: [s for s in obs.spans if s.name == 'nvm_store_service'],
     "the capture's CPU time is its steps' cycles, its elapsed time its first step's start to its last step's end"),
    ('capture: the elapsed time is its CPU time', tg, 'capture', _elapsed_is_cpu,
     "the capture's CPU time is its steps' cycles, its elapsed time its first step's start to its last step's end"),
    ('capture: the current writer\'s 24.5 ms bound imposed on F1', tg, 'capture', _bound_reimposed,
     'a capture of twice 24.5 ms of CPU time, every step within T_svc, is no finding'),
    ('order: settle last whatever the names', tg, 'expected_applies',
     lambda applied, expect, base: [*[c for c in ORDER if c != 'aecp_restore_settle'], 'aecp_restore_settle'],
     'the bindings first, then the D3 records in ascending id, settle before the first name'),
    ('order: only the first entry compared', tg, 'apply_order',
     lambda obs, want: ([], [] if not want else ['apply order'] if
                        [c for s in obs.spans for c in s.calls][:1] != want[:1] else []),
     'the settle after the names is caught'),
    ('answers: any sequence_id', tg, 'answers', lambda obs: dict(entity_status=0, entity_name=cases.SAVED_NAME,
                                                                 rx_status=0, rx_talker=7),
     'the answers are read by sequence_id: the name and the talker'),
    ('clocks: the report names the product clocks whatever it was given', RUN, 'clock_line', _fixed_clock_line,
     'a run at other clocks is reported at them: its clocks named, its figures converted at its CPU clock'),
    ('clocks: the last table without its clock line', RUN, 'table', _last_table_unclocked,
     'every table of the report has the clocks beside it'),
    ('clocks: results.json without its clocks', RUN, 'record', _unclocked_record,
     'the results record carries the clocks its builds recorded, through JSON'),
    ('clocks: a missing clock not refused', RUN, 'missing_clocks', lambda rec: [],
     'a record without its sys_hz is refused'),
    ('clocks: the figures not checked against the CPU clock', RUN, 'misconverted', lambda rec: [],
     'a record whose CPU clock is not the one its figures were converted at is refused'),
    ("clocks: the record not compared with its builds'", RUN, 'against_build', lambda rec, specs: [],
     "run.py refuses a run whose clocks are not its builds', writing no table"),
    ("clocks: the first build's clocks taken for all", RUN, 'clocks', _first_build_clocks,
     'builds that disagree on their clocks, lack one or are none are refused'),
    ('clocks: an unconditional 50 MHz and 100 MHz for the run', RUN, 'clocks',
     lambda specs: dict(cpu_hz=CPU_HZ, sys_hz=SYS_HZ),
     "run.py writes its builds' clocks to results.json and beside every table of table.md"),
    ('the current flash writer: its 24.5 ms check removed from its grader', SELF, 'shipping_source',
     _shipping_check_removed,
     "the current flash writer's capture is held to 24.5 ms: exactly 24.5 ms passes, one system tick more is "
     "refused"),
)


def run_mutants() -> list[Check]:
    """Each mutant applied alone: its named check must fail."""
    out = []
    for label, owner, name, value, check in MUTANTS:
        with replaced(owner, name, value):
            results = {n: ok for n, ok, _ in checks()}
        out.append((f'mutant caught: {label}', results.get(check) is False, f'{check}: {results.get(check)}'))
    return out


def main() -> int:
    """Print every check and mutant; 0 when all pass."""
    results = [*checks(), *run_mutants()]
    for name, ok, detail in results:
        print(f"{'PASS' if ok else 'FAIL'}: {name}" + ('' if ok else f' ({detail[:400]})'))
    failures = sum(not ok for _, ok, _ in results)
    print(f'checks: {len(results)}   failures: {failures}')
    return 1 if failures else 0
