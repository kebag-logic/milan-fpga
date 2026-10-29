// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// mbx.c - the portable mailbox driver (see mbx.h).
//
// The counters the core owns (RX_TAIL, TX_HEAD, EVT_TAIL) are cached here and
// written back as the doorbell, so a record costs one read of the fabric's
// counter, its words, and one write. mbx_open() takes the cache from the
// registers, so a restart of the firmware resumes where the fabric is.
//
// Every TX record carries the next value of one count over all channels
// (SEQ), which is the order the merge sends them in: a frame committed
// before another leaves before it, whatever channels they are on. The count
// belongs to one run of the firmware; the transmit rings are not readable,
// so a restart cannot resume it, and records a previous run left committed
// are not ordered against the new run's.
//
// A record is never trusted further than the counters allow: a length that
// would run past RX_HEAD, a KIND that is not an RX frame or a length outside
// the channel's limits resynchronises the ring to RX_HEAD, because a record
// whose length cannot be believed leaves no next record to find.

#include "mbx.h"

#include <stddef.h>

#include "mbx_hal.h"
#include "mbx_wire.h"
#ifdef CTRL_MBX_BASE
#include "../plat/mbx_mmio.h"
#endif
#ifdef CTRL_MBX_DMA_BASE
#include "../plat/mbx_dma.h"
#endif

// The window's two accesses. Built for the memory-mapped window
// (CTRL_MBX_BASE), the driver makes each in place, the load or store
// mbx_plat_mmio.c makes (mbx_mmio.h), so a record's words cost no call each
// and its loops keep their registers (#665). Any other build reaches the bus
// through mbx_hal.h. Either way the bus sees the same accesses in the same
// order.
static inline uint32_t mbx_bus_read32(uint32_t byte_offset)
{
#ifdef CTRL_MBX_BASE
	return mbx_mmio_read32(byte_offset);
#else
	return mbx_hal_read32(byte_offset);
#endif
}

static inline void mbx_bus_write32(uint32_t byte_offset, uint32_t value)
{
#ifdef CTRL_MBX_BASE
	mbx_mmio_write32(byte_offset, value);
#else
	mbx_hal_write32(byte_offset, value);
#endif
}

// A received frame's bytes take whole ring words (ring_lanes_store4).
_Static_assert(offsetof(struct mbx_frame, bytes) % 4u == 0u && _Alignof(struct mbx_frame) % 4u == 0u,
	       "a frame's bytes start on a word");

static const uint32_t rx_base[MBX_N_CH] = MBX_CH_RX_BASE_TBL;
static const uint32_t rx_words[MBX_N_CH] = MBX_CH_RX_WORDS_TBL;
static const uint32_t tx_base[MBX_N_CH] = MBX_CH_TX_BASE_TBL;
static const uint32_t tx_words[MBX_N_CH] = MBX_CH_TX_WORDS_TBL;
static const uint32_t max_frame[MBX_N_CH] = MBX_CH_MAX_FRAME_BYTES_TBL;

static uint16_t rx_tail[MBX_N_CH];
static uint16_t tx_head[MBX_N_CH];
static uint16_t tx_seq;
static uint16_t evt_tail;

static uint32_t ch_reg(unsigned ch, uint32_t reg)
{
	return MBX_CH_BASE + MBX_CH_STRIDE * (uint32_t)ch + reg;
}

static uint32_t if_reg(unsigned interface, uint32_t reg)
{
	return MBX_IF_BASE + MBX_IF_STRIDE * (uint32_t)interface + reg;
}

static uint32_t iff_reg(unsigned interface, uint32_t reg)
{
	return MBX_IFF_BASE + MBX_IFF_STRIDE * (uint32_t)interface + reg;
}

static uint32_t bnd_reg(unsigned interface, unsigned entry, uint32_t reg)
{
	return MBX_BND_BASE + MBX_BND_STRIDE * (uint32_t)interface + MBX_BND_ENTRY_STRIDE * (uint32_t)entry + reg;
}

static uint16_t counter(uint32_t byte_offset)
{
	return (uint16_t)mbx_field(mbx_bus_read32(byte_offset), 0u, MBX_INDEX_BITS);
}

static bool caps_match(uint32_t id, uint32_t caps)
{
	return mbx_field(id, MBX_ID_MAGIC_LSB, MBX_ID_MAGIC_WIDTH) == MBX_MAGIC &&
	       mbx_field(id, MBX_ID_MAJOR_LSB, MBX_ID_MAJOR_WIDTH) == MBX_VERSION_MAJOR &&
	       mbx_field(caps, MBX_CAPS_N_CH_LSB, MBX_CAPS_N_CH_WIDTH) == MBX_N_CH &&
	       mbx_field(caps, MBX_CAPS_N_IF_LSB, MBX_CAPS_N_IF_WIDTH) == MBX_N_IF &&
	       mbx_field(caps, MBX_CAPS_N_TIMERS_LSB, MBX_CAPS_N_TIMERS_WIDTH) == MBX_N_TIMERS &&
	       (1u << mbx_field(caps, MBX_CAPS_EVT_WORDS_LOG2_LSB, MBX_CAPS_EVT_WORDS_LOG2_WIDTH)) == MBX_EVT_WORDS;
}

