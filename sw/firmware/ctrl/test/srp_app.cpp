// SPDX-License-Identifier: CERN-OHL-W-2.0
#include <algorithm>
#include "srp_fixture.hpp"
#include "ctrl_app.h"
#include "srp_cost_probe.hpp"
FW_TALLY_LABEL("ctrl ADP MAAP SRP composition");
namespace {
TEST(SrpApp, AttachRefusalPreservesExistingComposition) {
    mbx_model model{}; mbx_model_reset(&model); mbx_model_bind(&model,nullptr,nullptr);
    ctrl_app app{};
    srp_mbx adapter{};
    auto receive=[](void*,const mbx_frame*) {};
    EXPECT_FALSE(ctrl_app_attach_srp(&app,&adapter));
    app.loop.rx[MBX_CH_ADP].fn=receive;
    EXPECT_FALSE(ctrl_app_attach_srp(&app,&adapter));
    app.loop.rx[MBX_CH_MAAP].fn=receive;
    EXPECT_FALSE(ctrl_app_attach_srp(&app,&adapter));
    EXPECT_EQ(app.loop.rx[MBX_CH_ADP].fn,receive);
    EXPECT_EQ(app.loop.rx[MBX_CH_MAAP].fn,receive);
    EXPECT_EQ(app.loop.rx[MBX_CH_SRP].fn,nullptr);
    EXPECT_EQ(app.loop.n_ticks,0u);
}

TEST(SrpApp, AllThreeProtocolsShareTheLoopAndWakeSources) {
    mbx_model model{}; mbx_model_reset(&model); mbx_model_bind(&model,nullptr,nullptr);
    ctrl_app app{}; srp_mbx adapter{};
    alignas(std::max_align_t) uint8_t arena[SRP_POOL_ARENA_BYTES]{};
    adp_entity entity{};
    entity.mac=0x020304050600ull; entity.entity_id=0x020304fffe050600ull;
    entity.talker_stream_sources=CTRL_SRP_SOURCES;
    ctrl_app_config cfg{&entity,0,arena,sizeof(arena),srp_pool_classes,SRP_POOL_N_CLASSES,nullptr,nullptr,nullptr,nullptr,nullptr,nullptr,0};
    unsigned allocations=0;
    auto allocation=[](void *ctx,unsigned,uint64_t,uint16_t,bool valid) {
        if(valid) ++*static_cast<unsigned*>(ctx);
    };
    for(unsigned i=0;i<MBX_N_IF;++i) mbx_model_set_link(&model,i,true);
    ASSERT_TRUE(ctrl_app_start_maap(&app,&cfg,allocation,&allocations,0));
    srp_source sources[MBX_N_IF][CTRL_SRP_SOURCES]{};
    srp_mbx_config config{}; config.link_rate_bps=1000000000;
    config.licence=[](void*,unsigned,unsigned,bool) {};
    for(unsigned i=0;i<MBX_N_IF;++i) {
        config.mac[i]=entity.mac; config.sources[i]=sources[i];
        for(unsigned s=0;s<CTRL_SRP_SOURCES;++s) {
            auto &v=sources[i][s].value;
            wire_put_be(v.stream_id.bytes,entity.mac,6);
            wire_put_be(v.stream_id.bytes+6,s,2);
            v.vlan_id=2; v.max_frame_size=224; v.max_interval_frames=1; v.priority_and_rank=0x60;
        }
    }
    ASSERT_TRUE(srp_mbx_init(&adapter,&config));
    ASSERT_TRUE(ctrl_app_attach_srp(&app,&adapter));
    const unsigned channels=(1u<<MBX_CH_ADP)|(1u<<MBX_CH_MAAP)|(1u<<MBX_CH_SRP);
    EXPECT_EQ(model.filter_en,channels);
    EXPECT_EQ(model.irq_enable,(channels<<MBX_IRQ_ENABLE_RX_LSB)|(1u<<MBX_IRQ_ENABLE_EVT_LSB));
    EXPECT_EQ(app.loop.n_sinks,3u);
    EXPECT_EQ(app.loop.n_polls,3u);
    EXPECT_EQ(app.loop.n_ticks,1u);
    EXPECT_FALSE(ctrl_app_attach_srp(&app,&adapter));
    EXPECT_EQ(model.filter_en,channels);
    for(unsigned i=0;i<MBX_N_IF;++i) {
        EXPECT_NE(app.maap.ifs[i].slot,app.adp.ifs[i].slot);
        EXPECT_EQ(model.own_mac[i],entity.mac);
    }
    for(unsigned ms=0;ms<2200;++ms) {
        mbx_model_advance_ms(&model,1);
        for(unsigned n=0;n<10 && ctrl_loop_service(&app.loop);++n) {}
    }
    EXPECT_EQ(allocations,MBX_N_IF);
    EXPECT_EQ(app.loop.stats.ticks,220u);
    bool sent[MBX_N_CH]{};
    for(unsigned n=0;n<model.tx_sent;++n) {
        const auto *f=mbx_model_tx_frame(&model,n);
        ASSERT_NE(f,nullptr); sent[f->channel]=true;
    }
    EXPECT_TRUE(sent[MBX_CH_ADP]);
    EXPECT_TRUE(sent[MBX_CH_MAAP]);
    EXPECT_TRUE(sent[MBX_CH_SRP]);
    srp_mbx_destroy(&adapter);
    maap_mbx_stop(&app.maap); adp_mbx_set_enable(&app.adp,false);
    EXPECT_EQ(ctrl_pool_in_use(&app.pool),0u);
    shlan_port_bind_pool(nullptr);
}
} // namespace

