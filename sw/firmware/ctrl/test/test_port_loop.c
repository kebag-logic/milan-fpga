// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// test_port_loop.c - the HAL's own half, on the host model (#665 lane F0):
//
//   P   the static pool behind lwSRP's shlan_malloc/calloc/free: classes,
//       exhaustion, release, double and foreign frees, calloc's overflow,
//       alignment, the high-water mark, and the four shlan_* functions;
//   S   the debug sink behind shlan_printf: delivery, truncation, discard;
//   D   the mailbox driver on the model: RX records byte for byte, a
//       malformed record resynchronised, TX records and their refusals, every
//       event type decoded, timers, the coherent grandmaster read;
//   L   the event loop: the order ctrl_loop_open brings the mailbox up in,
//       the per-pass bounds, the TICK fan-out to centisecond consumers.

#include <stdio.h>
#include <string.h>

#include "ctrl_debug.h"
#include "ctrl_loop.h"
#include "ctrl_pool.h"
#include "mbx.h"
#include "mbx_model.h"
#include "mbx_wire.h"
#include "shlan_port.h"
#include "test_check.h"

static struct mbx_model model;

static _Alignas(max_align_t) uint8_t arena[4096];

static const struct ctrl_pool_class classes[] = {{32u, 4u}, {64u, 2u}};

static void pool_refusals(void)
{
	struct ctrl_pool pool;
	size_t need = ctrl_pool_arena_bytes(classes, 2);
	const struct ctrl_pool_class unordered[] = {{64u, 2u}, {32u, 4u}};
	const struct ctrl_pool_class empty[] = {{32u, 0u}};
	check("P0 an arena one byte short is refused", !ctrl_pool_init(&pool, arena, need - 1u, classes, 2));
	check("P0 a misaligned arena is refused", !ctrl_pool_init(&pool, arena + 1, need, classes, 2));
	check("P0 classes that do not grow are refused", !ctrl_pool_init(&pool, arena, need, unordered, 2));
	check("P0 an empty class is refused", !ctrl_pool_init(&pool, arena, need, empty, 1));
	check("P0 the exact arena is accepted", ctrl_pool_init(&pool, arena, need, classes, 2));
}

static void pool_classes(void)
{
	struct ctrl_pool pool;
	(void)ctrl_pool_init(&pool, arena, sizeof arena, classes, 2);
	void *small[4];
	bool aligned = true;
	for (unsigned k = 0; k < 4u; ++k) {
		small[k] = ctrl_pool_alloc(&pool, 24u);
		aligned = aligned && small[k] != NULL && (uintptr_t)small[k] % CTRL_POOL_ALIGN == 0u;
	}
	check("P1 four 24-byte blocks come from the 32-byte class, aligned", aligned);
	void *spill = ctrl_pool_alloc(&pool, 8u);
	check("P1 an exhausted class spills into the next larger one",
	      spill != NULL && (uint8_t *)spill >= pool.bins[1].base);
	check("P1 a size no class holds is refused", ctrl_pool_alloc(&pool, 65u) == NULL);
	check("P1 a zero-byte allocation is refused", ctrl_pool_alloc(&pool, 0u) == NULL);
	check_eq("P1 refusals are counted", pool.refused, 2);
	void *last = ctrl_pool_alloc(&pool, 64u);
	check("P1 the last block of the large class", last != NULL);
	check("P1 then nothing is left", ctrl_pool_alloc(&pool, 1u) == NULL);
	check_eq("P1 every block is in use", ctrl_pool_in_use(&pool), 6);
	ctrl_pool_free(&pool, small[2]);
	check("P2 a released block is the next one handed out", ctrl_pool_alloc(&pool, 32u) == small[2]);
	ctrl_pool_free(&pool, small[1]);
	ctrl_pool_free(&pool, small[1]);
	check_eq("P2 a double free is refused and counted", pool.bad_frees, 1);
	ctrl_pool_free(&pool, (uint8_t *)small[0] + 8);
	check_eq("P2 a free into the middle of a block is refused", pool.bad_frees, 2);
	ctrl_pool_free(&pool, &pool);
	check_eq("P2 a free of a pointer the pool never handed out is refused", pool.bad_frees, 3);
	ctrl_pool_free(&pool, NULL);
	check_eq("P2 a free of NULL is a no-op", pool.bad_frees, 3);
	check_eq("P2 the high-water mark of the small class", pool.bins[0].high_water, 4);
}

