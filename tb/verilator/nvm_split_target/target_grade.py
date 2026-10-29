# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Grade one saved-state case's log from the split CPU (#665).

The log is the service-budget testbench's (tb/verilator/ctrl_service_budget/
sim_main.cpp), read through its own parser (grade.parse). Its SPAN lines give
each call of nvm_store_boot and nvm_store_service, from the commit of the
function's entry to the commit of its return address, in CPU cycles; its CALL
lines give each entry of the state port's owners and of the flash port's
calls. A service step is classified by the calls inside it:

  capture  the owners' latch (acmp_nvm's, which every record's latch passes),
           and the step after the last one, which ends the capture and seals
           the header (nvm_seal_begin);
  seal     nvm_crc32_update, 256 bytes a step;
  erase    ls_erase; program: ls_program; poll: ls_busy alone;
  read     ls_read (the blank check, or the verify);
  idle     none of them.

THE CAPTURE is the store's capture phase for one work set, every record of the
shape dirty: the sum of its steps' CPU cycles at the CPU's clock. It must be at
most half the shipping writer's unchanged hold floor
(tb/verilator/nvm_capture_cpu/recipe.py HOLD_FLOOR_MS / 2 = 24.5 ms), the bound
check_nvm_capture.py holds the shipping capture to. Each step's CPU time is
graded against the loop's T_svc (FR_NFR.md 3.4.1, scenario.T_SVC_MS).

THE APPLY ORDER is read inside the one nvm_store_boot span: the owners' apply
entries in order must be the saved container's, record by record: every
binding (acmp_restore_binding), then every D3 record in ascending id
(aecp_value_restore for a value, aecp_map_restore for a map), the settle step
(aecp_restore_settle) once, before the first name, and the names
(aecp_value_restore) last (ARCHITECTURE_HW_SW_SPLIT.md section 2;
ctrl_nvm/README.md "Boot" items 5 to 7).
"""
from __future__ import annotations

import struct
import sys
from dataclasses import dataclass, field
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
for path in (ROOT / 'tb/verilator/ctrl_service_budget', ROOT / 'tb/verilator/nvm_capture_cpu'):
    sys.path.insert(0, str(path))

import grade as budget  # noqa: E402  the service-budget harness's parser, read only
import recipe  # noqa: E402
import scenario  # noqa: E402

#: The capture's bound: half the shipping writer's guaranteed hold floor (check_nvm_capture.py).
BOUND_MS = recipe.HOLD_FLOOR_MS / 2
#: The owners' entries the boot's two walks make, by the record kind that makes each.
APPLY = ('acmp_restore_binding', 'aecp_value_restore', 'aecp_map_restore', 'aecp_restore_settle')
#: Each record group's apply entry (aecp_nvm.c apply: SUID and MCR are applied by no owner).
GROUP_CALL = {'BINDING': 'acmp_restore_binding', 'CFG_IDX': 'aecp_value_restore', 'RATE': 'aecp_value_restore',
              'CLKSRC': 'aecp_value_restore', 'FMT_IN': 'aecp_value_restore', 'FMT_OUT': 'aecp_value_restore',
              'PT_OFS': 'aecp_value_restore', 'MAPS_IN': 'aecp_map_restore', 'MAPS_OUT': 'aecp_map_restore',
              'NAME': 'aecp_value_restore'}
#: A service step's phase, by the first of these calls it makes.
PHASE_CALLS = (('acmp_nvm:latch', 'capture'), ('nvm_crc32_update', 'seal'), ('nvm_flash_litespi:ls_erase', 'erase'),
               ('nvm_flash_litespi:ls_program', 'program'), ('nvm_flash_litespi:ls_read', 'read'),
               ('nvm_flash_litespi:ls_busy', 'poll'))
AECP_RESPONSE, GET_RX_STATE_RESPONSE = 1, 11


@dataclass
class Step:
    """One traced call: its start in system and CPU cycles, its length in CPU cycles, its calls."""
    name: str
    sys: int
    cpu: int
    cycles: int
    calls: list[str] = field(default_factory=list)
    phase: str = 'idle'


@dataclass
class Observed:
    """What one case's log shows."""
    log: budget.Log
    spans: list[Step]
    flash: dict[str, int]
    flash_ops: list[int]
    text: str


