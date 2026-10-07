#include <gtest/gtest.h>
#include "acmp_fake.hpp"
#include "fw_gtest.hpp"
using namespace acmp_test;
FW_TALLY_LABEL("R531 accepted-send deadline probes");
namespace {
unsigned send_ms;
std::uint32_t last_send;
bool elapsed_send(void* ctx, unsigned iface, const std::uint8_t* frame, std::size_t len) {
    bool ok=f_send(ctx,iface,frame,len);
    if(ok && (frame[15]&15)==0) { fk.now+=send_ms; last_send=fk.now; }
    return ok;
}
struct Rig {
    acmp a{}; acmp_config cfg{}; acmp_ports ports=kPorts;
    Rig() {
        fk=Fake{}; fk.now=1000; send_ms=0; last_send=0;
        cfg.entity_id=kOwn; cfg.n_interfaces=1; cfg.n_sinks=1; cfg.mac[0]=kMac0;
        ports.send=elapsed_send;
        EXPECT_TRUE(acmp_init(&a,&cfg,&ports,&kEnv));
    }
    void bind() {
        Pdu cmd{}; cmd.msg=6; cmd.controller=kCtl1; cmd.talker=kTkA;
        cmd.listener=kOwn; cmd.talker_uid=1;
        auto frame=acmpdu(cmd); acmp_rx(&a,0,frame.data(),frame.size());
    }
};
TEST(ReviewerTimers, InitialImmediateSendStartsAtAcceptance) {
    Rig r; send_ms=5; r.bind();
    ASSERT_EQ(last_send,1005u);
    EXPECT_EQ(r.a.sinks[0].timer_deadline,last_send+200u)
        << "initial command must receive 200 ms after accepted send";
}
TEST(ReviewerTimers, DuplicateImmediateSendStartsAtAcceptance) {
    Rig r; r.bind(); fk.now=r.a.sinks[0].timer_deadline; send_ms=5;
    acmp_timer_expired(&r.a,0);
    ASSERT_EQ(last_send,1205u);
    EXPECT_EQ(r.a.sinks[0].timer_deadline,last_send+200u)
        << "duplicate must receive 200 ms after accepted send";
    fk.now=last_send+199u; acmp_timer_expired(&r.a,0);
    EXPECT_EQ(r.a.sinks[0].state,ACMP_PRB_W_RESP2)
        << "199 ms after duplicate acceptance is not a timeout";
    Pdu response{}; const auto& sink=r.a.sinks[0];
    response.msg=1; response.controller=sink.probe_controller; response.talker=sink.probe_talker;
    response.listener=kOwn; response.talker_uid=sink.probe_talker_uid; response.seq=sink.probe_seq;
    response.stream_id=kSid; response.dest_mac=kDa; response.vlan=2;
    auto frame=acmpdu(response); acmp_rx(&r.a,0,frame.data(),frame.size());
    EXPECT_EQ(r.a.sinks[0].state,ACMP_SETTLED_NO_RSV)
        << "matching success 199 ms after duplicate acceptance must settle";
}
TEST(ReviewerTimers, DeferredSendUsesFreshPostAcceptanceClock) {
    Rig r; fk.room=false; r.bind(); fk.room=true;
    acmp_poll(&r.a); send_ms=5; acmp_poll(&r.a);
    ASSERT_EQ(last_send,1005u);
    EXPECT_EQ(r.a.sinks[0].timer_deadline,last_send+200u);
}
TEST(ReviewerTimers, ZeroElapsedSendPositiveControl) {
    Rig r; r.bind();
    ASSERT_EQ(last_send,1000u);
    EXPECT_EQ(r.a.sinks[0].timer_deadline,1200u);
}
}
