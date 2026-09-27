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
SYS_HZ = 100_000_000
# Cover every command registered by the product translation unit, plus
# normal, boundary and refused parameter paths. BIOS maintenance is separate.
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


def inputs() -> dict[str, str]:
    """Hash measurement code and product inputs without recording local paths."""
    files = [ROOT / 'sw/firmware/milan_baremetal/milan_baremetal.c',
             ROOT / 'sw/firmware/milan_baremetal/Makefile', ROOT / 'sw/litex/milan_soc.py']
    files += [ROOT / 'configs' / (s + '.yaml') for s in SHAPES]
    files += sorted((ROOT / 'tb/verilator/nvm_capture_cpu').glob('*.py'))
    files += sorted(p for p in HERE.iterdir() if p.suffix in ('.py', '.cpp', '.hpp'))
    return {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}


def build_hashes(build_dir: Path, spec: dict) -> dict[str, str]:
    """Bind reuse to compiled sources, generated includes, BIOS and executable."""
    files = {Path(p) for p in spec['sources']}
    files.update(build_dir.glob('generated/**/*.svh'))
    files.update(build_dir.glob('gateware/*.init'))
    files.update(build_dir.glob('software/include/generated/*.h'))
    files.update(build_dir / p for p in ('native/Vsim', 'software/bios/bios.bin', 'aem_desc.bin'))
    files.update(HERE / p for p in ('build.py', 'sim_main.cpp', 'flash.hpp'))
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


