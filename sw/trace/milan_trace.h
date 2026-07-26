/* SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * milan_trace.h - the barectf platform layer: a DRAM ring of CTF packets.
 *
 * WHY A RING IN DRAM AND NOT A FILE ON FLASH.  The scarce resource is the NOR
 * flash (2 MiB of /user, 64 KiB erase blocks, finite erase cycles); DRAM is not
 * (512 MB on the AX7101, 256 MB on the Arty).  Continuous logging to flash
 * exhausts the part in weeks - the arithmetic is in
 * docs/design/TRACE_LOGGING.md section 5.  So: every record lands in DRAM, and
 * flash is written only when something has gone wrong (a record at WARN or
 * above), rate-limited and budgeted.
 *
 * WHAT SURVIVES A POWER CUT IS ONLY WHAT WAS ALREADY FLUSHED.  The DRAM ring
 * is volatile.  A fault that is still only in RAM when the rail drops is gone.
 * That is a deliberate trade, not an oversight: see TRACE_LOGGING.md section 9.
 *
 * Layering:
 *
 *   barectf_milan_trace_<event>()      generated, sw/trace/generated/barectf.c
 *        |  packet full -> close_packet callback
 *        v
 *   milan_trace ring (this file)       fixed-size packet slots, overwrite-oldest
 *        |  milan_trace_segment_*()    on a WARN+ record, rate-limited
 *        v
 *   compressor + writer                PRIVATE TEST REPO (fpga/), xz per segment
 *        v
 *   /user/log/seg-NNNNNN.ctf.xz
 *
 * The compressor and the /user writer are deliberately NOT here: they need a
 * filesystem, liblzma and an init script, all of which live in the private test
 * repo.  What this file owns is the part that must be identical everywhere -
 * where a packet goes, when a flush is armed, and what a segment IS.
 *
 * Freestanding C99.  Uses only <stdint.h>, <stddef.h> and <string.h>.
 */

#ifndef MILAN_TRACE_H
#define MILAN_TRACE_H

#include <stdint.h>
#include <stddef.h>

#include "generated/barectf.h"

