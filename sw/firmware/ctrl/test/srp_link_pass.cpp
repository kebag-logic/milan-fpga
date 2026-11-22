// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// A link that comes up at any phase of a loop pass (#973; srp/srp_mbx.c, poll; loop/ctrl_loop.c, service_events).
// The loop takes the event ring's LINK records as a pass starts, and SRP's poll reads the LINK register later in that
// pass. A link that comes up in between reads up in the register before any LINK has carried it. Were the poll to
// take that level, it would reset the interface on it, and the LINK the next pass dispatches would be a repeated UP,
// which resets the interface again: so a first UP would lose the clean startup participants it keeps (on_event), and
// any later UP would reset the interface twice. Four tests move interface 0's link at one phase each: before a pass,
// from a sink ahead of SRP's while the pass takes its events, from a poll ahead of SRP's, after the events, and from a
// poll after SRP's. Another raises it while the event ring is full, and two re-attach SRP, with the link's DOWN record
// elided and with a later UP. The arms run this suite in a process of its own, at 1x1/1if and 8x8/1if
// (srp_arms.link_pass_arms).
#include "srp_fixture.hpp"
FW_TALLY_LABEL("ctrl SRP link inside a pass");
namespace {

enum class Phase { BeforeAPass, InTheEvents, AfterTheEvents, AfterSrpsPoll };

// Interface 0's link, moved once to `up` by the first hook of `phase` once armed
struct Move {
    mbx_model *model = nullptr;
    Phase phase = Phase::BeforeAPass;
    bool up = true;
    bool armed = false;
    void at(Phase now) {
        if (armed && phase == now) {
            armed = false;
            mbx_model_set_link(model, 0, up);
        }
    }
};
Move moving;

void ahead_sink(void *, const mbx_event *) { moving.at(Phase::InTheEvents); }
bool ahead_poll(void *) {
    moving.at(Phase::AfterTheEvents);
    return false;
}
bool behind_poll(void *) {
    moving.at(Phase::AfterSrpsPoll);
    return false;
}

// Interface 0's resets: each publishes its LICENCE word once (reset_interface, publish_licence), and nothing else
// here does, since no Listener registers and no licence moves
unsigned resets;
void count_resets(void *, bool write, uint32_t off, uint32_t) {
    if (write && off == MBX_PUB_BASE + MBX_PUB_REG_LICENCE) {
        ++resets;
    }
}

class SrpLinkPass : public Srp {
protected:
    // The fixture's boot with every link down, a sink and a poll ahead of SRP's and a poll after it
    void SetUp() override {
        boot(false, [](ctrl_loop *l) {
            ASSERT_TRUE(ctrl_loop_add_sink(l, ahead_sink, nullptr));
            ASSERT_TRUE(ctrl_loop_add_poll(l, ahead_poll, nullptr));
        });
        if (HasFatalFailure()) {
            return;
        }
        ASSERT_TRUE(ctrl_loop_add_poll(&loop, behind_poll, nullptr));
        resets = 0;
        mbx_host_trace(count_resets, nullptr);
    }
    void TearDown() override {
        mbx_host_trace(nullptr, nullptr);
        moving = Move{};
        Srp::TearDown();
    }
    // Interface 0's link moved to `up` at `phase`, in the first pass that reaches the phase's hook: a pass given whole
    // reaches none, and one may come first. In the events, a TICK is posted first, so the pass has an event to take.
    void move_at(Phase phase, bool up) {
        moving = Move{&model, phase, up, true};
        if (phase == Phase::BeforeAPass) {
            moving.at(phase);
        } else if (phase == Phase::InTheEvents) {
            mbx_model_advance_ms(&model, 10);
        }
        for (unsigned k = 0; moving.armed && k < 16u; ++k) {
            (void)ctrl_loop_service(&loop);
        }
        ASSERT_FALSE(moving.armed) << "(no pass reached the phase's hook)";
    }
    // Interface 0's link up at `phase`, then the passes until the loop settles; returns the resets it made. After the
    // events, the pass that moved it has dispatched no LINK of it, so SRP still holds the level it held.
    unsigned up_at(Phase phase) {
        const srp_interface &i = adapter.ifs[0];
        const bool seen = i.link_seen;
        const unsigned before = resets;
        move_at(phase, true);
        if (phase == Phase::AfterTheEvents) {
            EXPECT_FALSE(i.link) << "SRP's poll took a level no LINK had carried";
            EXPECT_EQ(i.link_seen, seen) << "SRP's poll took a level no LINK had carried";
            EXPECT_EQ(resets, before) << "SRP's poll reset the interface on a level no LINK had carried";
        }
        settle();
        EXPECT_TRUE(i.link);
        EXPECT_TRUE(i.link_seen);
        return resets - before;
    }
    // The first UP at `phase`, then a DOWN between passes and another UP at `phase`: the first resets nothing and keeps
    // the startup participants, its declarations leaving; the DOWN resets once, and so does the UP after it.
    void first_up_and_another(Phase phase) {
        srp_interface &i = adapter.ifs[0];
        mrp_app *const startup = i.msrp;
        ASSERT_NE(startup, nullptr) << "(the startup participants exist before any link)";
        ASSERT_FALSE(i.link);
        ASSERT_FALSE(i.link_seen);
        const uint32_t sent = model.tx_sent;
        EXPECT_EQ(up_at(phase), 0u) << "a first UP resets nothing";
        EXPECT_EQ(i.msrp, startup) << "a first UP keeps the startup participants";
        const unsigned before = resets;
        advance(400);
        unsigned declared = 0;
        for (uint32_t k = sent; k < model.tx_sent; ++k) {
            const auto *f = mbx_model_tx_frame(&model, k);
            declared += f != nullptr && f->channel == MBX_CH_SRP && f->interface == 0u;
        }
        EXPECT_GT(declared, 0u) << "the first UP's declarations leave interface 0";
        EXPECT_EQ(i.msrp, startup) << "a first UP keeps the startup participants";
        mbx_model_set_link(&model, 0, false);
        settle();
        EXPECT_FALSE(i.link);
        EXPECT_EQ(resets - before, 1u) << "a DOWN resets the interface once";
        EXPECT_EQ(up_at(phase), 1u) << "a later UP resets the interface once";
        EXPECT_NE(i.msrp, nullptr) << "(the interface rebuilt)";
    }
};

TEST_F(SrpLinkPass, BeforeAPass) { first_up_and_another(Phase::BeforeAPass); }
TEST_F(SrpLinkPass, InTheEvents) { first_up_and_another(Phase::InTheEvents); }
TEST_F(SrpLinkPass, AfterTheEventsBeforeSrpsPoll) { first_up_and_another(Phase::AfterTheEvents); }
TEST_F(SrpLinkPass, AfterSrpsPoll) { first_up_and_another(Phase::AfterSrpsPoll); }

// A link that comes up after a pass's events while the event ring is full: its LINK is held until a take makes room,
// and then waits behind the records ahead of it for more than one pass, each pass taking CTRL_LOOP_EVENTS_PER_PASS. SRP
// takes no UP from the register while it is owed, so it is the first UP all the same (#973; srp_mbx.c, carried_up).
// Every stream's counter change, one record each (Milan v1.2 Table 5.22), fills the ring twice over.
TEST_F(SrpLinkPass, ALinkUpHeldBehindAFullEventRingIsTheFirstUp) {
    srp_interface &i = adapter.ifs[0];
    mrp_app *const startup = i.msrp;
    ASSERT_NE(startup, nullptr) << "(the startup participants exist before any link)";
    for (uint16_t type : {uint16_t{MBX_CTRCHG_STREAM_INPUT_TYPE}, uint16_t{MBX_CTRCHG_STREAM_OUTPUT_TYPE}}) {
        for (uint16_t n = 0; n < 16u; ++n) {
            mbx_model_face_event(&model, 0, MBX_MODEL_EV_COUNTERS, type, n);
        }
    }
    move_at(Phase::AfterTheEvents, true);
    ASSERT_TRUE(loop.events_left) << "(the pass took all it may, the ring refilled behind it)";
    ASSERT_FALSE(model.posted_up[0]) << "(the LINK is held behind the full ring)";
    EXPECT_FALSE(i.link_seen) << "SRP's poll took a level no LINK had carried";
    unsigned passes = 0;
    while (!model.posted_up[0] && passes < 4u) {
        (void)ctrl_loop_service(&loop);
        ++passes;
    }
    ASSERT_TRUE(model.posted_up[0]) << "(a take made room for the LINK)";
    (void)ctrl_loop_service(&loop);
    EXPECT_FALSE(i.link_seen) << "SRP took an UP from the register while its LINK waited behind the ring's records";
    settle();
    EXPECT_TRUE(i.link);
    EXPECT_EQ(resets, 0u) << "a first UP resets nothing";
    EXPECT_EQ(i.msrp, startup) << "a first UP keeps the startup participants";
}

// SRP re-attached while interface 0's link is momentarily down and its DOWN record is held, the level recovering
// before the record posts, so the fabric owes no LINK: a record posts only when its level differs from the last one
// posted (KL_mbx_evt.sv). Attach reads the DOWN. SRP follows the link that is up all the same, once a poll found no
// LINK owed, and resets the interface once for it (#973; srp_mbx.c, carried_up).
TEST_F(Srp, AReattachWhoseDownRecordIsElidedFollowsTheLinkThatIsUp) {
    settle(); advance(400);
    srp_mbx_destroy(&adapter);
    ASSERT_TRUE(srp_mbx_init(&adapter,&config));
    ctrl_loop_init(&loop);
    mbx_model_evt_pause(&model,true);
    model.link_up[0]=false;
    ASSERT_TRUE(srp_mbx_attach(&adapter,&loop));
    ASSERT_TRUE(ctrl_loop_open(&loop,0x020304fffe050600ull,config.mac));
    ASSERT_FALSE(adapter.ifs[0].link) << "(attach read the DOWN)";
    model.link_up[0]=true;
    ASSERT_TRUE(model.posted_up[0]) << "(the last posted record is UP: no LINK is owed)";
    mbx_model_evt_pause(&model,false);
    resets = 0; mbx_host_trace(count_resets,nullptr);
    advance(1500);
    mbx_host_trace(nullptr,nullptr);
    EXPECT_TRUE(adapter.ifs[0].link) << "SRP does not follow a link that is up";
    EXPECT_NE(adapter.ifs[0].msrp, nullptr) << "the interface has participants";
    EXPECT_EQ(resets, 1u) << "SRP resets the interface once for the link it follows";
}

// The same with the link staying down across the re-attach and coming up later: a LINK is owed, and SRP follows it.
TEST_F(Srp, AReattachWithTheLinkDownFollowsItsLaterUp) {
    settle(); advance(400);
    srp_mbx_destroy(&adapter);
    ASSERT_TRUE(srp_mbx_init(&adapter,&config));
    ctrl_loop_init(&loop);
    mbx_model_set_link(&model,0,false);
    ASSERT_TRUE(srp_mbx_attach(&adapter,&loop));
    ASSERT_TRUE(ctrl_loop_open(&loop,0x020304fffe050600ull,config.mac));
    advance(100);
    ASSERT_FALSE(adapter.ifs[0].link);
    mbx_model_set_link(&model,0,true);
    advance(1500);
    EXPECT_TRUE(adapter.ifs[0].link) << "a later UP is followed";
}

} // namespace