bool mbx_open(void)
{
	if (!caps_match(mbx_bus_read32(MBX_REG_ID), mbx_bus_read32(MBX_REG_CAPS))) {
		return false;
	}
	for (unsigned ch = 0; ch < MBX_N_CH; ++ch) {
		rx_tail[ch] = counter(ch_reg(ch, MBX_CH_REG_RX_TAIL));
		tx_head[ch] = counter(ch_reg(ch, MBX_CH_REG_TX_HEAD));
	}
	evt_tail = counter(MBX_REG_EVT_TAIL);
	return true;
}

void mbx_filter_set_own_eid(uint64_t entity_id)
{
	mbx_bus_write32(MBX_REG_OWN_EID_LO, (uint32_t)entity_id);
	mbx_bus_write32(MBX_REG_OWN_EID_HI, (uint32_t)(entity_id >> 32));
}

void mbx_filter_open(uint32_t channel_mask)
{
	mbx_bus_write32(MBX_REG_FILTER_EN, mbx_place(channel_mask, MBX_FILTER_EN_OPEN_LSB, MBX_FILTER_EN_OPEN_WIDTH));
}

void mbx_filter_set_maap_range(uint64_t base, uint16_t count)
{
	mbx_bus_write32(MBX_REG_MAAP_BASE_LO, (uint32_t)base);
	mbx_bus_write32(MBX_REG_MAAP_BASE_HI,
			mbx_place((uint32_t)(base >> 32), MBX_MAAP_BASE_HI_ADDR_LSB, MBX_MAAP_BASE_HI_ADDR_WIDTH));
	mbx_bus_write32(MBX_REG_MAAP_COUNT, mbx_place(count, MBX_MAAP_COUNT_COUNT_LSB, MBX_MAAP_COUNT_COUNT_WIDTH));
}

bool mbx_filter_set_own_mac(unsigned interface, uint64_t mac)
{
	if (interface >= MBX_N_IF) {
		return false;
	}
	mbx_bus_write32(iff_reg(interface, MBX_IFF_REG_OWN_MAC_LO),
			mbx_place((uint32_t)mac, MBX_OWN_MAC_LO_MAC_LSB, MBX_OWN_MAC_LO_MAC_WIDTH));
	mbx_bus_write32(iff_reg(interface, MBX_IFF_REG_OWN_MAC_HI),
			mbx_place((uint32_t)(mac >> 32), MBX_OWN_MAC_HI_MAC_LSB, MBX_OWN_MAC_HI_MAC_WIDTH));
	return true;
}

bool mbx_filter_set_bound_talker(unsigned interface, unsigned entry, bool bound, uint64_t talker_entity_id)
{
	if (interface >= MBX_N_IF || entry >= MBX_N_BOUND) {
		return false;
	}
	mbx_bus_write32(bnd_reg(interface, entry, MBX_BND_REG_BOUND_EN), 0u);
	if (bound) {
		mbx_bus_write32(bnd_reg(interface, entry, MBX_BND_REG_BOUND_EID_LO),
				mbx_place((uint32_t)talker_entity_id, MBX_BOUND_EID_LO_EID_LSB, MBX_BOUND_EID_LO_EID_WIDTH));
		mbx_bus_write32(bnd_reg(interface, entry, MBX_BND_REG_BOUND_EID_HI),
				mbx_place((uint32_t)(talker_entity_id >> 32), MBX_BOUND_EID_HI_EID_LSB,
					  MBX_BOUND_EID_HI_EID_WIDTH));
		mbx_bus_write32(bnd_reg(interface, entry, MBX_BND_REG_BOUND_EN),
				mbx_place(1u, MBX_BOUND_EN_EN_LSB, MBX_BOUND_EN_EN_WIDTH));
	}
	return true;
}

// Register `reg` of interface i's publication block, and of its sink k.
static uint32_t pub_reg(unsigned i, uint32_t reg)
{
	return MBX_PUB_BASE + MBX_PUB_STRIDE * i + reg;
}

static uint32_t pub_sink_reg(unsigned i, unsigned k, uint32_t reg)
{
	return pub_reg(i, MBX_PUB_SINK_BASE + MBX_PUB_SINK_STRIDE * k + reg);
}

bool mbx_pub_da_gate(unsigned interface, uint32_t open)
{
	if (interface >= MBX_N_IF) {
		return false;
	}
	mbx_bus_write32(pub_reg(interface, MBX_PUB_REG_DA_GATE),
			mbx_place(open, MBX_DA_GATE_OPEN_LSB, MBX_DA_GATE_OPEN_WIDTH));
	return true;
}