def observe(text: str, sys_hz: int, cpu_hz: int) -> Observed:
    """The log parsed: its spans with the calls inside each, the flash summary and its mutating operations."""
    log = budget.parse(text, sys_hz, cpu_hz)
    spans = [Step(rest[4], int(rest[0]), int(rest[1]), int(rest[2])) for kind, *rest in log.traced if kind == 'SPAN']
    for kind, *rest in log.traced:
        if kind != 'CALL':
            continue
        cpu = int(rest[1])
        for step in spans:
            if step.cpu <= cpu <= step.cpu + step.cycles:
                step.calls.append(rest[2])
    flash, ops = {}, []
    for line in text.splitlines():
        if line.startswith('FLASH '):
            flash = {k: int(v) for k, v in (kv.split('=') for kv in line.split()[1:])}
        elif line.startswith('FLASHOP '):
            ops.append(int(line.split()[2]))
    for step in spans:
        step.phase = next((phase for call, phase in PHASE_CALLS if call in step.calls), 'idle')
    return Observed(log, spans, flash, ops, text)


def service(obs: Observed) -> list[Step]:
    """The store's service steps in order, the step that ends the capture marked as the capture's."""
    steps = [s for s in obs.spans if s.name == 'nvm_store_service']
    last = max((i for i, s in enumerate(steps) if s.phase == 'capture'), default=None)
    if last is not None and last + 1 < len(steps) and steps[last + 1].phase == 'idle':
        steps[last + 1].phase = 'capture'
    return steps


def ms(cycles: int, cpu_hz: int) -> float:
    """CPU cycles as milliseconds at the CPU's clock."""
    return cycles * 1000.0 / cpu_hz