#ifdef __cplusplus
extern "C" {
#endif

/* ---- severities (mirror of the `sev` enum in milan_trace.yaml) ---------- */
#define MILAN_TRACE_SEV_DEBUG   0u
#define MILAN_TRACE_SEV_INFO    1u
#define MILAN_TRACE_SEV_NOTICE  2u
#define MILAN_TRACE_SEV_WARN    3u
#define MILAN_TRACE_SEV_ERROR   4u
#define MILAN_TRACE_SEV_FATAL   5u

/* ---- sources (mirror of the `src` enum in milan_trace.yaml) ------------- */
#define MILAN_TRACE_SRC_FABRIC     0u
#define MILAN_TRACE_SRC_JOURNALD   1u
#define MILAN_TRACE_SRC_LINKMON    2u
#define MILAN_TRACE_SRC_PROVISION  3u
#define MILAN_TRACE_SRC_AUDIO      4u
#define MILAN_TRACE_SRC_KERNEL     5u
#define MILAN_TRACE_SRC_TRACE      6u
#define MILAN_TRACE_SRC_TEST       7u

/* A record at or above this severity ARMS a flush to /user. */
#define MILAN_TRACE_FLUSH_SEV   MILAN_TRACE_SEV_WARN

/* The 32-bit event-record timestamp over the 1 MHz clock wraps every
 * 4294.967296 s.  A reader reconstructs the high half from the packet's 64-bit
 * timestamp_begin, which is only correct while consecutive records are less
 * than one wrap apart.  The heartbeat guarantees that with ~70x of margin.
 * Keep this in step with the note at the top of milan_trace.yaml. */
#define MILAN_TRACE_HEARTBEAT_MAX_US   60000000u   /* 60 s */
#define MILAN_TRACE_TS_WRAP_US         4294967296ull

/* Defaults.  A 4 KiB packet is 8 erase-block-friendly packets per 32 KiB and
 * ~150-250 records at our payload sizes; small enough that a torn segment
 * loses little, large enough that the 30-byte packet header is noise. */
#ifndef MILAN_TRACE_PACKET_BYTES
#define MILAN_TRACE_PACKET_BYTES   4096u
#endif

/* Segment = the unit of rotation, compression and loss.  64 packets of 4 KiB =
 * 256 KiB of CTF in, which the pinned xz chain takes to 40-73 KiB on real
 * produced traces (measured ratios in TRACE_LOGGING.md section 7). */
#ifndef MILAN_TRACE_SEGMENT_PACKETS
#define MILAN_TRACE_SEGMENT_PACKETS   64u
#endif

/* Default flash-wear budget: 512 KiB/hour = 12 MiB/day worst case.  With the
 * 1.5 MiB /user/log region (24 x 64 KiB erase blocks) and the part's
 * datasheet ">100 000 program/erase cycles per sector", that is >11 years at a
 * pessimistic 3x jffs2 write amplification, even on a board that faults
 * continuously from the day it ships.  TRACE_LOGGING.md section 5. */
#ifndef MILAN_TRACE_BUDGET_BYTES_PER_HOUR
#define MILAN_TRACE_BUDGET_BYTES_PER_HOUR   (512u * 1024u)
#endif

/* The bucket must hold at least one worst-case segment before a flush is
 * allowed; spending an erase block on a fragment is worse than waiting.
 * 96 KiB covers the worst measured per-segment output (0.2779 x 256 KiB =
 * 73 KiB) with margin for a less compressible run. */
#ifndef MILAN_TRACE_MIN_FLUSH_BYTES
#define MILAN_TRACE_MIN_FLUSH_BYTES   (96u * 1024u)
#endif

struct milan_trace_cfg {
    /* Ring storage, caller-owned.  Must be at least
     * `packet_bytes * n_packets` and 8-byte aligned. */
    uint8_t  *ring;
    uint32_t  packet_bytes;
    uint32_t  n_packets;

    /* Monotonic microseconds.  MUST NOT be the PHC - see milan_trace.yaml. */
    uint64_t (*clock_us)(void *user);
    void     *user;

    /* Distinguishes packets written by different boots of the same board.
     * Any value that changes across a reboot (a boot counter kept in /user, the
     * low word of the first PHC read, a random seed). */
    uint32_t  boot_id;

    /* Minimum microseconds between two flushes.  0 = the built-in default. */
    uint32_t  flush_min_interval_us;

    /* FLASH-WEAR BUDGET: bytes per hour this tracer may write to /user.
     * 0 = the built-in default (MILAN_TRACE_BUDGET_BYTES_PER_HOUR).
     *
     * The rate limiter alone is NOT enough.  One flush per 60 s of ~70 KiB
     * segments is ~98 MiB/day, which wears the log region out in about
     * eighteen months - and a permanently-faulting board is exactly the box
     * that would do it.  A token bucket refilled at this rate is what turns
     * "rare flushes" from an assumption into a property.  Arithmetic and the
     * resulting lifetimes: docs/design/TRACE_LOGGING.md section 5. */
    uint32_t  budget_bytes_per_hour;
};

/* Ring statistics - all free-running, all safe to read at any time. */
struct milan_trace_stats {
    uint32_t packets_written;    /* packets closed into the ring, ever */
    uint32_t packets_dropped;    /* packets overwritten before being flushed */
    uint32_t packets_resident;   /* complete packets currently in the ring */
    uint32_t flushes_armed;      /* WARN+ records seen since the last flush */
    uint32_t segments_taken;     /* milan_trace_segment_begin() calls */
    uint64_t last_flush_us;
    uint64_t last_heartbeat_us;
};

/* Initialise the tracer.  Returns 0, or -1 on a bad configuration
 * (null ring, packet_bytes < 64, n_packets < 2).
 *
 * n_packets < 2 is refused because a one-slot ring would have the open packet
 * and the segment reader fighting over the same buffer, which silently
 * produces torn packets instead of an error. */
int milan_trace_init(const struct milan_trace_cfg *cfg);

/* The barectf context to pass as the first argument of every
 * barectf_milan_trace_<event>() call.  NULL before milan_trace_init(). */
struct barectf_milan_ctx *milan_trace_ctx(void);

/* Emit any event with flush arming.  `evt` is the event-record type name from
 * milan_trace.yaml; the remaining arguments are that event's payload, in
 * declaration order.
 *
 *   MILAN_TRACE(link, MILAN_TRACE_SEV_WARN, MILAN_TRACE_SRC_LINKMON,
 *               linkg_stat, link_ctrl, bounce, state, rx, tx, ethrst, grst);
 *
 * The severity is passed to barectf as the common-context member AND fed to the
 * flush arming, so the two can never disagree. */
#define MILAN_TRACE(evt, sev, src, ...)                                     \
    do {                                                                    \
        barectf_milan_trace_##evt(milan_trace_ctx(), (uint8_t)(sev),        \
                                  (uint8_t)(src), __VA_ARGS__);             \
        milan_trace_arm((uint8_t)(sev));                                    \
    } while (0)

