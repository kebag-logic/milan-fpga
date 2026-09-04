/* SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * milan_trace.c - barectf platform callbacks over a DRAM ring of CTF packets.
 *
 * The ring is an array of `n_packets` fixed-size slots.  barectf writes
 * directly into the head slot; when the slot fills, barectf calls close_packet
 * (ring bookkeeping) and then open_packet (point barectf at the next slot).
 * When the head catches the oldest un-taken packet the oldest is DROPPED and
 * counted - the tracer never blocks a producer and never stalls the datapath,
 * because a tracer that can stall the thing it is tracing is a fault injector.
 *
 * Bookkeeping is in ABSOLUTE packet numbers (`w_abs`, `o_abs`), never in slot
 * indices, so "did the producer overwrite part of the segment I am compressing"
 * is a subtraction rather than a search.  Slot = abs % n_packets.
 *
 * Rationale for every non-obvious choice is in docs/design/TRACE_LOGGING.md.
 */

#include <string.h>

#include "milan_trace.h"

#define DEFAULT_FLUSH_MIN_INTERVAL_US   60000000u   /* 60 s - section 5 budget */

struct milan_trace_state {
    struct barectf_milan_ctx  bctx;
    struct milan_trace_cfg    cfg;

    /* Ring bookkeeping in absolute packet numbers.
     *   w_abs  = packets closed since init (the open packet is w_abs)
     *   o_abs  = oldest complete packet still in the ring
     *   resident = w_abs - o_abs, capped at n_packets - 1 (one slot is open) */
    uint64_t w_abs;
    uint64_t o_abs;

    /* Segment in flight: absolute range [seg_first, seg_first + seg_count). */
    uint64_t seg_first;
    uint32_t seg_count;
    int      seg_open;

    uint32_t armed;           /* WARN+ records since the last successful flush */
    int      forced;
    uint64_t last_flush_us;
    uint64_t last_heartbeat_us;

    /* export token bucket, bytes; refilled from the clock, spent by
     * milan_trace_flush_wrote() */
    uint32_t budget_left;
    uint64_t budget_refill_us;
    uint8_t  hold;

    uint32_t packets_dropped;
    uint32_t segments_taken;

    int      inited;
};

static struct milan_trace_state g_ts;

/* ---- helpers ----------------------------------------------------------- */

static uint8_t *slot_of(uint64_t abs)
{
    return g_ts.cfg.ring +
           (size_t)(abs % (uint64_t)g_ts.cfg.n_packets) * g_ts.cfg.packet_bytes;
}

static uint32_t capacity(void)
{
    return g_ts.cfg.n_packets - 1u;   /* one slot is always the open packet */
}

/* ---- barectf platform callbacks ---------------------------------------- */

static uint64_t cb_clock(void *data)
{
    struct milan_trace_state *ts = (struct milan_trace_state *)data;

    return ts->cfg.clock_us ? ts->cfg.clock_us(ts->cfg.user) : 0u;
}

/* Never full: we overwrite the oldest rather than refuse a record.  A tracer
 * that starts refusing records exactly when the system gets busy loses the
 * evidence for the busy period, which is the only period anyone cares about. */
static int cb_backend_full(void *data)
{
    (void)data;
    return 0;
}

static void cb_open_packet(void *data)
{
    struct milan_trace_state *ts = (struct milan_trace_state *)data;

    barectf_packet_set_buf(&ts->bctx, slot_of(ts->w_abs), ts->cfg.packet_bytes);
    barectf_milan_open_packet(&ts->bctx, ts->cfg.boot_id);
}

/* barectf calls open_packet itself right after this; do NOT open here. */
static void cb_close_packet(void *data)
{
    struct milan_trace_state *ts = (struct milan_trace_state *)data;

    barectf_milan_close_packet(&ts->bctx);
    ts->w_abs++;

    while (ts->w_abs - ts->o_abs > (uint64_t)capacity()) {
        ts->o_abs++;
        ts->packets_dropped++;
    }
}

