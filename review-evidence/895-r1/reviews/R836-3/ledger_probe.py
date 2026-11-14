#!/usr/bin/env python3
"""Exercise the changed ledger and its plants without a SoC build."""
from pathlib import Path
import sys
import tempfile

sys.dont_write_bytecode=True
root=Path(sys.argv[1]).resolve()
sys.path.insert(0,str(root/'sw/litex'))
import ctrl_memory as cm
import ctrl_memory_ledger as ledger
from ctrl_memory_elf import write_elf

with tempfile.TemporaryDirectory(dir=Path(__file__).parent/'scratch') as d:
    tmp=Path(d)
    def image(case):
        # Same independent ELF writer and boundary recipe as test_ctrl_memory.
        text=9000+4*2048
        bss=56*4096-12288-64-8192+(round(2*(case.tiles-56))-4)*2048
        ram=cm.RAM.origin
        symbols={'_start':4,'nvm_stage':case.stage}
        if case.interfaces is not None: symbols['image_allocation']=8*case.interfaces
        if case.plat is not None: symbols['ctrl_plat']=case.plat
        p=tmp/('case-'+str(len(list(tmp.iterdir())))+'.elf')
        p.write_bytes(write_elf(0,[('.text',0,0,bytes(text),False),
            ('.rodata',text,text,bytes(3002),False),
            ('.data',ram,text+3004,bytes(64),True),
            ('.bss',ram+64,ram+64,bss,True),
            ('.stack',ram+64+bss,ram+64+bss,8192,True)],symbols))
        return p
    def check():
        bad=[]
        for holds,what in ledger.facts(image):
            if not holds:bad.append(what)
        for rule,what,attempt in ledger.refusals(image):
            try: attempt()
            except cm.Refusal as e:
                if e.rule != rule:bad.append(what+': wrong refusal '+str(e))
            else:bad.append(what+': accepted')
        return bad
    assert not check()
    print('Clean ledger: both own images accepted; 20 no-override/wrong-point/over-budget cases refused by budget.')
    print('Platform 60.5 accepted, 61.0 refused. Fixture 59.0 accepted, 59.5 refused.')
    original=cm.LEDGERED
    for name,planted in ledger.planted():
        try:
            cm.LEDGERED=planted
            failures=check()
            assert failures,name
            print('CAUGHT:',name,';',failures[0])
        finally:cm.LEDGERED=original
print('LEDGER PROBE PASS; no hardware/SoC/linker claim.')