/* Same, for the two events with no payload members beyond the common context.
 * (There are none today; kept so a future zero-payload event does not need a
 * different spelling at every call site.) */
#define MILAN_TRACE0(evt, sev, src)                                         \
    do {                                                                    \
        barectf_milan_trace_##evt(milan_trace_ctx(), (uint8_t)(sev),        \
                                  (uint8_t)(src));                          \
        milan_trace_arm((uint8_t)(sev));                                    \
    } while (0)

/* Feed a severity to the flush-arming logic.  Called by the macros above;
 * exposed for producers that call the generated functions directly. */
void milan_trace_arm(uint8_t sev);

/* Non-zero when a flush to /user is DUE: something at MILAN_TRACE_FLUSH_SEV or
 * above has been recorded since the last flush, AND the rate limiter allows one
 * now, AND the flash-wear budget has tokens for it.  The caller (the board
 * daemon) does the compressing and writing. */
int milan_trace_flush_due(void);

/* Why the last milan_trace_flush_due() said no: one of the `flushv` enum values
 * from milan_trace.yaml (0 OK / 4 RATELIMIT / 5 DISABLED) or 6 for "budget
 * exhausted".  Emit it, do not swallow it: a fault log that stops writing for a
 * reason nobody recorded is the same as one that lost the records. */
#define MILAN_TRACE_HOLD_NONE       0u
#define MILAN_TRACE_HOLD_RATELIMIT  4u
#define MILAN_TRACE_HOLD_NOTARMED   5u
#define MILAN_TRACE_HOLD_BUDGET     6u
uint8_t milan_trace_flush_hold(void);

/* Report the bytes the caller actually wrote to /user for the flush it just
 * completed, so the flash-wear budget can refuse the next one.  Call it once
 * per successful flush, with the COMPRESSED size (that is what hits flash). */
void milan_trace_flush_wrote(uint32_t out_bytes);

/* Tokens left in the flash-wear bucket, bytes. */
uint32_t milan_trace_budget_left(void);

/* Force the next milan_trace_flush_due() to return non-zero, ignoring the
 * severity condition but NOT the rate limiter.  For "flush before I reboot"
 * and for the bench recipe. */
void milan_trace_flush_request(void);

/* ---- segments ---------------------------------------------------------- */

/* Take a segment: close the in-progress packet so the segment ends on a packet
 * boundary, then hand back the complete packets that have not been taken yet,
 * oldest first, up to `max_packets` (0 = MILAN_TRACE_SEGMENT_PACKETS).
 *
 * Returns the number of packets in the segment (0 if there is nothing to take).
 * The packets stay in the ring and stay readable until the ring laps them; the
 * caller must consume them with milan_trace_segment_packet() BEFORE emitting
 * further records, or a busy producer can overwrite a slot mid-compression.
 * That constraint is the price of a zero-copy ring and it is why
 * milan_trace_segment_end() reports how many slots were overwritten. */
uint32_t milan_trace_segment_begin(uint32_t max_packets);

/* Pointer to packet `i` (0 .. count-1) of the segment taken above.
 * Always exactly cfg.packet_bytes long: CTF packets are padded to the buffer
 * size and the packet context carries the real content_size, which is what
 * makes a fixed-size slot legal and a partial read decodable. */
const uint8_t *milan_trace_segment_packet(uint32_t i);

/* Close the segment.  `ok` = the caller durably wrote it (fsync + rename);
 * only then does the flush arming reset and the rate limiter restart.
 * Returns the number of segment packets that the producer overwrote while the
 * segment was open - non-zero means the segment the caller just wrote is
 * partly garbage and it should record a trace_drop(RING_FULL). */
uint32_t milan_trace_segment_end(int ok);

/* ---- introspection ----------------------------------------------------- */

void milan_trace_get_stats(struct milan_trace_stats *out);

/* Microseconds since the last heartbeat, for the caller's 60 s timer. */
uint64_t milan_trace_since_heartbeat(void);

/* Tell the tracer a heartbeat was just emitted (the caller emits it, because
 * only the caller knows uptime and which subsystems are armed). */
void milan_trace_heartbeat_done(void);

#ifdef __cplusplus
}
#endif

#endif /* MILAN_TRACE_H */
