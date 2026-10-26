// SPDX-License-Identifier: CERN-OHL-W-2.0
// The AECP owner's platform face on contract 2.3 (see aecp_face.h).
#include "aecp_face.h"
#include "aecp_internal.h"
#include "mbx_wire.h"

// IEEE 1722.1-2021 Table 7-1, and the fields the settings carry (7.2.6, 7.2.32)
enum { STREAM_INPUT = 5u, STREAM_OUTPUT = 6u, AVB_INTERFACE = 9u, CLOCK_DOMAIN = 36u };
#define FORMAT_AT 74u           // a STREAM_INPUT's or STREAM_OUTPUT's current_format
#define INTERFACE_AT 126u       // its avb_interface_index
#define CLOCK_SOURCE_AT 70u     // a CLOCK_DOMAIN's clock_source_index
// the core's override bits (aecp_override): a controller or a restore set the value
#define SET_FORMAT 1u
#define SET_LATENCY 2u

static const struct aecp_descriptor *current(struct aecp_face *f, uint16_t type, uint16_t index)
{
	return aecp_find(f->core, f->core->configuration, type, index);
}

// The interface a stream descriptor belongs to, or MBX_N_IF for none this build has.
static unsigned interface_of(struct aecp_face *f, const struct aecp_descriptor *d)
{
	unsigned i = d->length >= INTERFACE_AT + 2u ? (unsigned)wire_be16(d->value + INTERFACE_AT) : MBX_N_IF;
	return i < f->core->cfg.interfaces ? i : MBX_N_IF;
}

static void write_settings(struct aecp_face *f, unsigned i)
{
	const struct aecp_descriptor *clock = current(f, CLOCK_DOMAIN, 0);
	uint32_t source = clock != NULL && clock->length >= CLOCK_SOURCE_AT + 2u
		? (uint32_t)wire_be16(clock->value + CLOCK_SOURCE_AT) : 0u;
	(void)mbx_face_write(i, MBX_FACE_REG_F_CTRL, mbx_place(f->ready ? 1u : 0u, MBX_F_CTRL_READY_LSB,
							       MBX_F_CTRL_READY_WIDTH));
	(void)mbx_face_write(i, MBX_FACE_REG_F_ENTITY,
			     mbx_place(f->core->configuration, MBX_F_ENTITY_CUR_CONFIG_LSB, MBX_F_ENTITY_CUR_CONFIG_WIDTH) |
			     mbx_place(f->core->identify, MBX_F_ENTITY_IDENTIFY_LSB, MBX_F_ENTITY_IDENTIFY_WIDTH));
	(void)mbx_face_write(i, MBX_FACE_REG_F_CLOCK, mbx_place(source, MBX_F_CLOCK_SOURCE_INDEX_LSB,
								MBX_F_CLOCK_SOURCE_INDEX_WIDTH));
	(void)mbx_face_write(i, MBX_FACE_REG_F_AECP,
			     mbx_place(f->core->locked ? 1u : 0u, MBX_F_AECP_LOCK_HELD_LSB, MBX_F_AECP_LOCK_HELD_WIDTH) |
			     mbx_place(f->dirty ? 1u : 0u, MBX_F_AECP_DYN_DIRTY_LSB, MBX_F_AECP_DYN_DIRTY_WIDTH));
	(void)mbx_face_write(i, MBX_FACE_REG_F_RESTORE, f->restore);
	(void)mbx_face_write(i, MBX_FACE_REG_F_NVM, f->nvm);
}

