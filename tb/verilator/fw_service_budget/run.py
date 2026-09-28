#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Measure externally marked firmware service intervals on the product CPU."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
SHAPES = ('endstation_ax7101_1x1_tdm8', 'endstation_ax7101_8x8')
CPU_HZ = 50_000_000
PLANS = ('all', 'queued-input', 'queued-short', 'queued-builtins', 'uart-paced', 'device-wait')
SYS_HZ = 100_000_000
# Cover every command registered by the product translation unit, plus
# normal, boundary and refused parameter paths. A separate queued plan
# covers BIOS built-ins, unknown commands and empty lines.
COMMANDS = (
    'milan_status', 'milan_gettime', 'milan_nvm',
    'milan_nvm commit', 'milan_nvm commit', 'milan_nvm',
    'milan_nvm wipe', 'milan_nvm', 'milan_nvm invalid',
    'milan_settime 0 0', 'milan_settime 18446744073 709551615',
    'milan_settime 18446744073 709551616', 'milan_settime invalid',
    'milan_utc 0 0 37', 'milan_utc 18446744073709551615 0 1',
    'milan_utc invalid 0 0', 'milan_status',
)


def require(ok: bool, message: str) -> None:
    """Reject absent or inconsistent evidence at its owning boundary."""
    if not ok:
        raise RuntimeError(message)


def command_plan(plan: str, shape: str = SHAPES[0]) -> tuple[str, ...]:
    """Name the finite schedule; queued-input repeats the public 133-byte P3."""
    require(plan in PLANS, 'unknown command plan')
    if plan == 'queued-input':
        return ('milan_nvm',) * 12 + ('milan_status',)
    if plan == 'queued-short':
        return ('milan_status',) * 350
    if plan == 'queued-builtins':
        return ('mem_read 0x40000000 128', '', 'unknown_command') * 350 + ('milan_status',)
    if plan == 'device-wait':
        return ('milan_nvm commit', 'milan_status')
    return COMMANDS


def validate_waits(erase_us: int, program_us: int) -> None:
    """Admit device maxima, bounded below the unchanged 30-second guard."""
    # At most four erases and 100 pages in either supported command plan:
    # 12 s + 0.5 s WIP plus the measured <6 s no-WIP plan fits 30 s.
    require(0 <= erase_us <= 3_000_000, 'erase wait must be 0..3000000 us')
    require(0 <= program_us <= 5_000, 'program wait must be 0..5000 us')


def wait_controls() -> int:
    """Exercise each accepted boundary and each immediate input refusal."""
    count = 0
    for erase, program in ((0, 0), (3_000_000, 5_000)):
        validate_waits(erase, program)
        count += 1
    for erase, program in ((-1, 0), (3_000_001, 0), (0, -1), (0, 5_001)):
        try:
            validate_waits(erase, program)
        except RuntimeError:
            count += 1
        else:
            raise RuntimeError('unsupported device wait escaped')
    return count


def tick_span(events: list[dict], start: int, end: int) -> dict:
    """Reconstruct the maximum between function entries, including duty edges."""
    previous = start
    spans = []
    count = 0
    for event in events:
        if event['kind'] != 'ticks' or event['last'] < start or event['first'] > end:
            continue
        require(start <= event['first'] <= event['last'] <= end, 'tick block crossed a duty boundary')
        require(event['count'] > 0 and event['last'] <= event['cycle'], 'invalid tick block')
        require(previous <= event['first'], 'overlapping tick blocks')
        spans.append((previous, event['first']))
        if event['count'] > 1:
            require(0 < event['max_gap'] <= event['last'] - event['first'], 'invalid tick maximum')
            require(event['first'] <= event['gap_start'] < event['gap_start'] + event['max_gap'] <= event['last'],
                    'tick maximum lies outside its block')
            spans.append((event['gap_start'], event['gap_start'] + event['max_gap']))
        else:
            require(event['first'] == event['last'] and event['max_gap'] == 0, 'invalid singleton tick')
        previous = event['last']
        count += event['count']
    spans.append((previous, end))
    left, right = max(spans, key=lambda pair: pair[1] - pair[0])
    return dict(tick_calls=count, no_tick_sys_cycles=right - left,
                no_tick_ms=(right - left) / 100_000, no_tick_start=left, no_tick_end=right)