bool mbx_pub_licence(unsigned interface, uint32_t active)
{
	if (interface >= MBX_N_IF) {
		return false;
	}
	mbx_bus_write32(pub_reg(interface, MBX_PUB_REG_LICENCE),
			mbx_place(active, MBX_LICENCE_ACTIVE_LSB, MBX_LICENCE_ACTIVE_WIDTH));
	return true;
}

bool mbx_pub_idle_slope(unsigned interface, uint32_t bps)
{
	if (interface >= MBX_N_IF) {
		return false;
	}
	mbx_bus_write32(pub_reg(interface, MBX_PUB_REG_IDLE_SLOPE),
			mbx_place(bps, MBX_IDLE_SLOPE_BPS_LSB, MBX_IDLE_SLOPE_BPS_WIDTH));
	return true;
}

bool mbx_pub_domain(unsigned interface, bool adopted, uint8_t priority, uint16_t vid)
{
	if (interface >= MBX_N_IF) {
		return false;
	}
	mbx_bus_write32(pub_reg(interface, MBX_PUB_REG_SR_DOMAIN),
			mbx_place(vid, MBX_SR_DOMAIN_VID_LSB, MBX_SR_DOMAIN_VID_WIDTH) |
			mbx_place(priority, MBX_SR_DOMAIN_PRIORITY_LSB, MBX_SR_DOMAIN_PRIORITY_WIDTH) |
			mbx_place(adopted ? 1u : 0u, MBX_SR_DOMAIN_ADOPTED_LSB, MBX_SR_DOMAIN_ADOPTED_WIDTH));
	return true;
}

bool mbx_pub_talker_decl(unsigned interface, uint32_t declared)
{
	if (interface >= MBX_N_IF) {
		return false;
	}
	mbx_bus_write32(pub_reg(interface, MBX_PUB_REG_TALKER_DECL),
			mbx_place(declared, MBX_TALKER_DECL_DECLARED_LSB, MBX_TALKER_DECL_DECLARED_WIDTH));
	return true;
}

// BINDING's BOUND and STARTED, SID_VALID clear.
static uint32_t binding_of(bool bound, bool started)
{
	return mbx_place(bound ? 1u : 0u, MBX_BINDING_BOUND_LSB, MBX_BINDING_BOUND_WIDTH) |
	       mbx_place(started ? 1u : 0u, MBX_BINDING_STARTED_LSB, MBX_BINDING_STARTED_WIDTH);
}

bool mbx_pub_sink(unsigned interface, unsigned sink, bool bound, bool started, uint64_t stream_id)
{
	if (interface >= MBX_N_IF || sink >= MBX_N_PUB_SINKS) {
		return false;
	}
	uint32_t binding = binding_of(bound, started);
	mbx_bus_write32(pub_sink_reg(interface, sink, MBX_PUB_SINK_REG_BINDING), binding);
	if (stream_id != 0u) {
		mbx_bus_write32(pub_sink_reg(interface, sink, MBX_PUB_SINK_REG_SID_LO),
				mbx_place((uint32_t)stream_id, MBX_SID_LO_SID_LSB, MBX_SID_LO_SID_WIDTH));
		mbx_bus_write32(pub_sink_reg(interface, sink, MBX_PUB_SINK_REG_SID_HI),
				mbx_place((uint32_t)(stream_id >> 32), MBX_SID_HI_SID_LSB, MBX_SID_HI_SID_WIDTH));
		mbx_bus_write32(pub_sink_reg(interface, sink, MBX_PUB_SINK_REG_BINDING),
				binding | mbx_place(1u, MBX_BINDING_SID_VALID_LSB, MBX_BINDING_SID_VALID_WIDTH));
	}
	return true;
}

bool mbx_pub_sink_binding(unsigned interface, unsigned sink, bool bound, bool started, bool sid_valid)
{
	if (interface >= MBX_N_IF || sink >= MBX_N_PUB_SINKS) {
		return false;
	}
	mbx_bus_write32(pub_sink_reg(interface, sink, MBX_PUB_SINK_REG_BINDING),
			binding_of(bound, started) |
			mbx_place(sid_valid ? 1u : 0u, MBX_BINDING_SID_VALID_LSB, MBX_BINDING_SID_VALID_WIDTH));
	return true;
}

bool mbx_pub_licensed(unsigned interface, unsigned source)
{
	return interface < MBX_N_IF && source < MBX_N_PUB_SOURCES &&
	       ((mbx_field(mbx_bus_read32(pub_reg(interface, MBX_PUB_REG_LICENCE)), MBX_LICENCE_ACTIVE_LSB,
			   MBX_LICENCE_ACTIVE_WIDTH) >> source) & 1u) != 0u;
}