// A stream's entry: a sink's format, a source's format and presentation time
// offset, each beside whether a controller or the saved state set it. d names
// an interface (interface_of), so it is long enough to hold its format.
static void write_stream(struct aecp_face *f, unsigned i, const struct aecp_descriptor *d)
{
	uint64_t format = wire_be64(d->value + FORMAT_AT);
	bool set_format = aecp_overridden(f->core, d, SET_FORMAT);
	if (d->type == STREAM_INPUT) {
		(void)mbx_face_write_sink(i, d->index, MBX_FACE_SNK_REG_F_FMT_IN_LO, (uint32_t)format);
		(void)mbx_face_write_sink(i, d->index, MBX_FACE_SNK_REG_F_FMT_IN_HI, (uint32_t)(format >> 32));
		(void)mbx_face_write_sink(i, d->index, MBX_FACE_SNK_REG_F_SNK_VALID,
					  mbx_place(set_format ? 1u : 0u, MBX_F_SNK_VALID_FMT_IN_LSB, MBX_F_SNK_VALID_FMT_IN_WIDTH));
		return;
	}
	bool set_latency = aecp_overridden(f->core, d, SET_LATENCY);
	(void)mbx_face_write_source(i, d->index, MBX_FACE_SRC_REG_F_PT_OFFSET, f->core->cfg.latency[d->index]);
	(void)mbx_face_write_source(i, d->index, MBX_FACE_SRC_REG_F_FMT_OUT_LO, (uint32_t)format);
	(void)mbx_face_write_source(i, d->index, MBX_FACE_SRC_REG_F_FMT_OUT_HI, (uint32_t)(format >> 32));
	(void)mbx_face_write_source(i, d->index, MBX_FACE_SRC_REG_F_SRC_VALID,
				    mbx_place(set_latency ? 1u : 0u, MBX_F_SRC_VALID_PT_OFFSET_LSB, MBX_F_SRC_VALID_PT_OFFSET_WIDTH) |
				    mbx_place(set_format ? 1u : 0u, MBX_F_SRC_VALID_FMT_OUT_LSB, MBX_F_SRC_VALID_FMT_OUT_WIDTH));
}

// Write what moved on interface i, then commit it and wait for the
// acknowledgement: the settings, every stream entry of the current
// configuration on this interface (every), or one stream's. An interface
// whose earlier commit the datapath has not taken refuses writes: it is owed,
// and the next poll publishes everything.
static void publish(struct aecp_face *f, unsigned i, bool settings, const struct aecp_descriptor *stream, bool every)
{
	if (f->owed[i] || mbx_face_busy(i)) {
		f->owed[i] = true;
		return;
	}
	if (settings) {
		write_settings(f, i);
	}
	for (unsigned k = 0; every && k < MBX_N_PUB_SINKS + MBX_N_PUB_SOURCES; ++k) {
		bool input = k < MBX_N_PUB_SINKS;
		const struct aecp_descriptor *d = current(f, input ? STREAM_INPUT : STREAM_OUTPUT,
							  (uint16_t)(input ? k : k - MBX_N_PUB_SINKS));
		if (d != NULL && interface_of(f, d) == i) {
			write_stream(f, i, d);
		}
	}
	if (stream != NULL) {
		write_stream(f, i, stream);
	}
	if (mbx_face_commit(i) == MBX_STATUS_OK) {
		++f->commits;
	} else {
		++f->late;
		f->owed[i] = true;
	}
}

static void changed(void *ctx, enum aecp_change kind, uint16_t type, uint16_t index)
{
	struct aecp_face *f = ctx;
	// the kinds the saved-state store keeps (aecp_nvm_changed)
	bool persisted = kind != AECP_CHANGE_IDENTIFY && kind != AECP_CHANGE_SYSTEM_ID && kind != AECP_CHANGE_LOCK;
	bool settings = kind == AECP_CHANGE_CONFIGURATION || kind == AECP_CHANGE_IDENTIFY || kind == AECP_CHANGE_LOCK ||
			(kind == AECP_CHANGE_CLOCK && type == CLOCK_DOMAIN && index == 0u) || (persisted && !f->dirty);
	f->dirty = f->dirty || persisted;
	const struct aecp_descriptor *stream = NULL;
	if ((kind == AECP_CHANGE_FORMAT || kind == AECP_CHANGE_LATENCY) && (type == STREAM_INPUT || type == STREAM_OUTPUT)) {
		stream = current(f, type, index);
	}
	unsigned home = stream != NULL ? interface_of(f, stream) : MBX_N_IF;
	for (unsigned i = 0; i < f->core->cfg.interfaces; ++i) {
		if (settings || i == home) {
			publish(f, i, settings, i == home ? stream : NULL, kind == AECP_CHANGE_CONFIGURATION);
		}
	}
}

