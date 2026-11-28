# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Verify text receipt parts and reproduce native service grades from extracts.

Usage: python3 receipt_regrade.py PACKET [--case VARIANT/GROUP]
The packet's census.json lists case manifests. Each manifest binds the full
local log's size and hash, the extracted observations, the scenario, the
original grade and any saved-state journal. Parts are text, below 190 KB, or
in a compact census extract (census_extract.py) at most the part_limit its
census.json states, never 15 MB.
The full-log hash is provenance; the extract alone cannot prove omitted bytes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import tempfile
from pathlib import Path

import grade
import scenario
import shape_costs


def sha(data: bytes) -> str:
    """SHA256 of exactly the bytes named by a receipt."""
    return hashlib.sha256(data).hexdigest()


#: A part's size limit: below 190 KB in a packet, at most 15 MB in a compact census extract whose census.json states
#: its own part_limit (census_extract.py).
PART_LIMIT, EXTRACT_PART_LIMIT = 190_000, 15_000_000


def read_parts(directory: Path, record: dict, limit: int = PART_LIMIT) -> bytes:
    """Reassemble numbered text parts, checking each and the whole."""
    chunks = []
    for part in record['parts']:
        path = directory / part['file']
        if not path.resolve().is_relative_to(directory.resolve()):
            raise ValueError('receipt part escapes its directory')
        data = path.read_bytes()
        if len(data) >= limit or len(data) != part['bytes'] or sha(data) != part['sha256']:
            raise ValueError(f'part integrity failure: {part["file"]}')
        data.decode('utf-8')
        chunks.append(data)
    data = b''.join(chunks)
    if len(data) != record['bytes'] or sha(data) != record['sha256']:
        raise ValueError('whole receipt integrity failure')
    return data


def group_from(data: dict) -> scenario.Group:
    """Restore the scenario's typed probes from its JSON record."""
    fields = dict(data)
    probes = []
    for row in fields.pop('probes'):
        row = dict(row)
        row['recipients'] = tuple(tuple(value) for value in row['recipients'])
        row['owed'] = tuple(row['owed'])
        probes.append(scenario.Probe(**row))
    return scenario.Group(**fields, probes=probes)


def regrade(path: Path, staged: Path | None = None, limit: int = PART_LIMIT) -> dict:
    """Reproduce one complete original grade from its primary observations."""
    manifest = json.loads(path.read_text())
    directory = path.parent
    group = group_from(json.loads(read_parts(directory, manifest['group'], limit)))
    script = read_parts(directory, manifest['stimulus'], limit).decode()
    if group.script() != script:
        raise ValueError('scenario differs from the recorded stimulus')
    text = read_parts(directory, manifest['extract'], limit).decode()
    expected = json.loads(read_parts(directory, manifest['grade'], limit))
    with tempfile.TemporaryDirectory(prefix='receipt-') as tmp:
        journal = None
        if manifest.get('journal'):
            journal = Path(tmp) / 'journal.bin'
            journal.write_bytes(bytes.fromhex(read_parts(directory, manifest['journal'], limit).decode()))
        got = grade.grade(text, group, manifest['sys_hz'], manifest['cpu_hz'],
                          shape_costs.Shape(*manifest['shape']), journal)
    if json.loads(json.dumps(got)) != expected:
        raise ValueError(f'grade differs: {path.parent.name}')
    if manifest['native_status'] != 0:
        raise ValueError('native execution failed')
    if staged is not None:
        staged.mkdir(parents=True, exist_ok=True)
        (staged / f'{group.name}.log').write_text(text)
        (staged / f'{group.name}.json').write_text(json.dumps(got))
    return got


