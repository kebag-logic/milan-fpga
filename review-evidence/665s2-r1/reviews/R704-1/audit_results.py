#!/usr/bin/env python3
"""Recompute reported figures and audit actual admitted traffic from raw receipts."""
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import sys

root = Path(os.environ['REVIEW_ROOT'])
packet = Path(os.environ['REVIEW_PACKET'])
scratch = packet / 'scratch'
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_budget'))
import grade
import scenario

published = scratch / 'published/review-evidence/665s2-r1/author/receipts'
out = {}
for arm, point, reference in [('A1', '1x1', 'f1'), ('A8', '8x8', 'f8')]:
    spec = json.loads((scratch / arm / 'build.json').read_text())
    old = json.loads((published / 'builds' / (reference + '-build.json')).read_text())
    build_equal = {key: spec[key] == old[key] for key in ('sys_hz', 'cpu_hz', 'vexii_args',
                    'vexii_soc_args', 'memory_regions', 'cpu_memory_regions', 'ctrl_plan')}
    build_equal['elf_sha256'] = spec['inputs']['ctrl_app.elf'] == old['inputs']['ctrl_app.elf']
    p = scenario.point(point, spec)
    groups = scenario.all_groups(p, spec)
    grades, loads, comparisons, notifications = {}, {}, {}, {}
    stats = {}
    for group in groups:
        path = scratch / arm / 'results' / (group.name + '.log')
        if not path.exists() or 'RESULT: PASS' not in path.read_text():
            continue
        text = path.read_text()
        result = grade.grade(text, group, spec['sys_hz'], spec['cpu_hz'])
        grades[group.name] = result
        prev_path = published / arm / (group.name + '.json')
        if prev_path.exists():
            prev = json.loads(prev_path.read_text())
            comparisons[group.name] = {'probes_exact': result['probes'] == prev['probes'],
                                       'passes_exact': result['passes'] == prev['passes']}
        parsed = grade.parse(text, spec['sys_hz'], spec['cpu_hz'])
        marks = {n: c for c, n in parsed.marks}
        if 'composed' in marks:
            start, end = marks['composed'], marks['composed_end']
            loads[group.name] = {name: sum(start <= c < end and ch == n for c, ch, i, tag in parsed.rxc)
                                  for name, n in scenario.CH.items()}
        if group.name == 'aecp':
            for row in result['probes']:
                if 'set_name' not in row['probe']:
                    continue
                start = row['start_sys']
                end = min((c for c, n in parsed.marks if c > marks[row['probe']]), default=1 << 62)
                sent = [{'cycle': c, 'interface': i, 'controller': fr[26:34].hex(),
                         'command': int.from_bytes(fr[36:38], 'big') & 0x7fff,
                         'unsolicited': bool(fr[36] & 0x80)}
                        for c, ch, i, fr in parsed.tx if start <= c < end and ch == scenario.CH['aecp']
                        and len(fr) > 37 and fr[14] == 0xfb]
                last = max(x['cycle'] for x in sent if x['unsolicited'])
                notifications[row['probe']] = {'graded_start': start, 'graded_end': row['end_sys'],
                    'graded_ms': row['ms'], 'last_notification_ms': (last - start) / 100000,
                    'frames': sent}
        if group.name == 'aecp':
            stats['descriptor_memset_cycles'] = [r.get('pass_modules', {}).get('rt_memset') for r in result['probes']
                                                  if 'read_descriptor' in r['probe']]
        if group.name == 'backlog':
            summary = result['summary']
            stats['access_summary'] = {k: v for k, v in summary.items()
                                       if k in ['mbx_read', 'mbx_write', 'fetch_rom', 'load_flash']}
    worst = max((r['passes']['worst']['cycles'], g) for g, r in grades.items() if r['passes']['worst'])
    composed = max((r['passes']['composed']['cycles'], g) for g, r in grades.items() if r['passes']['composed'])
    out[arm] = {'build_equal': build_equal, 'elf_sha256': spec['inputs']['ctrl_app.elf'],
                'comparisons': comparisons, 'worst': worst, 'composed': composed,
                'backlog': {g: r['probes'] for g, r in grades.items() if g.startswith('backlog')},
                'actual_admitted_records': loads, 'notifications': notifications, 'costs': stats,
                'groups_completed': sorted(grades)}
(packet / 'measurement-audit.json').write_text(json.dumps(out, indent=2) + '\n')
for arm, data in out.items():
    print(arm, 'worst', data['worst'], 'composed', data['composed'])
    print('admitted', data['actual_admitted_records'])
    print('comparisons', data['comparisons'])
    print('notification checks', data['notifications'])