// ---- the face block (contract 2.3) ---------------------------------------------

static uint32_t face_reg(unsigned interface, uint32_t reg)
{
	return MBX_FACE_BASE + MBX_FACE_STRIDE * (uint32_t)interface + reg;
}

bool mbx_face_write(unsigned interface, uint32_t reg, uint32_t value)
{
	if (interface >= MBX_N_IF) {
		return false;
	}
	mbx_bus_write32(face_reg(interface, reg), value);
	return true;
}

bool mbx_face_write_source(unsigned interface, unsigned source, uint32_t reg, uint32_t value)
{
	if (source >= MBX_N_PUB_SOURCES) {
		return false;
	}
	return mbx_face_write(interface, MBX_FACE_SOURCE_BASE + MBX_FACE_SOURCE_STRIDE * (uint32_t)source + reg, value);
}

bool mbx_face_write_sink(unsigned interface, unsigned sink, uint32_t reg, uint32_t value)
{
	if (sink >= MBX_N_PUB_SINKS) {
		return false;
	}
	return mbx_face_write(interface, MBX_FACE_SINK_BASE + MBX_FACE_SINK_STRIDE * (uint32_t)sink + reg, value);
}

bool mbx_face_busy(unsigned interface)
{
	return interface < MBX_N_IF &&
	       mbx_field(mbx_bus_read32(face_reg(interface, MBX_FACE_REG_F_STATUS)), MBX_F_STATUS_BUSY_LSB,
			 MBX_F_STATUS_BUSY_WIDTH) != 0u;
}

enum mbx_status mbx_face_commit(unsigned interface)
{
	if (interface >= MBX_N_IF) {
		return MBX_STATUS_BAD;
	}
	if (mbx_face_busy(interface)) {
		return MBX_STATUS_FULL;
	}
	mbx_bus_write32(face_reg(interface, MBX_FACE_REG_F_COMMIT), mbx_place(1u, MBX_F_COMMIT_GO_LSB, MBX_F_COMMIT_GO_WIDTH));
	for (uint32_t k = 0; k <= MBX_FACE_ACK_CYCLES; ++k) {
		if (!mbx_face_busy(interface)) {
			return MBX_STATUS_OK;
		}
	}
	return MBX_STATUS_BAD;
}

// One window's registers, offsets inside an interface's block, in the contract's order.
struct window {
	uint32_t go;
	uint32_t status;
	uint32_t data_lo;
	uint32_t data_hi;  // data_hi == data_lo: a one-word answer
	uint32_t wait_cycles;
	uint32_t request[MBX_WIN_REQUEST_WORDS];
	unsigned words;
};
static const struct window windows[MBX_WINDOWS] = {
	{MBX_FACE_REG_CTR_CMD, MBX_FACE_REG_CTR_STATUS, MBX_FACE_REG_CTR_DATA, MBX_FACE_REG_CTR_DATA,
	 MBX_WIN_CTR_WAIT_CYCLES, {MBX_FACE_REG_CTR_REQ, MBX_FACE_REG_CTR_WORD}, 2},
	{MBX_FACE_REG_AMAP_CMD, MBX_FACE_REG_AMAP_STATUS, MBX_FACE_REG_AMAP_DATA_LO, MBX_FACE_REG_AMAP_DATA_HI,
	 MBX_WIN_AMAP_WAIT_CYCLES, {MBX_FACE_REG_AMAP_REQ, MBX_FACE_REG_AMAP_PAGE}, 2},
	{MBX_FACE_REG_EDIT_CMD, MBX_FACE_REG_EDIT_STATUS, MBX_FACE_REG_EDIT_DATA_LO, MBX_FACE_REG_EDIT_DATA_HI,
	 MBX_WIN_EDIT_WAIT_CYCLES, {MBX_FACE_REG_EDIT_REQ, MBX_FACE_REG_EDIT_BEAT, MBX_FACE_REG_EDIT_RECORD_LO,
				    MBX_FACE_REG_EDIT_RECORD_HI, MBX_FACE_REG_EDIT_VALUE_LO, MBX_FACE_REG_EDIT_VALUE_HI}, 6},
	{MBX_FACE_REG_GSI_CMD, MBX_FACE_REG_GSI_STATUS, MBX_FACE_REG_GSI_DATA_LO, MBX_FACE_REG_GSI_DATA_HI,
	 MBX_WIN_GSI_WAIT_CYCLES, {MBX_FACE_REG_GSI_REQ, MBX_FACE_REG_GSI_SEL, MBX_FACE_REG_GSI_PROP_LO,
				   MBX_FACE_REG_GSI_PROP_HI}, 4},
};
// every window's CMD and STATUS have CTR_CMD's and CTR_STATUS's layout (the contract's checks)
#define WIN_BUSY(s) (mbx_field((s), MBX_CTR_STATUS_BUSY_LSB, MBX_CTR_STATUS_BUSY_WIDTH) != 0u)
#define WIN_DONE(s) (mbx_field((s), MBX_CTR_STATUS_DONE_LSB, MBX_CTR_STATUS_DONE_WIDTH) != 0u)

