#!/usr/bin/env python3
"""Add one reviewer test to a disposable copy's face tests.
Usage: script SCRATCH_TREE. Never use on the candidate checkout.
A SET_CONTROL (IDENTIFY) whose commit is not acknowledged answers
ENTITY_MISBEHAVING. The test then lets the acknowledgement return and asks
whether the change the core kept, and the datapath then applied, is ever
announced to the other registered controller (FR-CTRL-03: state changes MUST
emit unsolicited responses to registered controllers). It also records what a
GET_CONTROL reports while the commit is held.
"""
import sys
from pathlib import Path
p = Path(sys.argv[1])/'sw/firmware/ctrl/test/test_aecp.cpp'
anchor = "// Each stream's entry goes to its own interface's block; a setting of the\n"
probe = r'''TEST_F(Face, ReviewerProbeALateAcknowledgedChangeIsAnnounced)
{
    receive(36,{},0,CTLR+1);
    const uint32_t before=fabric.tx_sent;
    far.ack=false;Bytes identify=target(26,0,5);identify[4]=255;
    receive(24,identify,AECP_ENTITY_MISBEHAVING);
    auto held=receive(25,target(26,0));
    std::printf("PROBE held: core_identify=%u get_control_identify=%u datapath_identify=%u\n",
        (unsigned)adapter.core.identify,(unsigned)held[42],
        (unsigned)at(taken(0),MBX_FACE_REG_F_ENTITY,MBX_F_ENTITY_IDENTIFY_LSB,8));
    far.ack=true;for(unsigned i=0;i<MBX_N_IF;++i)mbx_model_face_ack(&fabric,i);service(100);
    unsigned notes=0;
    for(uint32_t k=before;k<fabric.tx_sent;++k){auto f=mbx_model_tx_frame(&fabric,k);
        if(f!=nullptr&&f->bytes[14]==0xfb&&get(f->bytes+36,2)==0x8018)++notes;}
    std::printf("PROBE after: datapath_identify=%u owed0=%d unsolicited_set_control=%u\n",
        (unsigned)at(taken(0),MBX_FACE_REG_F_ENTITY,MBX_F_ENTITY_IDENTIFY_LSB,8),(int)face.owed[0],notes);
    EXPECT_EQ(at(taken(0),MBX_FACE_REG_F_ENTITY,MBX_F_ENTITY_IDENTIFY_LSB,8),255u)<<"the change took effect";
    EXPECT_GE(notes,1u)<<"a state change that took effect is announced to registered controllers (FR-CTRL-03)";
}

'''
s = p.read_text(); assert s.count(anchor) == 1
p.write_text(s.replace(anchor, probe + anchor))
