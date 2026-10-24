#!/usr/bin/env python3
"""Independent rational arithmetic and elaboration boundary checks."""
from fractions import Fraction as F
from math import ceil
from pathlib import Path
import os
import subprocess
import sys

repo = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
ps = F(10**9,48000)
def rnd(x):
    return (x.numerator*2+x.denominator)//(2*x.denominator)
for streams, slots, loop_pairs, audio in [(1,8,4,24576000),(8,32,1,98304000)]:
    marker = rnd(F(256*10**9,slots*32*48000))+rnd(F(10**9,audio))+90
    age = ceil(F(50_000_000,48000))+1
    walk = 4+loop_pairs+26*(4*streams-1)
    pipe = 4+(3 if streams>1 else 0)+24+30-1
    late = marker-int(ps)+(age+walk+pipe)*20
    delay = ceil(F(late,1)/ps)
    tc_late = marker+20+9*20
    tc = ceil(F(tc_late,1)/ps)
    print(f'{streams}x{streams}: marker={marker}; age={age}; walk={walk}; pipe={pipe}; late={late}; delay_periods={delay}; lead={ceil((6+delay)*ps)}; TC_periods={tc}; TC={ceil(tc*ps)}')
    print(f'  AAF spare={ceil(delay*ps)-late}; CRF spare={ceil(tc*ps)-tc_late}')
    max_frame = (1522+8+12)*8 # one VLAN frame, FCS included, preamble and IFG, 1 Gbit/s
    print(f'  One maximum wire frame including preamble/IFG={max_frame} ns; individually fits both spares: {max_frame < min(ceil(delay*ps)-late,ceil(tc*ps)-tc_late)}')
    assert delay==2 and tc==(2 if streams==1 else 1)

print('Startup observed lead=2059807 ns; five later events add ceil(5 Ps)=104167 ns')
print('Conservative 1x1 startup margin from stated queue bound:',2656119-2059807-ceil(5*ps),'ns')
verilator = os.environ.get('REVIEW_VERILATOR',os.environ.get('VERILATOR','verilator'))
for label,late,expected in [('exact_125us',123860,0),('past_125us',123861,1)]:
    cmd=[verilator,'--lint-only','-Wno-fatal','-Werror-USERERROR','--top-module','KL_aaf_packetizer','-GLEAD_P=1','-GIN_LATE_NS_P='+str(late),str(repo/'hdl/ieee1722/aaf/KL_aaf_packetizer.sv')]
    result=subprocess.run(cmd,capture_output=True,text=True,cwd=packet/'scratch')
    (packet/f'guard-{label}.log').write_text(result.stdout+result.stderr)
    print(label, 'returncode=',result.returncode)
    assert (result.returncode!=0)==bool(expected)
    if expected: assert 'exceeds the 0 to 125 us' in result.stderr
print('PASS: both shapes and the inclusive 125 us elaboration boundary')