enum mbx_status mbx_win_read(unsigned interface, unsigned window, const uint32_t *request, uint64_t *data)
{
	if (interface >= MBX_N_IF || window >= MBX_WINDOWS) {
		return MBX_STATUS_BAD;
	}
	const struct window *w = &windows[window];
	if (WIN_BUSY(mbx_bus_read32(face_reg(interface, w->status)))) {
		return MBX_STATUS_FULL;
	}
	for (unsigned k = 0; k < w->words; ++k) {
		mbx_bus_write32(face_reg(interface, w->request[k]), request[k]);
	}
	mbx_bus_write32(face_reg(interface, w->go), mbx_place(1u, MBX_CTR_CMD_GO_LSB, MBX_CTR_CMD_GO_WIDTH));
	for (uint32_t k = 0; k <= w->wait_cycles; ++k) {
		uint32_t s = mbx_bus_read32(face_reg(interface, w->status));
		if (!WIN_BUSY(s)) {
			if (!WIN_DONE(s)) {
				return MBX_STATUS_EMPTY;
			}
			uint64_t hi = w->data_hi == w->data_lo ? 0u : mbx_bus_read32(face_reg(interface, w->data_hi));
			*data = (hi << 32) | mbx_bus_read32(face_reg(interface, w->data_lo));
			return MBX_STATUS_OK;
		}
	}
	return MBX_STATUS_EMPTY;
}

uint16_t mbx_filter_mismatch(void)
{
	return (uint16_t)mbx_field(mbx_bus_read32(MBX_REG_FILTER_MISMATCH), MBX_FILTER_MISMATCH_COUNT_LSB,
				   MBX_FILTER_MISMATCH_COUNT_WIDTH);
}

static uint32_t rx_word(unsigned ch, uint32_t index)
{
	return mbx_bus_read32(rx_base[ch] + 4u * (index & (rx_words[ch] - 1u)));
}

// Release everything up to RX_HEAD.
static enum mbx_status rx_resync(unsigned ch, uint16_t head)
{
	rx_tail[ch] = head;
	mbx_bus_write32(ch_reg(ch, MBX_CH_REG_RX_TAIL), head);
	return MBX_STATUS_BAD;
}

enum mbx_status mbx_rx_take(unsigned ch, struct mbx_frame *f)
{
	if (ch >= MBX_N_CH) {
		return MBX_STATUS_BAD;
	}
	uint16_t head = counter(ch_reg(ch, MBX_CH_REG_RX_HEAD));
	uint16_t tail = rx_tail[ch];
	uint32_t occupied = (uint16_t)(head - tail);
	if (occupied == 0u) {
		return MBX_STATUS_EMPTY;
	}
	uint32_t w0 = rx_word(ch, tail);
	uint32_t w1 = rx_word(ch, (uint32_t)tail + 1u);
	uint32_t len = mbx_field(w0, MBX_RXREC_W0_LEN_LSB, MBX_RXREC_W0_LEN_WIDTH);
	uint32_t payload = (len + 3u) / 4u;
	uint32_t record = MBX_RX_HDR_WORDS + payload;
	if (mbx_field(w0, MBX_RXREC_W0_KIND_LSB, MBX_RXREC_W0_KIND_WIDTH) != MBX_RX_KIND || len < 14u ||
	    len > max_frame[ch] || occupied > rx_words[ch] || record > occupied) {
		return rx_resync(ch, head);
	}
#ifdef CTRL_MBX_DMA_BASE
	// The split placement's record mover copies the payload (mbx_dma.h); a
	// move that ends in error leaves no record to trust.
	if (!mbx_dma_move(rx_base[ch], rx_words[ch], (uint32_t)tail + MBX_RX_HDR_WORDS, f->bytes, len, false)) {
		return rx_resync(ch, head);
	}
#else
	// The payload's words in ring order, each whole word but a short last one,
	// a whole word stored at once (the frame's bytes start on a word).
	const uint32_t base = rx_base[ch];
	const uint32_t mask = rx_words[ch] - 1u;
	uint32_t at = (uint32_t)tail + MBX_RX_HDR_WORDS;
	uint8_t *p = f->bytes;
	for (uint32_t whole = len / 4u; whole != 0u; --whole, ++at, p += 4) {
		ring_lanes_store4(mbx_bus_read32(base + 4u * (at & mask)), p);
	}
	if (len % 4u != 0u) {
		ring_lanes_unpack(mbx_bus_read32(base + 4u * (at & mask)), p, len % 4u);
	}
#endif
	f->len = (uint16_t)len;
	f->interface = (uint8_t)mbx_field(w0, MBX_RXREC_W0_IF_LSB, MBX_RXREC_W0_IF_WIDTH);
	f->arrival_ms = mbx_field(w1, MBX_RXREC_W1_ARRIVAL_MS_LSB, MBX_RXREC_W1_ARRIVAL_MS_WIDTH);
	rx_tail[ch] = (uint16_t)(tail + record);
	mbx_bus_write32(ch_reg(ch, MBX_CH_REG_RX_TAIL), rx_tail[ch]);
	return MBX_STATUS_OK;
}

