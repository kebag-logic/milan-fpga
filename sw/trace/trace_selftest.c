/* SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * trace_selftest.c - drive the real producer through a scripted fault run and
 * write the resulting CTF segments to disk.
 *
 * This is NOT a mock.  It links the SAME generated barectf producer and the
 * SAME ring (milan_trace.c) that the bare-metal image links; only the clock and
 * CSR values are synthetic. That is what makes the compression ratios and the
 * truncation behaviour measured by sw/trace/test_trace_roundtrip.py properties
 * of the shipping producer rather than of a test fixture.
 *
 * The scripted run replays this project's own field faults, in order:
 *   1. boot + steady-state polling (the dull majority - this is what the
 *      compressor mostly sees);
 *   2. a provisioning burst through the 0x800 window (CTRL written BEFORE the
 *      stream id, the TROUBLESHOOTING section 21 ordering defect);
 *   3. the accept blocker itself: APRB parsed climbing, matched static,
 *      AVTPRX_FRX pinned at 0;
 *   4. a link bounce -> MAC reset -> RST_EPOCH tick (the shadow-lie canary);
 *   5. an lwSRP attribute-row shortfall (0x694[11]) - a refusal with no other
 *      software-visible footprint;
 *   6. RX ring lap, latency-tap saturation, media-clock drift;
 *   7. a persistence-journal CRC verdict then a clean ACCEPT on the other slot;
 *   8. the tracer's own flush / evict / drop bookkeeping.
 *
 * usage: trace_selftest <outdir> [n_rounds]
 * writes: <outdir>/seg-NNNNNN.ctf   raw CTF packets, one segment per file
 *         <outdir>/stats.txt        key=value ring statistics
 *
 * Build (host): see sw/trace/README.md, or just
 *   cc -std=c99 -O2 -I sw/trace -o trace_selftest \
 *      sw/trace/trace_selftest.c sw/trace/milan_trace.c sw/trace/generated/barectf.c
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "milan_trace.h"

/* ---- synthetic monotonic clock ----------------------------------------- */

static uint64_t g_now_us;

static uint64_t clock_us(void *user)
{
    (void)user;
    return g_now_us;
}

static void advance(uint64_t us)
{
    g_now_us += us;
}

/* Deterministic PRNG - a fixed sequence keeps the produced bytes, and therefore
 * every measured compression ratio, reproducible. */
static uint32_t g_rng = 0x1722C0DEu;

static uint32_t rnd(void)
{
    g_rng ^= g_rng << 13;
    g_rng ^= g_rng >> 17;
    g_rng ^= g_rng << 5;
    return g_rng;
}

/* ---- ring storage ------------------------------------------------------ */

#define N_PACKETS   256u
static uint8_t g_ring[N_PACKETS * MILAN_TRACE_PACKET_BYTES];

/* ---- segment writer ---------------------------------------------------- */

static const char *g_outdir;
static uint32_t    g_segno;

/* A flush takes at most one segment; take one as soon as a full segment's
 * worth of packets is resident, which is what the rate-limited bench transport
 * extracts when faults keep arriving. */
static int segment_ready(void)
{
    struct milan_trace_stats st;

    milan_trace_get_stats(&st);
    return st.packets_resident >= MILAN_TRACE_SEGMENT_PACKETS;
}

static int write_segment(void)
{
    char path[512];
    uint32_t n, i;
    FILE *f;

    n = milan_trace_segment_begin(0);
    if (n == 0)
        return 0;

    snprintf(path, sizeof(path), "%s/seg-%06u.ctf", g_outdir, g_segno);
    f = fopen(path, "wb");
    if (f == NULL) {
        milan_trace_segment_end(0);
        return -1;
    }
    for (i = 0; i < n; i++)
        fwrite(milan_trace_segment_packet(i), 1, MILAN_TRACE_PACKET_BYTES, f);
    fclose(f);

    if (milan_trace_segment_end(1) != 0) {
        /* Producer overwrote part of the segment while it was open.  Nothing
         * emits during write_segment() in this program, so this must never
         * happen here - it is checked, not assumed. */
        fprintf(stderr, "trace_selftest: segment %u clobbered\n", g_segno);
        return -1;
    }

    /* The tracer describing its own flush is part of the event set, so the
     * bookkeeping lands in the NEXT segment where a reader can find it. */
    MILAN_TRACE(trace_flush, MILAN_TRACE_SEV_INFO, MILAN_TRACE_SRC_TRACE,
                g_segno, n, n * MILAN_TRACE_PACKET_BYTES, 0u, 0u,
                /* flushv OK */ 0u, 1536u * 1024u);
    g_segno++;
    return 0;
}

