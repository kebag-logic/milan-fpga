// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// ctrl_plat_leds.h - the two status LEDs the control firmware owns (#1018):
// LD2 "a stream is connected" and LD3 "the clock source is satisfied", read
// from the AECP core's own state and its ports, as GET_STREAM_INFO and
// GET_COUNTERS read them, and written to the status register
// (status_leds_ctrl, sw/litex/usbnet_soc.py).
//
// Header only, and compiled only where the SoC has the register: the map
// header defines CTRL_PLAT_LEDS from the SoC's csr.csv (ctrl_plat_gen.py), so
// an image for a SoC without it compiles none of this.
//
//   LD2  some STREAM_INPUT is bound and receiving: its media locked (IEEE
//        1722.1-2021 7.4.42, STREAM_INPUT counters MEDIA_LOCKED and
//        MEDIA_UNLOCKED); or some STREAM_OUTPUT has a connected Listener. A
//        Milan Talker keeps no ACMP connection_count (Milan v1.2 5.5), so the
//        Listener's SRP registration for the stream, which the stream port
//        reports in flags_ex bit 0 (Milan v1.2 5.4.2.10.2), stands for a
//        connection_count above zero.
//   LD3  CLOCK_DOMAIN 0's clock source (SET_CLOCK_SOURCE, 7.4.23) is
//        INTERNAL; or it is INPUT_STREAM and that STREAM_INPUT is bound with
//        its media locked and the clock domain locked (CLOCK_DOMAIN counters
//        LOCKED and UNLOCKED); or it is EXTERNAL and the clock domain is
//        locked.
//
// A lock state is read from its two counters: each counts the edges into
// its state from an unlocked reset, so the state is locked exactly when
// LOCKED - UNLOCKED is odd, which survives either counter's wrap.
//
// Descriptor offsets are the full descriptors' (IEEE 1722.1-2021 7.2.32 and
// 7.2.9): CLOCK_DOMAIN clock_source_index at 70; CLOCK_SOURCE
// clock_source_type at 72, clock_source_location_type at 82 and
// clock_source_location_index at 84.

#ifndef CTRL_PLAT_LEDS_H
#define CTRL_PLAT_LEDS_H

#include <stdbool.h>
#include <stdint.h>
#include <string.h>

#include "aecp.h"
#include "aecp_internal.h"
#include "../mbx/mbx.h"
#include "../mbx/mbx_wire.h"