namespace {
// Isolate callback costs from loop/ring costs, using the same registered
// callbacks as production. The model counts every actual MMIO operation.
template<class Fn>
uint64_t srp_cost(mbx_model& model, Fn action) {
    const uint64_t before=model.reads+model.writes;
    action();
    return model.reads+model.writes-before;
}

TEST_F(Srp, EventReceiveAndTransmitPollFitTheirMeasuredBounds) {
    settle();
    auto cost=[&](auto action) { return srp_cost(model,action); };
    auto check=[](const char* label,uint64_t actual,unsigned limit) {
        std::printf("  %s: %u accesses, bound %u\n",label,static_cast<unsigned>(actual),limit);
        EXPECT_LE(actual,limit) << label;
    };
    mbx_event ev{}; ev.type=MBX_EV_TYPE_LINK; ev.interface=MBX_N_IF-1u; ev.link_up=true;
    const auto event=cost([&]{loop.sinks[0].fn(loop.sinks[0].ctx,&ev);});
    ASSERT_GT(event,0u);
    check("SRP event bound",event,SRP_MBX_EVENT_MAX);
    settle();
    const auto f=frame(4,{6,3,0,7},0);
    mbx_frame rx{};
    ASSERT_TRUE(mbx_model_rx(&model,f.data(),f.size(),MBX_N_IF-1u));
    loop.rx_order=mbx_rx_mark(MBX_CH_SRP);
    const auto ready=cost([&]{ASSERT_TRUE(loop.rx[MBX_CH_SRP].ready(&adapter));});
    ASSERT_EQ(mbx_rx_take(MBX_CH_SRP,&rx),MBX_STATUS_OK);
    calloc_before_failure=0;
    const auto receive=ready+cost([&]{loop.rx[MBX_CH_SRP].fn(&adapter,&rx);});
    ASSERT_EQ(adapter.pending_rx.len,rx.len);
    check("SRP refused receive bound",receive,SRP_MBX_RX_MAX);
    const auto refused_poll=cost([&]{loop.polls[0].fn(loop.polls[0].ctx);});
    ASSERT_GT(refused_poll,MBX_N_IF);
    check("SRP retained receive poll bound",refused_poll,SRP_MBX_POLL_MAX);
    calloc_before_failure=-1; settle();
    // Mature the real Applicant's transmit opportunity without polling it.
    for (unsigned n=0;n<20u;++n) loop.ticks[0]();
    const auto sent=adapter.transmitted;
    // The pass's frames padded to the channel's maximum (srp_cost_probe.hpp), so the measurement holds the whole
    // transmit term. THE TRANSMIT's call has a pass of its own, with no poll beside it (ctrl_loop.h).
    srp_probe={&model,0,0,0,true};
    const auto transmit_pass=cost([&]{loop.transmit(loop.transmit_ctx);});
    const auto observed=srp_probe;
    srp_probe={};
    ASSERT_GT(adapter.transmitted,sent);
    ASSERT_EQ(observed.sends,SRP_MBX_TRANSMIT_FRAMES);
    check("SRP transmitting pass bound",transmit_pass,SRP_MBX_PASS_MAX);
    // Per-frame bound independently measures the actual TX driver, at the
    // channel's maximum payload, so a one-access understatement is visible.
    std::vector<uint8_t> large(MBX_CH_SRP_MAX_FRAME_BYTES);
    const auto tx=cost([&]{ASSERT_EQ(mbx_tx_send(MBX_CH_SRP,0,large.data(),large.size()),MBX_STATUS_OK);});
    check("SRP maximum TX record bound",tx,SRP_MBX_TX_MAX);
    // Receive the maximum permitted wire record, through the real ring.
    // A valid empty MVRP PDU can carry Ethernet padding up to this ceiling.
    wire_put_be(large.data(),0x0180c2000021ull,6);
    wire_put_be(large.data()+6,0x020304010203ull,6);
    wire_put_be(large.data()+12,0x88f5u,2);
    ASSERT_TRUE(mbx_model_rx(&model,large.data(),large.size(),0));
    mbx_frame taken{};
    const auto record=cost([&]{ASSERT_EQ(mbx_rx_take(MBX_CH_SRP,&taken),MBX_STATUS_OK);});
    check("SRP maximum RX record bound",record,SRP_MBX_RX_RECORD_MAX);
    ASSERT_TRUE(mbx_model_rx(&model,large.data(),large.size(),0));
    while (adapter.tx_due!=0u) loop.transmit(loop.transmit_ctx);
    const auto pass=cost([&]{ctrl_loop_service(&loop);});
    ASSERT_GT(pass,record);
    check("SRP complete pass bound",pass,SRP_MBX_PASS_MAX);
}
} // namespace

