// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// lwsrp_port.cpp - lwSRP's own MRP core, unmodified, on this firmware's port
// layer and mailbox (#665 lanes F0 and FT; the owner directive of
// 2026-10-05: "the contract must carry MRP PDUs and the timer event in the
// form lwSRP's mrp_pdu codec and timer port take").
//
// Built only by the host test's lwsrp arm, from a lwSRP checkout the caller
// names (it is not vendored here): src/core/mrp_mad.c, mrp_pdu.c,
// src/ports/timer.c and src/modules/mvrp.c, with lwSRP's src/ports/alloc.c
// left out so shlan_malloc/calloc/free/printf resolve to ../port. What it
// shows, on the host model:
//
//   W0  mvrp_app_create draws its state from the static pool, never a heap;
//   W1  an MVRP JoinIn arrives as an SRP channel record and its MRPDU (frame
//       bytes 14 onward, the record's IF as port_id) goes to mrp_rx as is:
//       the registration indication fires for the VID;
//   W2  a Lv starts the registrar's leavetimer (802.1Q 10.7.11, 60 cs in
//       lwSRP), and the fabric's TICK events, fanned out to
//       shlan_timer_tick by the event loop, expire it: not before 59
//       centiseconds, by 61;
//   W3  the pool's high-water mark after the run, for F4's sizing, and every
//       block back once the application is destroyed.
//
// lwSRP's own suites are not run here: they run upstream, and with F4 at the
// pinned commit (sw/firmware/gtest/README.md).

#include <gtest/gtest.h>

#include <cstddef>
#include <cstdint>
#include <cstdio>
#include <cstring>

#include "ctrl_debug.h"
#include "ctrl_loop.h"
#include "ctrl_pool.h"
#include "fw_gtest.hpp"
#include "mbx_model.h"
#include "mbx_wire.h"
#include "shlan_port.h"

extern "C" {
#include "ports/timer.h"
#include "shish_lan/mvrp.h"
}

FW_TALLY_LABEL("ctrl lwSRP port (lwSRP core on the static pool and the mailbox)");

