// SPDX-License-Identifier: CERN-OHL-W-2.0
// Observe the real send_pdu callback. Only this test arm renames the library
// entry point; firmware and its static callback are compiled unchanged.
#pragma once
extern "C" int srp_test_transmit_real(mrp_app*,uint8_t,uint8_t*,size_t,mrp_send_fn,void*);
namespace {
struct SrpCostProbe {
    mbx_model* model=nullptr;
    unsigned calls=0;
    unsigned sends=0;
    uint64_t accesses=0;
    bool pad=false;
};
SrpCostProbe srp_probe;
struct SrpSendProbe { mrp_send_fn send; void* ctx; };
int observed_send(void* ctx,uint8_t port,const uint8_t* pdu,size_t len) {
    auto& probe=*static_cast<SrpSendProbe*>(ctx);
    // Maximum-size legal trailing padding exercises the actual frame copy
    // and the mailbox driver, including its commit.
    std::vector<uint8_t> padded(pdu,pdu+len);
    if (srp_probe.pad) padded.resize(MBX_CH_SRP_MAX_FRAME_BYTES-14u,0);
    const auto before=srp_probe.model->reads+srp_probe.model->writes;
    const int result=probe.send(probe.ctx,port,padded.data(),padded.size());
    const auto accesses=srp_probe.model->reads+srp_probe.model->writes-before;
    EXPECT_EQ(result,0);
    EXPECT_EQ(accesses,2u+MBX_TX_HDR_WORDS+(padded.size()+14u+3u)/4u)
        << "real send callback has only the TX record accesses";
    EXPECT_LE(accesses,SRP_MBX_TX_MAX) << "real send callback maximum";
    srp_probe.accesses+=accesses;
    ++srp_probe.sends;
    return result;
}
} // namespace
extern "C" int mrp_transmit(mrp_app* app,uint8_t port,uint8_t* pdu,size_t capacity,mrp_send_fn send,void* ctx) {
    if (!srp_probe.model) return srp_test_transmit_real(app,port,pdu,capacity,send,ctx);
    ++srp_probe.calls;
    SrpSendProbe probe{send,ctx};
    return srp_test_transmit_real(app,port,pdu,capacity,observed_send,&probe);
}