def tick_controls() -> int:
    """Check internal, inter-block and boundary spans with explicit counters."""
    blocks = [dict(kind='ticks', cycle=250, first=140, last=220, count=3, max_gap=50, gap_start=170),
              dict(kind='ticks', cycle=450, first=400, last=420, count=2, max_gap=20, gap_start=400)]
    got = tick_span(blocks, 100, 500)
    require((got['tick_calls'], got['no_tick_start'], got['no_tick_end']) == (5, 220, 400),
            'inter-block tick span changed')
    require(tick_span([], 100, 500)['no_tick_sys_cycles'] == 400, 'unserviced duty lost its edge span')
    for bad in ([dict(blocks[0], gap_start=0)], [dict(blocks[0], first=99)]):
        try:
            tick_span(bad, 100, 500)
        except RuntimeError:
            continue
        raise RuntimeError('invalid tick block escaped')
    return 4


def add_tick_bounds(rows: list[dict], events: list[dict], starts: list[dict],
                    ends: list[dict], commands: tuple[str, ...]) -> None:
    """Compare per-duty tick gaps with rate-limit phase and full TX allowance."""
    require(any(e['kind'] == 'ticks' for e in events), 'no retired heartbeat entries')
    for row in rows:
        start, end = row['start_sys_cycle'], row['end_sys_cycle']
        row.update(tick_span(events, start, end))
        owners = [(i, a, b) for i, (a, b) in enumerate(zip(starts, ends))
                  if a['cycle'] <= start and end <= b['cycle']]
        tx_bytes = ends[owners[0][0]]['tx_bytes'] - starts[owners[0][0]]['tx_bytes'] if owners else 0
        row['uart_tx_allowance_ms'] = tx_bytes * 10_000 / 115200
        row['period_bound_ms'] = 250 + row['no_tick_ms'] + row['uart_tx_allowance_ms']
        row['period_bound_margin_ms'] = 500 - row['period_bound_ms']
        row['liveness_bound_margin_ms'] = 2000 - row['period_bound_ms']
    require(len(starts) == len(commands), 'tick duty census')


def liveness_report(raw: str) -> list[dict]:
    """Retain UART backing-state observations; silence is never a clean proof."""
    chunks = re.split(r'^EVENT cycle=\d+ kind=command_start index=\d+.*$', raw, flags=re.M)[1:]
    result = []
    for index, chunk in enumerate(chunks):
        text = re.sub(r'\nEVENT [^\n]*\n', '', chunk)
        match = re.search(r'backed=([01])', text)
        pp = re.search(r'PP_STAT=([0-9a-fA-F]{8})', text)
        if match or pp:
            backed = int(match[1]) if match else (int(pp[1], 16) >> 6) & 1
            end = re.search(r'EVENT cycle=(\d+) kind=command_end', chunk)
            require(end is not None, 'liveness sample without completed command')
            result.append(dict(command_index=index, backed=backed, sampled_by_sys_cycle=int(end[1])))
    require(bool(result), 'no UART backing-state evidence')
    return result


def inputs() -> dict[str, str]:
    """Hash measurement code and product inputs without recording local paths."""
    files = [ROOT / 'sw/firmware/milan_baremetal/milan_baremetal.c',
             ROOT / 'sw/firmware/milan_baremetal/Makefile', ROOT / 'sw/litex/milan_soc.py']
    files += sorted((ROOT / 'sw/litex/patches').glob('*.patch'))
    files += [ROOT / 'configs' / (s + '.yaml') for s in SHAPES]
    files += sorted((ROOT / 'tb/verilator/nvm_capture_cpu').glob('*.py'))
    files += sorted(p for p in HERE.iterdir() if p.suffix in ('.py', '.cpp', '.hpp', '.vlt'))
    return {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}