namespace {

mbx_model model;
ctrl_loop loop;
ctrl_pool pool;
alignas(std::max_align_t) std::uint8_t arena[16384];
const ctrl_pool_class classes[] = {{64u, 32u}, {256u, 16u}, {1024u, 4u}};
mrp_app* mvrp;
unsigned registered;
unsigned deregistered;
std::uint16_t last_vid;

void on_registered(mvrp_ctx*, std::uint8_t, std::uint16_t vid, bool) {
    registered++;
    last_vid = vid;
}

void on_deregistered(mvrp_ctx*, std::uint8_t, std::uint16_t) {
    deregistered++;
}

mvrp_ctx mvrp_cb = {on_registered, on_deregistered};

// The SRP channel's records: the MRPDU is frame bytes 14 to LEN-1.
void on_srp(void*, const mbx_frame* f) {
    if (wire_be16(f->bytes + 12) == 0x88F5u) {
        static_cast<void>(mrp_rx(mvrp, f->interface, f->bytes + 14, static_cast<std::size_t>(f->len) - 14u));
    }
}

// An MVRP frame carrying one VID attribute event (802.1Q 10.8.1.2, 11.2.3).
std::size_t mvrp_frame(std::uint8_t* f, std::uint16_t vid, std::uint8_t event) {
    std::memset(f, 0, 64);
    wire_put_be(f, 0x0180C2000021ull, 6);
    wire_put_be(f + 6, 0x001B92AABBCCull, 6);
    wire_put_be(f + 12, 0x88F5u, 2);
    std::uint8_t* p = f + 14;
    p[0] = 0;                                       // ProtocolVersion
    p[1] = MVRP_ATTR_TYPE_VID;                      // AttributeType
    p[2] = MVRP_ATTR_LEN_VID;                       // AttributeLength
    wire_put_be(p + 3, 1u, 2);                      // VectorHeader: no LeaveAll, one value
    wire_put_be(p + 5, vid, 2);                     // FirstValue
    p[7] = static_cast<std::uint8_t>(event * 36u);  // ThreePackedEvents (event, 0, 0)
    wire_put_be(p + 8, 0u, 2);                      // EndMark of the AttributeList
    wire_put_be(p + 10, 0u, 2);                     // EndMark of the MRPDU
    return 14u + 12u;
}

void settle() {
    for (unsigned passes = 0; passes < 1000u && ctrl_loop_service(&loop) != 0u; ++passes) {}
}

void run_ms(std::uint32_t ms) {
    for (std::uint32_t k = 0; k < ms; ++k) {
        mbx_model_advance_ms(&model, 1);
        settle();
    }
}

void offer(std::uint16_t vid, std::uint8_t event) {
    std::uint8_t f[64];
    static_cast<void>(mbx_model_rx(&model, f, mvrp_frame(f, vid, event), 0));
    settle();
}

// The F0 composition of the SRP channel: the pool bound behind lwSRP's port,
// the channel and the centisecond tick bound, the loop open.
void compose() {
    mbx_model_reset(&model);
    mbx_model_bind(&model, nullptr, nullptr);
    EXPECT_TRUE(ctrl_pool_init(&pool, arena, sizeof arena, classes, 3)) << "W0 the pool is carved";
    shlan_port_bind_pool(&pool);
    ctrl_loop_init(&loop);
    EXPECT_TRUE(ctrl_loop_bind_rx(&loop, MBX_CH_SRP, on_srp, nullptr) && ctrl_loop_add_tick(&loop, shlan_timer_tick))
        << "W0 the SRP channel and the centisecond tick bind";
    const std::uint64_t own_mac[MBX_N_IF] = {0x001B92AABBCCull};
    EXPECT_TRUE(ctrl_loop_open(&loop, 0x1122334455667788ull, own_mac)) << "W0 the loop opens the mailbox";
}

void pool_report() {
    unsigned high = 0;
    for (unsigned i = 0; i < pool.n_bins; ++i) {
        std::printf("  pool class %u: %u-byte stride, high-water %u of %u blocks\n", i,
                    static_cast<unsigned>(pool.bins[i].stride), static_cast<unsigned>(pool.bins[i].high_water),
                    static_cast<unsigned>(pool.bins[i].blocks));
        high += pool.bins[i].high_water;
    }
    EXPECT_TRUE(high > 0u && pool.refused == 0u) << "W3 lwSRP allocated only from the pool, and nothing was refused";
}

// One application for the whole run, as a boot has: lwSRP's timer port keeps
// every timer it was ever given in one list and has no call that removes one,
// so an application destroyed and created again would leave the first one's
// timers, in freed blocks, on the list shlan_timer_tick walks.
TEST(LwsrpOnThePort, W0toW3MvrpOnThePoolAndTheFabricTicks) {
    compose();
    mvrp = mvrp_app_create(1, &mvrp_cb);
    ASSERT_NE(mvrp, nullptr) << "W0 mvrp_app_create succeeds on the static pool";
    EXPECT_GT(ctrl_pool_in_use(&pool), 0u) << "W0 and its state is pool blocks";
    offer(100, MRP_ATTR_EVENT_JOININ);
    EXPECT_EQ(registered, 1u) << "W1 a JoinIn through the SRP channel registers the VID";
    EXPECT_EQ(last_vid, 100u) << "W1 VID";
    offer(100, MRP_ATTR_EVENT_LV);
    run_ms(10u * (MRP_LEAVE_TIME_CS - 1u));
    EXPECT_EQ(deregistered, 0u) << "W2 the leavetimer has not expired after 59 fabric centiseconds";
    run_ms(20u);
    EXPECT_EQ(deregistered, 1u) << "W2 and has by 61: the deregistration indication fires";
    EXPECT_GE(loop.stats.ticks, static_cast<std::uint32_t>(MRP_LEAVE_TIME_CS))
        << "W2 the loop dispatched the fabric's ticks";
    pool_report();
    mvrp_app_destroy(mvrp);
    EXPECT_EQ(ctrl_pool_in_use(&pool), 0u) << "W3 mvrp_app_destroy returns every block";
    EXPECT_EQ(pool.bad_frees, 0u) << "W3 no free was refused";
    shlan_port_bind_pool(nullptr);
}

}  // namespace