/* ---- the scripted run -------------------------------------------------- */

/* Steady state: what the poller emits when nothing is wrong.  Deliberately the
 * bulk of the trace, because the compressor's job is to make the boring part
 * nearly free so the interesting part can be kept for longer. */
static void steady_round(uint32_t round, uint32_t parsed, uint32_t matched,
                         uint32_t frames_rx)
{
    advance(100000);   /* 100 ms poll interval */

    if (milan_trace_since_heartbeat() >= MILAN_TRACE_HEARTBEAT_MAX_US) {
        MILAN_TRACE(heartbeat, MILAN_TRACE_SEV_DEBUG, MILAN_TRACE_SRC_FABRIC,
                    (uint32_t)(g_now_us / 1000000u), 0x0000003Fu);
        milan_trace_heartbeat_done();
    }

    MILAN_TRACE(parser_probe, MILAN_TRACE_SEV_DEBUG, MILAN_TRACE_SRC_FABRIC,
                parsed, matched, 0x0200000000020000ull, 0x02u,
                (uint8_t)(matched != 0), 0u, 1u);

    MILAN_TRACE(avtp_rx, MILAN_TRACE_SEV_DEBUG, MILAN_TRACE_SRC_FABRIC,
                0x00000101u, frames_rx, 0u, (uint16_t)(frames_rx & 0xFFFFu),
                0u, (int32_t)(1000 + (int32_t)(rnd() % 64u)), 1u);

    if ((round % 8u) == 0u) {
        MILAN_TRACE(ltap, MILAN_TRACE_SEV_DEBUG, MILAN_TRACE_SRC_FABRIC,
                    /* RX_DEPKT_RING */ 5u, 10378u,
                    (uint16_t)(12000u + (rnd() % 600u)), 12541u,
                    (uint16_t)round, 0u, 0u);
        MILAN_TRACE(mediaclk, MILAN_TRACE_SEV_DEBUG, MILAN_TRACE_SRC_AUDIO,
                    0x00000003u, (int16_t)(-12 + (int16_t)(rnd() % 24u)),
                    (uint16_t)(256u + (rnd() % 8u)), 0u, 0u, 1u);
    }
    if ((round % 32u) == 0u) {
        MILAN_TRACE(srp, MILAN_TRACE_SEV_DEBUG, MILAN_TRACE_SRC_FABRIC,
                    0x0000037Eu, 6144000u, (uint16_t)round, (uint16_t)round,
                    0u, 0u, 1u, 1u, 0u, 0u);
        MILAN_TRACE(link, MILAN_TRACE_SEV_DEBUG, MILAN_TRACE_SRC_LINKMON,
                    0x00000083u, 0x00000001u, 0u, 0u, 1u, 1u, 0u, 0u);
    }
}