#ifdef __cplusplus
extern "C" {
#endif

#define CTRL_PLAT_LEDS_STREAM 0x1u   // LD2
#define CTRL_PLAT_LEDS_CLOCK  0x2u   // LD3
// How often the platform reads and writes them, in milliseconds.
#define CTRL_PLAT_LEDS_PERIOD_MS 250u

enum {
	CTRL_PLAT_LEDS_STREAM_INPUT = 5u, CTRL_PLAT_LEDS_STREAM_OUTPUT = 6u,
	CTRL_PLAT_LEDS_CLOCK_SOURCE = 10u, CTRL_PLAT_LEDS_CLOCK_DOMAIN = 36u,
	CTRL_PLAT_LEDS_INTERNAL = 0u, CTRL_PLAT_LEDS_EXTERNAL = 1u, CTRL_PLAT_LEDS_INPUT_STREAM = 2u,
};

static inline uint16_t ctrl_plat_leds_be16(const uint8_t *p)
{
	return (uint16_t)((unsigned)p[0] << 8 | p[1]);
}

typedef bool (*ctrl_plat_leds_counters_fn)(void *, unsigned, uint16_t, uint16_t, struct aecp_counters *);
typedef bool (*ctrl_plat_leds_stream_fn)(void *, unsigned, uint16_t, uint16_t, struct aecp_stream_info *);

// The platform needs only LOCKED, UNLOCKED and counters_valid. Read those
// three quadlets through the same bounded window GET_COUNTERS uses. Reading
// its other 30 quadlets here exceeded the Arty tick's service cost (#1018).
// The ordinary GET_COUNTERS port and every image without LEDs are unchanged.
static inline bool ctrl_plat_leds_counter_pair(void *ctx, unsigned interface, uint16_t type, uint16_t index,
					     struct aecp_counters *out)
{
	(void)ctx;
	const uint32_t words[] = {0u, 1u, 32u};
	uint32_t request[2] = {mbx_place(type, MBX_CTR_REQ_TYPE_LSB, MBX_CTR_REQ_TYPE_WIDTH) |
				       mbx_place(index, MBX_CTR_REQ_INDEX_LSB, MBX_CTR_REQ_INDEX_WIDTH), 0u};
	for (unsigned n = 0u; n < 3u; ++n) {
		uint64_t value = 0u;
		request[1] = mbx_place(words[n], MBX_CTR_WORD_WORD_LSB, MBX_CTR_WORD_WORD_WIDTH);
		if (mbx_win_read(interface, MBX_WIN_CTR, request, &value) != MBX_STATUS_OK) return false;
		if (words[n] == 32u) out->valid = (uint32_t)value;
		else out->value[words[n]] = (uint32_t)value;
	}
	return true;
}

// The lock state two counters give, quadlets 0 (LOCKED or MEDIA_LOCKED) and 1.
static inline bool ctrl_plat_leds_locked(struct aecp *a, ctrl_plat_leds_counters_fn counters,
				       uint16_t type, uint16_t index)
{
	struct aecp_counters c;
	memset(&c, 0, sizeof c);
	if (!counters(a->ports->ctx, 0u, type, index, &c) || (c.valid & 3u) != 3u) return false;
	return ((c.value[0] - c.value[1]) & 1u) != 0u;
}

static inline bool ctrl_plat_leds_receiving(struct aecp *a, ctrl_plat_leds_counters_fn counters,
					  ctrl_plat_leds_stream_fn stream, uint16_t index)
{
	struct aecp_stream_info s;
	memset(&s, 0, sizeof s);
	s.brief = true;   // bound is all this reads
	if (!stream(a->ports->ctx, 0u, CTRL_PLAT_LEDS_STREAM_INPUT, index, &s) || !s.bound) return false;
	return ctrl_plat_leds_locked(a, counters, CTRL_PLAT_LEDS_STREAM_INPUT, index);
}

static inline bool ctrl_plat_leds_listened(struct aecp *a, ctrl_plat_leds_stream_fn stream, uint16_t index)
{
	struct aecp_stream_info s;
	memset(&s, 0, sizeof s);   // observed whole: flags_ex is not a brief observation's
	return stream(a->ports->ctx, 0u, CTRL_PLAT_LEDS_STREAM_OUTPUT, index, &s) && (s.flags_ex & 1u) != 0u;
}

// LD2 and LD3 as the status register takes them.
static inline uint32_t ctrl_plat_leds_word(struct aecp *a, ctrl_plat_leds_counters_fn counters,
					ctrl_plat_leds_stream_fn stream)
{
	uint32_t word = 0u;
	for (uint16_t i = 0u; aecp_find(a, a->configuration, CTRL_PLAT_LEDS_STREAM_INPUT, i) != NULL; ++i) {
		if (ctrl_plat_leds_receiving(a, counters, stream, i)) {
			word |= CTRL_PLAT_LEDS_STREAM;
			break;
		}
	}
	for (uint16_t i = 0u; (word & CTRL_PLAT_LEDS_STREAM) == 0u &&
	     aecp_find(a, a->configuration, CTRL_PLAT_LEDS_STREAM_OUTPUT, i) != NULL; ++i) {
		if (ctrl_plat_leds_listened(a, stream, i)) word |= CTRL_PLAT_LEDS_STREAM;
	}
	const struct aecp_descriptor *domain = aecp_find(a, a->configuration, CTRL_PLAT_LEDS_CLOCK_DOMAIN, 0u);
	if (domain == NULL || domain->length < 72u) return word;
	uint16_t at = ctrl_plat_leds_be16(domain->value + 70);
	const struct aecp_descriptor *source = aecp_find(a, a->configuration, CTRL_PLAT_LEDS_CLOCK_SOURCE, at);
	if (source == NULL || source->length < 86u) return word;
	uint16_t kind = ctrl_plat_leds_be16(source->value + 72);
	bool domain_locked = kind != CTRL_PLAT_LEDS_INTERNAL &&
			     ctrl_plat_leds_locked(a, counters, CTRL_PLAT_LEDS_CLOCK_DOMAIN, 0u);
	if (kind == CTRL_PLAT_LEDS_INTERNAL) {
		word |= CTRL_PLAT_LEDS_CLOCK;
	} else if (kind == CTRL_PLAT_LEDS_INPUT_STREAM) {
		uint16_t type = ctrl_plat_leds_be16(source->value + 82), index = ctrl_plat_leds_be16(source->value + 84);
		if (type == CTRL_PLAT_LEDS_STREAM_INPUT && ctrl_plat_leds_receiving(a, counters, stream, index) && domain_locked) {
			word |= CTRL_PLAT_LEDS_CLOCK;
		}
	} else if (kind == CTRL_PLAT_LEDS_EXTERNAL && domain_locked) {
		word |= CTRL_PLAT_LEDS_CLOCK;
	}
	return word;
}

#ifdef __cplusplus
}
#endif
#endif