/* ---- API --------------------------------------------------------------- */

int milan_trace_init(const struct milan_trace_cfg *cfg)
{
    struct barectf_platform_callbacks cbs;

    if (cfg == NULL || cfg->ring == NULL)
        return -1;
    if (cfg->packet_bytes < 64u || cfg->n_packets < 2u)
        return -1;

    memset(&g_ts, 0, sizeof(g_ts));
    g_ts.cfg = *cfg;
    if (g_ts.cfg.flush_min_interval_us == 0u)
        g_ts.cfg.flush_min_interval_us = DEFAULT_FLUSH_MIN_INTERVAL_US;
    if (g_ts.cfg.budget_bytes_per_hour == 0u)
        g_ts.cfg.budget_bytes_per_hour = MILAN_TRACE_BUDGET_BYTES_PER_HOUR;

    cbs.mono_clock_get_value = cb_clock;
    cbs.is_backend_full      = cb_backend_full;
    cbs.open_packet          = cb_open_packet;
    cbs.close_packet         = cb_close_packet;

    barectf_init(&g_ts.bctx, slot_of(0), g_ts.cfg.packet_bytes, cbs, &g_ts);
    cb_open_packet(&g_ts);

    g_ts.last_flush_us     = cb_clock(&g_ts);
    g_ts.last_heartbeat_us = g_ts.last_flush_us;
    /* Start with a FULL bucket: the first minutes after a boot are when a
     * fault is most likely and least affordable to lose, and a cold start with
     * an empty bucket would silently refuse exactly those flushes. */
    g_ts.budget_left       = g_ts.cfg.budget_bytes_per_hour;
    g_ts.budget_refill_us  = g_ts.last_flush_us;
    g_ts.inited            = 1;
    return 0;
}

struct barectf_milan_ctx *milan_trace_ctx(void)
{
    return g_ts.inited ? &g_ts.bctx : NULL;
}

void milan_trace_arm(uint8_t sev)
{
    if (sev >= MILAN_TRACE_FLUSH_SEV && g_ts.armed != 0xFFFFFFFFu)
        g_ts.armed++;
}

void milan_trace_flush_request(void)
{
    g_ts.forced = 1;
}

/* Refill the export bucket for the elapsed time. Integer-only, and the
 * remainder is carried by advancing `budget_refill_us` only by the whole
 * microseconds actually consumed, so a fast poll loop cannot round the refill
 * down to zero forever. */
static void budget_refill(uint64_t now)
{
    uint64_t elapsed;
    uint64_t gain;
    uint64_t per_hour;
    uint64_t used_us;

    per_hour = (uint64_t)g_ts.cfg.budget_bytes_per_hour;
    if (per_hour == 0u)
        return;
    elapsed = now - g_ts.budget_refill_us;
    gain = (elapsed * per_hour) / 3600000000ull;
    if (gain == 0u)
        return;
    used_us = (gain * 3600000000ull) / per_hour;
    g_ts.budget_refill_us += used_us;
    if (gain > (uint64_t)(per_hour - g_ts.budget_left))
        g_ts.budget_left = (uint32_t)per_hour;   /* bucket depth = one hour */
    else
        g_ts.budget_left += (uint32_t)gain;
}

int milan_trace_flush_due(void)
{
    uint64_t now;

    g_ts.hold = MILAN_TRACE_HOLD_NOTARMED;
    if (!g_ts.inited)
        return 0;
    if (g_ts.armed == 0u && !g_ts.forced)
        return 0;

    now = cb_clock(&g_ts);
    budget_refill(now);

    /* Unsigned compare is wrap-safe on the 64-bit microsecond clock for any
     * uptime this hardware will ever reach (2^64 us = 584 000 years). */
    if (now - g_ts.last_flush_us < (uint64_t)g_ts.cfg.flush_min_interval_us) {
        g_ts.hold = MILAN_TRACE_HOLD_RATELIMIT;
        return 0;
    }
    /* Refuse when a whole segment's worth of compressed bytes cannot be
     * afforded.  Refusing a PARTIAL write would be worse than refusing: it
     * would spend an erase block on a fragment. */
    if (g_ts.budget_left < MILAN_TRACE_MIN_FLUSH_BYTES) {
        g_ts.hold = MILAN_TRACE_HOLD_BUDGET;
        return 0;
    }
    g_ts.hold = MILAN_TRACE_HOLD_NONE;
    return 1;
}