uint16_t mbx_rx_mark(unsigned ch)
{
    return ch < MBX_N_CH ? counter(ch_reg(ch, MBX_CH_REG_RX_HEAD)) : 0u;
}

bool mbx_rx_before(unsigned ch, uint16_t mark)
{
    return ch < MBX_N_CH && (uint16_t)(mark - rx_tail[ch]) < 0x8000u;
}

static void tx_word(unsigned ch, uint32_t index, uint32_t value)
{
	mbx_bus_write32(tx_base[ch] + 4u * (index & (tx_words[ch] - 1u)), value);
}

// The payload's words in ring order from ring index at, each whole word but a
// short last one; a frame that starts on a word gives each whole word in one
// load. The two loops stay apart, or the compiler takes the byte form for
// both.
static inline void tx_payload(unsigned ch, uint32_t at, const uint8_t *frame, uint16_t len)
{
	const uint32_t base = tx_base[ch];
	const uint32_t mask = tx_words[ch] - 1u;
	const uint8_t *p = frame;
	if (((uintptr_t)frame & 3u) == 0u) {
		for (uint32_t whole = len / 4u; whole != 0u; --whole, ++at, p += 4) {
			mbx_bus_write32(base + 4u * (at & mask), ring_lanes_load4(p));
		}
	} else {
		for (uint32_t whole = len / 4u; whole != 0u; --whole, ++at, p += 4) {
			mbx_bus_write32(base + 4u * (at & mask), ring_lanes_pack4(p));
		}
	}
	if (len % 4u != 0u) {
		mbx_bus_write32(base + 4u * (at & mask), ring_lanes_pack(p, len % 4u));
	}
}

enum mbx_status mbx_tx_send(unsigned ch, unsigned interface, const uint8_t *frame, uint16_t len)
{
	if (ch >= MBX_N_CH || interface >= MBX_N_IF || len < 14u || len > max_frame[ch]) {
		return MBX_STATUS_BAD;
	}
	uint32_t payload = ((uint32_t)len + 3u) / 4u;
	uint32_t record = MBX_TX_HDR_WORDS + payload;
	uint16_t head = tx_head[ch];
	uint16_t tail = counter(ch_reg(ch, MBX_CH_REG_TX_TAIL));
	uint32_t used = (uint16_t)(head - tail);
	if (used > tx_words[ch] || record > tx_words[ch] - used) {
		return MBX_STATUS_FULL;
	}
	tx_word(ch, head, mbx_place(len, MBX_TXREC_W0_LEN_LSB, MBX_TXREC_W0_LEN_WIDTH) |
				  mbx_place(interface, MBX_TXREC_W0_IF_LSB, MBX_TXREC_W0_IF_WIDTH) |
				  mbx_place(MBX_TX_KIND, MBX_TXREC_W0_KIND_LSB, MBX_TXREC_W0_KIND_WIDTH));
	tx_word(ch, (uint32_t)head + 1u, mbx_place(tx_seq, MBX_TXREC_W1_SEQ_LSB, MBX_TXREC_W1_SEQ_WIDTH));
	const uint32_t at = (uint32_t)head + MBX_TX_HDR_WORDS;
#ifdef CTRL_MBX_DMA_BASE
	// The split placement's record mover takes a frame on a word (mbx_dma.h);
	// a record whose payload did not reach the ring is not committed.
	if (((uintptr_t)frame & 3u) == 0u) {
		if (!mbx_dma_move(tx_base[ch], tx_words[ch], at, frame, len, true)) {
			return MBX_STATUS_BAD;
		}
	} else {
		tx_payload(ch, at, frame, len);
	}
#else
	tx_payload(ch, at, frame, len);
#endif
	tx_head[ch] = (uint16_t)(head + record);
	tx_seq = (uint16_t)(tx_seq + 1u);
	mbx_bus_write32(ch_reg(ch, MBX_CH_REG_TX_HEAD), tx_head[ch]);
	return MBX_STATUS_OK;
}

static uint32_t evt_word(uint32_t index)
{
	return mbx_bus_read32(MBX_EVT_BASE + 4u * (index & (MBX_EVT_WORDS - 1u)));
}