namespace {
// The writes a callback makes into the publication block (contract 2.2).
uint64_t pub_block_writes;
void count_pub_writes(void*, bool write, uint32_t off, uint32_t) {
    if (write && off>=MBX_PUB_BASE && off<MBX_PUB_BASE+MBX_N_IF*MBX_PUB_STRIDE) ++pub_block_writes;
}

TEST_F(Srp, PollTermsAreMeasuredSeparatelyThroughRealCallbacks) {
    settle();
    auto poll=[&] { return srp_cost(model,[&]{loop.polls[0].fn(loop.polls[0].ctx);}); };
    const auto idle=poll();
    EXPECT_EQ(idle,MBX_N_IF) << "one link read per interface";
    uint64_t reset_extra=0;
    uint64_t retry_extra=0;
    uint64_t reset_pub=0;
    uint64_t reopen_pub=0;
    // Reset and retained reception are mutually exclusive on one interface.
    // Measure both branches separately, then add their increments to the one
    // common link read. This reaches three reads, one under the bound's four;
    // the reset's publication writes are the publication term's, counted apart,
    // the withdrawal's in its poll and the new participants' in the next.
    for (unsigned i=0;i<MBX_N_IF;++i) {
        mbx_model_set_link(&model,i,false);
        pub_block_writes=0; mbx_host_trace(count_pub_writes,nullptr);
        reset_extra+=poll()-idle;
        mbx_host_trace(nullptr,nullptr);
        reset_pub+=pub_block_writes;
        reset_extra-=pub_block_writes;
        pub_block_writes=0; mbx_host_trace(count_pub_writes,nullptr);
        const auto build=poll()-idle;
        mbx_host_trace(nullptr,nullptr);
        reopen_pub+=pub_block_writes;
        EXPECT_EQ(build,pub_block_writes) << "the poll that builds reads nothing a quiet poll does not";
        settle();
        mbx_model_set_link(&model,i,true); settle();
        const auto f=frame(4,{6,3,0,7},0);
        mbx_frame rx{};
        ASSERT_TRUE(mbx_model_rx(&model,f.data(),f.size(),i));
        ASSERT_EQ(mbx_rx_take(MBX_CH_SRP,&rx),MBX_STATUS_OK);
        calloc_before_failure=0;
        loop.rx[MBX_CH_SRP].fn(&adapter,&rx);
        ASSERT_NE(adapter.pending_rx.len,0u);
        retry_extra+=poll()-idle;
        calloc_before_failure=-1; settle();
    }
    const uint64_t fixed=idle+reset_extra+retry_extra;
    EXPECT_EQ(fixed,MBX_N_IF*3u) << "fixed poll branch envelope";
    EXPECT_EQ(reset_pub,MBX_N_IF*SRP_MBX_PUB_WITHDRAW) << "a reset publishes LICENCE and TALKER_DECL, once each";
    EXPECT_EQ(reopen_pub,MBX_N_IF*SRP_MBX_PUB_REOPEN)
        << "the poll after it publishes SR_DOMAIN, IDLE_SLOPE and TALKER_DECL, once each";
    const int64_t pub_term=static_cast<int64_t>(MBX_N_IF*SRP_MBX_PUB_POLL_MAX);
    EXPECT_LE(static_cast<int64_t>(fixed),
              static_cast<int64_t>(SRP_MBX_POLL_MAX)-pub_term-SRP_MBX_POLL_FRAMES*SRP_MBX_TX_MAX)
        << "poll fixed term is funded independently";
    for (unsigned n=0;n<20u;++n) loop.ticks[0]();
    // Every participant now owes a frame. The poll sends none of them: THE TRANSMIT's call does, both of an
    // interface's, in a pass of its own, and the next takes the next interface (#665, the share; ctrl_loop.h).
    srp_probe={&model,0,0,0,true};
    EXPECT_EQ(poll(),idle) << "the poll builds no MRPDU";
    EXPECT_EQ(srp_probe.sends,0u) << "the poll builds no MRPDU";
    srp_probe={};
    auto build=[&] { return srp_cost(model,[&]{loop.transmit(loop.transmit_ctx);}); };
    unsigned sends=0;
    uint64_t most=0;
    // a declaration made after a build owes the participant whose join timer is idle a pass of its own
    for (unsigned n=0;n<4u*MBX_N_IF && adapter.tx_due!=0u;++n) {
        srp_probe={&model,0,0,0,true};
        const auto transmitting=build();
        const auto observed=srp_probe;
        srp_probe={};
        EXPECT_TRUE(observed.sends==0u || observed.sends==SRP_MBX_TRANSMIT_FRAMES)
            << "both of an interface's MRPDUs a call, the next's on the next";
        EXPECT_EQ(observed.calls,SRP_MBX_TRANSMIT_FRAMES) << "every call reached mrp_transmit";
        EXPECT_EQ(transmitting,observed.accesses) << "a build's call adds only measured sends";
        EXPECT_LE(observed.sends*SRP_MBX_TX_MAX,SRP_MBX_PASS_MAX) << "a pass given whole funds its frames";
        EXPECT_LE(observed.accesses,SRP_MBX_PASS_MAX) << "measured complete build envelope";
        sends+=observed.sends;
        most=std::max<uint64_t>(most,observed.accesses);
    }
    EXPECT_EQ(sends,2u*MBX_N_IF) << "both participants on every interface are visited";
    srp_probe={&model,0,0,0,true};
    (void)build();
    EXPECT_EQ(srp_probe.sends,0u) << "and each sent once";
    srp_probe={};
    std::printf("  SRP poll terms: fixed %u, frames a poll %u, real send accesses %u, envelope %u/%u\n",
                unsigned(fixed),SRP_MBX_POLL_FRAMES,unsigned(most),
                unsigned(fixed+most),SRP_MBX_POLL_MAX);
}

// Each publication a poll may make, measured through the real callbacks: a
// reset's five writes, two in its own poll and three in the next that builds,
// a Domain adoption's three, one before each licence change.
// SRP_MBX_PUB_POLL_MAX funds a reset, an adoption and two licence changes for
// every source the publication block holds.
TEST_F(Srp, PollPublicationTermIsMeasuredThroughRealCallbacks) {
    settle();
    auto pub=[&](auto action) {
        pub_block_writes=0; mbx_host_trace(count_pub_writes,nullptr);
        action();
        mbx_host_trace(nullptr,nullptr);
        return pub_block_writes;
    };
    auto poll=[&] { loop.polls[0].fn(loop.polls[0].ctx); };
    mbx_model_set_link(&model,0,false);
    const auto withdraw=pub(poll);
    EXPECT_EQ(withdraw,SRP_MBX_PUB_WITHDRAW) << "a reset publishes LICENCE and TALKER_DECL, once each";
    const auto reopen=pub(poll);
    EXPECT_EQ(reopen,SRP_MBX_PUB_REOPEN) << "the poll after it publishes SR_DOMAIN, IDLE_SLOPE and TALKER_DECL, once each";
    const auto reset=withdraw+reopen;
    mbx_model_set_link(&model,0,true); settle();
    receive_before_poll(frame(4,{6,4,0,3},0));
    // the adoption is a declaration, which THE TRANSMIT's call makes with its build after the pass's poll
    // (ctrl_loop.h), so the pass's term is the two together
    const auto adoption=pub([&] { poll(); loop.transmit(loop.transmit_ctx); });
    EXPECT_EQ(adoption,3u) << "a Domain adoption publishes SR_DOMAIN, IDLE_SLOPE and TALKER_DECL once each";
    settle(); advance(200);
    EXPECT_CALL(licence,Change(0,0,true));
    receive_before_poll(frame(3,identity(0),1,2));
    const auto grant=pub(poll);
    EXPECT_EQ(grant,1u) << "a licence change publishes LICENCE once, before it is reported";
    EXPECT_LE(reset+adoption+2u*MBX_N_PUB_SOURCES*grant,SRP_MBX_PUB_POLL_MAX)
        << "the poll's publication term funds a reset, an adoption and two changes per source";
    std::printf("  SRP publication terms: reset %u, adoption %u, licence change %u, term %u\n",
                unsigned(reset),unsigned(adoption),unsigned(grant),SRP_MBX_PUB_POLL_MAX);
    EXPECT_CALL(licence,Change(0,0,false));
}

TEST_F(Srp, PassFundsEveryEventRecordAndBothMaximumReceives) {
    settle();
    // Take a full pass of real LINK records with no RX/poll work to hide a
    // missing event-record term. Each repeated edge forces a participant reset.
    loop.n_polls=0;
    const auto receive=loop.rx[MBX_CH_SRP];
    loop.rx[MBX_CH_SRP]={};
    for (unsigned n=0;n<CTRL_LOOP_EVENTS_PER_PASS;++n) mbx_model_set_link(&model,0,(n%2u)!=0u);
    const auto events0=loop.stats.events;
    const auto events=srp_cost(model,[&]{ctrl_loop_service(&loop);});
    ASSERT_EQ(loop.stats.events-events0,CTRL_LOOP_EVENTS_PER_PASS);
    // and the ring's mark, read once a pass, with the read that gives a pass whole its row (ctrl_loop.c)
    EXPECT_EQ(events,CTRL_LOOP_EVENTS_PER_PASS*(MBX_EV_WORDS+2u+1u+SRP_MBX_PUB_WITHDRAW)+2u);
    EXPECT_LE(static_cast<int64_t>(events),static_cast<int64_t>(SRP_MBX_PASS_MAX)-
              CTRL_LOOP_RX_PER_PASS*(SRP_MBX_RX_RECORD_MAX+SRP_MBX_RX_MAX)-SRP_MBX_POLL_MAX)
        << "pass event records are funded independently";
    // Those resets' polls: receive waits until the new participants are built.
    for (unsigned n=0;n<2u;++n) loop.polls[0].fn(loop.polls[0].ctx);
    while (adapter.tx_due!=0u) loop.transmit(loop.transmit_ctx);
    // Drain two maximum-length MVRP records in one pass. Empty MVRP plus
    // Ethernet padding needs no allocation; the real readiness check runs.
    loop.rx[MBX_CH_SRP]=receive;
    std::vector<uint8_t> large(MBX_CH_SRP_MAX_FRAME_BYTES);
    wire_put_be(large.data(),0x0180c2000021ull,6);
    wire_put_be(large.data()+6,0x020304010203ull,6); wire_put_be(large.data()+12,0x88f5u,2);
    for (unsigned n=0;n<CTRL_LOOP_RX_PER_PASS;++n) ASSERT_TRUE(mbx_model_rx(&model,large.data(),large.size(),0));
    const auto rx0=loop.stats.rx_records;
    const auto rx=srp_cost(model,[&]{ctrl_loop_service(&loop);});
    ASSERT_EQ(loop.stats.rx_records-rx0,CTRL_LOOP_RX_PER_PASS);
    // The loop's reads, then each record, whose readiness reads nothing: the head the ring's mark read stands.
    EXPECT_EQ(rx,SRP_MBX_LOOP_READS+CTRL_LOOP_RX_PER_PASS*SRP_MBX_RX_RECORD_MAX);
    // Retained allocation refusal needs one further clock read, measured by
    // EventReceiveAndTransmitPollFitTheirMeasuredBounds. Fund that alternative
    // for each record; it cannot be hidden by a short frame or a quiet poll.
    const auto receive_envelope=rx-SRP_MBX_LOOP_READS+CTRL_LOOP_RX_PER_PASS;
    EXPECT_LE(static_cast<int64_t>(receive_envelope),static_cast<int64_t>(SRP_MBX_PASS_MAX)-events-SRP_MBX_POLL_MAX)
        << "pass receive count is funded independently";
    // The poll's: its fixed and publication terms on every interface, and one
    // MRPDU a poll (Srp.PollTermsAreMeasuredSeparatelyThroughRealCallbacks).
    const auto poll_envelope=MBX_N_IF*(4u+SRP_MBX_PUB_POLL_MAX)+SRP_MBX_POLL_FRAMES*SRP_MBX_TX_MAX;
    const auto pass_envelope=events+receive_envelope+poll_envelope;
    EXPECT_LE(pass_envelope,SRP_MBX_PASS_MAX) << "pass funds the independently measured poll envelope";
    std::printf("  SRP pass terms: event %u, receive %u, poll %u, envelope %u/%u\n",
                unsigned(events),unsigned(receive_envelope),unsigned(poll_envelope),
                unsigned(pass_envelope),SRP_MBX_PASS_MAX);
    loop.n_polls=1;
}

// A link change withdraws in the pass that takes it, the next pass's poll builds the new
// participants and SRP's receive waits for it: destroying and building in one pass is over the
// per-pass share at 8x8 (#665, srp_bounds.h, the share in ctrl_loop.h).
uint64_t domain_writes;
uint32_t domain_reg;
void count_domain_writes(void*, bool write, uint32_t off, uint32_t) {
    if (write && off==domain_reg) ++domain_writes;
}

// The next pass with a poll: THE TRANSMIT's pass, which what a build declared owes, comes between two.
void ordinary(ctrl_loop &loop) {
    unsigned given=0;
    do {
        given=loop.stats.transmit_passes;
        ctrl_loop_service(&loop);
    } while (loop.stats.transmit_passes!=given);
}

TEST_F(Srp, LinkChangeBuildsTheNewParticipantsOnTheNextPass) {
    settle();
    const unsigned last=MBX_N_IF-1u;
    domain_reg=MBX_PUB_BASE+MBX_PUB_STRIDE*last+MBX_PUB_REG_SR_DOMAIN; domain_writes=0;
    mbx_host_trace(count_domain_writes,nullptr);
    mbx_model_set_link(&model,last,false); mbx_model_set_link(&model,last,true);
    ordinary(loop);
    EXPECT_EQ(adapter.ifs[last].msrp,nullptr) << "the pass that takes the link change withdraws";
    EXPECT_EQ(adapter.ifs[last].mvrp,nullptr) << "the pass that takes the link change withdraws";
    EXPECT_EQ(domain_writes,0u) << "the pass that takes the link change builds nothing";
    const auto f=frame(4,{6,3,0,7},0);
    ASSERT_TRUE(mbx_model_rx(&model,f.data(),f.size(),last));
    const auto taken=loop.stats.rx_records; const auto received=adapter.received; const auto refused=adapter.refused;
    ordinary(loop);
    EXPECT_NE(adapter.ifs[last].msrp,nullptr) << "the next pass's poll builds the new participants";
    EXPECT_NE(adapter.ifs[last].mvrp,nullptr) << "the next pass's poll builds the new participants";
    EXPECT_EQ(domain_writes,1u) << "the next pass's poll builds the new participants";
    EXPECT_EQ(loop.stats.rx_records,taken) << "receive waits until the new participants are built";
    EXPECT_EQ(adapter.refused,refused) << "a record that waits is not a refusal";
    ordinary(loop);
    mbx_host_trace(nullptr,nullptr);
    EXPECT_EQ(loop.stats.rx_records,taken+1u) << "the record that waited is taken on the pass after";
    EXPECT_EQ(adapter.received,received+1u) << "the record that waited is taken on the pass after";
    settle();
    mbx_model_set_link(&model,last,false);
    EXPECT_TRUE(loop.polls[0].fn(loop.polls[0].ctx)) << "a poll that withdraws owes the build, so the loop runs on";
}

TEST_F(Srp, LinkEdgesOfOnePassBuildOnce) {
    settle();
    domain_reg=MBX_PUB_BASE+MBX_PUB_REG_SR_DOMAIN; domain_writes=0;
    mbx_host_trace(count_domain_writes,nullptr);
    for (unsigned n=0;n<CTRL_LOOP_EVENTS_PER_PASS;++n) mbx_model_set_link(&model,0,(n%2u)!=0u);
    const auto events0=loop.stats.events;
    ordinary(loop); ordinary(loop);
    mbx_host_trace(nullptr,nullptr);
    ASSERT_EQ(loop.stats.events-events0,CTRL_LOOP_EVENTS_PER_PASS);
    EXPECT_NE(adapter.ifs[0].msrp,nullptr) << "a pass of link edges builds once";
    EXPECT_EQ(domain_writes,1u) << "a pass of link edges builds once";
}

#if MBX_N_IF > 1
// Both links changing together (#665, srp_bounds.h): a pass builds one
// interface at most, the other on the next pass, and SRP's receive waits
// until both are built. The interface whose build waited goes first, and an
// interface due beside one still withdrawing builds at once.
TEST_F(Srp, JointLinkChangeBuildsOneInterfaceAPass) {
    settle();
    auto built=[this](unsigned n) { return adapter.ifs[n].msrp!=nullptr && adapter.ifs[n].mvrp!=nullptr; };
    mbx_model_set_link(&model,0,false); mbx_model_set_link(&model,1,false);
    ordinary(loop);
    ASSERT_TRUE(!built(0) && !built(1)) << "(both interfaces withdraw in the pass that takes the changes)";
    const auto f=frame(4,{6,3,0,7},0);
    ASSERT_TRUE(mbx_model_rx(&model,f.data(),f.size(),0));
    const auto taken=loop.stats.rx_records;
    ordinary(loop);
    EXPECT_TRUE(built(0) && !built(1)) << "a pass builds one interface at most";
    ordinary(loop);
    EXPECT_TRUE(built(0) && built(1)) << "the other is built on the next pass";
    EXPECT_EQ(loop.stats.rx_records,taken) << "receive waits until both are built";
    ordinary(loop);
    EXPECT_EQ(loop.stats.rx_records,taken+1u) << "the record that waited is taken on the pass after";
    settle();
    // interface 1 built last, so interface 0 has the turn; interface 0 rebuilt alone gives it to interface 1
    mbx_model_set_link(&model,0,true); ordinary(loop); ordinary(loop);
    ASSERT_TRUE(built(0) && built(1)) << "(interface 0 rebuilt alone)";
    settle();
    mbx_model_set_link(&model,0,false); mbx_model_set_link(&model,1,true);
    ordinary(loop); ordinary(loop);
    EXPECT_TRUE(built(1) && !built(0)) << "the interface whose turn it is is built first";
    ordinary(loop);
    EXPECT_TRUE(built(0) && built(1)) << "the other is built on the next pass";
    settle();
    // interface 1 has the turn and withdraws in the pass interface 0 is due
    mbx_model_set_link(&model,0,true); ordinary(loop);
    mbx_model_set_link(&model,1,false); ordinary(loop);
    EXPECT_TRUE(built(0) && !built(1)) << "an interface due beside one still withdrawing is built at once";
    ordinary(loop);
    EXPECT_TRUE(built(0) && built(1)) << "the other is built on the next pass";
}

// The same rule with the turn at interface 0, which the poll visits first:
// interface 0 withdraws in the pass interface 1 is due (#665, srp_bounds.h).
TEST_F(Srp, JointLinkChangeBuildsInterfaceOneBesideAWithdrawal) {
    settle();
    auto built=[this](unsigned n) { return adapter.ifs[n].msrp!=nullptr && adapter.ifs[n].mvrp!=nullptr; };
    // interface 1 rebuilt alone last, so interface 0 has the turn
    mbx_model_set_link(&model,1,false); ordinary(loop); ordinary(loop);
    ASSERT_TRUE(built(0) && built(1)) << "(interface 1 rebuilt alone)";
    ASSERT_EQ(adapter.build_turn,0u) << "(interface 0 has the turn)";
    settle();
    mbx_model_set_link(&model,1,true); ordinary(loop);
    ASSERT_TRUE(built(0) && !built(1)) << "(interface 1 withdrew and is due)";
    mbx_model_set_link(&model,0,false); ordinary(loop);
    EXPECT_TRUE(built(1) && !built(0))
        << "interface 1, due beside interface 0 still withdrawing with the turn, is built at once";
    ordinary(loop);
    EXPECT_TRUE(built(0) && built(1)) << "interface 0 is built on the next pass";
}
#endif
} // namespace