def build_hashes(build_dir: Path, spec: dict) -> dict[str, str]:
    """Bind reuse to compiled sources, generated includes, BIOS and executable."""
    files = {Path(p) for p in spec['sources']}
    files.update(build_dir.glob('generated/**/*.svh'))
    files.update(build_dir.glob('gateware/*.init'))
    files.update(build_dir.glob('software/include/generated/*.h'))
    files.update(build_dir / p for p in ('native/Vsim', 'software/bios/bios.bin', 'software/bios/bios.elf',
                                       'retirement.hpp', 'aem_desc.bin'))
    files.update(HERE / p for p in ('build.py', 'sim_main.cpp', 'flash.hpp', 'observe.vlt',
                                       'phy.py', 'phy.hpp'))
    files.update(ROOT / p for p in inputs() if not p.startswith('tb/verilator/fw_service_budget/'))
    result = {}
    for path in sorted(files):
        if path.is_relative_to(build_dir):
            name = 'build/' + str(path.relative_to(build_dir))
        elif path.is_relative_to(ROOT):
            name = str(path.relative_to(ROOT))
        else:
            name = 'external/' + path.name
        require(name not in result, 'ambiguous build input: ' + name)
        result[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def fixtures(build_dir: Path, shape_name: str, populated: bool, plan: str = 'all') -> dict:
    """Prepare independent KLJ2 media; neither CPU memory nor RTL is forced."""
    sys.path.insert(0, str(ROOT / 'scripts'))
    from nvm_contract import Donor, Ident, Shape
    from nvm_klj2 import frame_record, klj2_assemble, payload_bytes
    from nvm_shape import binding_base, inventory, layout_version
    generated = build_dir / 'generated' / shape_name
    overlay = json.loads((generated / 'aem_overlay.json').read_text())
    blob = (build_dir / 'aem_desc.bin').read_bytes()
    shape = Shape(cfg=ROOT / 'configs' / (shape_name + '.yaml'), names=int.from_bytes(blob[10:12], 'big'),
                  dc=overlay['descriptor_counts'], spi=overlay['stream_ports']['input'],
                  spo=overlay['stream_ports']['output'])
    donor = Donor(base=binding_base(), layout=layout_version())
    rows = inventory(shape, donor.base)
    require(all(rid is not None for _, _, rid, _, _ in rows), 'record allocation overflow')
    frames = {rid: frame_record(rid, payload_bytes(group, index, rid, plen), donor.layout)
              for group, index, rid, plen, _ in rows}
    ident = Ident(seq=1, entity_id=int(overlay['adp']['entity_id'], 16),
                  model_id=int(overlay['entity']['entity_model_id'], 16))
    valid, _ = klj2_assemble(frames, donor, ident)
    media = bytearray(b'\xff' * 0x20000)
    if populated:
        media[:len(valid)] = valid
        media[0x10000:0x10000 + len(valid)] = valid
    (build_dir / 'slots.bin').write_bytes(media)
    (build_dir / 'commands.txt').write_text('\n'.join(command_plan(plan, shape_name)) + '\n')
    return dict(image_bytes=len(valid), records=len(rows), aem_bytes=len(blob), populated=populated,
                slots_sha256=hashlib.sha256(media).hexdigest(), plan=plan, shape=shape_name)


def read_events(raw: str) -> list[dict]:
    """Read only complete native event lines, retaining integer cycle counters."""
    result = []
    for line in raw.splitlines():
        if not line.startswith('EVENT '):
            continue
        pairs = dict(part.split('=', 1) for part in line[6:].split())
        result.append({key: value if key == 'kind' else int(value) for key, value in pairs.items()})
    require(bool(result), 'no external marker evidence')
    require(all(a['cycle'] <= b['cycle'] for a, b in zip(result, result[1:])), 'markers out of order')
    return result


def interval(name: str, start: int, end: int, budget_ms: int | None, wait_cycles: int = 0) -> dict:
    """Preserve the measured interval; round up its CPU-cycle representation."""
    require(end > start and 0 <= wait_cycles <= end - start, f'invalid interval: {name}')
    cycles = end - start
    return dict(duty=name, start_sys_cycle=start, end_sys_cycle=end, sys_cycles=cycles, cpu_cycles=(cycles + 1) // 2,
                ms=cycles / 100_000, device_wait_ms=wait_cycles / 100_000,
                service_ms=(cycles - wait_cycles) / 100_000, budget_ms=budget_ms,
                margin_ms=None if budget_ms is None else budget_ms - cycles / 100_000)


def grade_rows(rows: list[dict]) -> None:
    """Each declared budget is executable, including an over-budget duty."""
    require(bool(rows), 'no measured duties')
    for row in rows:
        require(row['sys_cycles'] > 0, 'nonpositive service interval')
        if row['budget_ms'] is not None:
            require(row['sys_cycles'] <= row['budget_ms'] * 100_000, 'over-budget duty: ' + row['duty'])


def budget_findings(rows: list[dict]) -> list[str]:
    """Retain every strict budget refusal for the measurement-only report."""
    findings = []
    for row in rows:
        try:
            grade_rows([row])
        except RuntimeError as error:
            findings.append(str(error))
    return findings


def grade(raw: str, media: dict) -> dict:
    """Grade marker census and functional completion before deriving times."""
    commands = command_plan(media.get('plan', 'all'), media.get('shape', SHAPES[0]))
    events = read_events(raw)
    # Passive observations can interrupt a UART word, especially when paced.
    uart = re.sub(r'\nEVENT [^\n]*\n', '', raw)
    starts = [e for e in events if e['kind'] == 'command_start']
    ends = [e for e in events if e['kind'] == 'command_end']
    require([e['index'] for e in starts] == list(range(len(commands))), 'command start census')
    require([e['index'] for e in ends] == list(range(len(commands))), 'command end census')
    require('fabric entity enabled' in uart and 'AEM=loaded' in uart, 'boot did not enable verified AEM')
    require('walk done=1 fail=0' in uart, 'restore walk did not complete successfully')
    commits = commands.count('milan_nvm commit')
    wipes = commands.count('milan_nvm wipe')
    require(uart.count('acknowledged.') == commits, 'console commit acknowledgement census')
    require(uart.count('slot A erased, slot B erased') == wipes, 'wipe erase census')
    require('FAILED' not in uart and 'deferred' not in uart, 'firmware operation failed')
    pages = (media['image_bytes'] + 255) // 256
    require(ends[-1]['erases'] == commits + 2 * wipes and ends[-1]['programs'] == commits * pages
            and ends[-1]['bytes'] == commits * media['image_bytes'], 'flash operation census')
    writes = [e for e in events if e['kind'] == 'write']
    enable = next(e for e in writes if e['address'] == 0x920 and e['value'] & 1)
    walk_start = next(e for e in writes if e['address'] == 0x920 and e['value'] & 2)
    walk_end = next(e for e in writes if e['address'] == 0x920 and not e['value'] & 2
                    and e['cycle'] > walk_start['cycle'])
    require(walk_end['requests'] > walk_start['requests'] and walk_end['responses'] > walk_start['responses'],
            'restore interval contains no backend memory handshakes')
    require(walk_end['requests'] - walk_start['requests'] == walk_end['responses'] - walk_start['responses'],
            'restore request/response count mismatch')
    require(walk_end['errors'] == 0, 'restore backend returned an error')
    aem = next(e for e in events if e['kind'] == 'aem_read')
    rows = [interval('boot_to_entity_enabled', 64, enable['cycle'], 20000),
            interval('aem_copy_crc', aem['cycle'], enable['cycle'], None),
            interval('restore_walk', walk_start['cycle'], walk_end['cycle'], 3000)]
    for index, (start, end) in enumerate(zip(starts, ends)):
        require(start['cycle'] < end['cycle'], 'command end precedes start')
        if index:
            require(ends[index - 1]['cycle'] < start['cycle'], 'overlapping command intervals')
        active = [e for e in events if start['cycle'] <= e['cycle'] <= end['cycle']]
        wait = sum(e['wait_cycles'] for e in active if e['kind'] == 'flash')
        command = commands[index]
        budget = None if command.endswith(' wipe') else 8000 if command.endswith(' commit') else 500
        rows.append(interval(command, start['cycle'], end['cycle'], budget, wait))
        rows[-1]['command_index'] = index
        rows[-1]['uart_bytes'] = end['tx_bytes'] - start['tx_bytes'] + len(command) + 1
        rows[-1]['uart_115200_ms'] = rows[-1]['uart_bytes'] * 10_000 / 115200
        if command.endswith(' wipe'):
            erases = [e for e in active if e['kind'] == 'flash' and e['opcode'] == 0xd8]
            require(len(erases) == 2, 'wipe erase census')
            for erase, stop in zip(erases, [erases[1], end]):
                rows.append(interval('wipe_erase_envelope', erase['cycle'], stop['cycle'], 3500,
                                     erase['wait_cycles']))
    commit_starts = [e for e in writes if e['address'] == 0x93c and e['value'] == 4]
    acknowledgements = [e for e in writes if e['address'] == 0x93c and e['value'] & 2]
    require(len(commit_starts) == len(acknowledgements) == commits, 'commit bracket census')
    for start, end in zip(commit_starts, acknowledgements):
        active = [e for e in events if start['cycle'] <= e['cycle'] <= end['cycle'] and e['kind'] == 'flash']
        require(sum(e['opcode'] == 0xd8 for e in active) == 1
                and sum(e['opcode'] == 2 for e in active) == pages, 'commit flash sequence')
        rows.append(interval('journal_commit_bracket', start['cycle'], end['cycle'], 8000,
                             sum(e['wait_cycles'] for e in active)))
        erase = next(e for e in active if e['opcode'] == 0xd8)
        program = next(e for e in active if e['opcode'] == 2)
        rows.append(interval('erase_enclosed_to_first_program', erase['cycle'], program['cycle'], 3500,
                             erase['wait_cycles']))
    heartbeats = [e['cycle'] for e in writes if e['address'] == 0x93c and e['value'] == 1]
    require(bool(heartbeats), 'no writer heartbeat')
    gap_start, gap_end = max(zip(heartbeats, heartbeats[1:] + [ends[-1]['cycle']]), key=lambda pair: pair[1] - pair[0])
    gap_wait = sum(max(0, min(gap_end, e['cycle'] + e['wait_cycles']) - max(gap_start, e['cycle']))
                   for e in events if e['kind'] == 'flash')
    rows.append(interval('maximum_heartbeat_gap', gap_start, gap_end, 500, gap_wait))
    rows[-1]['plan'] = media.get('plan', 'all')
    # Report rather than conceal a lapse: measurement completion is independent
    # of the manager's hardware proof and architecture decision.
    heartbeat = dict(plan=media.get('plan', 'all'), start_sys_cycle=gap_start, end_sys_cycle=gap_end,
                     right_censored=gap_end == ends[-1]['cycle'],
                     period_margin_ms=rows[-1]['margin_ms'], liveness_margin_ms=2000 - rows[-1]['ms'])
    add_tick_bounds(rows, events, starts, ends, commands)
    return dict(rows=rows, media=media, events=events, heartbeat_max_gap_ms=rows[-1]['ms'],
                heartbeat_500ms_met=rows[-1]['sys_cycles'] <= 50_000_000, budget_findings=budget_findings(rows),
                heartbeat=heartbeat, liveness=liveness_report(raw))


def service_findings(result: dict, raw: str) -> list[str]:
    """Apply the assigned service rule to opportunities, deadlines and backing."""
    findings = []
    for row in result['rows']:
        if result['media']['plan'] == 'queued-builtins' and 'command_index' in row:
            if row['tick_calls'] == 0:
                findings.append('console line lacks a dispatch opportunity: ' + row['duty'])
        # Ordinary console response time has no protocol deadline. Its shared
        # heartbeat deadline applies to opportunities inside the handler.
        if row['duty'] in ('boot_to_entity_enabled', 'restore_walk',
                           'journal_commit_bracket', 'erase_enclosed_to_first_program',
                           'wipe_erase_envelope', 'maximum_heartbeat_gap'):
            findings.extend(budget_findings([row]))
        if row['duty'] not in ('boot_to_entity_enabled', 'maximum_heartbeat_gap'):
            if row['period_bound_ms'] > 500:
                findings.append('over-budget tick stretch: ' + row['duty'])
    backing = re.search(r'BACKING armed=(\d+) unbacked_cycles=(\d+)', raw)
    require(backing is not None, 'no continuous backing observation')
    if backing[1] != '1' or backing[2] != '0':
        findings.append('continuous backing lost')
    if any(sample['backed'] != 1 for sample in result['liveness']):
        findings.append('console observed backing lost')
    timing = re.search(r'PHY_TIMING transactions=(\d+) publications=(\d+) '
                       r'max_transaction_cycles=(\d+) max_poll_cycles=(\d+) '
                       r'down_edges=(\d+) up_edges=(\d+)', raw)
    require(timing is not None, 'no target MDIO timing')
    result['phy'] = dict(zip(('transactions', 'publications', 'max_transaction_sys_cycles',
                             'max_poll_sys_cycles', 'down_edges', 'up_edges'), map(int, timing.groups())))
    # The 125 ms trigger interval leaves another 125 ms for service jitter.
    # Startup rows compare isolated service cost; actual read gaps include intervening work.
    # Nine reads cover discovery and the longest negotiation fallback. Use
    # the whole observed poll as bookkeeping allowance, counting MDIO twice.
    charge_cycles = int(timing[4]) + 9 * int(timing[3])
    result['phy']['scheduling_charge_sys_cycles'] = charge_cycles
    poll_ms = charge_cycles / 100_000
    for row in result['rows']:
        if row['duty'] in ('boot_to_entity_enabled', 'maximum_heartbeat_gap'):
            continue
        phase_ms = 0 if row['duty'] in ('aem_copy_crc', 'restore_walk') else 125
        publication_ms = phase_ms + row['period_bound_ms'] - 250 + poll_ms
        row['phy_publication_bound_ms'] = publication_ms
        if publication_ms > 250 + 1e-9:
            findings.append('over-budget PHY service stretch: ' + row['duty'])
    reads = [event for event in result.get('events', []) if event['kind'] == 'phy_read']
    if any(right['cycle'] - left['cycle'] > 25_000_000 for left, right in zip(reads, reads[1:])):
        findings.append('PHY publication interval exceeds 250 ms')
    if reads and reads[0]['status'] != 13:
        findings.append('PHY initial gigabit negotiation was not published')
    if reads and reads[-1]['cycle'] >= 265_000_000:
        if not any(event['cycle'] >= 240_000_000 and event['status'] == 11 for event in reads):
            findings.append('PHY did not publish the 100 Mb/s negotiation')
    if result['media']['plan'] in ('queued-input', 'queued-short', 'queued-builtins', 'device-wait'):
        if (int(timing[5]), int(timing[6])) != (1, 1):
            findings.append('PHY cycle did not reach both fabric counters exactly once')
    return findings


def trace_controls() -> int:
    """Pin both clock ratios, marker choices and deadlines against fixed traces."""
    controls = json.loads((HERE / 'oracle.json').read_text())
    count = 0
    for receipt in controls:
        raw = receipt['raw_log']
        require(hashlib.sha256(raw.encode()).hexdigest() == receipt['log_sha256'], 'control trace digest mismatch')
        got = grade(raw, receipt['media'])
        for key in ('rows', 'budget_findings', 'heartbeat', 'liveness'):
            require(got[key] == receipt[key], 'control trace changed: ' + receipt['shape'] + ' ' + key)
            count += 1
    raw = controls[0]['raw_log']

    def delay(match: re.Match) -> str:
        """Delay the final response by 500 ms without changing its markers."""
        return f'EVENT cycle={int(match[1]) + 50_000_000} kind=command_end index=16'

    planted, changed = re.subn(r'EVENT cycle=(\d+) kind=command_end index=16\b', delay, raw)
    require(changed == 1, 'control must alter exactly one response marker')
    require('over-budget duty: milan_status' in grade(planted, controls[0]['media'])['budget_findings'],
            'over-budget UART trace escaped; unrelated heartbeat refusal is insufficient')
    # Bit zero in a combined control word is not the exact heartbeat marker.
    # The recorded plans contain only standalone writes; add a discriminator
    # at the final command start so a permissive bitmask cannot pass unnoticed.
    boundary = re.search(r'^EVENT cycle=(\d+) kind=command_start index=16\b', raw, re.M)
    require(boundary is not None, 'missing control boundary')
    extra = f"EVENT cycle={boundary[1]} kind=write address=2364 value=5\n\n"
    combined = raw[:boundary.start()] + extra + raw[boundary.start():]
    require(grade(combined, controls[0]['media'])['rows'] == controls[0]['rows'],
            'combined control word was accepted as a standalone heartbeat')
    return count + 2


def service_controls() -> int:
    """Pin the new service rule at its boundary and kill independent defects."""
    row = dict(interval('milan_nvm', 1, 80_000_001, 500), period_bound_ms=370)
    raw = ('BACKING armed=1 unbacked_cycles=0\n'
           'PHY_TIMING transactions=8 publications=1 max_transaction_cycles=10 '
           'max_poll_cycles=90 down_edges=1 up_edges=1\n')
    result = dict(rows=[row], media=dict(plan='queued-input'), liveness=[dict(backed=1)])
    require(service_findings(result, raw) == [], 'serviced long command must fit')
    row['period_bound_ms'] = 500.00001
    require(service_findings(result, raw) == ['over-budget tick stretch: milan_nvm',
                                            'over-budget PHY service stretch: milan_nvm'],
            'one cycle past service allowance escaped')
    row['period_bound_ms'] = 374.9982
    require(service_findings(result, raw) == [], 'PHY service boundary changed')
    row['period_bound_ms'] += 0.00001
    require(service_findings(result, raw) == ['over-budget PHY service stretch: milan_nvm'],
            'one cycle past PHY service allowance escaped')
    row['period_bound_ms'] = 370
    require(service_findings(result, raw.replace('unbacked_cycles=0', 'unbacked_cycles=1'))
            == ['continuous backing lost'], 'single-cycle backing loss escaped')
    require(service_findings(result, raw.replace('up_edges=1', 'up_edges=2'))
            == ['PHY cycle did not reach both fabric counters exactly once'],
            'duplicate fabric link edge escaped')
    for shape in SHAPES:
        require(sum(len(command) + 1 for command in command_plan('queued-input', shape)) == 133,
                'queued plan is not the full 133-byte schedule')
    require(sum(len(command) + 1 for command in command_plan('queued-builtins')) >= 133,
            'built-in queue is shorter than the required paste')
    return 9 + publication_controls(result, raw)


def publication_controls(result: dict, raw: str) -> int:
    """Reject false negotiation values and one-cycle publication overruns."""
    result['events'] = [dict(kind='phy_read', cycle=240_000_000, status=13),
                        dict(kind='phy_read', cycle=265_000_000, status=11)]
    require(service_findings(result, raw) == [], '250 ms publication boundary changed')
    result['events'][1]['status'] = 13
    require(service_findings(result, raw) == ['PHY did not publish the 100 Mb/s negotiation'],
            'missing negotiated speed change escaped')
    result['events'][1]['status'] = 11
    result['events'][1]['cycle'] += 1
    require(service_findings(result, raw) == ['PHY publication interval exceeds 250 ms'],
            'one-cycle publication gap escaped')
    result['events'][1]['cycle'] -= 1
    result['events'][0]['status'] = 0
    require(service_findings(result, raw) == ['PHY initial gigabit negotiation was not published'],
            'missing initial negotiated status escaped')
    return 4


def self_test() -> None:
    """A legal boundary passes; one additional system cycle must be refused."""
    count = 0
    row = interval('planted-duty', 1, 50_000_001, 500)
    grade_rows([row])
    count += 1
    try:
        grade_rows([interval('planted-duty', 1, 50_000_002, 500)])
    except RuntimeError as exc:
        require(str(exc) == 'over-budget duty: planted-duty', 'unrelated self-test failure')
        count += 1
    else:
        raise RuntimeError('over-budget duty escaped')
    require(budget_findings([row, interval('planted-duty', 1, 50_000_002, 500)])
            == ['over-budget duty: planted-duty'], 'measurement report lost the budget refusal')
    count += 1
    for raw in ('', 'EVENT cycle=2 kind=start\nEVENT cycle=1 kind=end\n'):
        try:
            read_events(raw)
        except RuntimeError:
            count += 1
            continue
        raise RuntimeError('missing or unordered marker evidence escaped')
    registered = set(re.findall(r'\bdefine_command\s*\(\s*(\w+)\s*,',
                               (ROOT / 'sw/firmware/milan_baremetal/milan_baremetal.c').read_text()))
    require(registered == {command.split()[0] for command in COMMANDS}, 'product dispatch census changed')
    count += 1
    count += trace_controls() + wait_controls() + tick_controls() + service_controls()
    with tempfile.TemporaryDirectory(prefix='fw-service-budget-') as directory:
        executable = Path(directory) / 'flash-test'
        subprocess.run(['c++', '-std=c++17', '-Wall', '-Wextra', '-Werror',
                        '-I' + str(ROOT / 'tb/common'), str(HERE / 'flash_test.cpp'),
                        '-o', str(executable)], check=True)
        subprocess.run([str(executable)], check=True)
    print(f'fw_service_budget_oracle: checks: {count} failures: 0')
    print('PASS: over-budget duty, marker integrity and product dispatch census')


def report_verdict(mutation: str, findings: list[str], record_budget_findings: bool) -> None:
    """Controls must fail their named oracle; ordinary runs retain every finding."""
    if mutation == 'remove-dispatch':
        require('continuous backing lost' in findings, 'dispatch removal escaped backing check')
        print('PASS: dispatch removal caught by continuous backing check')
        return
    if mutation == 'late-sample':
        require('PHY initial gigabit negotiation was not published' in findings,
                'late sampling escaped negotiated-status check')
        print('PASS: late MDIO sampling caught by target negotiation check')
        return
    for finding in findings:
        print('BUDGET FINDING: ' + finding)
    require(record_budget_findings or not findings, 'budget findings require disposition')
    print('PASS: measurement evidence; budget findings: ' + str(len(findings)))


def main() -> None:
    """Run foreground builds outside the checkout; keep receipts separate."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test', action='store_true')
    parser.add_argument('--shape', choices=SHAPES, default=SHAPES[0])
    parser.add_argument('--build-dir', type=Path)
    parser.add_argument('--build-only', action='store_true')
    parser.add_argument('--reuse-build', action='store_true')
    parser.add_argument('--regrade', action='store_true', help='regrade a previously bound log without simulating')
    parser.add_argument('--record-budget-findings', action='store_true',
                        help='record budget refusals as findings; fail on invalid measurement evidence')
    parser.add_argument('--populated', action='store_true')
    parser.add_argument('--enforce-service', action='store_true',
                        help='grade duty tick stretches and continuous backing')
    parser.add_argument('--mutation', choices=('none', 'remove-dispatch', 'no-publish', 'late-sample'), default='none')
    parser.add_argument('--plan', choices=PLANS, default='all')
    parser.add_argument('--device-wait-us', type=int, default=0, help='erase WIP in microseconds')
    parser.add_argument('--program-wait-us', type=int, default=0, help='page-program WIP in microseconds')
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    if args.build_dir is None:
        parser.error('--build-dir is required for measurement')
    if args.mutation == 'remove-dispatch' and args.plan not in ('queued-short', 'queued-builtins'):
        parser.error('dispatch control requires queued-short or queued-builtins')
    if args.mutation != 'none' and not args.enforce_service:
        parser.error('mutation controls require --enforce-service')
    args.build_dir = args.build_dir.resolve()
    if args.regrade:
        require(not args.build_only, '--regrade and --build-only are incompatible')
        args.reuse_build = True
    require(ROOT not in (args.build_dir, *args.build_dir.parents), 'use an external build directory')
    validate_waits(args.device_wait_us, args.program_wait_us)
    args.cpu_hz = CPU_HZ
    args.captures = 2
    args.traffic = 'off'
    from build import build, compile_sim
    if not args.reuse_build:
        spec = build(args)
        compile_sim(args.build_dir, spec)
        spec['build_hashes'] = build_hashes(args.build_dir, spec)
        (args.build_dir / 'service_spec.json').write_text(json.dumps(spec, indent=2) + '\n')
    else:
        spec = json.loads((args.build_dir / 'service_spec.json').read_text())
        require(spec['shape'] == args.shape and spec['cpu_hz'] == CPU_HZ
                and spec['mutation'] == args.mutation, 'build shape/clock/mutation mismatch')
        require(spec.get('build_hashes') == build_hashes(args.build_dir, spec), 'stale or unbound build; rebuild')
    if args.build_only:
        return
    name = f'service-{args.plan}-{int(args.populated)}-{args.device_wait_us}-{args.program_wait_us}'
    hashes = inputs()
    if args.regrade:
        old = json.loads((args.build_dir / (name + '.json')).read_text())
        media = old['media']
        require(old['build_hashes'] == spec['build_hashes'], 'log belongs to a different build')
        require(old['log_sha256'] == hashlib.sha256((args.build_dir / (name + '.log')).read_bytes()).hexdigest(),
                'recorded log changed')
    else:
        media = fixtures(args.build_dir, args.shape, args.populated, args.plan)
    argv = [str(args.build_dir / 'native/Vsim'), str(args.build_dir / 'aem_desc.bin'),
            str(args.build_dir / 'slots.bin'), str(args.build_dir / 'commands.txt'), str(args.device_wait_us),
            str(args.program_wait_us), str(int(args.plan == 'uart-paced'))]
    if not args.regrade:
        with (args.build_dir / (name + '.log')).open('w') as log:
            native = subprocess.run(argv, cwd=args.build_dir / 'gateware', stdout=log,
                                    stderr=subprocess.STDOUT, check=False)
        if args.mutation == 'no-publish':
            raw = (args.build_dir / (name + '.log')).read_text()
            require(native.returncode != 0 and 'missing MDIO/publication evidence' in raw,
                    'missing publisher escaped its named simulation check')
            print('PASS: missing publication caught by target simulation')
            return
        require(native.returncode == 0, 'native simulation failed')
    raw = (args.build_dir / (name + '.log')).read_bytes().decode()
    result = dict(media=media, shape=args.shape, cpu_hz=CPU_HZ, sys_hz=SYS_HZ, device_wait_us=args.device_wait_us,
                  program_wait_us=args.program_wait_us, raw_log=raw,
                  input_hashes=hashes, build_hashes=spec['build_hashes'],
                  log_sha256=hashlib.sha256(raw.encode()).hexdigest())
    # Keep the native evidence bound even if its analysis fails, for regrade.
    (args.build_dir / (name + '.json')).write_text(json.dumps(result, indent=2) + '\n')
    result.update(grade(raw, media))
    if args.enforce_service:
        result['service_findings'] = service_findings(result, raw)
    (args.build_dir / (name + '.json')).write_text(json.dumps(result, indent=2) + '\n')
    require(inputs() == hashes, 'measurement code changed during the run; receipt requires regrade')
    print(json.dumps(result['rows'], indent=2))
    findings = result.get('service_findings', result['budget_findings'])
    report_verdict(args.mutation, findings, args.record_budget_findings)


if __name__ == '__main__':
    main()
