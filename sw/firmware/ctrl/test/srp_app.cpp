// SPDX-License-Identifier: CERN-OHL-W-2.0
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
    ASSERT_EQ(mbx_rx_take(MBX_CH_SRP,&rx),MBX_STATUS_OK);
    calloc_before_failure=0;
    const auto receive=cost([&] {
        ASSERT_TRUE(loop.rx[MBX_CH_SRP].ready(&adapter));
        loop.rx[MBX_CH_SRP].fn(&adapter,&rx);
    });
    ASSERT_EQ(adapter.pending_rx.len,rx.len);
    check("SRP refused receive bound",receive,SRP_MBX_RX_MAX);
    const auto refused_poll=cost([&]{loop.polls[0].fn(loop.polls[0].ctx);});
    ASSERT_GT(refused_poll,MBX_N_IF);
    check("SRP retained receive poll bound",refused_poll,SRP_MBX_POLL_MAX);
    calloc_before_failure=-1; settle();
    // Mature the real Applicant's transmit opportunity without polling it.
    for (unsigned n=0;n<20u;++n) loop.ticks[0]();
    const auto sent=adapter.transmitted;
    const auto transmit_poll=cost([&]{loop.polls[0].fn(loop.polls[0].ctx);});
    ASSERT_GT(adapter.transmitted,sent);
    check("SRP transmitting poll bound",transmit_poll,SRP_MBX_POLL_MAX);
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
    // Reset and retained reception are mutually exclusive on one interface.
    // Measure both branches separately, then add their increments to the one
    // common link read. This reaches the conservative four-read envelope;
    // the reset's publication writes are the publication term's, counted apart.
    for (unsigned i=0;i<MBX_N_IF;++i) {
        mbx_model_set_link(&model,i,false);
        pub_block_writes=0; mbx_host_trace(count_pub_writes,nullptr);
        reset_extra+=poll()-idle;
        mbx_host_trace(nullptr,nullptr);
        reset_pub+=pub_block_writes;
        reset_extra-=pub_block_writes;
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
    EXPECT_EQ(fixed,MBX_N_IF*4u) << "fixed poll branch envelope";
    EXPECT_EQ(reset_pub,MBX_N_IF*SRP_MBX_PUB_RESET) << "a reset publishes LICENCE and TALKER_DECL, then SR_DOMAIN, IDLE_SLOPE and TALKER_DECL, once each";
    const int64_t pub_term=static_cast<int64_t>(MBX_N_IF*SRP_MBX_PUB_POLL_MAX);
    EXPECT_LE(static_cast<int64_t>(fixed),
              static_cast<int64_t>(SRP_MBX_POLL_MAX)-pub_term-2*MBX_N_IF*SRP_MBX_TX_MAX)
        << "poll fixed term is funded independently";
    for (unsigned n=0;n<20u;++n) loop.ticks[0]();
    srp_probe={&model,0,0,0,true};
    const auto transmitting=poll();
    const auto observed=srp_probe;
    srp_probe={};
    EXPECT_EQ(observed.calls,2u*MBX_N_IF) << "both participants on every interface are visited";
    EXPECT_EQ(observed.sends,observed.calls) << "every call reached real send_pdu";
    EXPECT_EQ(transmitting,idle+observed.accesses) << "transmitting poll adds only measured sends";
    EXPECT_LE(static_cast<int64_t>(observed.calls),
              (static_cast<int64_t>(SRP_MBX_POLL_MAX)-static_cast<int64_t>(fixed)-pub_term)/SRP_MBX_TX_MAX)
        << "poll transmit count is funded independently";
    EXPECT_LE(fixed+reset_pub+observed.accesses,SRP_MBX_POLL_MAX) << "measured complete poll envelope";
    std::printf("  SRP poll terms: fixed %u, calls %u, real send accesses %u, envelope %u/%u\n",
                unsigned(fixed),observed.calls,unsigned(observed.accesses),
                unsigned(fixed+observed.accesses),SRP_MBX_POLL_MAX);
}

// Each publication a poll may make, measured through the real callbacks: a
// reset's five writes, a Domain adoption's three, one before each licence
// change. SRP_MBX_PUB_POLL_MAX funds a reset, an adoption and two licence
// changes for every source the publication block holds.
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
    const auto reset=pub(poll);
    EXPECT_EQ(reset,SRP_MBX_PUB_RESET) << "a reset publishes LICENCE and TALKER_DECL, then SR_DOMAIN, IDLE_SLOPE and TALKER_DECL, once each";
    mbx_model_set_link(&model,0,true); settle();
    receive_before_poll(frame(4,{6,4,0,3},0));
    const auto adoption=pub(poll);
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
    EXPECT_EQ(events,CTRL_LOOP_EVENTS_PER_PASS*(MBX_EV_WORDS+2u+1u+SRP_MBX_PUB_RESET));
    EXPECT_LE(static_cast<int64_t>(events),static_cast<int64_t>(SRP_MBX_PASS_MAX)-
              CTRL_LOOP_RX_PER_PASS*(SRP_MBX_RX_RECORD_MAX+SRP_MBX_RX_MAX)-SRP_MBX_POLL_MAX)
        << "pass event records are funded independently";
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
    // One empty event-head read, then each record and its one readiness read.
    EXPECT_EQ(rx,1u+CTRL_LOOP_RX_PER_PASS*(SRP_MBX_RX_RECORD_MAX+1u));
    // Retained allocation refusal needs one further clock read, measured by
    // EventReceiveAndTransmitPollFitTheirMeasuredBounds. Fund that alternative
    // for each record; it cannot be hidden by a short frame or a quiet poll.
    const auto receive_envelope=rx-1u+CTRL_LOOP_RX_PER_PASS;
    EXPECT_LE(static_cast<int64_t>(receive_envelope),static_cast<int64_t>(SRP_MBX_PASS_MAX)-events-SRP_MBX_POLL_MAX)
        << "pass receive count is funded independently";
    const auto pass_envelope=events+receive_envelope+MBX_N_IF*(4u+SRP_MBX_PUB_POLL_MAX+2u*SRP_MBX_TX_MAX);
    EXPECT_LE(pass_envelope,SRP_MBX_PASS_MAX) << "pass funds the independently measured poll envelope";
    std::printf("  SRP pass terms: event %u, receive %u, poll %u, envelope %u/%u\n",
                unsigned(events),unsigned(receive_envelope),MBX_N_IF*(4u+SRP_MBX_PUB_POLL_MAX+2u*SRP_MBX_TX_MAX),
                unsigned(pass_envelope),SRP_MBX_PASS_MAX);
    loop.n_polls=1;
}
} // namespace