static void event_decode_timer(struct mbx_event *ev, uint32_t w1, uint32_t w2, uint32_t w3)
{
	ev->timer_tag = (uint16_t)mbx_field(w1, MBX_EV_TIMER_W1_TAG_LSB, MBX_EV_TIMER_W1_TAG_WIDTH);
	ev->timer_slot = (uint8_t)mbx_field(w1, MBX_EV_TIMER_W1_SLOT_LSB, MBX_EV_TIMER_W1_SLOT_WIDTH);
	ev->deadline_ms = mbx_field(w2, MBX_EV_TIMER_W2_DEADLINE_MS_LSB, MBX_EV_TIMER_W2_DEADLINE_MS_WIDTH);
	ev->now_ms = mbx_field(w3, MBX_EV_TIMER_W3_NOW_MS_LSB, MBX_EV_TIMER_W3_NOW_MS_WIDTH);
}

static void event_decode(struct mbx_event *ev, uint32_t w1, uint32_t w2, uint32_t w3)
{
	if (ev->type == MBX_EV_TYPE_TIMER) {
		event_decode_timer(ev, w1, w2, w3);
	} else if (ev->type == MBX_EV_TYPE_LINK) {
		ev->link_up = mbx_field(w1, MBX_EV_LINK_W1_UP_LSB, MBX_EV_LINK_W1_UP_WIDTH) != 0u;
		ev->now_ms = mbx_field(w3, MBX_EV_LINK_W3_NOW_MS_LSB, MBX_EV_LINK_W3_NOW_MS_WIDTH);
	} else if (ev->type == MBX_EV_TYPE_GM) {
		ev->gm_id = ((uint64_t)mbx_field(w2, MBX_EV_GM_W2_ID_HI_LSB, MBX_EV_GM_W2_ID_HI_WIDTH) << 32) |
			    (uint64_t)mbx_field(w1, MBX_EV_GM_W1_ID_LO_LSB, MBX_EV_GM_W1_ID_LO_WIDTH);
		ev->domain = (uint8_t)mbx_field(w3, MBX_EV_GM_W3_DOMAIN_LSB, MBX_EV_GM_W3_DOMAIN_WIDTH);
	} else if (ev->type == MBX_EV_TYPE_TICK) {
		ev->tick_count = (uint16_t)mbx_field(w1, MBX_EV_TICK_W1_COUNT_LSB, MBX_EV_TICK_W1_COUNT_WIDTH);
		ev->now_ms = mbx_field(w3, MBX_EV_TICK_W3_NOW_MS_LSB, MBX_EV_TICK_W3_NOW_MS_WIDTH);
	} else if (ev->type == MBX_EV_TYPE_COUNTERS_CHANGED) {
		ev->desc_type = (uint16_t)mbx_field(w1, MBX_EV_COUNTERS_CHANGED_W1_TYPE_LSB,
						    MBX_EV_COUNTERS_CHANGED_W1_TYPE_WIDTH);
		ev->desc_index = (uint16_t)mbx_field(w1, MBX_EV_COUNTERS_CHANGED_W1_INDEX_LSB,
						     MBX_EV_COUNTERS_CHANGED_W1_INDEX_WIDTH);
		ev->every = mbx_field(w2, MBX_EV_COUNTERS_CHANGED_W2_ALL_LSB, MBX_EV_COUNTERS_CHANGED_W2_ALL_WIDTH) != 0u;
		ev->now_ms = mbx_field(w3, MBX_EV_COUNTERS_CHANGED_W3_NOW_MS_LSB, MBX_EV_COUNTERS_CHANGED_W3_NOW_MS_WIDTH);
	} else if (ev->type == MBX_EV_TYPE_AVB_INFO_CHANGED || ev->type == MBX_EV_TYPE_AS_PATH_CHANGED ||
		   ev->type == MBX_EV_TYPE_AMAP_LIVE_WRITE) {
		// AVB_INFO_CHANGED, AS_PATH_CHANGED and AMAP_LIVE_WRITE share one layout;
		// a type the contract does not define decodes no field
		_Static_assert(MBX_EV_AVB_INFO_CHANGED_W1_COUNT_LSB == MBX_EV_AMAP_LIVE_WRITE_W1_COUNT_LSB &&
				       MBX_EV_AS_PATH_CHANGED_W1_COUNT_LSB == MBX_EV_AMAP_LIVE_WRITE_W1_COUNT_LSB &&
				       MBX_EV_AVB_INFO_CHANGED_W1_COUNT_WIDTH == MBX_EV_AMAP_LIVE_WRITE_W1_COUNT_WIDTH &&
				       MBX_EV_AS_PATH_CHANGED_W1_COUNT_WIDTH == MBX_EV_AMAP_LIVE_WRITE_W1_COUNT_WIDTH,
			       "the counted face events share COUNT's place");
		ev->count = (uint16_t)mbx_field(w1, MBX_EV_AMAP_LIVE_WRITE_W1_COUNT_LSB, MBX_EV_AMAP_LIVE_WRITE_W1_COUNT_WIDTH);
		ev->now_ms = w3;
	}
}