def qualify(packet: Path, staged: Path, results: list[dict], limit: int = PART_LIMIT) -> None:
    """Reapply the cross-case costs, record classes, ledger and owner bounds."""
    import arty_grade
    import declaring_outputs
    import egress_ledger
    import kept_grade
    import long_notice
    import record_classes
    import run
    # run.py's disposition of #969's registrations, over the staged srp-kept and srp-bound extracts: their owed STATED
    # and SHARE lines fail nothing while kept_grade's conditions hold, and each breach of one is a finding.
    owed = kept_grade.Disposition(results, staged / 'none', dict(
        shape='endstation_arty_current', interfaces=1, variant='none', sys_hz=80_000_000, cpu_hz=80_000_000))
    found = (owed.shares(run.share_misses(results)) + owed.stated(run.stated_misses(results))
             + run.save_misses(results) + run.burst_misses(results)
             + run.notice_misses(results, 1) + long_notice.missing(results))
    for line in owed.owed:
        print('OWED', line)
    legs, instances = [], []
    for directory in sorted(staged.iterdir()):
        spec = dict(shape='endstation_arty_current', interfaces=1, variant=directory.name,
                    sys_hz=80_000_000, cpu_hz=80_000_000)
        (directory / 'build.json').write_text(json.dumps(spec))
        legs.append(record_classes.read_leg(directory)[0])
        instances.extend(egress_ledger.from_results(directory))
        groups = [group_from(json.loads(read_parts(path.parent, json.loads(path.read_text())['group'], limit)))
                  for path in sorted((packet / 'census' / directory.name).glob('*/manifest.json'))]
        found.extend(declaring_outputs.findings(spec, directory, groups))
        found.extend(line for group in groups for line in run.unstated(group))
    arm = {'arty-1x1': next(sorted(leg.groups) for leg in legs if leg.variant == 'none')}
    failed, reported = record_classes.findings(legs, arm)
    found.extend(failed)
    found.extend(egress_ledger.findings(instances, 'arty-1x1'))
    for line in reported:
        print('REPORTED', line)
    print('\n'.join(egress_ledger.table(instances, 'arty-1x1')))
    model, failed = arty_grade.inspect()
    found.extend(failed)
    original = json.loads((packet / 'published-qualification.json').read_text())
    if model != original['model'] or len(results) != original['groups']:
        found.append('owner model or case count differs from the published qualification')
    for line in found:
        print('REFUSED', line)
    print('OWNER', json.dumps(model, sort_keys=True))
    if found:
        raise ValueError('cross-case qualification failed')
    print('RESULT: PASS cross-case costs, record classes, held-egress ledger and owner bounds')


def timing(packet: Path, index: Path) -> None:
    """Regrade every setup/hold corner, including rounded-zero hold failures."""
    sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'scripts'))
    from area_baseline import parse_timing
    candidates: dict[str, list[dict]] = {}
    for row in json.loads(index.read_text()):
        path = packet / row['manifest']
        if sha(path.read_bytes()) != row['sha256']:
            raise ValueError('timing manifest integrity failure')
        manifest = json.loads(path.read_text())
        data = read_parts(path.parent, manifest['published'])
        with tempfile.TemporaryDirectory(prefix='timing-') as tmp:
            report = Path(tmp) / 'timing.rpt'
            report.write_bytes(data)
            result = parse_timing(report)
        match = re.search(r'WNS\(ns\).*?\n\s*-+.*?\n\s*[-\d.]+\s+[-\d.]+\s+\d+\s+'
                          r'\d+\s+[-\d.]+\s+[-\d.]+\s+(\d+)\s+(\d+)', data.decode(), re.S)
        if not result or match is None:
            raise ValueError('missing setup/hold summary')
        result['failing_hold_endpoints'] = int(match[1])
        result['pass'] = (result['wns'] >= 0.030 and result['whs'] >= 0
                          and result['failing_endpoints'] == 0 and int(match[1]) == 0)
        candidates.setdefault(path.parent.name, []).append(result)
        print(f'{index.stem} {path.name}: {json.dumps(result, sort_keys=True)}')
    if any(len(rows) != 4 for rows in candidates.values()):
        raise ValueError('each directive needs four corner reports')
    passed = [(min(r['wns'] for r in rows), min(r['whs'] for r in rows), name)
              for name, rows in candidates.items() if all(r['pass'] for r in rows)]
    if not passed:
        raise ValueError('no directive meets every signoff floor')
    print(f'{index.stem} selected: {max(passed)[2]}')


def main() -> int:
    """Check every case and report exact grade equality."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('packet', type=Path)
    parser.add_argument('--case')
    parser.add_argument('--timing-only', action='store_true')
    args = parser.parse_args()
    if args.case is None:
        for index in sorted(args.packet.glob('timing-*.json')):
            timing(args.packet, index)
    if args.timing_only:
        return 0
    census = json.loads((args.packet / 'census.json').read_text())
    # A compact extract states its parts' largest size; a part reaching the limit is refused (read_parts).
    limit = min(census['part_limit'] + 1, EXTRACT_PART_LIMIT) if 'part_limit' in census else PART_LIMIT
    rows = [r for r in census['cases'] if args.case is None or r['case'] == args.case]
    if not rows:
        parser.error('no selected cases')
    worst, results = 0, []
    with tempfile.TemporaryDirectory(prefix='receipt-census-') as tmp:
        staged = Path(tmp)
        for row in rows:
            path = args.packet / row['manifest']
            if sha(path.read_bytes()) != row['sha256']:
                raise ValueError(f'manifest integrity failure: {row["case"]}')
            got = regrade(path, staged / row['case'].split('/')[0] if args.case is None else None, limit)
            results.append(got)
            worst = max(worst, got['passes']['worst']['cycles'])
            print(f'PASS {row["case"]}: complete grade reproduced', flush=True)
        if args.case is None:
            qualify(args.packet, staged, results, limit)
    print(f'RESULT: PASS cases={len(rows)} worst_pass_cycles={worst}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