// One GSI word: kind, selector and ordinal of a descriptor, the proposed format beside them.
static bool gsi(struct aecp_face *f, unsigned interface, unsigned kind, uint16_t type, uint16_t index,
		unsigned sel, unsigned ord, uint64_t proposed, uint64_t *word)
{
	const uint32_t request[4] = {
		mbx_place(type, MBX_GSI_REQ_TYPE_LSB, MBX_GSI_REQ_TYPE_WIDTH) |
			mbx_place(index, MBX_GSI_REQ_INDEX_LSB, MBX_GSI_REQ_INDEX_WIDTH),
		mbx_place(kind, MBX_GSI_SEL_KIND_LSB, MBX_GSI_SEL_KIND_WIDTH) |
			mbx_place(sel, MBX_GSI_SEL_SEL_LSB, MBX_GSI_SEL_SEL_WIDTH) |
			mbx_place(ord, MBX_GSI_SEL_ORD_LSB, MBX_GSI_SEL_ORD_WIDTH),
		(uint32_t)proposed, (uint32_t)(proposed >> 32)};
	if (mbx_win_read(interface, MBX_WIN_GSI, request, word) != MBX_STATUS_OK) {
		++f->unanswered;
		return false;
	}
	return true;
}

// GET_STREAM_INFO's words (the processor's KL_aecp_engine gather face, kind 0):
// 0 flags, 2 stream_id, 3 msrp_accumulated_latency, 4 {dest_mac, failure_code},
// 5 failure_bridge_id, 6 {stream_vlan_id, flags_ex}. Selector 1, the format,
// is the descriptor's own; 7 is the ACMP view's (ctrl_app_aecp.c).
static bool stream(void *ctx, unsigned interface, uint16_t type, uint16_t index, struct aecp_stream_info *out)
{
	struct aecp_face *f = ctx;
	uint64_t w[7] = {0};
	for (unsigned sel = 0; sel < 7u; ++sel) {
		if (sel != 1u && !gsi(f, interface, 0u, type, index, sel, 0u, 0u, &w[sel])) {
			return false;
		}
	}
	out->flags = (uint32_t)w[0];
	out->stream_id = w[2];
	out->latency = (uint32_t)w[3];
	out->dest_mac = w[4] >> 16;
	out->failure_code = (uint8_t)(w[4] >> 8);
	out->failure_bridge_id = w[5];
	out->vlan = (uint16_t)(w[6] >> 48);
	out->flags_ex = (uint32_t)w[6];
	// Milan v1.2 5.3.7.3: an output streams while it declares a Talker Advertise and
	// receives a Listener Ready or Ready Failed, the SRP owner's licence
	out->running = type == STREAM_OUTPUT && mbx_pub_licensed(interface, index);
	return true;
}

// GET_AVB_INFO's words (kind 1): 0 gptp_grandmaster_id, 1 {propagation_delay,
// domain, flags, msrp_mappings_count}, 8 the first msrp_mapping {traffic_class,
// priority, vlan_id}, the SR class A one.
static bool avb(void *ctx, unsigned interface, uint16_t index, struct aecp_avb_info *out)
{
	struct aecp_face *f = ctx;
	uint64_t gm = 0;
	uint64_t info = 0;
	uint64_t map = 0;
	if (!gsi(f, interface, 1u, AVB_INTERFACE, index, 0u, 0u, 0u, &gm) ||
	    !gsi(f, interface, 1u, AVB_INTERFACE, index, 1u, 0u, 0u, &info) ||
	    !gsi(f, interface, 1u, AVB_INTERFACE, index, 8u, 0u, 0u, &map)) {
		return false;
	}
	out->gm_id = gm;
	out->propagation_delay = (uint32_t)(info >> 32);
	out->domain = (uint8_t)(info >> 24);
	out->flags = (uint8_t)(info >> 16);
	out->class_priority = (uint8_t)(map >> 16);
	out->class_vlan = (uint16_t)map;
	return true;
}

