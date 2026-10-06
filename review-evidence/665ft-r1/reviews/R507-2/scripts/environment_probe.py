#!/usr/bin/env python3
"""Prove a parent negative filter cannot remove the new P9 test."""
import os
from pathlib import Path
import sys

root,packet=map(lambda p:Path(p).resolve(),sys.argv[1:3])
sys.path.insert(0,str(root/'sw/firmware/gtest'))
import fw_gtest
import suite_tally

exe=packet/'scratch/ctrl/checkout/test_port_loop'
r=fw_gtest.run([str(exe)],env=dict(os.environ,GTEST_FILTER='-Pool.P9*',GTEST_REPEAT='0'))
print(r.stdout)
print(r.stderr)
checks,failures,*_=suite_tally.scan(r.stdout+r.stderr)
assert r.returncode==0 and checks==30 and failures==0
assert '[ RUN      ] Pool.P9AFreeListShorterThanItsCountIsExhausted' in r.stdout
print('negative GTEST_FILTER and zero GTEST_REPEAT dropped; P9 and all 30 port tests ran: PASS')
