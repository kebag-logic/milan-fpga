#!/usr/bin/env python3
"""Add one reviewer assertion to a disposable copy's existing timeout test.
Usage: script SCRATCH_TREE. Never use on the candidate checkout.
The original test expects success for both commands while the face is held.
The added assertion requires the second successful value to have been written.
"""
import sys
from pathlib import Path
p = Path(sys.argv[1])/'sw/firmware/ctrl/test/test_aecp.cpp'
old = 'auto count=far.commits.size();identify[4]=0;receive(24,identify);'
new = old + '''
    EXPECT_EQ(at(taken(0),MBX_FACE_REG_F_ENTITY,MBX_F_ENTITY_IDENTIFY_LSB,8),0u)
        <<"a successful second response must not precede its F value";
'''
s=p.read_text(); assert s.count(old)==1
p.write_text(s.replace(old,new))
