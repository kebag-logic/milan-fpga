// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// lwsrp_port.c - lwSRP's own MRP core, unmodified, on this firmware's port
// layer and mailbox (#665 lane F0; the owner directive of 2026-10-05: "the
// contract must carry MRP PDUs and the timer event in the form lwSRP's
// mrp_pdu codec and timer port take").
//
// Built only by the host test's lwsrp-port arm, from a lwSRP checkout the
// caller names (it is not vendored here): src/core/mrp_mad.c, mrp_pdu.c,
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
//   W3  the pool's high-water mark after the run, for F4's sizing.

#include <stdio.h>
#include <string.h>

#include "ctrl_debug.h"
#include "ctrl_loop.h"
#include "ctrl_pool.h"
#include "mbx_model.h"
#include "mbx_wire.h"
#include "ports/timer.h"
#include "shish_lan/mvrp.h"
#include "shlan_port.h"
#include "test_check.h"

static struct mbx_model model;
static struct ctrl_loop loop;
static struct ctrl_pool pool;
static _Alignas(max_align_t) uint8_t arena[16384];
static const struct ctrl_pool_class classes[] = {{64u, 32u}, {256u, 16u}, {1024u, 4u}};
static struct mrp_app *mvrp;
static unsigned registered;
static unsigned deregistered;
static uint16_t last_vid;

static void on_registered(struct mvrp_ctx *ctx, uint8_t port_id, uint16_t vid, bool is_new)
{
	(void)ctx;
	(void)port_id;
	(void)is_new;
	registered++;
	last_vid = vid;
}

static void on_deregistered(struct mvrp_ctx *ctx, uint8_t port_id, uint16_t vid)
{
	(void)ctx;
	(void)port_id;
	(void)vid;
	deregistered++;
}

static struct mvrp_ctx mvrp_cb = {on_registered, on_deregistered};

// The SRP channel's records: the MRPDU is frame bytes 14 to LEN-1.
static void on_srp(void *ctx, const struct mbx_frame *f)
{
	(void)ctx;
	if (wire_be16(f->bytes + 12) == 0x88F5u) {
		(void)mrp_rx(mvrp, f->interface, f->bytes + 14, (size_t)f->len - 14u);
	}
}

// An MVRP frame carrying one VID attribute event (802.1Q 10.8.1.2, 11.2.3).
static size_t mvrp_frame(uint8_t *f, uint16_t vid, uint8_t event)
{
	memset(f, 0, 64);
	wire_put_be(f, 0x0180C2000021ull, 6);
	wire_put_be(f + 6, 0x001B92AABBCCull, 6);
	wire_put_be(f + 12, 0x88F5u, 2);
	uint8_t *p = f + 14;
	p[0] = 0;                               // ProtocolVersion
	p[1] = MVRP_ATTR_TYPE_VID;              // AttributeType
	p[2] = MVRP_ATTR_LEN_VID;               // AttributeLength
	wire_put_be(p + 3, 1u, 2);              // VectorHeader: no LeaveAll, one value
	wire_put_be(p + 5, vid, 2);             // FirstValue
	p[7] = (uint8_t)(event * 36u);          // ThreePackedEvents (event, 0, 0)
	wire_put_be(p + 8, 0u, 2);              // EndMark of the AttributeList
	wire_put_be(p + 10, 0u, 2);             // EndMark of the MRPDU
	return 14u + 12u;
}

static void settle(void)
{
	while (ctrl_loop_service(&loop) != 0u) {
	}
}

static void run_ms(uint32_t ms)
{
	for (uint32_t k = 0; k < ms; ++k) {
		mbx_model_advance_ms(&model, 1);
		settle();
	}
}

int main(void)
{
	uint8_t f[64];
	mbx_model_reset(&model);
	mbx_model_bind(&model, NULL, NULL);
	check("W0 the pool is carved", ctrl_pool_init(&pool, arena, sizeof arena, classes, 3));
	shlan_port_bind_pool(&pool);
	ctrl_loop_init(&loop);
	check("W0 the SRP channel and the centisecond tick bind",
	      ctrl_loop_bind_rx(&loop, MBX_CH_SRP, on_srp, NULL) && ctrl_loop_add_tick(&loop, shlan_timer_tick));
	check("W0 the loop opens the mailbox", ctrl_loop_open(&loop, 0x1122334455667788ull));
	mvrp = mvrp_app_create(1, &mvrp_cb);
	check("W0 mvrp_app_create succeeds on the static pool", mvrp != NULL);
	check("W0 and its state is pool blocks", ctrl_pool_in_use(&pool) > 0u);
	(void)mbx_model_rx(&model, f, mvrp_frame(f, 100, MRP_ATTR_EVENT_JOININ), 0);
	settle();
	check_eq("W1 a JoinIn through the SRP channel registers the VID", registered, 1);
	check_eq("W1 VID", last_vid, 100);
	(void)mbx_model_rx(&model, f, mvrp_frame(f, 100, MRP_ATTR_EVENT_LV), 0);
	settle();
	run_ms(10u * (MRP_LEAVE_TIME_CS - 1u));
	check_eq("W2 the leavetimer has not expired after 59 fabric centiseconds", deregistered, 0);
	run_ms(20u);
	check_eq("W2 and has by 61: the deregistration indication fires", deregistered, 1);
	check("W2 the loop dispatched the fabric's ticks", loop.stats.ticks >= MRP_LEAVE_TIME_CS);
	unsigned high = 0;
	for (unsigned i = 0; i < pool.n_bins; ++i) {
		printf("  pool class %u: %u-byte stride, high-water %u of %u blocks\n", i, (unsigned)pool.bins[i].stride,
		       (unsigned)pool.bins[i].high_water, (unsigned)pool.bins[i].blocks);
		high += pool.bins[i].high_water;
	}
	check("W3 lwSRP allocated only from the pool, and nothing was refused", high > 0u && pool.refused == 0u);
	mvrp_app_destroy(mvrp);
	check_eq("W3 mvrp_app_destroy returns every block", ctrl_pool_in_use(&pool), 0);
	check_eq("W3 no free was refused", pool.bad_frees, 0);
	return check_report("ctrl lwSRP port (lwSRP core on the static pool and the mailbox)");
}
