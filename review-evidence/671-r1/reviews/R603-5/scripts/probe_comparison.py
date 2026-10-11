#!/usr/bin/env python3
"""Check refused-read comparison and regression sensitivity in disposable copies."""
import argparse
from dataclasses import replace
import json
import os
from pathlib import Path
import sys
import time

p = argparse.ArgumentParser()
p.add_argument('root', type=Path)
p.add_argument('--jobs', type=int, default=4)
a = p.parse_args()
packet = Path(__file__).resolve().parents[1]
os.environ['TMPDIR'] = str(packet / 'scratch')
sys.path.insert(0, str(a.root / 'sw/firmware/nvm_hosttest'))
import test_nvm_firmware as t
import read_fault_cases as c

source = t.FIRMWARE.read_text()
old = 'a.tail == b.tail;'
assert source.count(old) == 1
omit_tail = source.replace(old, '1;')
result = []
begin = time.monotonic()
for shape in ('endstation_arty_4x4', *c.PRODUCT_SHAPES):
    work = packet / 'scratch' / 'comparison' / shape
    work.mkdir(parents=True, exist_ok=True)
    base = replace(t.make_bench(a.root / 'configs' / (shape + '.yaml'), work / 'base', source), jobs=a.jobs)
    mutants = {'omit_tail': t.replant(base, work / 'omit_tail', omit_tail)}
    pairs, words = c.READ_FAULT_MUTATIONS['r_digest_with_trailer']
    text = source
    for before, after in pairs:
        assert text.count(before) == 1
        text = text.replace(before, after)
    mutants['inclusive_crc'] = t.replant(base, work / 'inclusive_crc', text)
    fr = t.fault_run(base)
    body = t.KLJ2_HDR + (base.img_len - t.KLJ2_HDR - t.KLJ2_TRAILER) // 2
    cases = c.fault_cases(body)
    coverage = {(case.valid, case.restart, case.seq) for case in cases
                if not case.older and case.fault[0] == '--read-sealed'
                and case.fault[1].startswith(case.valid + ':')
                and c.expect(case).judgement['ab'.index(case.valid)] == 'ffc'}
    expected = {(slot, restart, seq) for slot in 'ab' for restart in (False, True) for seq in c.FAULT_SEQS}
    assert coverage == expected
    print(shape, 'standing_cases', len(cases), 'sealed_core_combinations', len(coverage), flush=True)
    for label, bench in [('head', base), *mutants.items()]:
        focused = []
        for restart in (False, True):
            for slot in 'ab':
                for seq in c.FAULT_SEQS:
                    # Global mapped-read count: cold AEM read, A judgement,
                    # or two blank A reads before B judgement.
                    skip = (0 if restart else 1) + (2 if slot == 'b' else 0)
                    for kind, off, option in [('sealed_entity',20,'--read-sealed'),
                                               ('sealed_body',body,'--read-sealed'),
                                               ('trailer_only',base.img_len-1,'--read-fault')]:
                        case = c.FaultCase(slot, False, seq,
                            (option, f'{slot}:{off}:{skip}:2:8'), skip, 2, restart)
                        out = work / label / f'{slot}-{restart}-{seq}-{kind}'
                        out.mkdir(parents=True, exist_ok=True)
                        findings = t.grade_fault_case(bench, fr, case, out)
                        focused.append({'kind':kind,'slot':slot,'restart':restart,'seq':seq,'findings':findings})
        if label == 'head':
            assert not any(x['findings'] for x in focused)
        elif label == 'inclusive_crc':
            assert all(any(words in f for f in x['findings']) for x in focused if x['kind'].startswith('sealed'))
        else:
            assert all(any('on reads that returned different bytes' in f for f in x['findings'])
                       for x in focused if x['kind'] == 'trailer_only')
        print(shape, label, 'focused_cases',len(focused),'failing_cases',sum(bool(x['findings']) for x in focused),flush=True)
        standing = t.grade(bench) if label == 'omit_tail' else None
        if standing is not None:
            print(shape, label, 'standing_findings',len(standing),flush=True)
        result.append({'shape':shape,'variant':label,'focused':focused,'standing_findings':standing})
(packet/'receipts/comparison.json').write_text(json.dumps(result,indent=2)+'\n')
print('Comparison probe completed in',round(time.monotonic()-begin,3),'seconds',flush=True)