static void pool_calloc_and_port(void)
{
	struct ctrl_pool pool;
	(void)ctrl_pool_init(&pool, arena, sizeof arena, classes, 2);
	uint8_t *dirty = ctrl_pool_alloc(&pool, 32u);
	memset(dirty, 0xA5, 32u);
	ctrl_pool_free(&pool, dirty);
	uint8_t *clean = ctrl_pool_calloc(&pool, 4u, 8u);
	bool zero = clean != NULL;
	for (unsigned k = 0; zero && k < 32u; ++k) {
		zero = clean[k] == 0u;
	}
	check("P3 calloc hands out a zeroed block, even a reused one", zero);
	check("P3 calloc refuses a count times size that wraps to a small size",
	      ctrl_pool_calloc(&pool, SIZE_MAX / 4u + 2u, 4u) == NULL);
	shlan_port_bind_pool(NULL);
	check("P4 shlan_malloc before the pool is bound refuses", shlan_malloc(16u) == NULL);
	shlan_port_bind_pool(&pool);
	void *a = shlan_malloc(40u);
	void *b = shlan_calloc(2u, 8u);
	check("P4 shlan_malloc and shlan_calloc draw on the bound pool",
	      a != NULL && b != NULL && (uint8_t *)a >= pool.bins[1].base && (uint8_t *)b < pool.bins[1].base);
	unsigned before = ctrl_pool_in_use(&pool);
	shlan_free(a);
	shlan_free(b);
	check_eq("P4 shlan_free returns both blocks", ctrl_pool_in_use(&pool), before - 2u);
	shlan_port_bind_pool(NULL);
}

struct sink_capture {
	char text[256];
	size_t len;
	unsigned calls;
};

static void capture_sink(void *ctx, const char *text, size_t len)
{
	struct sink_capture *c = ctx;
	memcpy(c->text, text, len);
	c->text[len] = '\0';
	c->len = len;
	c->calls++;
}

static void debug_sink(void)
{
	struct sink_capture cap = {{0}, 0u, 0u};
	ctrl_debug_bind(NULL, NULL);
	check_eq("S0 with no sink bound shlan_printf emits nothing", (uint64_t)shlan_printf("lost %d", 1), 0);
	check_eq("S0 and counts the discard", ctrl_debug_discarded(), 1);
	ctrl_debug_bind(capture_sink, &cap);
	int n = shlan_printf("mrp port %u attr %02x", 3u, 0x2Au);
	check("S1 shlan_printf reaches the bound sink formatted", n == 18 && strcmp(cap.text, "mrp port 3 attr 2a") == 0);
	char longer[200];
	memset(longer, 'x', sizeof longer - 1u);
	longer[sizeof longer - 1u] = '\0';
	n = shlan_printf("%s", longer);
	check_eq("S2 a line over the buffer is truncated to it", (uint64_t)n, CTRL_DEBUG_LINE_BYTES);
	check_eq("S2 and the sink receives that many bytes", cap.len, CTRL_DEBUG_LINE_BYTES);
	check_eq("S2 in one call", cap.calls, 2);
	check_eq("S2 the truncation is counted", ctrl_debug_truncated(), 1);
	ctrl_debug_bind(NULL, NULL);
}

static void build_frame(uint8_t *f, size_t len, uint16_t ethertype, uint8_t sub, uint8_t msg)
{
	memset(f, 0, len);
	wire_put_be(f, 0x91E0F0010000ull, 6);
	wire_put_be(f + 6, 0x001122334455ull, 6);
	wire_put_be(f + 12, ethertype, 2);
	f[14] = sub;
	f[15] = msg;
	for (size_t k = 26; k < len; ++k) {
		f[k] = (uint8_t)(k * 7u);
	}
}

