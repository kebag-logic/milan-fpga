#!/usr/bin/env python3
"""Raw transcripts: two different trailer-only refusals, then a clean read."""
from dataclasses import replace
from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root/'sw/firmware/nvm_hosttest'))
import test_nvm_firmware as t
import read_fault_cases as c
run = t.run
def recorded(bench, *args):
    out, state, boot = run(bench, *args)
    # Arguments contain generated file paths; publish role-relative paths.
    print('ARGS', ' '.join(args).replace(str(packet/'scratch'), '<scratch>'))
    print(out)
    return out, state, boot
t.run = recorded
text = t.FIRMWARE.read_text()
assert text.count('a.tail == b.tail;') == 1
for shape in c.PRODUCT_SHAPES:
    work=packet/'scratch'/'trailer-raw'/shape
    bench=t.make_bench(root/'configs'/(shape+'.yaml'),work/'head',text)
    plant=t.replant(bench,work/'omit_tail',text.replace('a.tail == b.tail;','1;'))
    fr=t.fault_run(bench)
    for label, b in [('head',bench),('omit_tail',plant)]:
        for slot in 'ab':
            skip=1 if slot=='a' else 3
            case=c.FaultCase(slot,False,0x5a5a5,('--read-fault',f'{slot}:{b.img_len-1}:{skip}:2:8'),skip,2)
            w=work/label/slot;w.mkdir(parents=True)
            print('CASE',shape,label,slot,'trailer byte',b.img_len-1)
            findings=t.grade_fault_case(b,fr,case,w)
            print('FINDINGS',len(findings))
            for finding in findings: print(finding)
            assert bool(findings)==(label=='omit_tail')
print('PASS head preserves every record; trailer-omission control exposes unsafe refusal and loss')