def decomposed(obs: Observed, plens: list[int]) -> dict:
    """The capture's cost split into a fixed cost a step and a cost a payload byte: the least-squares line
    through each latch step's CPU cycles against the payload length of the record it latched (plens, the
    shape's records in ascending id, which the capture walks), and the median idle step, which every step
    pays too."""
    latches = [s.cycles for s in service(obs) if s.phase == 'capture' and 'acmp_nvm:latch' in s.calls]
    idle = sorted(s.cycles for s in service(obs) if s.phase == 'idle')
    pairs = list(zip(plens, latches))
    n = len(pairs)
    if n < 2 or len({p for p, _ in pairs}) < 2:
        return {}
    mean_p, mean_c = sum(p for p, _ in pairs) / n, sum(c for _, c in pairs) / n
    slope = sum((p - mean_p) * (c - mean_c) for p, c in pairs) / sum((p - mean_p) ** 2 for p, _ in pairs)
    return dict(per_step_cycles=round(mean_c - slope * mean_p), per_byte_cycles=round(slope, 1),
                idle_step_cycles=idle[len(idle) // 2] if idle else 0, payload_bytes=sum(plens[:n]))


def fits(capture_ms: float) -> bool:
    """A capture fits at or under its bound."""
    return capture_ms <= BOUND_MS


def capture(obs: Observed, records: int, cpu_hz: int) -> dict:
    """The capture of a full work set: its steps, CPU cycles and ms, its longest step, and findings."""
    steps = [s for s in service(obs) if s.phase == 'capture']
    latches = sum(s.calls.count('acmp_nvm:latch') for s in steps)
    cycles = sum(s.cycles for s in steps)
    findings = []
    if latches != records or len(steps) != records + 1:
        findings.append(f'the capture latched {latches} records in {len(steps)} steps, not the shape\'s '
                        f'{records} records and the step that ends it')
    result = dict(steps=len(steps), latches=latches, cycles=cycles, ms=ms(cycles, cpu_hz),
                  longest_cycles=max((s.cycles for s in steps), default=0), bound_ms=BOUND_MS)
    result['within_bound'] = fits(result['ms'])
    if not result['within_bound']:
        findings.append(f"the capture takes {result['ms']:.3f} ms, over its {BOUND_MS} ms bound")
    return dict(result, findings=findings)


def lengthened(obs: Observed, extra: int) -> Observed:
    """The observation with its capture's closing step `extra` CPU cycles longer, its calls as they were: the
    capture made that much slower. The bound's control plants it in the measured commit (run.py)."""
    spans = [Step(s.name, s.sys, s.cpu, s.cycles, list(s.calls), s.phase) for s in obs.spans]
    closing = [s for s in service(Observed(obs.log, spans, obs.flash, obs.flash_ops, obs.text))
               if s.phase == 'capture']
    if not closing:
        raise ValueError('the capture has no closing step to lengthen')
    closing[-1].cycles += extra
    return Observed(obs.log, spans, obs.flash, obs.flash_ops, obs.text)


def phases(obs: Observed, cpu_hz: int) -> dict[str, dict]:
    """Each phase's steps: their count, longest and total CPU cycles, and the longest in ms against T_svc."""
    out: dict[str, dict] = {}
    for step in service(obs):
        row = out.setdefault(step.phase, dict(steps=0, longest_cycles=0, cycles=0))
        row['steps'] += 1
        row['cycles'] += step.cycles
        row['longest_cycles'] = max(row['longest_cycles'], step.cycles)
    for row in out.values():
        row['longest_ms'] = ms(row['longest_cycles'], cpu_hz)
        row['within_t_svc'] = row['longest_ms'] <= scenario.T_SVC_MS
    return out


def expected_applies(applied: dict, expect: dict, base: int) -> list[str]:
    """The owners' apply entries a boot of this container makes, in order: the bindings, then the D3
    records in ascending id with the settle step before the first name, or last when there is none."""
    sys.path.insert(0, str(ROOT / 'scripts'))
    from nvm_klj2 import rid_of_key
    keys = sorted(applied, key=lambda k: rid_of_key(k, base))
    out = [GROUP_CALL[k[0]] for k in keys if k[0] == 'BINDING']
    settled = False
    for key in keys:
        if key[0] == 'BINDING' or key[0] not in GROUP_CALL:
            continue
        if key[0] == 'NAME' and not settled:
            out.append('aecp_restore_settle')
            settled = True
        out.append(GROUP_CALL[key[0]])
    return out if settled else [*out, 'aecp_restore_settle']


def apply_order(obs: Observed, want: list[str]) -> tuple[list[str], list[str]]:
    """The owners' apply entries inside the one boot, and the findings against want."""
    boots = [s for s in obs.spans if s.name == 'nvm_store_boot']
    if len(boots) != 1:
        return [], [f'apply order: {len(boots)} boots traced, not one']
    seen = [c for c in boots[0].calls if c in APPLY]
    if seen == want:
        return seen, []
    first = next((i for i, (a, b) in enumerate(zip(seen, want)) if a != b), min(len(seen), len(want)))
    return seen, [f'apply order: entry {first} is {seen[first] if first < len(seen) else "absent"}, the container '
                  f'needs {want[first] if first < len(want) else "none"} ({len(seen)} entries, {len(want)} wanted)']


def answers(obs: Observed) -> dict:
    """The entity_name READ_DESCRIPTOR answered and sink 0's GET_RX_STATE talker, from the wire."""
    sys.path.insert(0, str(HERE))
    from target_cases import SEQ
    out: dict = {}
    for _cycle, ch, _interface, frame in obs.log.wire:
        if ch == scenario.CH['aecp'] and frame[14] == 0xFB and frame[15] & 0x0F == AECP_RESPONSE \
                and struct.unpack_from('>H', frame, 34)[0] == SEQ['read_entity']:
            out['entity_status'] = frame[16] >> 3
            out['entity_name'] = frame[90:154]
        if ch == scenario.CH['acmp'] and frame[14] == 0xFC and frame[15] & 0x0F == GET_RX_STATE_RESPONSE \
                and struct.unpack_from('>H', frame, 62)[0] == SEQ['rx_state']:
            out['rx_status'] = frame[16] >> 3
            out['rx_talker'] = struct.unpack_from('>Q', frame, 34)[0]
    return out


def completed(obs: Observed) -> list[str]:
    """The run's own failures: a trap, a bus error, a failed testbench check, a script left unfinished."""
    found = [f'trapped: {t}' for t in obs.log.traps]
    found += [f'testbench: {e}' for e in obs.log.errors]
    if obs.log.result != 'PASS':
        found.append(f'the testbench result is {obs.log.result or "absent"}')
    found += [f'a wait timed out: {text}' for _cycle, text in obs.log.steps if text.endswith('TIMEOUT')]
    return found


@dataclass(frozen=True)
class Context:
    """What a case is graded against: the point's clocks and shape, the journal it booted, the one it left,
    and the committed container's records and their apply entries (empty before the commit case ran)."""
    cpu_hz: int
    records: int
    pages: int
    journal_in: bytes
    journal_out: bytes
    applied: dict
    applies: list[str]
    plens: tuple[int, ...] = ()


def unwritten(obs: Observed, ctx: Context) -> list[str]:
    """Nothing programmed or erased, and the journal left as it booted."""
    found = [f'the boot wrote the flash: operations {obs.flash_ops}'] if obs.flash_ops else []
    if ctx.journal_out != ctx.journal_in:
        found.append('the journal the boot left is not the one it booted')
    return found


def held_to(obs: Observed, name: bytes | None, talker: int) -> list[str]:
    """The entity's name and sink 0's talker as AECP and ACMP answer them: name None means any name but the
    two the cases write."""
    from target_cases import NEWER_NAME, SAVED_NAME
    got = answers(obs)
    found = []
    if got.get('entity_status') != 0 or got.get('rx_status') != 0:
        found.append(f"the questions were not answered SUCCESS: {got.get('entity_status')}, {got.get('rx_status')}")
    seen = got.get('entity_name')
    if name is not None and seen != name or name is None and seen in (SAVED_NAME, NEWER_NAME, None):
        found.append(f"the entity_name answered is {seen!r}, not {name!r}" if name else
                     f"the entity_name answered is {seen!r}, a saved one")
    if got.get('rx_talker') != talker:
        found.append(f"sink 0's talker is {got.get('rx_talker')}, not {talker:#x}")
    return found


def guarded(obs: Observed) -> list[str]:
    """The guard's probe: before the loop's first step, every outside call reached the port and was refused
    (no device operation), and the one erase inside the journal reached the device; then the boot opened."""
    from target_cases import GUARD_CALLS
    first = min((s.cpu for s in obs.spans if s.name == 'nvm_store_service'), default=None)
    calls = [rest[2] for kind, *rest in obs.log.traced if kind == 'CALL' and (first is None or int(rest[1]) < first)]
    erases, programs = calls.count('nvm_flash_litespi:ls_erase'), calls.count('nvm_flash_litespi:ls_program')
    found = []
    if (erases, programs) != (GUARD_CALLS['erase_outside'] + GUARD_CALLS['erase_inside'], GUARD_CALLS['program_outside']):
        found.append(f'the probe reached the port with {erases} erases and {programs} programs')
    if obs.flash_ops != [0xD8] or obs.flash.get('erases') != 1 or obs.flash.get('programs') != 0:
        found.append(f'the device saw {obs.flash_ops} ({obs.flash}), not the one erase inside the journal')
    if first is None:
        found.append('the loop never ran: the probe parked the hart')
    return found


def committed(obs: Observed, ctx: Context, bench: object) -> list[str]:
    """The commit: one erase and the container's pages programmed, and the journal it left holds, by the
    reference codec, the saved name and sink 0's binding to the talker it was bound to."""
    from target_cases import SAVED_NAME
    found = []
    if (obs.flash.get('erases'), obs.flash.get('programs')) != (1, ctx.pages):
        found.append(f"the commit erased {obs.flash.get('erases')} blocks and programmed {obs.flash.get('programs')} "
                     f'pages, not one block and {ctx.pages} pages')
    img = struct.unpack_from('<I', ctx.journal_out, 16)[0]
    verdict, applied = bench.decode(ctx.journal_out[:img]) if 44 <= img <= len(ctx.journal_out) else (-1, {})
    if verdict != 0:
        return [*found, f'the journal the commit left does not decode: verdict {verdict}']
    if SAVED_NAME not in applied.values():
        found.append('the committed container holds no NAME record of the saved name')
    if scenario.TALKER_A.to_bytes(8, 'big') not in applied.get(('BINDING', 0), b''):
        found.append("the committed container's sink 0 binding does not name the talker it was bound to")
    return found


def grade_case(case: object, obs: Observed, ctx: Context, bench: object) -> dict:
    """One case's verdict: its measurement where it has one, its findings, and whether it passed (a control
    passes when its planted defect is caught by its words)."""
    from target_cases import SAVED_NAME
    result: dict = dict(case=case.name, findings=completed(obs))
    if case.control:
        words = [f for f in apply_order(obs, ctx.applies)[1]] if case.control == 'apply order' else \
            [case.control] if case.control in obs.text else []
        result.update(caught=bool(words), words=words, passed=bool(words))
        return result
    if case.commit:
        result['capture'] = capture(obs, ctx.records, ctx.cpu_hz)
        result['capture']['decomposed'] = decomposed(obs, list(ctx.plens))
        result['phases'] = phases(obs, ctx.cpu_hz)
        result['findings'] += result['capture'].pop('findings') + committed(obs, ctx, bench)
        result['findings'] += held_to(obs, SAVED_NAME, scenario.TALKER_A)
        result['t_svc_misses'] = [p for p, row in result['phases'].items() if not row['within_t_svc']]
    elif case.name == 'guard':
        result['findings'] += guarded(obs)
    else:
        restores = case.journal in ('saved', 'torn')
        seen, order = apply_order(obs, ctx.applies if restores else [])
        result.update(applies=len(seen), boot_cycles=next((s.cycles for s in obs.spans if s.name == 'nvm_store_boot'), 0))
        result['findings'] += order + unwritten(obs, ctx)
        result['findings'] += held_to(obs, SAVED_NAME if restores else None, scenario.TALKER_A if restores else 0)
    result['passed'] = not result['findings']
    return result