static void driver_rx(void)
{
	static struct mbx_frame got;
	uint8_t f[82];
	build_frame(f, sizeof f, 0x22F0, 0xFA, 2);
	mbx_model_reset(&model);
	check("D0 mbx_open accepts the model's contract", mbx_open());
	mbx_filter_set_own_eid(0x1122334455667788ull);
	mbx_filter_open(1u << MBX_CH_ADP);
	mbx_model_advance_ms(&model, 9);
	check("D0 the model commits a DISCOVER", mbx_model_rx(&model, f, sizeof f, 0));
	check_eq("D0 mbx_rx_take returns it", mbx_rx_take(MBX_CH_ADP, &got), MBX_STATUS_OK);
	check("D0 byte for byte, with its length, interface and arrival",
	      got.len == sizeof f && memcmp(got.bytes, f, sizeof f) == 0 && got.interface == 0u && got.arrival_ms == 9u);
	check_eq("D0 the release moved RX_TAIL to RX_HEAD", model.ch[MBX_CH_ADP].rx_tail, model.ch[MBX_CH_ADP].rx_head);
	check_eq("D0 an empty ring", mbx_rx_take(MBX_CH_ADP, &got), MBX_STATUS_EMPTY);
	(void)mbx_model_rx(&model, f, sizeof f, 0);
	(void)mbx_model_rx(&model, f, sizeof f, 0);
	model.window[(MBX_CH_ADP_RX_BASE + 4u * (model.ch[MBX_CH_ADP].rx_tail & (MBX_CH_ADP_RX_WORDS - 1u))) / 4u] ^=
		1u << MBX_RXREC_W0_KIND_LSB;
	check_eq("D1 a record with the wrong KIND is refused", mbx_rx_take(MBX_CH_ADP, &got), MBX_STATUS_BAD);
	check_eq("D1 and the ring is resynchronised to RX_HEAD, the next record included",
		 model.ch[MBX_CH_ADP].rx_tail, model.ch[MBX_CH_ADP].rx_head);
	check_eq("D1 bad channel", mbx_rx_take(MBX_N_CH, &got), MBX_STATUS_BAD);
}

static void driver_tx(void)
{
	uint8_t f[82];
	build_frame(f, sizeof f, 0x22F0, 0xFA, 0);
	mbx_model_reset(&model);
	(void)mbx_open();
	check_eq("D2 a frame becomes a TX record", mbx_tx_send(MBX_CH_ADP, 0, f, sizeof f), MBX_STATUS_OK);
	const struct mbx_model_tx *sent = mbx_model_tx_frame(&model, 0);
	check("D2 and leaves the merge byte for byte",
	      sent != NULL && sent->len == sizeof f && memcmp(sent->bytes, f, sizeof f) == 0 && sent->channel == MBX_CH_ADP);
	check_eq("D2 a 13-byte frame is refused", mbx_tx_send(MBX_CH_ADP, 0, f, 13u), MBX_STATUS_BAD);
	check_eq("D2 a frame over max_frame_bytes is refused",
		 mbx_tx_send(MBX_CH_ADP, 0, f, MBX_CH_ADP_MAX_FRAME_BYTES + 2u), MBX_STATUS_BAD);
	check_eq("D2 an unknown interface is refused", mbx_tx_send(MBX_CH_ADP, MBX_N_IF, f, sizeof f), MBX_STATUS_BAD);
	mbx_model_tx_pause(&model, true);
	unsigned taken = 0;
	while (mbx_tx_send(MBX_CH_ADP, 0, f, sizeof f) == MBX_STATUS_OK) {
		taken++;
	}
	check_eq("D3 a held merge fills the ring to its last whole record", taken,
		 MBX_CH_ADP_TX_WORDS / (MBX_TX_HDR_WORDS + (sizeof f + 3u) / 4u));
	mbx_model_tx_pause(&model, false);
	check_eq("D3 once drained every record leaves", model.tx_sent, 1u + taken);
	check_eq("D3 and none was refused", model.ch[MBX_CH_ADP].tx_err, 0);
}