bool mbx_event_take(struct mbx_event *ev)
{
	uint16_t head = counter(MBX_REG_EVT_HEAD);
	if (head == evt_tail) {
		return false;
	}
	uint32_t w0 = evt_word(evt_tail);
	uint32_t w1 = evt_word((uint32_t)evt_tail + 1u);
	uint32_t w2 = evt_word((uint32_t)evt_tail + 2u);
	uint32_t w3 = evt_word((uint32_t)evt_tail + 3u);
	*ev = (struct mbx_event){0};
	ev->type = (uint8_t)mbx_field(w0, MBX_EVREC_W0_TYPE_LSB, MBX_EVREC_W0_TYPE_WIDTH);
	ev->interface = (uint8_t)mbx_field(w0, MBX_EVREC_W0_IF_LSB, MBX_EVREC_W0_IF_WIDTH);
	ev->seq = (uint16_t)mbx_field(w0, MBX_EVREC_W0_SEQ_LSB, MBX_EVREC_W0_SEQ_WIDTH);
	event_decode(ev, w1, w2, w3);
	evt_tail = (uint16_t)(evt_tail + MBX_EV_WORDS);
	mbx_bus_write32(MBX_REG_EVT_TAIL, evt_tail);
	return true;
}

uint32_t mbx_now_ms(void)
{
	return mbx_bus_read32(MBX_REG_NOW_MS);
}

void mbx_timer_arm(unsigned slot, uint16_t tag, uint32_t deadline_ms)
{
	mbx_bus_write32(MBX_REG_TMR_DEADLINE, deadline_ms);
	mbx_bus_write32(MBX_REG_TMR_CMD, mbx_place(slot, MBX_TMR_CMD_SLOT_LSB, MBX_TMR_CMD_SLOT_WIDTH) |
					 mbx_place(tag, MBX_TMR_CMD_TAG_LSB, MBX_TMR_CMD_TAG_WIDTH) |
					 mbx_place(MBX_TMR_OP_ARM, MBX_TMR_CMD_OP_LSB, MBX_TMR_CMD_OP_WIDTH));
}

void mbx_timer_cancel(unsigned slot)
{
	mbx_bus_write32(MBX_REG_TMR_CMD, mbx_place(slot, MBX_TMR_CMD_SLOT_LSB, MBX_TMR_CMD_SLOT_WIDTH) |
					 mbx_place(MBX_TMR_OP_CANCEL, MBX_TMR_CMD_OP_LSB, MBX_TMR_CMD_OP_WIDTH));
}

void mbx_tick_enable(bool enable)
{
	mbx_bus_write32(MBX_REG_TICK_CTL, mbx_place(enable ? 1u : 0u, MBX_TICK_CTL_EN_LSB, MBX_TICK_CTL_EN_WIDTH));
}

bool mbx_link_up(unsigned interface)
{
	uint32_t up = mbx_field(mbx_bus_read32(MBX_REG_LINK), MBX_LINK_UP_LSB, MBX_LINK_UP_WIDTH);
	return ((up >> interface) & 1u) != 0u;
}

uint64_t mbx_gm_id(unsigned interface, uint8_t *domain)
{
	// GM_LO first: reading it snapshots GM_HI and DOMAIN for the next reads
	uint32_t lo = mbx_bus_read32(if_reg(interface, MBX_IF_REG_GM_LO));
	uint32_t hi = mbx_bus_read32(if_reg(interface, MBX_IF_REG_GM_HI));
	uint32_t dom = mbx_bus_read32(if_reg(interface, MBX_IF_REG_DOMAIN));
	if (domain != NULL) {
		*domain = (uint8_t)mbx_field(dom, MBX_DOMAIN_NUMBER_LSB, MBX_DOMAIN_NUMBER_WIDTH);
	}
	return ((uint64_t)mbx_field(hi, MBX_GM_HI_ID_LSB, MBX_GM_HI_ID_WIDTH) << 32) |
	       (uint64_t)mbx_field(lo, MBX_GM_LO_ID_LSB, MBX_GM_LO_ID_WIDTH);
}

uint32_t mbx_irq_status(void)
{
	return mbx_bus_read32(MBX_REG_IRQ_STATUS);
}

void mbx_irq_enable(uint32_t mask)
{
	mbx_bus_write32(MBX_REG_IRQ_ENABLE, mask);
}

void mbx_irq_clear_err(void)
{
	mbx_bus_write32(MBX_REG_IRQ_STATUS, mbx_place(1u, MBX_IRQ_STATUS_ERR_LSB, MBX_IRQ_STATUS_ERR_WIDTH));
}