def fixtures(build_dir: Path, shape_name: str, populated: bool) -> dict:
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
    (build_dir / 'commands.txt').write_text('\n'.join(COMMANDS) + '\n')
    return dict(image_bytes=len(valid), records=len(rows), aem_bytes=len(blob), populated=populated,
                slots_sha256=hashlib.sha256(media).hexdigest())


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
    return dict(duty=name, sys_cycles=cycles, cpu_cycles=(cycles + 1) // 2,
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
    events = read_events(raw)
    starts = [e for e in events if e['kind'] == 'command_start']
    ends = [e for e in events if e['kind'] == 'command_end']
    require([e['index'] for e in starts] == list(range(len(COMMANDS))), 'command start census')
    require([e['index'] for e in ends] == list(range(len(COMMANDS))), 'command end census')
    require('fabric entity enabled' in raw and 'AEM=loaded' in raw, 'boot did not enable verified AEM')
    require('walk done=1 fail=0' in raw, 'restore walk did not complete successfully')
    require(raw.count('acknowledged.') == 2, 'both console commits must be acknowledged')
    require('slot A erased, slot B erased' in raw, 'wipe did not erase both slots')
    require('FAILED' not in raw and 'deferred' not in raw, 'firmware operation failed')
    pages = (media['image_bytes'] + 255) // 256
    require(ends[-1]['erases'] == 4 and ends[-1]['programs'] == 2 * pages
            and ends[-1]['bytes'] == 2 * media['image_bytes'], 'flash operation census')
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
    rows = [interval('boot_to_entity_enabled', 64, enable['cycle'], None),
            interval('aem_copy_crc_enclosed_by_boot', 64, enable['cycle'], None),
            interval('restore_walk', walk_start['cycle'], walk_end['cycle'], 3000)]
    for index, (start, end) in enumerate(zip(starts, ends)):
        require(start['cycle'] < end['cycle'], 'command end precedes start')
        if index:
            require(ends[index - 1]['cycle'] < start['cycle'], 'overlapping command intervals')
        active = [e for e in events if start['cycle'] <= e['cycle'] <= end['cycle']]
        wait = sum(e['wait_cycles'] for e in active if e['kind'] == 'flash')
        command = COMMANDS[index]
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
    require(len(commit_starts) == len(acknowledgements) == 2, 'commit bracket census')
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
    # Report rather than conceal a lapse: measurement completion is independent
    # of the manager's hardware proof and architecture decision.
    return dict(rows=rows, media=media, events=events, heartbeat_max_gap_ms=rows[-1]['ms'],
                heartbeat_500ms_met=rows[-1]['sys_cycles'] <= 50_000_000, budget_findings=budget_findings(rows))


def trace_controls() -> None:
    """Arm the real event-to-budget path with a completed measured trace."""
    receipt = json.loads((ROOT / 'docs/findings/397_SERVICE_BUDGET_1X1.json').read_text())
    raw = receipt['raw_log']
    require(hashlib.sha256(raw.encode()).hexdigest() == receipt['log_sha256'], 'control trace digest mismatch')
    require(not grade(raw, receipt['media'])['budget_findings'], 'unmodified control trace must fit budgets')

    def delay(match: re.Match) -> str:
        """Delay the final response by 500 ms without changing its markers."""
        return f'EVENT cycle={int(match[1]) + 50_000_000} kind=command_end index=16'

    planted, count = re.subn(r'EVENT cycle=(\d+) kind=command_end index=16\b', delay, raw)
    require(count == 1, 'control must alter exactly one response marker')
    require('over-budget duty: milan_status' in grade(planted, receipt['media'])['budget_findings'],
            'over-budget UART trace escaped; unrelated heartbeat refusal is insufficient')


def self_test() -> None:
    """A legal boundary passes; one additional system cycle must be refused."""
    row = interval('planted-duty', 1, 50_000_001, 500)
    grade_rows([row])
    try:
        grade_rows([interval('planted-duty', 1, 50_000_002, 500)])
    except RuntimeError as exc:
        require(str(exc) == 'over-budget duty: planted-duty', 'unrelated self-test failure')
    else:
        raise RuntimeError('over-budget duty escaped')
    require(budget_findings([row, interval('planted-duty', 1, 50_000_002, 500)])
            == ['over-budget duty: planted-duty'], 'measurement report lost the budget refusal')
    for raw in ('', 'EVENT cycle=2 kind=start\nEVENT cycle=1 kind=end\n'):
        try:
            read_events(raw)
        except RuntimeError:
            continue
        raise RuntimeError('missing or unordered marker evidence escaped')
    registered = set(re.findall(r'\bdefine_command\s*\(\s*(\w+)\s*,',
                               (ROOT / 'sw/firmware/milan_baremetal/milan_baremetal.c').read_text()))
    require(registered == {command.split()[0] for command in COMMANDS}, 'product dispatch census changed')
    trace_controls()
    with tempfile.TemporaryDirectory(prefix='fw-service-budget-') as directory:
        executable = Path(directory) / 'flash-test'
        subprocess.run(['c++', '-std=c++17', '-Wall', '-Wextra', '-Werror',
                        '-I' + str(ROOT / 'tb/common'), str(HERE / 'flash_test.cpp'),
                        '-o', str(executable)], check=True)
        subprocess.run([str(executable)], check=True)
    print('fw_service_budget_oracle: checks: 8 failures: 0')
    print('PASS: over-budget duty, marker integrity and product dispatch census')


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
    parser.add_argument('--device-wait-us', type=int, default=0)
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    if args.build_dir is None:
        parser.error('--build-dir is required for measurement')
    args.build_dir = args.build_dir.resolve()
    if args.regrade:
        require(not args.build_only, '--regrade and --build-only are incompatible')
        args.reuse_build = True
    require(ROOT not in (args.build_dir, *args.build_dir.parents), 'use an external build directory')
    require(0 <= args.device_wait_us <= 3_000_000, 'invalid device wait')
    args.cpu_hz = CPU_HZ
    args.captures = 2
    args.traffic = 'off'
    args.mutation = 'none'
    from build import build, compile_sim
    if not args.reuse_build:
        spec = build(args)
        compile_sim(args.build_dir, spec)
        spec['build_hashes'] = build_hashes(args.build_dir, spec)
        (args.build_dir / 'service_spec.json').write_text(json.dumps(spec, indent=2) + '\n')
    else:
        spec = json.loads((args.build_dir / 'service_spec.json').read_text())
        require(spec['shape'] == args.shape and spec['cpu_hz'] == CPU_HZ, 'build shape/clock mismatch')
        require(spec.get('build_hashes') == build_hashes(args.build_dir, spec), 'stale or unbound build; rebuild')
    if args.build_only:
        return
    name = f'service-{int(args.populated)}-{args.device_wait_us}'
    hashes = inputs()
    if args.regrade:
        old = json.loads((args.build_dir / (name + '.json')).read_text())
        media = old['media']
        require(old['build_hashes'] == spec['build_hashes'], 'log belongs to a different build')
        require(old['log_sha256'] == hashlib.sha256((args.build_dir / (name + '.log')).read_bytes()).hexdigest(),
                'recorded log changed')
    else:
        media = fixtures(args.build_dir, args.shape, args.populated)
    argv = [str(args.build_dir / 'native/Vsim'), str(args.build_dir / 'aem_desc.bin'),
            str(args.build_dir / 'slots.bin'), str(args.build_dir / 'commands.txt'), str(args.device_wait_us)]
    if not args.regrade:
        with (args.build_dir / (name + '.log')).open('w') as log:
            subprocess.run(argv, cwd=args.build_dir / 'gateware', stdout=log, stderr=subprocess.STDOUT, check=True)
    raw = (args.build_dir / (name + '.log')).read_bytes().decode()
    result = grade(raw, media)
    result.update(shape=args.shape, cpu_hz=CPU_HZ, sys_hz=SYS_HZ, device_wait_us=args.device_wait_us,
                  input_hashes=hashes, build_hashes=spec['build_hashes'],
                  log_sha256=hashlib.sha256(raw.encode()).hexdigest())
    require(inputs() == hashes, 'measurement code changed during the run')
    (args.build_dir / (name + '.json')).write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result['rows'], indent=2))
    for finding in result['budget_findings']:
        print('BUDGET FINDING: ' + finding)
    require(args.record_budget_findings or not result['budget_findings'], 'budget findings require disposition')
    print('PASS: measurement evidence; budget findings: ' + str(len(result['budget_findings'])))


if __name__ == '__main__':
    main()