static void driver_events(void)
{
	struct mbx_event ev;
	mbx_model_reset(&model);
	(void)mbx_open();
	mbx_model_advance_ms(&model, 4);
	mbx_model_set_link(&model, 0, true);
	check("D4 a LINK event", mbx_event_take(&ev) && ev.type == MBX_EV_TYPE_LINK && ev.link_up && ev.now_ms == 4u);
	mbx_model_gm_change(&model, 0, 0xA1A2A3A4A5A6A7A8ull, 5);
	check("D4 a GM event with the identity and domain",
	      mbx_event_take(&ev) && ev.type == MBX_EV_TYPE_GM && ev.gm_id == 0xA1A2A3A4A5A6A7A8ull && ev.domain == 5u);
	mbx_timer_arm(7, 0xBEEF, mbx_now_ms() + 3u);
	mbx_model_advance_ms(&model, 3);
	check("D4 a TIMER event with slot, tag and deadline",
	      mbx_event_take(&ev) && ev.type == MBX_EV_TYPE_TIMER && ev.timer_slot == 7u && ev.timer_tag == 0xBEEFu &&
		      ev.deadline_ms == 7u);
	mbx_timer_arm(8, 1, mbx_now_ms() + 2u);
	mbx_timer_cancel(8);
	mbx_model_advance_ms(&model, 5);
	check("D4 a cancelled timer posts nothing", !mbx_event_take(&ev));
	mbx_tick_enable(true);
	mbx_model_advance_ms(&model, 3u * MBX_TICK_MS);
	unsigned ticks = 0;
	while (mbx_event_take(&ev)) {
		ticks += ev.type == MBX_EV_TYPE_TICK ? ev.tick_count : 0u;
	}
	check_eq("D4 TICK events count the centiseconds", ticks, 3);
	mbx_model_set_gm(&model, 0, 0x0102030405060708ull, 9);
	uint8_t dom = 0;
	check("D5 the grandmaster read is coherent", mbx_gm_id(0, &dom) == 0x0102030405060708ull && dom == 9u);
}

struct loop_probe {
	unsigned rx;
	unsigned events;
	unsigned polls;
	unsigned ticks_a;
	unsigned ticks_b;
	uint32_t order;         // the tick consumers' call order, two bits per call
	unsigned calls;
};

static struct loop_probe probe;

static void probe_rx(void *ctx, const struct mbx_frame *f)
{
	(void)ctx;
	(void)f;
	probe.rx++;
}

static void probe_event(void *ctx, const struct mbx_event *ev)
{
	(void)ctx;
	(void)ev;
	probe.events++;
}

static void probe_poll(void *ctx)
{
	(void)ctx;
	probe.polls++;
}

static void tick_a(void)
{
	probe.ticks_a++;
	probe.order |= 1u << (2u * (probe.calls++ % 16u));
}

static void tick_b(void)
{
	probe.ticks_b++;
	probe.order |= 2u << (2u * (probe.calls++ % 16u));
}

struct open_order {
	int own_eid_hi_at;
	int filter_en_at;
	int tick_ctl_at;
	uint32_t tick_ctl;
	uint32_t filter_en;
	int n;
};

static struct open_order order;

static void trace_open(void *ctx, bool write, uint32_t off, uint32_t value)
{
	(void)ctx;
	order.n++;
	if (!write) {
		return;
	}
	if (off == MBX_REG_OWN_EID_HI) {
		order.own_eid_hi_at = order.n;
	} else if (off == MBX_REG_FILTER_EN) {
		if (order.filter_en_at == 0 && value != 0u) {
			order.filter_en_at = order.n;
		}
		order.filter_en = value;
	} else if (off == MBX_REG_TICK_CTL) {
		order.tick_ctl_at = order.n;
		order.tick_ctl = value;
	}
}