uint8_t milan_trace_flush_hold(void)
{
    return g_ts.hold;
}

void milan_trace_flush_wrote(uint32_t out_bytes)
{
    g_ts.budget_left = (out_bytes >= g_ts.budget_left)
                       ? 0u : (g_ts.budget_left - out_bytes);
}

uint32_t milan_trace_budget_left(void)
{
    if (!g_ts.inited)
        return 0u;
    budget_refill(cb_clock(&g_ts));
    return g_ts.budget_left;
}

uint32_t milan_trace_segment_begin(uint32_t max_packets)
{
    uint32_t want;
    uint32_t resident;

    if (!g_ts.inited || g_ts.seg_open)
        return 0;

    /* End the segment on a packet boundary: whatever is half-written now goes
     * INTO this segment rather than being split across two.  A CTF packet split
     * across two compressed segments is undecodable in both. */
    if (!barectf_packet_is_empty(&g_ts.bctx)) {
        cb_close_packet(&g_ts);
        cb_open_packet(&g_ts);
    }

    resident = (uint32_t)(g_ts.w_abs - g_ts.o_abs);
    if (resident == 0u)
        return 0;

    want = (max_packets == 0u) ? MILAN_TRACE_SEGMENT_PACKETS : max_packets;
    if (want > resident)
        want = resident;

    g_ts.seg_first = g_ts.o_abs;
    g_ts.seg_count = want;
    g_ts.seg_open  = 1;
    g_ts.segments_taken++;
    return want;
}

const uint8_t *milan_trace_segment_packet(uint32_t i)
{
    if (!g_ts.seg_open || i >= g_ts.seg_count)
        return NULL;
    return slot_of(g_ts.seg_first + i);
}

uint32_t milan_trace_segment_end(int ok)
{
    uint32_t clobbered = 0;
    uint64_t seg_top;

    if (!g_ts.seg_open)
        return 0;

    seg_top = g_ts.seg_first + (uint64_t)g_ts.seg_count;

    /* The producer overwrote every segment packet the ring has since retired. */
    if (g_ts.o_abs > g_ts.seg_first) {
        uint64_t n = g_ts.o_abs - g_ts.seg_first;

        clobbered = (uint32_t)((n > (uint64_t)g_ts.seg_count)
                               ? g_ts.seg_count : n);
    }

    if (ok) {
        if (g_ts.o_abs < seg_top)
            g_ts.o_abs = seg_top;
        g_ts.armed         = 0;
        g_ts.forced        = 0;
        g_ts.last_flush_us = cb_clock(&g_ts);
    }

    g_ts.seg_open  = 0;
    g_ts.seg_count = 0;
    return clobbered;
}

void milan_trace_get_stats(struct milan_trace_stats *out)
{
    if (out == NULL)
        return;
    out->packets_written   = (uint32_t)g_ts.w_abs;
    out->packets_dropped   = g_ts.packets_dropped;
    out->packets_resident  = (uint32_t)(g_ts.w_abs - g_ts.o_abs);
    out->flushes_armed     = g_ts.armed;
    out->segments_taken    = g_ts.segments_taken;
    out->last_flush_us     = g_ts.last_flush_us;
    out->last_heartbeat_us = g_ts.last_heartbeat_us;
}

uint64_t milan_trace_since_heartbeat(void)
{
    return g_ts.inited ? (cb_clock(&g_ts) - g_ts.last_heartbeat_us) : 0u;
}

void milan_trace_heartbeat_done(void)
{
    g_ts.last_heartbeat_us = cb_clock(&g_ts);
}
