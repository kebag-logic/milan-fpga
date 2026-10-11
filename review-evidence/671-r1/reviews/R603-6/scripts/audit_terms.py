#!/usr/bin/env python3
"""Observe actual refusal tuples and independently check the ruled class matrix."""
import concurrent.futures
import dataclasses
import json
import os
from pathlib import Path
import re
import sys

root, packet = map(lambda x: Path(x).resolve(), sys.argv[1:3])
sys.dont_write_bytecode = True
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
os.environ['TMPDIR'] = str(packet / 'scratch')
sys.path.insert(0, str(root / 'sw/firmware/nvm_hosttest'))
import test_nvm_firmware as t
import read_fault_cases as c

source = t.FIRMWARE.read_text()
anchor = '\treturn rd;\n}\n\n/* Whether two refused reads'
assert source.count(anchor) == 1
trace = ('\tprintf("REVIEW_READ %c %u %u %u %u\\n", slot == NVM_SLOT_A ? \'A\' : \'B\', '
         'rd.vd, (unsigned int)rd.bytes, (unsigned int)rd.digest, (unsigned int)rd.tail);\n')
instrumented = source.replace(anchor, trace + anchor)
shapes = ('endstation_arty_4x4', 'endstation_ax7101_1x1_tdm8', 'endstation_ax7101_8x8')
terms = ('verdict', 'byte count', 'prefix CRC', 'trailer')
seqs = (1, 0x5a5a5, 0x80000000, 0xffffffff)
trace_re = re.compile(r'^REVIEW_READ ([AB]) (\d+) (\d+) (\d+) (\d+)$', re.M)

def shape_run(shape):
    work = packet / 'scratch/term-audit' / shape
    work.mkdir(parents=True, exist_ok=True)
    bench = t.make_bench(root / 'configs' / (shape + '.yaml'), work, instrumented)
    fr = t.fault_run(bench)
    cases = c.fault_cases(t.KLJ2_HDR + (bench.img_len - t.KLJ2_HDR - t.KLJ2_TRAILER)//2)
    assert not c.comparison_findings(source, cases)
    selected = [case for case in cases if c.term_of(case)]
    assert len(selected) == 128
    want = {(term, slot, seq, restart) for term in terms for slot in 'ab'
            for seq in seqs for restart in (False, True)}
    have = {(c.term_of(case), case.valid, case.seq, case.restart) for case in selected if not case.older}
    assert have == want
    observations = []
    with (packet / 'receipts' / ('terms-' + shape + '.log')).open('w') as log:
        for i, case in enumerate(selected):
            casework = work / str(i)
            casework.mkdir(exist_ok=True)
            # Same graders as the standing campaign, with every reboot executed.
            findings = t.grade_fault_case(bench, fr, case, casework, None)
            assert not findings, findings
            # A separate boot/restart exposes the actual read tuples.
            args = ['--slot-a', str(casework / 'rf_a.bin'), '--slot-b', str(casework / 'rf_b.bin')]
            if case.restart:
                args += ['--boot', '--idle-ms', '100', *case.fault, '--restart']
            else:
                args += [*case.fault, '--boot']
            out, state, boot = t.run(bench, *args)
            if case.restart:
                out = out.split('HOST restarting\n', 1)[1].split('HOST restarted\n', 1)[0]
            slot = case.fault[1][0].upper()
            reads = [tuple(map(int, match[1:])) for match in trace_re.findall(out) if match[0] == slot]
            a, b, clean = reads[:3]
            index = terms.index(c.term_of(case))
            assert a[0] != t.VD_OK and b[0] != t.VD_OK and clean[0] == t.VD_OK, (case, reads)
            assert [j for j in range(4) if a[j] != b[j]] == [index], (case, reads)
            expected_reads = (5 if case.restart else 6) + (not case.older)
            actual_reads = state['restart_reads' if case.restart else 'boot_reads']
            assert actual_reads == expected_reads == c.expect(case).reads
            assert 'the writer is HELD' not in out and 'unread=0.' in out
            print('CASE', case.name, file=log)
            print(out, file=log)
            observations.append({'case': dataclasses.asdict(case), 'term': terms[index],
                                 'tuples': [a, b, clean], 'reads': actual_reads,
                                 'full_grader_findings': findings})
        print('PASS: 128 cases; 32 per term; exact tuple isolation; read/hold/record assertions', file=log)
    (packet / 'receipts' / ('terms-' + shape + '.json')).write_text(json.dumps(observations, indent=2)+'\n')
    return shape, len(observations)

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    for shape, count in pool.map(shape_run, shapes):
        print(shape, count, 'PASS', flush=True)