static void loop_open_and_bounds(struct ctrl_loop *l)
{
	uint8_t f[82];
	build_frame(f, sizeof f, 0x22F0, 0xFA, 2);
	mbx_model_reset(&model);
	ctrl_loop_init(l);
	memset(&probe, 0, sizeof probe);
	memset(&order, 0, sizeof order);
	check("L0 bindings fit their tables", ctrl_loop_bind_rx(l, MBX_CH_ADP, probe_rx, NULL) &&
						      ctrl_loop_add_sink(l, probe_event, NULL) &&
						      ctrl_loop_add_poll(l, probe_poll, NULL) && ctrl_loop_add_tick(l, tick_a) &&
						      ctrl_loop_add_tick(l, tick_b));
	check("L0 an unknown channel cannot be bound", !ctrl_loop_bind_rx(l, MBX_N_CH, probe_rx, NULL));
	mbx_host_trace(trace_open, NULL);
	check("L1 ctrl_loop_open brings the mailbox up", ctrl_loop_open(l, 0));
	mbx_host_trace(NULL, NULL);
	check("L1 OWN_EID is written before any channel opens", order.own_eid_hi_at > 0 &&
								order.own_eid_hi_at < order.filter_en_at);
	check_eq("L1 only the bound channel opens", order.filter_en, 1u << MBX_CH_ADP);
	check_eq("L1 the tick starts because a centisecond consumer is bound", order.tick_ctl, 1);
	check_eq("L1 IRQ_ENABLE holds the bound channel and the event ring", model.irq_enable,
		 (1u << MBX_CH_ADP) | (1u << MBX_IRQ_ENABLE_EVT_LSB));
	for (unsigned k = 0; k < 5u; ++k) {
		(void)mbx_model_rx(&model, f, sizeof f, 0);
	}
	(void)ctrl_loop_service(l);
	check_eq("L2 a pass takes at most CTRL_LOOP_RX_PER_PASS records of a channel", probe.rx, CTRL_LOOP_RX_PER_PASS);
	check_eq("L2 and polls every module once", probe.polls, 1);
	while (ctrl_loop_service(l) != 0u) {
	}
	check_eq("L2 the rest follow in later passes", probe.rx, 5);
}

static void loop_ticks_and_events(struct ctrl_loop *l)
{
	for (unsigned s = 0; s < 12u; ++s) {
		mbx_timer_arm(s, (uint16_t)s, mbx_now_ms());
	}
	mbx_model_advance_ms(&model, 0);
	probe.events = 0;
	(void)ctrl_loop_service(l);
	check_eq("L3 a pass takes at most CTRL_LOOP_EVENTS_PER_PASS events", probe.events, CTRL_LOOP_EVENTS_PER_PASS);
	while (ctrl_loop_service(l) != 0u) {
	}
	check_eq("L3 the rest follow in the next pass", probe.events, 12);
	probe.ticks_a = 0;
	probe.ticks_b = 0;
	probe.order = 0;
	probe.calls = 0;
	for (unsigned s = 0; s < MBX_EVT_WORDS / MBX_EV_WORDS; ++s) {
		mbx_timer_arm(s % MBX_N_TIMERS, 0x200u, mbx_now_ms());
	}
	mbx_model_advance_ms(&model, 3u * MBX_TICK_MS);
	check_eq("L4 (a late firmware: the ring is full while three ticks pass)", model.tick_count, 3);
	while (ctrl_loop_service(l) != 0u) {
	}
	check_eq("L4 every centisecond reaches the first consumer", probe.ticks_a, 3);
	check_eq("L4 and the second", probe.ticks_b, 3);
	check_eq("L4 in registration order, tick by tick (a b a b a b)", probe.order, 0x999u);
	uint8_t f[82];
	build_frame(f, sizeof f, 0x22F0, 0xFA, 2);
	(void)mbx_model_rx(&model, f, sizeof f, 0);
	model.window[(MBX_CH_ADP_RX_BASE + 4u * (model.ch[MBX_CH_ADP].rx_tail & (MBX_CH_ADP_RX_WORDS - 1u))) / 4u] = 0;
	unsigned rx_before = probe.rx;
	(void)ctrl_loop_service(l);
	check_eq("L5 a malformed record is counted, not handed out", l->stats.rx_bad, 1);
	check_eq("L5 and no handler saw it", probe.rx, rx_before);
}

int main(void)
{
	static struct ctrl_loop loop;
	mbx_model_reset(&model);
	mbx_model_bind(&model, NULL, NULL);
	pool_refusals();
	pool_classes();
	pool_calloc_and_port();
	debug_sink();
	driver_rx();
	driver_tx();
	driver_events();
	loop_open_and_bounds(&loop);
	loop_ticks_and_events(&loop);
	return check_report("ctrl port, driver and loop (host model)");
}