// SET_STREAM_FORMAT's verdict (kind 0, selector 15): the low byte must be
// exactly 3, supported and every mapped channel surviving, as the processor's
// CHECK_ARG reads it.
static bool format(void *ctx, uint16_t type, uint16_t index, uint64_t proposed)
{
	struct aecp_face *f = ctx;
	const struct aecp_descriptor *d = current(f, type, index);
	uint64_t verdict = 0;
	return d != NULL && interface_of(f, d) < MBX_N_IF &&
	       gsi(f, interface_of(f, d), 0u, type, index, 15u, 0u, proposed, &verdict) && (verdict & 0xFFu) == 3u;
}

// GET_COUNTERS (IEEE 1722.1-2021 7.4.42): quadlets 0 to 31 of the block, then
// 32, counters_valid.
static bool counters(void *ctx, unsigned interface, uint16_t type, uint16_t index, struct aecp_counters *out)
{
	struct aecp_face *f = ctx;
	uint32_t request[2] = {mbx_place(type, MBX_CTR_REQ_TYPE_LSB, MBX_CTR_REQ_TYPE_WIDTH) |
				       mbx_place(index, MBX_CTR_REQ_INDEX_LSB, MBX_CTR_REQ_INDEX_WIDTH), 0u};
	for (uint32_t word = 0; word <= 32u; ++word) {
		uint64_t v = 0;
		request[1] = mbx_place(word, MBX_CTR_WORD_WORD_LSB, MBX_CTR_WORD_WORD_WIDTH);
		if (mbx_win_read(interface, MBX_WIN_CTR, request, &v) != MBX_STATUS_OK) {
			++f->unanswered;
			return false;
		}
		if (word == 32u) {
			out->valid = (uint32_t)v;
		} else {
			out->value[word] = (uint32_t)v;
		}
	}
	return true;
}

static uint32_t random_value(void *ctx)
{
	struct aecp_face *f = ctx;
	return f->platform->random(f->platform->ctx);
}

static bool path(void *ctx, unsigned interface, uint16_t index, uint64_t *out, size_t capacity, size_t *count)
{
	struct aecp_face *f = ctx;
	return f->platform->path(f->platform->ctx, interface, index, out, capacity, count);
}

void aecp_face_init(struct aecp_face *f, const struct aecp_ports *platform)
{
	memset(f, 0, sizeof *f);
	f->platform = platform;
	f->ports = (struct aecp_ports){.ctx = f, .random = random_value, .stream = stream, .avb = avb, .path = path,
		.counters = counters, .changed = changed, .format = format};
}

void aecp_face_attach(struct aecp_face *f, struct aecp *core)
{
	f->core = core;
}

void aecp_face_status(struct aecp_face *f, uint32_t restore, uint32_t nvm, bool dirty)
{
	bool moved = restore != f->restore || nvm != f->nvm || dirty != f->dirty;
	f->restore = restore;
	f->nvm = nvm;
	f->dirty = dirty;
	for (unsigned i = 0; f->ready && moved && i < f->core->cfg.interfaces; ++i) {
		publish(f, i, true, NULL, false);
	}
}

void aecp_face_open(struct aecp_face *f)
{
	f->ready = true;
	for (unsigned i = 0; i < f->core->cfg.interfaces; ++i) {
		publish(f, i, true, NULL, true);
	}
}

bool aecp_face_poll(struct aecp_face *f)
{
	bool owed = false;
	for (unsigned i = 0; i < f->core->cfg.interfaces; ++i) {
		if (f->owed[i] && !mbx_face_busy(i)) {
			f->owed[i] = false;
			publish(f, i, true, NULL, true);
		}
		owed = owed || f->owed[i];
	}
	return owed;
}
