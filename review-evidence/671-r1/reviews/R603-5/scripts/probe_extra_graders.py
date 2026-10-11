#!/usr/bin/env python3
"""Check the command-line gate's extra graders on the trailer omission."""
from pathlib import Path
import sys
root=Path(sys.argv[1]).resolve()
packet=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root/'sw/firmware/nvm_hosttest'))
import test_nvm_firmware as t
import test_disabled_writer as disabled
import test_boot_walk as bootwalk
text=t.FIRMWARE.read_text()
assert text.count('a.tail == b.tail;')==1
text=text.replace('a.tail == b.tail;','1;')
for name in ('endstation_arty_4x4','endstation_ax7101_1x1_tdm8','endstation_ax7101_8x8'):
    cfg=root/'configs'/(name+'.yaml')
    work=packet/'scratch'/'extra-graders'/name
    bench=t.make_bench(cfg,work/'bench',text)
    findings=disabled.grade(cfg,work/'disabled',text)
    findings+=bootwalk.grade(cfg,work/'boot-walk',text,bench)
    disabled.check_link_guard(bench)
    print(name,'trailer-omission extra grader findings',len(findings))
    assert not findings
print('PASS: the command-line gate extra graders also miss the trailer omission')