int main(int argc, char **argv)
{
    struct milan_trace_cfg cfg;
    struct milan_trace_stats st;
    uint32_t rounds = 12000, i;
    uint32_t parsed = 0, matched = 0, frames_rx = 0, epoch = 3;
    uint32_t budget_flushes = 0, budget_after_1h = 0;
    uint64_t sim_us_at_end = 0;
    uint8_t  budget_hold = 0;
    char path[512];
    FILE *f;

    if (argc < 2) {
        fprintf(stderr, "usage: %s <outdir> [n_rounds]\n", argv[0]);
        return 2;
    }
    g_outdir = argv[1];
    if (argc > 2)
        rounds = (uint32_t)strtoul(argv[2], NULL, 0);

    memset(&cfg, 0, sizeof(cfg));
    cfg.ring         = g_ring;
    cfg.packet_bytes = MILAN_TRACE_PACKET_BYTES;
    cfg.n_packets    = N_PACKETS;
    cfg.clock_us     = clock_us;
    cfg.boot_id      = 0xB0071D01u;
    cfg.flush_min_interval_us = 1;   /* the host run is not rate-limited */

    if (milan_trace_init(&cfg) != 0) {
        fprintf(stderr, "trace_selftest: milan_trace_init failed\n");
        return 1;
    }

    /* -- 1. boot ---------------------------------------------------------- */
    MILAN_TRACE(boot, MILAN_TRACE_SEV_NOTICE, MILAN_TRACE_SRC_TRACE,
                cfg.boot_id, 0x4D494C4Eu /* 'MILN' */, 0x00010010u,
                0x0200000000020000ull, "ax7101", 8u, 8u,
                (uint32_t)sizeof(g_ring), MILAN_TRACE_ABI);
    MILAN_TRACE(firmware_lifecycle, MILAN_TRACE_SEV_INFO, MILAN_TRACE_SRC_TRACE,
                0u, 0u, "bare-metal tracer up; raw segment export armed");
    MILAN_TRACE(heartbeat, MILAN_TRACE_SEV_DEBUG, MILAN_TRACE_SRC_FABRIC,
                0u, 0x0000003Fu);
    milan_trace_heartbeat_done();

    /* -- 2. provisioning burst, CTRL written BEFORE the stream id --------- */
    MILAN_TRACE(stream_ctx_write, MILAN_TRACE_SEV_INFO, MILAN_TRACE_SRC_PROVISION,
                0u, 0u, 0x0800u, 0x00000000u, 0u);   /* SELECT idx 0 */
    MILAN_TRACE(stream_ctx_write, MILAN_TRACE_SEV_INFO, MILAN_TRACE_SRC_PROVISION,
                0u, 0u, 0x0810u, 0x00000000u, 1u);   /* CTRL first - the defect */
    MILAN_TRACE(stream_ctx_write, MILAN_TRACE_SEV_INFO, MILAN_TRACE_SRC_PROVISION,
                0u, 0u, 0x0814u, 0x00020000u, 2u);
    MILAN_TRACE(stream_ctx_write, MILAN_TRACE_SEV_INFO, MILAN_TRACE_SRC_PROVISION,
                0u, 0u, 0x0818u, 0x02000000u, 3u);
    MILAN_TRACE(acmp_listener, MILAN_TRACE_SEV_NOTICE, MILAN_TRACE_SRC_FABRIC,
                0u, /* SETTLED_NO_RSV */ 6u, /* UNBOUND */ 0u, 0x001Eu, 0u, 3u,
                0x0200000000020001ull, 0u, 2u, 0u);
    /* The bind record says bound; CTRL reads 0.  Both halves in one record is
     * the whole point of the stream_ctx event. */
    MILAN_TRACE(stream_ctx, MILAN_TRACE_SEV_ERROR, MILAN_TRACE_SRC_FABRIC,
                0u, 0u, 0x00000000u, 0x0200000000020000ull,
                0x91E0F000FE01ull, 2u, 1u, 0u, 1u);

    /* -- 3. the accept blocker: parsed climbs, matched does not ----------- */
    for (i = 0; i < rounds / 3u; i++) {
        parsed += 900u + (rnd() % 200u);
        steady_round(i, parsed, matched, frames_rx);
        if (segment_ready())
            write_segment();
    }
    MILAN_TRACE(note, MILAN_TRACE_SEV_ERROR, MILAN_TRACE_SRC_FABRIC, 21u,
                "APRB parsed climbing, matched static: compare misses");

    /* -- 4. link bounce -> MAC reset -> RST_EPOCH tick -------------------- */
    advance(1500000);
    MILAN_TRACE(link, MILAN_TRACE_SEV_WARN, MILAN_TRACE_SRC_LINKMON,
                0x00010010u, 0x00000000u, 1u, 1u, 0u, 0u, 0u, 1u);
    advance(48000);
    MILAN_TRACE(link, MILAN_TRACE_SEV_WARN, MILAN_TRACE_SRC_LINKMON,
                0x00010024u, 0x00000000u, 1u, 2u, 0u, 0u, 1u, 1u);
    advance(120000);
    epoch++;
    MILAN_TRACE(mac_reset, MILAN_TRACE_SEV_ERROR, MILAN_TRACE_SRC_LINKMON,
                epoch, epoch - 1u);
    MILAN_TRACE(link, MILAN_TRACE_SEV_NOTICE, MILAN_TRACE_SRC_LINKMON,
                0x00010083u, 0x00000001u, 1u, 0u, 1u, 1u, 0u, 0u);
    write_segment();

    /* -- 5. lwSRP attribute-row shortfall (0x694[11]) --------------------- */
    MILAN_TRACE(srp, MILAN_TRACE_SEV_WARN, MILAN_TRACE_SRC_FABRIC,
                0x00000C7Eu, 6144000u, 4u, 4u, 0u, 0u, 1u, 1u, 1u, 0u);
    MILAN_TRACE(srp_refusal, MILAN_TRACE_SEV_ERROR, MILAN_TRACE_SRC_PROVISION,
                11u, 0u, 216u, 1u, 2u, 6144000u, 0u);

    /* -- 6. ring lap, tap saturation, media-clock drift ------------------- */
    MILAN_TRACE(ring, MILAN_TRACE_SEV_ERROR, MILAN_TRACE_SRC_FIRMWARE,
                /* MEDIA_RX */ 2u, 4096u, 3712u, 384u, 256u, 1u);
    MILAN_TRACE(ltap, MILAN_TRACE_SEV_WARN, MILAN_TRACE_SRC_FABRIC,
                /* RX_MAC_ACCEPT */ 3u, 49u, 50u, 0xFFFFu, 0u, 0xFFFFu, 1u);
    MILAN_TRACE(mediaclk, MILAN_TRACE_SEV_WARN, MILAN_TRACE_SRC_AUDIO,
                0x00000000u, (int16_t)-512, 40u, 37u, 0u, 0u);
    MILAN_TRACE(maap, MILAN_TRACE_SEV_WARN, MILAN_TRACE_SRC_FABRIC,
                2u, 0x0100u, 3u, 5u, 1u);
    MILAN_TRACE(ptp, MILAN_TRACE_SEV_WARN, MILAN_TRACE_SRC_FABRIC,
                0x001B19FFFE000001ull, 0x001B19FFFE000002ull,
                1785000000000000000ull, (int64_t)-1843, 812u, 0u, 1u);
    write_segment();

    /* -- 7. journal: a CRC verdict, then a clean ACCEPT on the other slot -- */
    MILAN_TRACE(journal, MILAN_TRACE_SEV_ERROR, MILAN_TRACE_SRC_JOURNAL,
                /* VERIFY */ 1u, 0u, /* CRC */ 6u, 0u, 0u, 0u, 0x00u);
    MILAN_TRACE(journal, MILAN_TRACE_SEV_NOTICE, MILAN_TRACE_SRC_JOURNAL,
                /* REPLAY */ 2u, 1u, /* ACCEPT */ 1u, 41u, 8u, 8u, 0x00u);

    /* -- 8. recovery: the fix lands and matched starts climbing ----------- */
    MILAN_TRACE(stream_ctx_write, MILAN_TRACE_SEV_NOTICE, MILAN_TRACE_SRC_PROVISION,
                0u, 0u, 0x0814u, 0x00020000u, 0u);
    MILAN_TRACE(stream_ctx_write, MILAN_TRACE_SEV_NOTICE, MILAN_TRACE_SRC_PROVISION,
                0u, 0u, 0x0818u, 0x02000000u, 1u);
    MILAN_TRACE(stream_ctx_write, MILAN_TRACE_SEV_NOTICE, MILAN_TRACE_SRC_PROVISION,
                0u, 0u, 0x0810u, 0x00000003u, 2u);
    MILAN_TRACE(stream_ctx, MILAN_TRACE_SEV_NOTICE, MILAN_TRACE_SRC_FABRIC,
                0u, 0u, 0x00000003u, 0x0200000000020000ull,
                0x91E0F000FE01ull, 2u, 1u, 1u, 1u);

    for (i = 0; i < rounds; i++) {
        parsed  += 900u + (rnd() % 200u);
        matched += 890u + (rnd() % 190u);
        frames_rx += 960u;
        steady_round(i, parsed, matched, frames_rx);
        if (segment_ready())
            write_segment();
    }

    /* -- 9. a storm the flush cannot keep up with -------------------------
     * The rate limiter holds flushes to one per interval; a fault that fires
     * thousands of records per second therefore LAPS the ring.  That is the
     * designed behaviour (overwrite-oldest, never block the producer) and the
     * loss must be visible in the trace rather than inferred from a gap, so
     * this run deliberately provokes it.  The ring is N_PACKETS slots, so a
     * burst longer than that guarantees drops on any host. */
    {
        uint32_t before;

        milan_trace_get_stats(&st);
        before = st.packets_dropped;
        for (i = 0; i < (N_PACKETS + 64u) * 160u; i++) {
            advance(120);
            MILAN_TRACE(csr_access, MILAN_TRACE_SEV_DEBUG,
                        MILAN_TRACE_SRC_FABRIC,
                        0x900008B4u + ((i % 5u) * 4u), parsed + i, 0u);
        }
        milan_trace_get_stats(&st);
        if (st.packets_dropped <= before) {
            fprintf(stderr, "trace_selftest: the storm did not lap the ring\n");
            return 1;
        }
        MILAN_TRACE(trace_drop, MILAN_TRACE_SEV_WARN, MILAN_TRACE_SRC_TRACE,
                    /* RING_FULL */ 0u, 0u,
                    (st.packets_dropped - before) * MILAN_TRACE_PACKET_BYTES);
    }

    /* -- 10. wind-down ---------------------------------------------------- */
    MILAN_TRACE(trace_evict, MILAN_TRACE_SEV_INFO, MILAN_TRACE_SRC_TRACE,
                0u, 65536u, 1048576u, 0u);
    MILAN_TRACE(firmware_lifecycle, MILAN_TRACE_SEV_INFO, MILAN_TRACE_SRC_TRACE,
                1u, 0u, "tracer down, final flush");
    milan_trace_flush_request();
    /* DRAIN, oldest first.  One flush takes at most one segment, so after a
     * storm the ring still holds several segments' worth; a single final flush
     * would write the OLDEST 64 packets and silently lose the shutdown
     * records.  Draining oldest-first keeps ONE policy in the system: the ring
     * is emptied in order and workstation rotation decides what survives - see
     * TRACE_LOGGING.md section 6.  Bounded: each pass retires 64 packets. */
    while (write_segment() == 0) {
        milan_trace_get_stats(&st);
        if (st.packets_resident == 0u)
            break;
    }

    milan_trace_get_stats(&st);
    sim_us_at_end = g_now_us;

    /* -- 11. export-byte budget drill -------------------------------------
     * Drive the REAL token bucket with the shipping defaults and record how
     * many 100 KiB exports a continuously-faulting device gets before the
     * budget refuses one. This bounds bench-transport use and is exercised
     * rather than asserted. */
    {
        struct milan_trace_cfg bcfg = cfg;
        uint32_t n = 0;

        bcfg.flush_min_interval_us = 0;   /* = the 60 s default */
        bcfg.budget_bytes_per_hour = 0;   /* = the 512 KiB/h default */
        g_now_us = 0;
        milan_trace_init(&bcfg);
        MILAN_TRACE(note, MILAN_TRACE_SEV_ERROR, MILAN_TRACE_SRC_TEST, 0u,
                    "budget drill: arm the flush");
        for (n = 0; n < 1000u; ) {
            advance(60000000);            /* the rate limiter's interval */
            if (!milan_trace_flush_due())
                break;
            milan_trace_flush_wrote(100u * 1024u);
            n++;
        }
        budget_flushes = n;
        budget_hold    = milan_trace_flush_hold();
        advance(3600000000ull);
        budget_after_1h = milan_trace_budget_left();
    }

    snprintf(path, sizeof(path), "%s/stats.txt", g_outdir);
    f = fopen(path, "w");
    if (f == NULL)
        return 1;
    fprintf(f, "segments=%u\n", g_segno);
    fprintf(f, "packet_bytes=%u\n", (unsigned)MILAN_TRACE_PACKET_BYTES);
    fprintf(f, "packets_written=%u\n", st.packets_written);
    fprintf(f, "packets_dropped=%u\n", st.packets_dropped);
    fprintf(f, "packets_resident=%u\n", st.packets_resident);
    fprintf(f, "sim_us=%llu\n", (unsigned long long)sim_us_at_end);
    fprintf(f, "budget_flushes=%u\n", budget_flushes);
    fprintf(f, "budget_hold=%u\n", (unsigned)budget_hold);
    fprintf(f, "budget_after_1h=%u\n", budget_after_1h);
    fclose(f);

    printf("trace_selftest: %u segments, %u packets, %u dropped, %llu us simulated;"
           " budget drill %u flushes then hold %u\n",
           g_segno, st.packets_written, st.packets_dropped,
           (unsigned long long)sim_us_at_end, budget_flushes,
           (unsigned)budget_hold);
    return 0;
}
