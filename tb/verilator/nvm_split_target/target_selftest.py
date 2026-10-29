# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The saved-state cases' portable self-test (#665): Python and PyYAML only, no LiteX or simulator.

It runs the graders on synthetic logs and the case builders on the shipping
1x1 shape, then replaces each grading rule in turn with a weaker one (MUTANTS)
and requires a named check to fail. Run it through run.py --self-test.
"""
from __future__ import annotations

import contextlib
import struct
import sys
import tempfile
from collections.abc import Callable, Iterator
from pathlib import Path
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import target_cases as cases  # noqa: E402
import target_grade as tg  # noqa: E402

CPU_HZ, SYS_HZ = 50_000_000, 100_000_000
Check = tuple[str, bool, str]


def span(cpu: int, cycles: int, name: str = 'nvm_store_service') -> str:
    """A SPAN line as sim_main.cpp prints it."""
    return f'SPAN {2 * cpu} {cpu} {cycles} 00000fd4 {name}'


def call(cpu: int, name: str) -> str:
    """A CALL line as sim_main.cpp prints it."""
    return f'CALL {2 * cpu} {cpu} {name}'


def commit_log(records: int, step: int, closing: int) -> str:
    """A commit's service steps: an idle step, a latch step per record of `step` cycles, the step that ends the
    capture of `closing` cycles, two seal steps, the erase and its poll, a program and its read-back."""
    lines, cpu = [span(100, 50)], 1000
    for _ in range(records):
        lines += [span(cpu, step), call(cpu + 1, 'acmp_nvm:latch'), call(cpu + 2, 'aecp_value_latch')]
        cpu += step + 10_000
    lines.append(span(cpu, closing))
    cpu += closing + 10_000
    for phase in ('nvm_crc32_update', 'nvm_crc32_update', 'nvm_flash_litespi:ls_erase', 'nvm_flash_litespi:ls_busy',
                  'nvm_flash_litespi:ls_program', 'nvm_flash_litespi:ls_read'):
        lines += [span(cpu, 300), call(cpu + 1, phase)]
        cpu += 10_000
    return '\n'.join([*lines, 'RESULT: PASS']) + '\n'


def capture_checks() -> list[Check]:
    """The capture's steps and the bound: at the bound it fits, one page of its own cost past it is caught,
    and a capture missing a record or its closing step is refused."""
    bound = tg.recipe.HOLD_FLOOR_MS * CPU_HZ // 2000
    records, closing = 4, 1000
    step = (bound - closing) // records
    exact = commit_log(records, step, bound - records * step)
    got = tg.capture(tg.observe(exact, SYS_HZ, CPU_HZ), records, CPU_HZ)
    out = [('a capture at exactly its bound fits', got['within_bound'] and got['cycles'] == bound and
            not got['findings'], str(got))]
    page = got['cycles'] * cases.PAGE // (records * 64)
    over = tg.capture(tg.lengthened(tg.observe(exact, SYS_HZ, CPU_HZ), page), records, CPU_HZ)
    out.append(('a capture one page of its own cost past its bound is caught',
                not over['within_bound'] and any('over its' in f for f in over['findings']), str(over)))
    short = tg.capture(tg.observe(commit_log(records - 1, step, closing), SYS_HZ, CPU_HZ), records, CPU_HZ)
    out.append(('a capture that latched one record fewer than the shape is refused',
                any('latched 3 records' in f for f in short['findings']), str(short['findings'])))
    phases = tg.phases(tg.observe(exact, SYS_HZ, CPU_HZ), CPU_HZ)
    out.append(('every service step is classified by its calls, the closing step as the capture\'s',
                {p: r['steps'] for p, r in phases.items()} == dict(idle=1, capture=records + 1, seal=2, erase=1,
                                                                  poll=1, program=1, read=1), str(phases)))
    slow = tg.phases(tg.observe(commit_log(1, int(10.5 * CPU_HZ / 1000), closing), SYS_HZ, CPU_HZ), CPU_HZ)
    out.append(('a step over T_svc is reported against it', not slow['capture']['within_t_svc'], str(slow['capture'])))
    return out


def boot_log(applies: list[str]) -> str:
    """One boot span holding the owners' apply entries in order, then a service step."""
    lines = [span(100, 90_000, 'nvm_store_boot')]
    lines += [call(200 + 10 * i, name) for i, name in enumerate(applies)]
    return '\n'.join([*lines, span(200_000, 50), 'RESULT: PASS']) + '\n'


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
    graded = {name: tg.grade_case(case, tg.observe(text, SYS_HZ, CPU_HZ), ctx, None)['caught'] for name, case, text in (
        ('reordered', reorder, boot_log([*ORDER[1:], ORDER[0]])), ('in order', reorder, boot_log(ORDER)),
        ('escaped write', escape, 'FAIL: flash write escaped the journal\nRESULT: FAIL\n'),
        ('no write', escape, 'RESULT: PASS\n'))}
    return [('a control is caught by its words and escapes without them',
             graded == {'reordered': True, 'in order': False, 'escaped write': True, 'no write': False}, str(graded))]


def checks() -> list[Check]:
    """Every check."""
    return [*capture_checks(), *order_checks(), *answer_checks(), *journal_checks(), *plant_checks(),
            *control_checks()]


@contextlib.contextmanager
def replaced(name: str, value: object) -> Iterator[None]:
    """target_grade's `name` replaced for the block."""
    with patch.object(tg, name, value):
        yield


def _strict(obs: tg.Observed, extra: int) -> tg.Observed:
    """lengthened, but the extra cycles dropped."""
    return obs


#: Each grading rule replaced by a weaker one, and the check that must then fail.
MUTANTS: tuple[tuple[str, str, object, str], ...] = (
    ('capture: strictly below the bound', 'fits', lambda capture_ms: capture_ms < tg.BOUND_MS,
     'a capture at exactly its bound fits'),
    ('capture: the bound is the whole hold floor', 'BOUND_MS', tg.recipe.HOLD_FLOOR_MS,
     'a capture one page of its own cost past its bound is caught'),
    ('capture: the closing step is not the capture\'s', 'service',
     lambda obs: [s for s in obs.spans if s.name == 'nvm_store_service'],
     'a capture at exactly its bound fits'),
    ('capture: the planted page is not added', 'lengthened', _strict,
     'a capture one page of its own cost past its bound is caught'),
    ('order: settle last whatever the names', 'expected_applies',
     lambda applied, expect, base: [*[c for c in ORDER if c != 'aecp_restore_settle'], 'aecp_restore_settle'],
     'the bindings first, then the D3 records in ascending id, settle before the first name'),
    ('order: only the first entry compared', 'apply_order',
     lambda obs, want: ([], [] if not want else ['apply order'] if
                        [c for s in obs.spans for c in s.calls][:1] != want[:1] else []),
     'the settle after the names is caught'),
    ('answers: any sequence_id', 'answers', lambda obs: dict(entity_status=0, entity_name=cases.SAVED_NAME,
                                                             rx_status=0, rx_talker=7),
     'the answers are read by sequence_id: the name and the talker'),
)


def run_mutants() -> list[Check]:
    """Each mutant applied alone: its named check must fail."""
    out = []
    for label, name, value, check in MUTANTS:
        with replaced(name, value):
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
