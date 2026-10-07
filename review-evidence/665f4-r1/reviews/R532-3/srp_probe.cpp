// SPDX-License-Identifier: CERN-OHL-W-2.0
// Reviewer scenario probes for PR #690 round 3. Disposable: compiled only in a
// scratch copy of the tree by probe_scenarios.py, never added to the suite.
#include "srp_fixture.hpp"
FW_TALLY_LABEL("reviewer SRP probe");
namespace {
std::vector<uint8_t> talker_value(const msrp_stream_id &sid, const uint8_t da[6], uint16_t vid) {
    std::vector<uint8_t> value(25);
    std::copy(sid.bytes,sid.bytes+8,value.begin());
    std::copy(da,da+6,value.begin()+8);
    wire_put_be(value.data()+14,vid,2);
    wire_put_be(value.data()+16,224,2);
    wire_put_be(value.data()+18,1,2);
    value[20]=0x60;
    return value;
}

// R533-2-F1 root: a binding that JOINS an already-declared StreamID in another
// slot must carry that Applicant, so the original's departure withdraws Ready.
TEST_F(Srp, ProbeJoiningSharedBindingCarriesApplicantWhenOriginalLeaves) {
    settle(); advance(400);
    const msrp_stream_id sid{{2,1,2,3,4,5,6,7}};
    const uint8_t da[2][6]={{0x91,0xe0,0xf0,0,0,9},{0x91,0xe0,0xf0,0,0,10}};
    for(unsigned i=0;i<MBX_N_IF;++i) for(unsigned first : {0u,1u}) {
        SCOPED_TRACE(::testing::Message()<<i<<'/'<<first);
        ASSERT_TRUE(srp_mbx_bind(&adapter,i,first,&sid,da[0],7));
        offer(frame(1,talker_value(sid,da[0],7),1),i); advance(400);
        ASSERT_EQ(adapter.ifs[i].sinks[first].declared,2u);
        // A second, ineligible binding (no matching Talker) joins the StreamID.
        ASSERT_TRUE(srp_mbx_bind(&adapter,i,1-first,&sid,da[1],7));
        ASSERT_TRUE(srp_mbx_bind(&adapter,i,first,nullptr,nullptr,0));
        capture(); model.tx_sent=0; advance(2200); capture();
        bool left=false;
        for(const auto &d:declarations) if(d.interface==i && d.ethertype==0x22ea && d.type==3 &&
            d.value==std::vector<uint8_t>(sid.bytes,sid.bytes+8)) {
            left|=d.event==5; EXPECT_EQ(d.event,5u)<<"no stale Ready after the eligible user leaves";
        }
        EXPECT_TRUE(left)<<"Listener Ready must be withdrawn when only an ineligible binding remains";
        EXPECT_EQ(adapter.ifs[i].sinks[1-first].declared,0u);
        ASSERT_TRUE(srp_mbx_bind(&adapter,i,1-first,nullptr,nullptr,0)); advance(1200);
    }
}

// R532-2-F3 boundary: the last binding on the Domain's own VID leaving must not
// withdraw the SR class VLAN that the Talkers and Domain still need.
TEST_F(Srp, ProbeUnbindingTheLastDomainVidBindingKeepsSrClassVlan) {
    settle(); advance(400);
    const msrp_stream_id sid{{2,1,2,3,4,5,6,7}};
    const uint8_t da[6]={0x91,0xe0,0xf0,0,0,9};
    for(unsigned i=0;i<MBX_N_IF;++i) {
        ASSERT_TRUE(srp_mbx_bind(&adapter,i,0,&sid,da,2));
        offer(frame(1,talker_value(sid,da,2),1),i); advance(1200);
        ASSERT_EQ(adapter.ifs[i].sinks[0].declared,2u);
        ASSERT_TRUE(srp_mbx_bind(&adapter,i,0,nullptr,nullptr,0));
        capture(); model.tx_sent=0; advance(2200); capture();
        bool listener_left=false;
        for(const auto &d:declarations) if(d.interface==i) {
            if(d.ethertype==0x88f5 && d.value==std::vector<uint8_t>({0,2})) {
                EXPECT_NE(d.event,5u)<<"SR class VID 2 membership must survive the unbind";
            }
            if(d.ethertype==0x22ea && d.type==3) { listener_left|=d.event==5; }
        }
        EXPECT_TRUE(listener_left)<<"the unbind itself was serviced";
    }
}

// R533-2-F1 confinement: inheritance is keyed by StreamID. A rebind to a
// StreamID whose Talker is still registered must declare Ready even while an
// unrelated StreamID is Ready on the same VID.
TEST_F(Srp, ProbeRebindToRegisteredStreamDeclaresReadyBesideAnotherReadyStream) {
    settle(); advance(400);
    const msrp_stream_id z{{2,1,2,3,4,5,6,7}};
    const msrp_stream_id y{{2,1,2,3,4,5,6,8}};
    const uint8_t da[6]={0x91,0xe0,0xf0,0,0,9};
    for(unsigned i=0;i<MBX_N_IF;++i) {
        ASSERT_TRUE(srp_mbx_bind(&adapter,i,0,&z,da,7));
        offer(frame(1,talker_value(z,da,7),1),i); advance(400);
        ASSERT_EQ(adapter.ifs[i].sinks[0].declared,2u);
        ASSERT_TRUE(srp_mbx_bind(&adapter,i,0,nullptr,nullptr,0)); advance(400);
        ASSERT_TRUE(srp_mbx_bind(&adapter,i,1,&y,da,7));
        offer(frame(1,talker_value(y,da,7),1),i); advance(400);
        ASSERT_EQ(adapter.ifs[i].sinks[1].declared,2u);
        capture(); model.tx_sent=0;
        ASSERT_TRUE(srp_mbx_bind(&adapter,i,0,&z,da,7)); advance(400); capture();
        bool ready=false;
        for(const auto &d:declarations) if(d.interface==i && d.ethertype==0x22ea && d.type==3 &&
            d.value==std::vector<uint8_t>(z.bytes,z.bytes+8) && d.event!=5) ready|=d.subtype==2;
        EXPECT_TRUE(ready)<<"the rebound StreamID's Talker is registered, so Ready is owed";
        ASSERT_TRUE(srp_mbx_bind(&adapter,i,0,nullptr,nullptr,0));
        ASSERT_TRUE(srp_mbx_bind(&adapter,i,1,nullptr,nullptr,0)); advance(1200);
    }
}
// R533-2-F1 replay: two sinks share a StreamID on VID 2 (destinations ...09 and
// ...0A), the Talker registers for ...09, then sink 0 is rebound to ...0A. No
// binding matches, so the shared Ready must be withdrawn and never renewed.
TEST_F(Srp, ProbeR533OverlappingRebindWithdrawsSharedReady) {
    settle(); advance(400);
    const msrp_stream_id sid{{2,1,2,3,4,5,6,7}};
    const uint8_t da[2][6]={{0x91,0xe0,0xf0,0,0,9},{0x91,0xe0,0xf0,0,0,10}};
    for(unsigned i=0;i<MBX_N_IF;++i) {
        ASSERT_TRUE(srp_mbx_bind(&adapter,i,0,&sid,da[0],2));
        ASSERT_TRUE(srp_mbx_bind(&adapter,i,1,&sid,da[1],2));
        offer(frame(1,talker_value(sid,da[0],2),1),i); advance(400);
        ASSERT_EQ(adapter.ifs[i].sinks[0].declared,2u);
        ASSERT_EQ(adapter.ifs[i].sinks[1].declared,2u);
        ASSERT_TRUE(srp_mbx_bind(&adapter,i,0,&sid,da[1],2));
        capture(); model.tx_sent=0; advance(2200); capture();
        bool left=false;
        for(const auto &d:declarations) if(d.interface==i && d.ethertype==0x22ea && d.type==3) {
            left|=d.event==5; EXPECT_EQ(d.event,5u)<<"no stale shared Ready renewal at "<<d.time_ms;
        }
        EXPECT_TRUE(left);
        ASSERT_TRUE(srp_mbx_bind(&adapter,i,0,nullptr,nullptr,0));
        ASSERT_TRUE(srp_mbx_bind(&adapter,i,1,nullptr,nullptr,0)); advance(1200);
    }
}
} // namespace
