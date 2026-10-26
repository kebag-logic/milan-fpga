#!/usr/bin/env python3
"""Focused real-CPU probes of fan-out completion and changed runtime ROM."""
import concurrent.futures
import json
from pathlib import Path
import sys
import run_review as review
sys.path.insert(0, str(review.HARNESS))
import grade
import scenario
import build

def fanout():
    spec = json.loads((review.SCRATCH / 'A8/build.json').read_text())
    p = scenario.point('8x8', spec)
    g = scenario.Group('review-fanout')
    scenario.ready(g, p, link=False)
    ch = scenario.CH['aecp']
    for i in range(2):
        cmd = scenario.f.aem_command(scenario.f.Aem(p.entity_id, scenario.CTL1,
                  scenario.CTL_MAC, p.mac, 0x7900 + i), 0x24, bytes(4))
        g.add(f'frame {i} {cmd.hex()}', f'wait tx {ch} 1 within {50 * scenario.MS}',
              f'wait cycles {10 * scenario.MS}')
    cmd = scenario.f.aem_command(scenario.f.Aem(p.entity_id, scenario.CTL2,
            scenario.CTL_MAC, p.mac, 0x7902), 0x10, bytes(8) + b'review value'.ljust(64, b'\0'))
    g.probe(scenario.Probe('review.fanout.if0', 'two-interface SET_NAME fan-out', 'notify',
             f'rxc:{ch}', [f'resp:{ch}:7902', f'notify:{ch}']),
             f'frame 0 {cmd.hex()}', wait=f'tx {ch} 3 within {100 * scenario.MS}',
             settle=f'cycles {30 * scenario.MS}')
    script = review.SCRATCH / 'fanout.txt'
    script.write_text(g.script())
    rc = review.run('fanout-native', [str(review.SCRATCH / 'A8/native/Vsim'), str(script), '-'],
                    review.SCRATCH / 'A8/gateware')
    assert rc == 0
    text = (review.SCRATCH / 'fanout-native.raw.log').read_text()
    result = grade.grade(text, g, 100000000, 50000000)
    row = result['probes'][0]
    parsed = grade.parse(text, 100000000, 50000000)
    frames = [{'cycle': c, 'interface': i, 'controller': frame[26:34].hex()}
              for c, channel, i, frame in parsed.tx if c >= row['start_sys'] and channel == ch
              and len(frame) > 37 and frame[36] & 0x80]
    assert len(frames) == 2 and frames[-1]['cycle'] > row['end_sys']
    result['all_required_recipients'] = frames
    result['actual_last_commit_ms'] = (frames[-1]['cycle'] - row['start_sys']) / 100000
    (review.PACKET / 'native-fanout.json').write_text(json.dumps(result, indent=2) + '\n')
    return rc

def rom():
    folder = review.SCRATCH / 'reuse-probe'
    build.reused(folder)
    script = review.SCRATCH / 'rom-probe.txt'
    script.write_text('wait ms 30\nend\n')
    rc = review.run('changed-rom-native', [str(folder / 'native/Vsim'), str(script), '-'], folder / 'gateware')
    assert rc == 0
    text = (review.SCRATCH / 'changed-rom-native.raw.log').read_text()
    parsed = grade.parse(text, 100000000, 50000000)
    assert parsed.summary['passes'] == '0'
    (review.PACKET / 'changed-rom-native.json').write_text(json.dumps({
        'reuse_accepted': True, 'native_returncode': rc,
        'summary': parsed.summary, 'code': parsed.code,
        'mutation': 'First ROM instruction replaced with jal zero,0; native model unchanged'}, indent=2) + '\n')
    return rc

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    jobs = [pool.submit(fanout), pool.submit(rom)]
    raise SystemExit(bool(any(job.result() for job in jobs)))
