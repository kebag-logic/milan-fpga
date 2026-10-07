#include <gtest/gtest.h>
#include "fw_gtest.hpp"
FW_TALLY_LABEL("R531 independent protocol and boundary probes");
#include <climits>
#include <cstddef>
#include "acmp_fake.hpp"
#include "acmp_mbx.h"
#include "ctrl_app.h"
#include "mbx_model.h"
using namespace acmp_test;
namespace {
acmp_config shape() {
 acmp_config c{}; c.entity_id=kOwn; c.n_interfaces=MBX_N_IF; c.n_sinks=MBX_N_IF;
 for(unsigned i=0;i<MBX_N_IF;i++){ c.mac[i]=kMac0+i;c.sink_interface[i]=i; }
 return c;
}
Pdu bind(unsigned k=0) {
 Pdu p{};p.msg=spec::MSG_BIND_RX_COMMAND;p.controller=kCtl1;p.talker=kTkA;p.listener=kOwn;
 p.talker_uid=1;p.listener_uid=k;p.seq=0x1234;return p;
}
class CoreProbe:public ::testing::Test {
 protected: acmp a{};acmp_config cfg{};
 void SetUp() override {fk=Fake{};cfg=shape();ASSERT_TRUE(acmp_init(&a,&cfg,&kPorts,&kEnv));}
};
TEST_F(CoreProbe, VersionZeroBinds) {
 auto f=acmpdu(bind());acmp_rx(&a,0,f.data(),f.size());ASSERT_TRUE(a.sinks[0].bound);
 EXPECT_EQ(a.sinks[0].state,ACMP_PRB_W_RESP);EXPECT_EQ(fk.sent.size(),2u);
}
TEST_F(CoreProbe, UnsupportedVersionCannotBind) {
 auto f=acmpdu(bind());f[15]|=0x10;acmp_rx(&a,0,f.data(),f.size());
 EXPECT_FALSE(a.sinks[0].bound);EXPECT_TRUE(fk.sent.empty());EXPECT_EQ(fk.count(Call::PERSIST),0u);
}
TEST_F(CoreProbe, UnsupportedVersionCannotDiscover) {
 uint8_t rec[20]={3,0,0,1};wire_put_be(rec+4,kTkA,8);wire_put_be(rec+12,kCtl1,8);
 ASSERT_EQ(acmp_restore_binding(&a,0,rec,sizeof rec),ACMP_RESTORE_APPLIED);
 auto f=adpdu(Adp{});f[15]|=0x10;acmp_adp_rx(&a,0,f.data(),f.size());
 EXPECT_FALSE(a.sinks[0].discovered);EXPECT_EQ(a.sinks[0].state,ACMP_PRB_W_AVAIL);
 f[15]&=0x0f;acmp_adp_rx(&a,0,f.data(),f.size());EXPECT_TRUE(a.sinks[0].discovered);
}
TEST_F(CoreProbe, UnstalledDuplicateAcceptsResponseAt197ms) {
 const auto t=fk.now;auto f=acmpdu(bind());acmp_rx(&a,0,f.data(),f.size());
 fk.now=t+200;acmp_timer_expired(&a,0);
 ASSERT_EQ(a.sinks[0].state,ACMP_PRB_W_RESP2);
 Pdu response=read(fk.sent.back().bytes.data());response.msg=spec::MSG_PROBE_TX_RESPONSE;
 response.stream_id=kSid;response.dest_mac=kDa;response.vlan=2;
 fk.now=t+397;f=acmpdu(response);acmp_rx(&a,0,f.data(),f.size());
 EXPECT_EQ(a.sinks[0].state,ACMP_SETTLED_NO_RSV);
}
TEST_F(CoreProbe, DuplicateGets200msAfterFiveMsSendStall) {
 const auto t=fk.now;auto f=acmpdu(bind());acmp_rx(&a,0,f.data(),f.size());
 const auto seq=a.sinks[0].probe_seq;
 fk.now=t+200;fk.room=false;acmp_timer_expired(&a,0);
 ASSERT_EQ(a.owed_count,1u);ASSERT_EQ(a.sinks[0].state,ACMP_PRB_W_RESP2);
 fk.now=t+205;fk.room=true;EXPECT_FALSE(acmp_poll(&a));
 ASSERT_EQ(fk.sent.size(),3u);EXPECT_EQ(read(fk.sent.back().bytes.data()).seq,seq);
 EXPECT_EQ(a.sinks[0].timer_deadline,t+405);
 fk.now=t+400;acmp_timer_expired(&a,0);
 EXPECT_EQ(a.sinks[0].state,ACMP_PRB_W_RESP2);
 Pdu response=read(fk.sent.back().bytes.data());response.msg=spec::MSG_PROBE_TX_RESPONSE;
 response.stream_id=kSid;response.dest_mac=kDa;response.vlan=2;
 fk.now=t+402;f=acmpdu(response);acmp_rx(&a,0,f.data(),f.size());
 EXPECT_EQ(a.sinks[0].state,ACMP_SETTLED_NO_RSV);
}
TEST_F(CoreProbe, TimerSlotBoundsIncludeUnsignedMaximum) {
 acmp_mbx m{};EXPECT_TRUE(acmp_mbx_init(&m,&cfg,&kEnv,MBX_N_TIMERS-MBX_N_IF));
 EXPECT_FALSE(acmp_mbx_init(&m,&cfg,&kEnv,MBX_N_TIMERS-MBX_N_IF+1));
 EXPECT_FALSE(acmp_mbx_init(&m,&cfg,&kEnv,UINT_MAX));
}
mbx_model model; ctrl_app app;
alignas(std::max_align_t) uint8_t arena[1024];
const ctrl_pool_class classes[]={{32,8}};
const adp_entity ent={kOwn,0x99AABBCCDDEEFF01ull,kMac0,0xC588u,2,0x4801u,2,0x4801u,0};
class MailboxProbe:public ::testing::Test {
 protected: acmp_config cfg{};
 void settle(){for(unsigned i=0;i<256 && ctrl_loop_service(&app.loop);i++) {}}
 void SetUp() override {
 fk=Fake{};cfg=shape();mbx_model_reset(&model);mbx_model_bind(&model,nullptr,nullptr);
 for(unsigned i=0;i<MBX_N_IF;i++)mbx_model_set_gm(&model,i,kGm0,0);
 ctrl_app_config c={&ent,0,arena,sizeof arena,classes,1,nullptr,nullptr,&cfg,&kEnv};
 ASSERT_TRUE(ctrl_app_start(&app,&c));settle();fk.clear();
 }
};
TEST_F(MailboxProbe, UnsupportedVersionPassesFilterButMustNotBind) {
 auto f=acmpdu(bind());f[15]|=0x10;
 ASSERT_TRUE(mbx_model_rx(&model,f.data(),f.size(),0));settle();
 EXPECT_FALSE(app.acmp.acmp.sinks[0].bound);EXPECT_EQ(fk.count(Call::PERSIST),0u);
}
TEST_F(MailboxProbe, OverflowSlotCannotReceiveItsFabricExpiry) {
 const auto next=app.acmp.adp_next;
 bool accepted=acmp_mbx_init(&app.acmp,&cfg,&kEnv,UINT_MAX);
 EXPECT_FALSE(accepted);if(!accepted)return;
 app.acmp.adp_next=next;
 auto f=acmpdu(bind());acmp_rx(&app.acmp.acmp,0,f.data(),f.size());
 ASSERT_EQ(app.acmp.ifs[0].slot,255u);
 EXPECT_GT(model.bus_err,0u);
 mbx_model_advance_ms(&model,app.acmp.acmp.sinks[0].timer_deadline-model.now_ms);
 settle();
 EXPECT_EQ(app.acmp.acmp.sinks[0].state,ACMP_PRB_W_RESP2);
}
TEST_F(MailboxProbe, ConfiguredInterfacesHaveSeparateTimersAndProbeRoutes) {
 for(unsigned i=0;i<MBX_N_IF;i++) {
  auto f=acmpdu(bind(i));ASSERT_TRUE(mbx_model_rx(&model,f.data(),f.size(),i));settle();
  EXPECT_EQ(app.acmp.acmp.sinks[i].state,ACMP_PRB_W_RESP);
  EXPECT_TRUE(model.timers[CTRL_APP_ACMP_FIRST_SLOT+i].armed);
  EXPECT_EQ(app.acmp.ifs[i].slot,CTRL_APP_ACMP_FIRST_SLOT+i);
  for(unsigned j=i+1;j<MBX_N_IF;j++)EXPECT_FALSE(app.acmp.acmp.sinks[j].bound);
 }
 unsigned seen=0;
 for(unsigned k=0;k<model.tx_sent;k++){
  const auto* t=mbx_model_tx_frame(&model,k);
  if(t && t->bytes[14]==spec::SUBTYPE && read(t->bytes).msg==spec::MSG_PROBE_TX_COMMAND){
   EXPECT_EQ(t->interface,read(t->bytes).listener_uid);seen++;
  }
 }
 EXPECT_EQ(seen,MBX_N_IF);
}
}
