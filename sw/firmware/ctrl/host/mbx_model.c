// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// mbx_model.c - the fabric side of the packet-mailbox contract, modeled at
// the transaction level (see mbx_model.h). Each rule below is the RTL's
// (hdl/milan/mailbox), stated in the leaf that implements it:
//
//   KL_mbx_rx   classification by the full tuple (destination MAC, or the
//               arrival interface's OWN_MAC for an `own` tuple, EtherType,
//               subtype and message_type), FILTER_MISMATCH for a control
//               EtherType no tuple holds, the accept terms (eq_bound on the
//               arrival interface's bound-talker table), the record
//               committed whole or dropped (RX_DROP for size or space,
//               RATE_DROP for an empty bucket), one token per refill period
//               up to the burst;
//   KL_mbx_tx   the record whose SEQ comes first modulo 2^16 among each
//               channel's oldest, scanned from the channel after the one
//               served last (so equal SEQs go round-robin), a record checked
//               before a byte leaves, a refused record counted and the ring
//               flushed to TX_HEAD;
//   KL_mbx_evt  timers expiring at their deadline, every source coalesced,
//               posted only into four free words, in the priority link,
//               grandmaster, lowest slot, tick, live map write, AVB_INFO,
//               AS_PATH, and the lowest pending counter-change descriptor
//               not posted in this holdoff epoch;
//   KL_mbx      the register file, the GM_LO snapshot, the sticky ERR, the
//               refusal of a partial write, the interrupt levels, the
//               publication block (its fields masked, a hole reading 0 and
//               taking no write, the stream_id taken only while SID_VALID),
//               the face block (the same, a write that would move a held
//               setting or request refused, the commit and each window's
//               request open until its acknowledgement, its answer or its
//               timeout, an answer under another tag discarded).

#include "mbx_model.h"

#include <string.h>

#include "mbx_wire.h"

static const uint32_t rx_base[MBX_N_CH] = MBX_CH_RX_BASE_TBL;
static const uint32_t rx_words[MBX_N_CH] = MBX_CH_RX_WORDS_TBL;
static const uint32_t tx_base[MBX_N_CH] = MBX_CH_TX_BASE_TBL;
static const uint32_t tx_words[MBX_N_CH] = MBX_CH_TX_WORDS_TBL;
static const uint32_t max_frame[MBX_N_CH] = MBX_CH_MAX_FRAME_BYTES_TBL;
static const uint32_t tuple_dst[MBX_N_CH * MBX_MAX_TUPLES] = MBX_TUPLE_DST_TBL;
static const uint32_t tuple_dst_hi[MBX_N_CH * MBX_MAX_TUPLES] = MBX_TUPLE_DST_HI_TBL;
static const uint32_t tuple_dst_lo[MBX_N_CH * MBX_MAX_TUPLES] = MBX_TUPLE_DST_LO_TBL;
static const uint32_t tuple_ethertype[MBX_N_CH * MBX_MAX_TUPLES] = MBX_TUPLE_ETHERTYPE_TBL;
static const uint32_t tuple_has_subtype[MBX_N_CH * MBX_MAX_TUPLES] = MBX_TUPLE_HAS_SUBTYPE_TBL;
static const uint32_t tuple_subtype[MBX_N_CH * MBX_MAX_TUPLES] = MBX_TUPLE_SUBTYPE_TBL;
static const uint32_t tuple_msg_mask[MBX_N_CH * MBX_MAX_TUPLES] = MBX_TUPLE_MSG_MASK_TBL;
static const uint32_t burst[MBX_N_CH] = MBX_CH_RATE_BURST_TBL;
static const uint32_t refill_ms[MBX_N_CH] = MBX_CH_RATE_REFILL_MS_TBL;
static const uint32_t term_test[MBX_N_CH * MBX_MAX_TERMS] = MBX_TERM_TEST_TBL;
static const uint32_t term_offset[MBX_N_CH * MBX_MAX_TERMS] = MBX_TERM_OFFSET_TBL;
static const uint32_t term_mask[MBX_N_CH * MBX_MAX_TERMS] = MBX_TERM_MASK_TBL;

static uint32_t *ring_word(struct mbx_model *m, uint32_t base, uint32_t words, uint32_t index)
{
	return &m->window[(base + 4u * (index & (words - 1u))) / 4u];
}

static uint16_t sat16(uint16_t v)
{
	return v == 0xFFFFu ? v : (uint16_t)(v + 1u);
}

// ---- the face block's events ------------------------------------------------

static const uint32_t ctrchg_type[MBX_CTRCHG_N_SRC] = MBX_CTRCHG_TYPE_TBL;
static const uint32_t ctrchg_count[MBX_CTRCHG_N_SRC] = MBX_CTRCHG_COUNT_TBL;
static const uint32_t ctrchg_first[MBX_CTRCHG_N_SRC] = MBX_CTRCHG_FIRST_TBL;

_Static_assert(MBX_CTRCHG_N_PEND <= 64u, "the model keeps a counter-change interface's pending bits in one word");

// The pending bit a counter change names: its descriptor's, or ALL.
static unsigned ctr_bit(uint16_t type, uint16_t index)
{
	for (unsigned f = 0; f < MBX_CTRCHG_N_SRC; ++f) {
		if (type == ctrchg_type[f] && index < ctrchg_count[f]) {
			return ctrchg_first[f] + index;
		}
	}
	return MBX_CTRCHG_ALL_BIT;
}

// The face events after the tick, in KL_mbx_evt's priority.
static bool next_face_source(const struct mbx_model *m, uint32_t w[4])
{
	static const struct {
		uint32_t type;
		uint32_t count_lsb;
		uint32_t count_width;
	} counted[3] = {
		{MBX_EV_TYPE_AMAP_LIVE_WRITE, MBX_EV_AMAP_LIVE_WRITE_W1_COUNT_LSB, MBX_EV_AMAP_LIVE_WRITE_W1_COUNT_WIDTH},
		{MBX_EV_TYPE_AVB_INFO_CHANGED, MBX_EV_AVB_INFO_CHANGED_W1_COUNT_LSB, MBX_EV_AVB_INFO_CHANGED_W1_COUNT_WIDTH},
		{MBX_EV_TYPE_AS_PATH_CHANGED, MBX_EV_AS_PATH_CHANGED_W1_COUNT_LSB, MBX_EV_AS_PATH_CHANGED_W1_COUNT_WIDTH},
	};
	for (unsigned k = 0; k < 3u; ++k) {
		for (unsigned i = 0; i < MBX_N_IF; ++i) {
			uint16_t count = k == 0u ? m->amap_count[i] : k == 1u ? m->avb_count[i] : m->asp_count[i];
			if (count != 0u) {
				w[0] = mbx_place(counted[k].type, MBX_EVREC_W0_TYPE_LSB, MBX_EVREC_W0_TYPE_WIDTH) |
				       mbx_place(i, MBX_EVREC_W0_IF_LSB, MBX_EVREC_W0_IF_WIDTH);
				w[1] = mbx_place(count, counted[k].count_lsb, counted[k].count_width);
				w[2] = 0;
				w[3] = m->now_ms;
				return true;
			}
		}
	}
	for (unsigned i = 0; i < MBX_N_IF; ++i) {
		uint64_t ready = m->ctr_pending[i] & ~m->ctr_seen[i];
		for (unsigned b = 0; b < MBX_CTRCHG_N_PEND; ++b) {
			if (((ready >> b) & 1u) == 0u) {
				continue;
			}
			uint32_t type = 0;
			uint32_t index = 0;
			for (unsigned f = 0; f < MBX_CTRCHG_N_SRC; ++f) {
				if (b >= ctrchg_first[f] && b < ctrchg_first[f] + ctrchg_count[f]) {
					type = ctrchg_type[f];
					index = b - ctrchg_first[f];
				}
			}
			w[0] = mbx_place(MBX_EV_TYPE_COUNTERS_CHANGED, MBX_EVREC_W0_TYPE_LSB, MBX_EVREC_W0_TYPE_WIDTH) |
			       mbx_place(i, MBX_EVREC_W0_IF_LSB, MBX_EVREC_W0_IF_WIDTH);
			w[1] = mbx_place(type, MBX_EV_COUNTERS_CHANGED_W1_TYPE_LSB, MBX_EV_COUNTERS_CHANGED_W1_TYPE_WIDTH) |
			       mbx_place(index, MBX_EV_COUNTERS_CHANGED_W1_INDEX_LSB, MBX_EV_COUNTERS_CHANGED_W1_INDEX_WIDTH);
			w[2] = mbx_place(b == MBX_CTRCHG_ALL_BIT ? 1u : 0u, MBX_EV_COUNTERS_CHANGED_W2_ALL_LSB,
					 MBX_EV_COUNTERS_CHANGED_W2_ALL_WIDTH);
			w[3] = m->now_ms;
			return true;
		}
	}
	return false;
}

// Clear the face source the record in w[] came from.
static void face_source_posted(struct mbx_model *m, uint32_t type, uint32_t i, const uint32_t w[4])
{
	if (type == MBX_EV_TYPE_AMAP_LIVE_WRITE) {
		m->amap_count[i] = 0;
	} else if (type == MBX_EV_TYPE_AVB_INFO_CHANGED) {
		m->avb_count[i] = 0;
	} else if (type == MBX_EV_TYPE_AS_PATH_CHANGED) {
		m->asp_count[i] = 0;
	} else {
		unsigned b = mbx_field(w[2], MBX_EV_COUNTERS_CHANGED_W2_ALL_LSB, MBX_EV_COUNTERS_CHANGED_W2_ALL_WIDTH) != 0u
				     ? MBX_CTRCHG_ALL_BIT
				     : ctr_bit((uint16_t)mbx_field(w[1], MBX_EV_COUNTERS_CHANGED_W1_TYPE_LSB,
								   MBX_EV_COUNTERS_CHANGED_W1_TYPE_WIDTH),
					       (uint16_t)mbx_field(w[1], MBX_EV_COUNTERS_CHANGED_W1_INDEX_LSB,
								   MBX_EV_COUNTERS_CHANGED_W1_INDEX_WIDTH));
		m->ctr_pending[i] &= ~(1ull << b);
		m->ctr_seen[i] |= 1ull << b;
	}
}

// ---- the event poster -----------------------------------------------------

static bool next_source(const struct mbx_model *m, uint32_t w[4])
{
	uint32_t w0_if = 0;
	for (unsigned i = 0; i < MBX_N_IF; ++i) {
		if (m->link_up[i] != m->posted_up[i]) {
			w[0] = mbx_place(MBX_EV_TYPE_LINK, MBX_EVREC_W0_TYPE_LSB, MBX_EVREC_W0_TYPE_WIDTH) |
			       mbx_place(i, MBX_EVREC_W0_IF_LSB, MBX_EVREC_W0_IF_WIDTH);
			w[1] = mbx_place(m->link_up[i] ? 1u : 0u, MBX_EV_LINK_W1_UP_LSB, MBX_EV_LINK_W1_UP_WIDTH);
			w[2] = 0;
			w[3] = m->now_ms;
			return true;
		}
	}
	for (unsigned i = 0; i < MBX_N_IF; ++i) {
		if (m->gm_pending[i]) {
			w0_if = mbx_place(i, MBX_EVREC_W0_IF_LSB, MBX_EVREC_W0_IF_WIDTH);
			w[0] = mbx_place(MBX_EV_TYPE_GM, MBX_EVREC_W0_TYPE_LSB, MBX_EVREC_W0_TYPE_WIDTH) | w0_if;
			w[1] = (uint32_t)m->gm_id[i];
			w[2] = (uint32_t)(m->gm_id[i] >> 32);
			w[3] = mbx_place(m->domain[i], MBX_EV_GM_W3_DOMAIN_LSB, MBX_EV_GM_W3_DOMAIN_WIDTH);
			return true;
		}
	}
	for (unsigned s = 0; s < MBX_N_TIMERS; ++s) {
		if (m->timers[s].pending) {
			w[0] = mbx_place(MBX_EV_TYPE_TIMER, MBX_EVREC_W0_TYPE_LSB, MBX_EVREC_W0_TYPE_WIDTH);
			w[1] = mbx_place(m->timers[s].tag, MBX_EV_TIMER_W1_TAG_LSB, MBX_EV_TIMER_W1_TAG_WIDTH) |
			       mbx_place(s, MBX_EV_TIMER_W1_SLOT_LSB, MBX_EV_TIMER_W1_SLOT_WIDTH);
			w[2] = m->timers[s].deadline_ms;
			w[3] = m->now_ms;
			return true;
		}
	}
	if (m->tick_count != 0u) {
		w[0] = mbx_place(MBX_EV_TYPE_TICK, MBX_EVREC_W0_TYPE_LSB, MBX_EVREC_W0_TYPE_WIDTH);
		w[1] = mbx_place(m->tick_count, MBX_EV_TICK_W1_COUNT_LSB, MBX_EV_TICK_W1_COUNT_WIDTH);
		w[2] = 0;
		w[3] = m->now_ms;
		return true;
	}
	return next_face_source(m, w);
}

// Clear the source the record in w[] came from.
static void source_posted(struct mbx_model *m, const uint32_t w[4])
{
	uint32_t type = mbx_field(w[0], MBX_EVREC_W0_TYPE_LSB, MBX_EVREC_W0_TYPE_WIDTH);
	uint32_t i = mbx_field(w[0], MBX_EVREC_W0_IF_LSB, MBX_EVREC_W0_IF_WIDTH);
	if (type == MBX_EV_TYPE_LINK) {
		m->posted_up[i] = m->link_up[i];
	} else if (type == MBX_EV_TYPE_GM) {
		m->gm_pending[i] = false;
	} else if (type == MBX_EV_TYPE_TIMER) {
		m->timers[mbx_field(w[1], MBX_EV_TIMER_W1_SLOT_LSB, MBX_EV_TIMER_W1_SLOT_WIDTH)].pending = false;
	} else if (type == MBX_EV_TYPE_TICK) {
		m->tick_count = 0;
	} else {
		face_source_posted(m, type, i, w);
	}
}

static void post(struct mbx_model *m)
{
	uint32_t w[4];
	for (;;) {
		uint16_t used = (uint16_t)(m->evt_head - m->evt_tail);
		uint16_t free_words = used > MBX_EVT_WORDS ? 0u : (uint16_t)(MBX_EVT_WORDS - used);
		if (m->evt_paused || free_words < MBX_EV_WORDS || !next_source(m, w)) {
			return;
		}
		w[0] |= mbx_place(m->seq, MBX_EVREC_W0_SEQ_LSB, MBX_EVREC_W0_SEQ_WIDTH);
		for (uint32_t k = 0; k < MBX_EV_WORDS; ++k) {
			*ring_word(m, MBX_EVT_BASE, MBX_EVT_WORDS, (uint32_t)m->evt_head + k) = w[k];
		}
		source_posted(m, w);
		m->evt_head = (uint16_t)(m->evt_head + MBX_EV_WORDS);
		m->seq = (uint16_t)(m->seq + 1u);
	}
}

// ---- the timer bank and time ---------------------------------------------------

static void timers_expire(struct mbx_model *m)
{
	for (unsigned s = 0; s < MBX_N_TIMERS; ++s) {
		struct mbx_model_timer *t = &m->timers[s];
		if (t->armed && (int32_t)(m->now_ms - t->deadline_ms) >= 0) {
			t->armed = false;
			t->pending = true;
		}
	}
}

static void one_ms(struct mbx_model *m)
{
	m->now_ms++;
	for (unsigned c = 0; c < MBX_N_CH; ++c) {
		struct mbx_model_channel *ch = &m->ch[c];
		if ((uint32_t)ch->refill + 1u >= refill_ms[c]) {
			ch->refill = 0;
			if (ch->tokens < burst[c]) {
				ch->tokens++;
			}
		} else {
			ch->refill++;
		}
	}
	if (m->tick_ctl != 0u) {
		bool tick = (uint32_t)m->tick_div + 1u >= MBX_TICK_MS;
		m->tick_div = tick ? 0u : (uint8_t)(m->tick_div + 1u);
		if (tick) {
			m->tick_count = sat16(m->tick_count);
		}
	}
	if ((uint32_t)m->ctr_epoch_ms + 1u >= MBX_CTRCHG_HOLDOFF_MS) {
		m->ctr_epoch_ms = 0;
		memset(m->ctr_seen, 0, sizeof m->ctr_seen);
	} else {
		m->ctr_epoch_ms++;
	}
	timers_expire(m);
	post(m);
}

void mbx_model_advance_ms(struct mbx_model *m, uint32_t ms)
{
	for (uint32_t k = 0; k < ms; ++k) {
		one_ms(m);
	}
}

static void timer_command(struct mbx_model *m, uint32_t v)
{
	uint32_t slot = mbx_field(v, MBX_TMR_CMD_SLOT_LSB, MBX_TMR_CMD_SLOT_WIDTH);
	uint32_t op = mbx_field(v, MBX_TMR_CMD_OP_LSB, MBX_TMR_CMD_OP_WIDTH);
	if (slot >= MBX_N_TIMERS || (op != MBX_TMR_OP_ARM && op != MBX_TMR_OP_CANCEL)) {
		m->bus_err = sat16(m->bus_err);
		m->err = true;
		return;
	}
	struct mbx_model_tmr_op *log = &m->tmr_log[m->tmr_ops % MBX_MODEL_TMR_LOG];
	log->op = (uint8_t)op;
	log->slot = (uint8_t)slot;
	log->tag = (uint16_t)mbx_field(v, MBX_TMR_CMD_TAG_LSB, MBX_TMR_CMD_TAG_WIDTH);
	log->deadline_ms = m->tmr_deadline;
	log->now_ms = m->now_ms;
	m->tmr_ops++;
	struct mbx_model_timer *t = &m->timers[slot];
	t->pending = false;
	t->armed = op == MBX_TMR_OP_ARM;
	if (t->armed) {
		t->tag = log->tag;
		t->deadline_ms = m->tmr_deadline;
	}
	timers_expire(m);
}

// ---- the TX merge ----------------------------------------------------------------

static bool tx_record_ok(struct mbx_model *m, unsigned c, uint32_t w0, uint32_t w1)
{
	uint32_t len = mbx_field(w0, MBX_TXREC_W0_LEN_LSB, MBX_TXREC_W0_LEN_WIDTH);
	uint32_t occ = (uint16_t)(m->ch[c].tx_head - m->ch[c].tx_tail);
	uint32_t record = MBX_TX_HDR_WORDS + (len + 3u) / 4u;
	return mbx_field(w0, MBX_TXREC_W0_KIND_LSB, MBX_TXREC_W0_KIND_WIDTH) == MBX_TX_KIND &&
	       mbx_field(w0, MBX_TXREC_W0_IF_LSB, MBX_TXREC_W0_IF_WIDTH) < MBX_N_IF && len >= 14u &&
	       len <= max_frame[c] && occ <= tx_words[c] && record <= occ &&
	       (w1 >> MBX_TXREC_W1_RSVD_LSB) == 0u;
}

static void tx_capture(struct mbx_model *m, unsigned c, uint32_t w0)
{
	struct mbx_model_tx *f = &m->tx[m->tx_sent % MBX_MODEL_TX_CAPTURE];
	struct mbx_model_channel *ch = &m->ch[c];
	f->len = (uint16_t)mbx_field(w0, MBX_TXREC_W0_LEN_LSB, MBX_TXREC_W0_LEN_WIDTH);
	f->interface = (uint8_t)mbx_field(w0, MBX_TXREC_W0_IF_LSB, MBX_TXREC_W0_IF_WIDTH);
	f->channel = (uint8_t)c;
	f->now_ms = m->now_ms;
	for (uint32_t k = 0; k < f->len; k += 4u) {
		uint32_t word = *ring_word(m, tx_base[c], tx_words[c], (uint32_t)ch->tx_tail + MBX_TX_HDR_WORDS + k / 4u);
		ring_lanes_unpack(word, &f->bytes[k], f->len - k > 4u ? 4u : f->len - k);
	}
	m->tx_sent++;
}

static void tx_drain(struct mbx_model *m)
{
	while (!m->tx_paused) {
		unsigned c = MBX_N_CH;
		uint16_t best = 0;
		for (unsigned k = 1; k <= MBX_N_CH; ++k) {
			unsigned cand = (m->tx_last_ch + k) % MBX_N_CH;
			struct mbx_model_channel *cc = &m->ch[cand];
			if (cc->tx_head == cc->tx_tail) {
				continue;
			}
			uint16_t seq = (uint16_t)mbx_field(*ring_word(m, tx_base[cand], tx_words[cand],
								     (uint32_t)cc->tx_tail + 1u),
							   MBX_TXREC_W1_SEQ_LSB, MBX_TXREC_W1_SEQ_WIDTH);
			if (c == MBX_N_CH || ((uint16_t)(seq - best) & 0x8000u) != 0u) {
				c = cand;
				best = seq;
			}
		}
		if (c == MBX_N_CH) {
			return;
		}
		struct mbx_model_channel *ch = &m->ch[c];
		uint32_t w0 = *ring_word(m, tx_base[c], tx_words[c], ch->tx_tail);
		uint32_t w1 = *ring_word(m, tx_base[c], tx_words[c], (uint32_t)ch->tx_tail + 1u);
		if (tx_record_ok(m, c, w0, w1)) {
			tx_capture(m, c, w0);
			uint32_t len = mbx_field(w0, MBX_TXREC_W0_LEN_LSB, MBX_TXREC_W0_LEN_WIDTH);
			ch->tx_tail = (uint16_t)(ch->tx_tail + MBX_TX_HDR_WORDS + (len + 3u) / 4u);
		} else {
			ch->tx_err = sat16(ch->tx_err);
			m->err = true;
			ch->tx_tail = ch->tx_head;
		}
		m->tx_last_ch = (uint8_t)c;
	}
}

void mbx_model_tx_pause(struct mbx_model *m, bool paused)
{
	m->tx_paused = paused;
	tx_drain(m);
}

void mbx_model_evt_pause(struct mbx_model *m, bool paused)
{
	m->evt_paused = paused;
	post(m);
}

// ---- the ingress filter ----------------------------------------------------------

// The destination a tuple compares with: its address, or the OWN_MAC of the
// interface the frame arrived on; false when it has none (an unused tuple,
// or an `own` tuple on an index with no interface).
static bool tuple_dst_mac(const struct mbx_model *m, unsigned j, unsigned interface, uint64_t *mac)
{
	if (tuple_dst[j] == MBX_DST_MAC) {
		*mac = ((uint64_t)tuple_dst_hi[j] << 32) | tuple_dst_lo[j];
		return true;
	}
	if (tuple_dst[j] == MBX_DST_OWN && interface < MBX_N_IF) {
		*mac = m->own_mac[interface];
		return true;
	}
	return false;
}

// The message_type the accept terms and the tuples read: 0 for a frame that
// ends before its byte.
static uint32_t msg_type(const uint8_t *frame, size_t len)
{
	return len > MBX_MSG_TYPE_BYTE ? frame[MBX_MSG_TYPE_BYTE] & 0x0Fu : 0u;
}

// The channel whose match tuple holds for the frame's destination, EtherType,
// subtype and message_type, or -1. *mismatch when none holds and the EtherType
// is one some tuple names (a tagged frame's is its TPID, which no tuple names).
// A frame that ends before the subtype byte carries no PDU: no channel, no count.
static int classify(const struct mbx_model *m, const uint8_t *frame, size_t len, unsigned interface, bool *mismatch)
{
	*mismatch = false;
	if (len <= MBX_SUBTYPE_BYTE) {
		return -1;
	}
	uint64_t dst = ((uint64_t)wire_be16(frame + MBX_DST_BYTE) << 32) | wire_be32(frame + MBX_DST_BYTE + 2u);
	uint32_t et = wire_be16(frame + MBX_ETHERTYPE_BYTE);
	uint32_t msg = msg_type(frame, len);
	bool control = false;
	for (unsigned j = 0; j < MBX_N_CH * MBX_MAX_TUPLES; ++j) {
		uint64_t mac = 0;
		bool named = tuple_dst[j] != MBX_DST_NONE && et == tuple_ethertype[j];
		control = control || named;
		if (named && tuple_dst_mac(m, j, interface, &mac) && dst == mac &&
		    (tuple_has_subtype[j] == 0u || frame[MBX_SUBTYPE_BYTE] == tuple_subtype[j]) &&
		    ((tuple_msg_mask[j] >> msg) & 1u) != 0u) {
			return (int)(j / MBX_MAX_TUPLES);
		}
	}
	*mismatch = control;
	return -1;
}

static bool maap_overlap(const struct mbx_model *m, uint64_t start, uint32_t count)
{
	if (count == 0u || m->maap_count == 0u) {
		return false;
	}
	uint64_t own_end = m->maap_base + m->maap_count - 1u;
	uint64_t req_end = start + count - 1u;
	return start <= own_end && m->maap_base <= req_end;
}

// The field equals an enabled entry of the arrival interface's bound-talker
// table; an index with no interface behind it has no table.
static bool bound_talker(const struct mbx_model *m, unsigned interface, uint64_t field)
{
	if (interface >= MBX_N_IF) {
		return false;
	}
	for (unsigned e = 0; e < MBX_N_BOUND; ++e) {
		if (m->bound_en[interface][e] && m->bound_eid[interface][e] == field) {
			return true;
		}
	}
	return false;
}

static bool term_holds(const struct mbx_model *m, unsigned j, const uint8_t *frame, size_t len, unsigned interface)
{
	uint32_t off = term_offset[j];
	bool field_ok = len >= (size_t)off + MBX_TERM_FIELD_BYTES;
	switch (term_test[j]) {
	case MBX_TEST_ANY:
		return true;
	case MBX_TEST_EQ_OWN:
		return field_ok && wire_be64(frame + off) == m->own_eid;
	case MBX_TEST_EQ_ZERO:
		return field_ok && wire_be64(frame + off) == 0u;
	case MBX_TEST_RANGE_OVERLAP:
		return field_ok && maap_overlap(m, wire_be64(frame + off) >> 16, wire_be16(frame + off + 6u));
	case MBX_TEST_EQ_BOUND:
		return field_ok && bound_talker(m, interface, wire_be64(frame + off));
	default:
		return false;
	}
}

static bool rule_passes(const struct mbx_model *m, unsigned c, const uint8_t *frame, size_t len, unsigned interface)
{
	uint32_t msg = msg_type(frame, len);
	for (unsigned t = 0; t < MBX_MAX_TERMS; ++t) {
		unsigned j = c * MBX_MAX_TERMS + t;
		if (((term_mask[j] >> msg) & 1u) != 0u && term_holds(m, j, frame, len, interface)) {
			return true;
		}
	}
	return false;
}

static void rx_commit(struct mbx_model *m, unsigned c, const uint8_t *frame, size_t len, unsigned interface)
{
	struct mbx_model_channel *ch = &m->ch[c];
	*ring_word(m, rx_base[c], rx_words[c], ch->rx_head) =
		mbx_place((uint32_t)len, MBX_RXREC_W0_LEN_LSB, MBX_RXREC_W0_LEN_WIDTH) |
		mbx_place(interface, MBX_RXREC_W0_IF_LSB, MBX_RXREC_W0_IF_WIDTH) |
		mbx_place(MBX_RX_KIND, MBX_RXREC_W0_KIND_LSB, MBX_RXREC_W0_KIND_WIDTH);
	*ring_word(m, rx_base[c], rx_words[c], (uint32_t)ch->rx_head + 1u) = m->now_ms;
	for (size_t k = 0; k < len; k += 4u) {
		*ring_word(m, rx_base[c], rx_words[c], (uint32_t)ch->rx_head + MBX_RX_HDR_WORDS + (uint32_t)(k / 4u)) =
			ring_lanes_pack(frame + k, len - k > 4u ? 4u : (unsigned)(len - k));
	}
	ch->rx_head = (uint16_t)(ch->rx_head + MBX_RX_HDR_WORDS + (len + 3u) / 4u);
	ch->rx_pass = (uint16_t)(ch->rx_pass + 1u);
	ch->tokens--;
}

bool mbx_model_rx(struct mbx_model *m, const uint8_t *frame, size_t len, unsigned interface)
{
	bool mismatch = false;
	int found = classify(m, frame, len, interface, &mismatch);
	if (mismatch) {
		m->filter_mismatch = sat16(m->filter_mismatch);
		m->err = true;
	}
	if (found < 0 || ((m->filter_en >> found) & 1u) == 0u) {
		return false;
	}
	unsigned c = (unsigned)found;
	if (!rule_passes(m, c, frame, len, interface)) {
		return false;
	}
	struct mbx_model_channel *ch = &m->ch[c];
	uint32_t used = (uint16_t)(ch->rx_head - ch->rx_tail);
	uint32_t free_words = used > rx_words[c] ? 0u : rx_words[c] - used;
	if (len > max_frame[c] || MBX_RX_HDR_WORDS + (len + 3u) / 4u > free_words) {
		ch->rx_drop = sat16(ch->rx_drop);
		m->err = true;
		return false;
	}
	if (ch->tokens == 0u) {
		ch->rate_drop = sat16(ch->rate_drop);
		m->err = true;
		return false;
	}
	rx_commit(m, c, frame, len, interface);
	return true;
}

// ---- the inputs the gPTP plane and the PHY drive ----------------------------------

void mbx_model_set_link(struct mbx_model *m, unsigned interface, bool up)
{
	m->link_up[interface] = up;
	post(m);
}

void mbx_model_set_gm(struct mbx_model *m, unsigned interface, uint64_t gm_id, uint8_t domain)
{
	m->gm_id[interface] = gm_id;
	m->domain[interface] = domain;
}

void mbx_model_gm_change(struct mbx_model *m, unsigned interface, uint64_t gm_id, uint8_t domain)
{
	mbx_model_set_gm(m, interface, gm_id, domain);
	m->gm_pending[interface] = true;
	post(m);
}

// ---- the register file ------------------------------------------------------------

void mbx_model_reset(struct mbx_model *m)
{
	// the far side is the harness's, not the fabric's: a reset keeps it
	const struct mbx_model_far *far = m->far;
	memset(m, 0, sizeof *m);
	m->far = far;
	for (unsigned c = 0; c < MBX_N_CH; ++c) {
		m->ch[c].tokens = (uint8_t)burst[c];
	}
	m->tx_last_ch = MBX_N_CH - 1u;
}

static uint32_t irq_status(const struct mbx_model *m)
{
	uint32_t rx = 0;
	for (unsigned c = 0; c < MBX_N_CH; ++c) {
		if (m->ch[c].rx_head != m->ch[c].rx_tail) {
			rx |= 1u << c;
		}
	}
	return mbx_place(rx, MBX_IRQ_STATUS_RX_LSB, MBX_IRQ_STATUS_RX_WIDTH) |
	       mbx_place(m->evt_head != m->evt_tail ? 1u : 0u, MBX_IRQ_STATUS_EVT_LSB, MBX_IRQ_STATUS_EVT_WIDTH) |
	       mbx_place(m->err ? 1u : 0u, MBX_IRQ_STATUS_ERR_LSB, MBX_IRQ_STATUS_ERR_WIDTH);
}

bool mbx_model_irq(const struct mbx_model *m)
{
	return (irq_status(m) & m->irq_enable) != 0u;
}

static uint32_t read_identity(uint32_t off)
{
	if (off == MBX_REG_ID) {
		return mbx_place(MBX_VERSION_MINOR, MBX_ID_MINOR_LSB, MBX_ID_MINOR_WIDTH) |
		       mbx_place(MBX_VERSION_MAJOR, MBX_ID_MAJOR_LSB, MBX_ID_MAJOR_WIDTH) |
		       mbx_place(MBX_MAGIC, MBX_ID_MAGIC_LSB, MBX_ID_MAGIC_WIDTH);
	}
	uint32_t log2 = 0;
	while ((1u << log2) < MBX_EVT_WORDS) {
		log2++;
	}
	return mbx_place(MBX_N_CH, MBX_CAPS_N_CH_LSB, MBX_CAPS_N_CH_WIDTH) |
	       mbx_place(MBX_N_IF, MBX_CAPS_N_IF_LSB, MBX_CAPS_N_IF_WIDTH) |
	       mbx_place(MBX_N_TIMERS, MBX_CAPS_N_TIMERS_LSB, MBX_CAPS_N_TIMERS_WIDTH) |
	       mbx_place(log2, MBX_CAPS_EVT_WORDS_LOG2_LSB, MBX_CAPS_EVT_WORDS_LOG2_WIDTH);
}

static uint32_t read_global(const struct mbx_model *m, uint32_t off)
{
	uint32_t link = 0;
	for (unsigned i = 0; i < MBX_N_IF; ++i) {
		link |= (m->link_up[i] ? 1u : 0u) << i;
	}
	switch (off) {
	case MBX_REG_ID:
	case MBX_REG_CAPS:
		return read_identity(off);
	case MBX_REG_IRQ_STATUS:
		return irq_status(m);
	case MBX_REG_IRQ_ENABLE:
		return m->irq_enable;
	case MBX_REG_NOW_MS:
		return m->now_ms;
	case MBX_REG_LINK:
		return mbx_place(link, MBX_LINK_UP_LSB, MBX_LINK_UP_WIDTH);
	case MBX_REG_TICK_CTL:
		return m->tick_ctl;
	case MBX_REG_OWN_EID_LO:
		return (uint32_t)m->own_eid;
	case MBX_REG_OWN_EID_HI:
		return (uint32_t)(m->own_eid >> 32);
	case MBX_REG_FILTER_EN:
		return m->filter_en;
	case MBX_REG_MAAP_BASE_LO:
		return (uint32_t)m->maap_base;
	case MBX_REG_MAAP_BASE_HI:
		return (uint32_t)(m->maap_base >> 32);
	case MBX_REG_MAAP_COUNT:
		return m->maap_count;
	case MBX_REG_TMR_DEADLINE:
		return m->tmr_deadline;
	case MBX_REG_EVT_HEAD:
		return m->evt_head;
	case MBX_REG_EVT_TAIL:
		return m->evt_tail;
	case MBX_REG_BUS_ERR:
		return m->bus_err;
	case MBX_REG_FILTER_MISMATCH:
		return m->filter_mismatch;
	default:
		return 0;
	}
}

// OWN_MAC_LO or OWN_MAC_HI of interface i.
static uint32_t read_interface_filter(const struct mbx_model *m, unsigned i, uint32_t reg)
{
	if (reg == MBX_IFF_REG_OWN_MAC_LO) {
		return (uint32_t)m->own_mac[i];
	}
	return reg == MBX_IFF_REG_OWN_MAC_HI ? (uint32_t)(m->own_mac[i] >> 32) : 0u;
}

static void write_interface_filter(struct mbx_model *m, unsigned i, uint32_t reg, uint32_t v)
{
	if (reg == MBX_IFF_REG_OWN_MAC_LO) {
		m->own_mac[i] = (m->own_mac[i] & 0xFFFF00000000ull) |
				mbx_field(v, MBX_OWN_MAC_LO_MAC_LSB, MBX_OWN_MAC_LO_MAC_WIDTH);
	} else if (reg == MBX_IFF_REG_OWN_MAC_HI) {
		m->own_mac[i] = (m->own_mac[i] & 0xFFFFFFFFull) |
				((uint64_t)mbx_field(v, MBX_OWN_MAC_HI_MAC_LSB, MBX_OWN_MAC_HI_MAC_WIDTH) << 32);
	}
}

// BOUND_EID_LO, BOUND_EID_HI or BOUND_EN of entry e of interface i.
static uint32_t read_bound(const struct mbx_model *m, unsigned i, unsigned e, uint32_t reg)
{
	if (reg == MBX_BND_REG_BOUND_EID_LO) {
		return (uint32_t)m->bound_eid[i][e];
	}
	if (reg == MBX_BND_REG_BOUND_EID_HI) {
		return (uint32_t)(m->bound_eid[i][e] >> 32);
	}
	return reg == MBX_BND_REG_BOUND_EN && m->bound_en[i][e] ? 1u : 0u;
}

static void write_bound(struct mbx_model *m, unsigned i, unsigned e, uint32_t reg, uint32_t v)
{
	if (reg == MBX_BND_REG_BOUND_EID_LO) {
		m->bound_eid[i][e] = (m->bound_eid[i][e] & 0xFFFFFFFF00000000ull) |
				     mbx_field(v, MBX_BOUND_EID_LO_EID_LSB, MBX_BOUND_EID_LO_EID_WIDTH);
	} else if (reg == MBX_BND_REG_BOUND_EID_HI) {
		m->bound_eid[i][e] = (m->bound_eid[i][e] & 0xFFFFFFFFull) |
				     ((uint64_t)mbx_field(v, MBX_BOUND_EID_HI_EID_LSB, MBX_BOUND_EID_HI_EID_WIDTH) << 32);
	} else if (reg == MBX_BND_REG_BOUND_EN) {
		m->bound_en[i][e] = mbx_field(v, MBX_BOUND_EN_EN_LSB, MBX_BOUND_EN_EN_WIDTH) != 0u;
	}
}

// The publication block an offset falls in: interface *i and the offset *rel
// inside that interface's block; false outside every interface's.
static bool pub_at(uint32_t off, unsigned *i, uint32_t *rel)
{
	if (off < MBX_PUB_BASE || off >= MBX_PUB_BASE + MBX_PUB_STRIDE * MBX_N_IF) {
		return false;
	}
	*i = (off - MBX_PUB_BASE) / MBX_PUB_STRIDE;
	*rel = (off - MBX_PUB_BASE) % MBX_PUB_STRIDE;
	return true;
}

static uint32_t ones(uint32_t lsb, uint32_t width)
{
	return mbx_place(0xFFFFFFFFu, lsb, width);
}

// The fields of the publication word at `rel` inside an interface's block: 0
// for a hole, so a hole takes no write and reads 0.
static uint32_t pub_mask(uint32_t rel)
{
	if (rel >= MBX_PUB_SINK_BASE) {
		uint32_t in = (rel - MBX_PUB_SINK_BASE) % MBX_PUB_SINK_STRIDE;
		if ((rel - MBX_PUB_SINK_BASE) / MBX_PUB_SINK_STRIDE >= MBX_N_PUB_SINKS) {
			return 0;
		}
		switch (in) {
		case MBX_PUB_SINK_REG_SID_LO:
			return ones(MBX_SID_LO_SID_LSB, MBX_SID_LO_SID_WIDTH);
		case MBX_PUB_SINK_REG_SID_HI:
			return ones(MBX_SID_HI_SID_LSB, MBX_SID_HI_SID_WIDTH);
		case MBX_PUB_SINK_REG_BINDING:
			return ones(MBX_BINDING_BOUND_LSB, MBX_BINDING_BOUND_WIDTH) |
			       ones(MBX_BINDING_SID_VALID_LSB, MBX_BINDING_SID_VALID_WIDTH) |
			       ones(MBX_BINDING_STARTED_LSB, MBX_BINDING_STARTED_WIDTH);
		default:
			return 0;
		}
	}
	switch (rel) {
	case MBX_PUB_REG_DA_GATE:
		return ones(MBX_DA_GATE_OPEN_LSB, MBX_DA_GATE_OPEN_WIDTH);
	case MBX_PUB_REG_LICENCE:
		return ones(MBX_LICENCE_ACTIVE_LSB, MBX_LICENCE_ACTIVE_WIDTH);
	case MBX_PUB_REG_IDLE_SLOPE:
		return ones(MBX_IDLE_SLOPE_BPS_LSB, MBX_IDLE_SLOPE_BPS_WIDTH);
	case MBX_PUB_REG_SR_DOMAIN:
		return ones(MBX_SR_DOMAIN_VID_LSB, MBX_SR_DOMAIN_VID_WIDTH) |
		       ones(MBX_SR_DOMAIN_PRIORITY_LSB, MBX_SR_DOMAIN_PRIORITY_WIDTH) |
		       ones(MBX_SR_DOMAIN_ADOPTED_LSB, MBX_SR_DOMAIN_ADOPTED_WIDTH);
	case MBX_PUB_REG_TALKER_DECL:
		return ones(MBX_TALKER_DECL_DECLARED_LSB, MBX_TALKER_DECL_DECLARED_WIDTH);
	default:
		return 0;
	}
}

void mbx_model_pub_view(const struct mbx_model *m, unsigned interface, struct mbx_model_pub *out)
{
	memset(out, 0, sizeof *out);
	if (interface >= MBX_N_IF) {
		return;
	}
	const uint32_t *w = m->pub[interface];
	uint32_t domain = w[MBX_PUB_REG_SR_DOMAIN / 4u];
	out->da_gate = mbx_field(w[MBX_PUB_REG_DA_GATE / 4u], MBX_DA_GATE_OPEN_LSB, MBX_DA_GATE_OPEN_WIDTH);
	out->licence = mbx_field(w[MBX_PUB_REG_LICENCE / 4u], MBX_LICENCE_ACTIVE_LSB, MBX_LICENCE_ACTIVE_WIDTH);
	out->idle_slope_bps = mbx_field(w[MBX_PUB_REG_IDLE_SLOPE / 4u], MBX_IDLE_SLOPE_BPS_LSB, MBX_IDLE_SLOPE_BPS_WIDTH);
	out->vid = (uint16_t)mbx_field(domain, MBX_SR_DOMAIN_VID_LSB, MBX_SR_DOMAIN_VID_WIDTH);
	out->priority = (uint8_t)mbx_field(domain, MBX_SR_DOMAIN_PRIORITY_LSB, MBX_SR_DOMAIN_PRIORITY_WIDTH);
	out->adopted = mbx_field(domain, MBX_SR_DOMAIN_ADOPTED_LSB, MBX_SR_DOMAIN_ADOPTED_WIDTH) != 0u;
	out->talker_decl = mbx_field(w[MBX_PUB_REG_TALKER_DECL / 4u], MBX_TALKER_DECL_DECLARED_LSB,
				     MBX_TALKER_DECL_DECLARED_WIDTH);
	for (unsigned k = 0; k < MBX_N_PUB_SINKS; ++k) {
		const uint32_t *e = w + (MBX_PUB_SINK_BASE + MBX_PUB_SINK_STRIDE * k) / 4u;
		uint32_t binding = e[MBX_PUB_SINK_REG_BINDING / 4u];
		out->bound[k] = mbx_field(binding, MBX_BINDING_BOUND_LSB, MBX_BINDING_BOUND_WIDTH) != 0u;
		out->started[k] = mbx_field(binding, MBX_BINDING_STARTED_LSB, MBX_BINDING_STARTED_WIDTH) != 0u;
		if (mbx_field(binding, MBX_BINDING_SID_VALID_LSB, MBX_BINDING_SID_VALID_WIDTH) != 0u) {
			out->sid[k] = ((uint64_t)e[MBX_PUB_SINK_REG_SID_HI / 4u] << 32) | e[MBX_PUB_SINK_REG_SID_LO / 4u];
		}
	}
}

// ---- the face block (contract 2.3) ------------------------------------------------

#define FIELD_MASK(r, f) \
	((MBX_##r##_##f##_WIDTH >= 32u ? 0xFFFFFFFFu : ((1u << MBX_##r##_##f##_WIDTH) - 1u)) << MBX_##r##_##f##_LSB)

// One window: its GO, status and data registers and its request registers,
// each an offset inside an interface's block, in the contract's order.
struct face_window {
	uint32_t go;
	uint32_t status;
	uint32_t data_lo;
	uint32_t data_hi;          // data_hi == data_lo: one data word
	uint32_t req[MBX_MODEL_WIN_WORDS];
	unsigned n_req;
};
static const struct face_window face_windows[MBX_MODEL_WINDOWS] = {
	{MBX_FACE_REG_CTR_CMD, MBX_FACE_REG_CTR_STATUS, MBX_FACE_REG_CTR_DATA, MBX_FACE_REG_CTR_DATA,
	 {MBX_FACE_REG_CTR_REQ, MBX_FACE_REG_CTR_WORD}, 2},
	{MBX_FACE_REG_AMAP_CMD, MBX_FACE_REG_AMAP_STATUS, MBX_FACE_REG_AMAP_DATA_LO, MBX_FACE_REG_AMAP_DATA_HI,
	 {MBX_FACE_REG_AMAP_REQ, MBX_FACE_REG_AMAP_PAGE}, 2},
	{MBX_FACE_REG_EDIT_CMD, MBX_FACE_REG_EDIT_STATUS, MBX_FACE_REG_EDIT_DATA_LO, MBX_FACE_REG_EDIT_DATA_HI,
	 {MBX_FACE_REG_EDIT_REQ, MBX_FACE_REG_EDIT_BEAT, MBX_FACE_REG_EDIT_RECORD_LO, MBX_FACE_REG_EDIT_RECORD_HI,
	  MBX_FACE_REG_EDIT_VALUE_LO, MBX_FACE_REG_EDIT_VALUE_HI}, 6},
	{MBX_FACE_REG_GSI_CMD, MBX_FACE_REG_GSI_STATUS, MBX_FACE_REG_GSI_DATA_LO, MBX_FACE_REG_GSI_DATA_HI,
	 {MBX_FACE_REG_GSI_REQ, MBX_FACE_REG_GSI_SEL, MBX_FACE_REG_GSI_PROP_LO, MBX_FACE_REG_GSI_PROP_HI}, 4},
};

// The fields of a setting or request register at `rel` inside an interface's
// block, an entry's included: 0 for a hole, an ro or wo register and an entry
// past the last.
static uint32_t face_mask(uint32_t rel)
{
	if (rel >= MBX_FACE_SINK_BASE) {
		if ((rel - MBX_FACE_SINK_BASE) / MBX_FACE_SINK_STRIDE >= MBX_N_PUB_SINKS) {
			return 0;
		}
		switch ((rel - MBX_FACE_SINK_BASE) % MBX_FACE_SINK_STRIDE) {
		case MBX_FACE_SNK_REG_F_FMT_IN_LO:
			return FIELD_MASK(F_FMT_IN_LO, FMT);
		case MBX_FACE_SNK_REG_F_FMT_IN_HI:
			return FIELD_MASK(F_FMT_IN_HI, FMT);
		case MBX_FACE_SNK_REG_F_SNK_VALID:
			return FIELD_MASK(F_SNK_VALID, FMT_IN);
		default:
			return 0;
		}
	}
	if (rel >= MBX_FACE_SOURCE_BASE) {
		if ((rel - MBX_FACE_SOURCE_BASE) / MBX_FACE_SOURCE_STRIDE >= MBX_N_PUB_SOURCES) {
			return 0;
		}
		switch ((rel - MBX_FACE_SOURCE_BASE) % MBX_FACE_SOURCE_STRIDE) {
		case MBX_FACE_SRC_REG_F_PT_OFFSET:
			return FIELD_MASK(F_PT_OFFSET, NS);
		case MBX_FACE_SRC_REG_F_FMT_OUT_LO:
			return FIELD_MASK(F_FMT_OUT_LO, FMT);
		case MBX_FACE_SRC_REG_F_FMT_OUT_HI:
			return FIELD_MASK(F_FMT_OUT_HI, FMT);
		case MBX_FACE_SRC_REG_F_SRC_VALID:
			return FIELD_MASK(F_SRC_VALID, PT_OFFSET) | FIELD_MASK(F_SRC_VALID, FMT_OUT);
		default:
			return 0;
		}
	}
	switch (rel) {
	case MBX_FACE_REG_F_CTRL:
		return FIELD_MASK(F_CTRL, READY);
	case MBX_FACE_REG_F_ENTITY:
		return FIELD_MASK(F_ENTITY, CUR_CONFIG) | FIELD_MASK(F_ENTITY, IDENTIFY);
	case MBX_FACE_REG_F_CLOCK:
		return FIELD_MASK(F_CLOCK, SOURCE_INDEX);
	case MBX_FACE_REG_F_AECP:
		return FIELD_MASK(F_AECP, LOCK_HELD) | FIELD_MASK(F_AECP, DYN_DIRTY);
	case MBX_FACE_REG_F_RESTORE:
		return FIELD_MASK(F_RESTORE, BUSY) | FIELD_MASK(F_RESTORE, DONE) | FIELD_MASK(F_RESTORE, FAIL) |
		       FIELD_MASK(F_RESTORE, BLANK) | FIELD_MASK(F_RESTORE, CLOSED) | FIELD_MASK(F_RESTORE, RB) |
		       FIELD_MASK(F_RESTORE, RS_CAUSE) | FIELD_MASK(F_RESTORE, CAUSE);
	case MBX_FACE_REG_F_NVM:
		return FIELD_MASK(F_NVM, BACKED) | FIELD_MASK(F_NVM, ALARM) | FIELD_MASK(F_NVM, DIRTY) |
		       FIELD_MASK(F_NVM, STALE) | FIELD_MASK(F_NVM, PEND) | FIELD_MASK(F_NVM, IMG_VALID) |
		       FIELD_MASK(F_NVM, VERDICT);
	case MBX_FACE_REG_CTR_REQ:
		return FIELD_MASK(CTR_REQ, TYPE) | FIELD_MASK(CTR_REQ, INDEX);
	case MBX_FACE_REG_CTR_WORD:
		return FIELD_MASK(CTR_WORD, WORD);
	case MBX_FACE_REG_AMAP_REQ:
		return FIELD_MASK(AMAP_REQ, TYPE) | FIELD_MASK(AMAP_REQ, INDEX);
	case MBX_FACE_REG_AMAP_PAGE:
		return FIELD_MASK(AMAP_PAGE, MAP_INDEX) | FIELD_MASK(AMAP_PAGE, SEL) | FIELD_MASK(AMAP_PAGE, REC);
	case MBX_FACE_REG_EDIT_REQ:
		return FIELD_MASK(EDIT_REQ, TYPE) | FIELD_MASK(EDIT_REQ, INDEX);
	case MBX_FACE_REG_EDIT_BEAT:
		return FIELD_MASK(EDIT_BEAT, PHASE) | FIELD_MASK(EDIT_BEAT, REMOVE) | FIELD_MASK(EDIT_BEAT, REC) |
		       FIELD_MASK(EDIT_BEAT, COUNT);
	case MBX_FACE_REG_EDIT_RECORD_LO:
	case MBX_FACE_REG_EDIT_RECORD_HI:
	case MBX_FACE_REG_EDIT_VALUE_LO:
	case MBX_FACE_REG_EDIT_VALUE_HI:
	case MBX_FACE_REG_GSI_PROP_LO:
	case MBX_FACE_REG_GSI_PROP_HI:
		return 0xFFFFFFFFu;
	case MBX_FACE_REG_GSI_REQ:
		return FIELD_MASK(GSI_REQ, TYPE) | FIELD_MASK(GSI_REQ, INDEX);
	case MBX_FACE_REG_GSI_SEL:
		return FIELD_MASK(GSI_SEL, KIND) | FIELD_MASK(GSI_SEL, SEL) | FIELD_MASK(GSI_SEL, ORD);
	default:
		return 0;
	}
}

// The window whose request register sits at `rel`, or MBX_MODEL_WINDOWS.
static unsigned face_request_window(uint32_t rel)
{
	for (unsigned w = 0; w < MBX_MODEL_WINDOWS; ++w) {
		for (unsigned k = 0; k < face_windows[w].n_req; ++k) {
			if (face_windows[w].req[k] == rel) {
				return w;
			}
		}
	}
	return MBX_MODEL_WINDOWS;
}

// The face block an offset falls in: interface *i and the offset *rel inside
// that interface's block; false outside every interface's.
static bool face_at(uint32_t off, unsigned *i, uint32_t *rel)
{
	if (off < MBX_FACE_BASE || off >= MBX_FACE_BASE + MBX_FACE_STRIDE * MBX_N_IF) {
		return false;
	}
	*i = (off - MBX_FACE_BASE) / MBX_FACE_STRIDE;
	*rel = (off - MBX_FACE_BASE) % MBX_FACE_STRIDE;
	return true;
}

static uint32_t face_read(const struct mbx_model *m, unsigned i, uint32_t rel)
{
	if (rel == MBX_FACE_REG_F_STATUS) {
		return mbx_place(m->fw_busy[i] ? 1u : 0u, MBX_F_STATUS_BUSY_LSB, MBX_F_STATUS_BUSY_WIDTH);
	}
	for (unsigned w = 0; w < MBX_MODEL_WINDOWS; ++w) {
		const struct face_window *fw = &face_windows[w];
		const struct mbx_model_win *s = &m->win[i][w];
		if (rel == fw->status) {
			// every window's STATUS has CTR_STATUS's layout (gen_mailbox.py refuses another)
			return mbx_place(s->busy ? 1u : 0u, MBX_CTR_STATUS_BUSY_LSB, MBX_CTR_STATUS_BUSY_WIDTH) |
			       mbx_place(s->done ? 1u : 0u, MBX_CTR_STATUS_DONE_LSB, MBX_CTR_STATUS_DONE_WIDTH) |
			       mbx_place(s->timeout ? 1u : 0u, MBX_CTR_STATUS_TIMEOUT_LSB, MBX_CTR_STATUS_TIMEOUT_WIDTH) |
			       mbx_place(s->tag, MBX_CTR_STATUS_TAG_LSB, MBX_CTR_STATUS_TAG_WIDTH);
		}
		if (rel == fw->data_lo) {
			return (uint32_t)s->data;
		}
		if (rel == fw->data_hi) {
			return (uint32_t)(s->data >> 32);
		}
	}
	return m->face[i][rel / 4u];
}

// The request registers' words of window w on interface i, in the contract's order.
static void face_request(const struct mbx_model *m, unsigned i, unsigned w, uint32_t *out)
{
	memset(out, 0, sizeof(uint32_t) * MBX_MODEL_WIN_WORDS);
	for (unsigned k = 0; k < face_windows[w].n_req; ++k) {
		out[k] = m->face[i][face_windows[w].req[k] / 4u];
	}
}

static void face_go(struct mbx_model *m, unsigned i, unsigned w)
{
	struct mbx_model_win *s = &m->win[i][w];
	s->busy = true;
	s->done = false;
	s->timeout = false;
	s->tag = (uint8_t)((s->tag + 1u) & ((1u << MBX_CTR_STATUS_TAG_WIDTH) - 1u));
	if (m->far != NULL && m->far->answer != NULL) {
		uint32_t request[MBX_MODEL_WIN_WORDS];
		uint64_t data = 0;
		face_request(m, i, w, request);
		enum mbx_model_reply reply = m->far->answer(m->far->ctx, i, w, request, &data);
		if (reply == MBX_MODEL_ANSWER) {
			mbx_model_win_answer(m, i, w, s->tag, data);
		} else if (reply == MBX_MODEL_SILENT) {
			mbx_model_win_expire(m, i, w);
		}
	}
}

// A write into interface i's face block: refused while it would move a held value.
static void face_write(struct mbx_model *m, unsigned i, uint32_t rel, uint32_t v)
{
	unsigned w = face_request_window(rel);
	bool setting = w == MBX_MODEL_WINDOWS && face_mask(rel) != 0u;
	bool held = (setting || rel == MBX_FACE_REG_F_COMMIT) ? m->fw_busy[i] : false;
	for (unsigned k = 0; k < MBX_MODEL_WINDOWS; ++k) {
		held = held || ((w == k || rel == face_windows[k].go) && m->win[i][k].busy);
	}
	if (held) {
		m->bus_err = sat16(m->bus_err);
		m->err = true;
		return;
	}
	if (rel == MBX_FACE_REG_F_COMMIT) {
		if (mbx_field(v, MBX_F_COMMIT_GO_LSB, MBX_F_COMMIT_GO_WIDTH) != 0u) {
			m->fw_busy[i] = true;
			if (m->far != NULL && m->far->commit != NULL && m->far->commit(m->far->ctx, i, m->face[i])) {
				m->fw_busy[i] = false;
			}
		}
		return;
	}
	for (unsigned k = 0; k < MBX_MODEL_WINDOWS; ++k) {
		if (rel == face_windows[k].go) {
			// every window's CMD has CTR_CMD's layout
			if (mbx_field(v, MBX_CTR_CMD_GO_LSB, MBX_CTR_CMD_GO_WIDTH) != 0u) {
				face_go(m, i, k);
			}
			return;
		}
	}
	m->face[i][rel / 4u] = v & face_mask(rel);
}

void mbx_model_face_view(const struct mbx_model *m, unsigned interface, struct mbx_model_face *out)
{
	memset(out, 0, sizeof *out);
	if (interface >= MBX_N_IF) {
		return;
	}
	const uint32_t *w = m->face[interface];
	out->send = m->fw_busy[interface];
	out->ctrl = w[MBX_FACE_REG_F_CTRL / 4u];
	out->entity = w[MBX_FACE_REG_F_ENTITY / 4u];
	out->clock = w[MBX_FACE_REG_F_CLOCK / 4u];
	out->aecp = w[MBX_FACE_REG_F_AECP / 4u];
	out->restore = w[MBX_FACE_REG_F_RESTORE / 4u];
	out->nvm = w[MBX_FACE_REG_F_NVM / 4u];
	for (unsigned s = 0; s < MBX_N_PUB_SOURCES; ++s) {
		const uint32_t *e = w + (MBX_FACE_SOURCE_BASE + MBX_FACE_SOURCE_STRIDE * s) / 4u;
		out->pt_offset[s] = e[MBX_FACE_SRC_REG_F_PT_OFFSET / 4u];
		out->fmt_out[s] = ((uint64_t)e[MBX_FACE_SRC_REG_F_FMT_OUT_HI / 4u] << 32) | e[MBX_FACE_SRC_REG_F_FMT_OUT_LO / 4u];
		out->src_valid[s] = e[MBX_FACE_SRC_REG_F_SRC_VALID / 4u];
	}
	for (unsigned k = 0; k < MBX_N_PUB_SINKS; ++k) {
		const uint32_t *e = w + (MBX_FACE_SINK_BASE + MBX_FACE_SINK_STRIDE * k) / 4u;
		out->fmt_in[k] = ((uint64_t)e[MBX_FACE_SNK_REG_F_FMT_IN_HI / 4u] << 32) | e[MBX_FACE_SNK_REG_F_FMT_IN_LO / 4u];
		out->snk_valid[k] = e[MBX_FACE_SNK_REG_F_SNK_VALID / 4u];
	}
	for (unsigned k = 0; k < MBX_MODEL_WINDOWS; ++k) {
		out->req[k] = m->win[interface][k].busy;
		out->tag[k] = m->win[interface][k].tag;
		face_request(m, interface, k, out->request[k]);
	}
}

void mbx_model_far_bind(struct mbx_model *m, const struct mbx_model_far *far)
{
	m->far = far;
}

void mbx_model_face_ack(struct mbx_model *m, unsigned interface)
{
	if (interface < MBX_N_IF) {
		m->fw_busy[interface] = false;
	}
}

void mbx_model_win_answer(struct mbx_model *m, unsigned interface, unsigned window, uint8_t tag, uint64_t data)
{
	if (interface >= MBX_N_IF || window >= MBX_MODEL_WINDOWS) {
		return;
	}
	struct mbx_model_win *s = &m->win[interface][window];
	if (s->busy && s->tag == tag) {
		s->busy = false;
		s->done = true;
		// a one-word window keeps the answer's low word
		s->data = face_windows[window].data_hi == face_windows[window].data_lo ? (uint32_t)data : data;
	}
}

void mbx_model_win_expire(struct mbx_model *m, unsigned interface, unsigned window)
{
	if (interface < MBX_N_IF && window < MBX_MODEL_WINDOWS && m->win[interface][window].busy) {
		m->win[interface][window].busy = false;
		m->win[interface][window].timeout = true;
	}
}

void mbx_model_face_event(struct mbx_model *m, unsigned interface, enum mbx_model_face_ev kind, uint16_t type,
			  uint16_t index)
{
	if (interface >= MBX_N_IF) {
		return;
	}
	switch (kind) {
	case MBX_MODEL_EV_COUNTERS:
		m->ctr_pending[interface] |= 1ull << ctr_bit(type, index);
		break;
	case MBX_MODEL_EV_AVB:
		m->avb_count[interface] = sat16(m->avb_count[interface]);
		break;
	case MBX_MODEL_EV_ASP:
		m->asp_count[interface] = sat16(m->asp_count[interface]);
		break;
	default:
		m->amap_count[interface] = sat16(m->amap_count[interface]);
		break;
	}
	post(m);
}

// The bound-talker block an offset falls in: interface *i, entry *e and the
// register's offset inside the entry; false outside it.
static bool bound_at(uint32_t off, unsigned *i, unsigned *e, uint32_t *reg)
{
	if (off < MBX_BND_BASE || off >= MBX_BND_BASE + MBX_BND_STRIDE * MBX_N_IF) {
		return false;
	}
	uint32_t rel = off - MBX_BND_BASE;
	*i = rel / MBX_BND_STRIDE;
	*e = (rel % MBX_BND_STRIDE) / MBX_BND_ENTRY_STRIDE;
	*reg = (rel % MBX_BND_STRIDE) % MBX_BND_ENTRY_STRIDE;
	return *e < MBX_N_BOUND;
}

static uint32_t read_channel(const struct mbx_model *m, unsigned c, uint32_t reg)
{
	const struct mbx_model_channel *ch = &m->ch[c];
	switch (reg) {
	case MBX_CH_REG_RX_HEAD:
		return ch->rx_head;
	case MBX_CH_REG_RX_TAIL:
		return ch->rx_tail;
	case MBX_CH_REG_TX_HEAD:
		return ch->tx_head;
	case MBX_CH_REG_TX_TAIL:
		return ch->tx_tail;
	case MBX_CH_REG_RX_DROP:
		return ch->rx_drop;
	case MBX_CH_REG_RATE_DROP:
		return ch->rate_drop;
	case MBX_CH_REG_TX_ERR:
		return ch->tx_err;
	case MBX_CH_REG_RX_PASS:
		return ch->rx_pass;
	default:
		return 0;
	}
}

static uint32_t read_interface(struct mbx_model *m, unsigned i, uint32_t reg)
{
	if (reg == MBX_IF_REG_GM_LO) {
		m->gm_hi_snap[i] = (uint32_t)(m->gm_id[i] >> 32);
		m->domain_snap[i] = m->domain[i];
		return (uint32_t)m->gm_id[i];
	}
	if (reg == MBX_IF_REG_GM_HI) {
		return m->gm_hi_snap[i];
	}
	return reg == MBX_IF_REG_DOMAIN ? m->domain_snap[i] : 0u;
}

// The ring a byte offset falls in, as an receive ring of channel *c, or the event
// ring (*c = MBX_N_CH); -1 when it falls in none the host may read.
static int readable_ring(uint32_t off, unsigned *c)
{
	if (off >= MBX_EVT_BASE && off < MBX_EVT_BASE + 4u * MBX_EVT_WORDS) {
		*c = MBX_N_CH;
		return 0;
	}
	for (unsigned k = 0; k < MBX_N_CH; ++k) {
		if (off >= rx_base[k] && off < rx_base[k] + 4u * rx_words[k]) {
			*c = k;
			return 0;
		}
	}
	return -1;
}

uint32_t mbx_model_read(struct mbx_model *m, uint32_t byte_offset)
{
	uint32_t off = byte_offset & (MBX_WINDOW_BYTES - 4u);
	unsigned c = 0;
	m->reads++;
	if (off < MBX_IF_BASE) {
		return read_global(m, off);
	}
	if (off < MBX_IF_BASE + MBX_IF_STRIDE * MBX_N_IF) {
		return read_interface(m, (off - MBX_IF_BASE) / MBX_IF_STRIDE, (off - MBX_IF_BASE) % MBX_IF_STRIDE);
	}
	if (off >= MBX_IFF_BASE && off < MBX_IFF_BASE + MBX_IFF_STRIDE * MBX_N_IF) {
		return read_interface_filter(m, (off - MBX_IFF_BASE) / MBX_IFF_STRIDE, (off - MBX_IFF_BASE) % MBX_IFF_STRIDE);
	}
	if (off >= MBX_CH_BASE && off < MBX_CH_BASE + MBX_CH_STRIDE * MBX_N_CH) {
		return read_channel(m, (off - MBX_CH_BASE) / MBX_CH_STRIDE, (off - MBX_CH_BASE) % MBX_CH_STRIDE);
	}
	unsigned i = 0;
	unsigned e = 0;
	uint32_t reg = 0;
	if (bound_at(off, &i, &e, &reg)) {
		return read_bound(m, i, e, reg);
	}
	if (pub_at(off, &i, &reg)) {
		return m->pub[i][reg / 4u];
	}
	if (face_at(off, &i, &reg)) {
		return face_read(m, i, reg);
	}
	if (off < MBX_REGISTER_SPACE_BYTES) {
		return read_global(m, off);
	}
	return readable_ring(off, &c) == 0 ? m->window[off / 4u] : 0u;
}

static uint32_t masked(uint32_t v, uint32_t lsb, uint32_t width)
{
	return mbx_place(mbx_field(v, lsb, width), lsb, width);
}

static void write_channel(struct mbx_model *m, unsigned c, uint32_t reg, uint32_t v)
{
	if (reg == MBX_CH_REG_RX_TAIL) {
		m->ch[c].rx_tail = (uint16_t)mbx_field(v, MBX_RX_TAIL_WORDS_LSB, MBX_RX_TAIL_WORDS_WIDTH);
	} else if (reg == MBX_CH_REG_TX_HEAD) {
		m->ch[c].tx_head = (uint16_t)mbx_field(v, MBX_TX_HEAD_WORDS_LSB, MBX_TX_HEAD_WORDS_WIDTH);
		tx_drain(m);
	}
}

static void write_tick_ctl(struct mbx_model *m, uint32_t v)
{
	m->tick_ctl = masked(v, MBX_TICK_CTL_EN_LSB, MBX_TICK_CTL_EN_WIDTH);
	if (m->tick_ctl == 0u) {
		m->tick_div = 0;
		m->tick_count = 0;
	}
}

static void write_global(struct mbx_model *m, uint32_t off, uint32_t v)
{
	switch (off) {
	case MBX_REG_IRQ_STATUS:
		if (mbx_field(v, MBX_IRQ_STATUS_ERR_LSB, MBX_IRQ_STATUS_ERR_WIDTH) != 0u) {
			m->err = false;
		}
		break;
	case MBX_REG_IRQ_ENABLE:
		m->irq_enable = masked(v, MBX_IRQ_ENABLE_RX_LSB, MBX_IRQ_ENABLE_RX_WIDTH) |
				masked(v, MBX_IRQ_ENABLE_EVT_LSB, MBX_IRQ_ENABLE_EVT_WIDTH) |
				masked(v, MBX_IRQ_ENABLE_ERR_LSB, MBX_IRQ_ENABLE_ERR_WIDTH);
		break;
	case MBX_REG_TICK_CTL:
		write_tick_ctl(m, v);
		break;
	case MBX_REG_OWN_EID_LO:
		m->own_eid = (m->own_eid & 0xFFFFFFFF00000000ull) | v;
		break;
	case MBX_REG_OWN_EID_HI:
		m->own_eid = (m->own_eid & 0xFFFFFFFFull) | ((uint64_t)v << 32);
		break;
	case MBX_REG_FILTER_EN:
		m->filter_en = masked(v, MBX_FILTER_EN_OPEN_LSB, MBX_FILTER_EN_OPEN_WIDTH);
		break;
	case MBX_REG_MAAP_BASE_LO:
		m->maap_base = (m->maap_base & 0xFFFF00000000ull) | v;
		break;
	case MBX_REG_MAAP_BASE_HI:
		m->maap_base = (m->maap_base & 0xFFFFFFFFull) |
			       ((uint64_t)mbx_field(v, MBX_MAAP_BASE_HI_ADDR_LSB, MBX_MAAP_BASE_HI_ADDR_WIDTH) << 32);
		break;
	case MBX_REG_MAAP_COUNT:
		m->maap_count = (uint16_t)mbx_field(v, MBX_MAAP_COUNT_COUNT_LSB, MBX_MAAP_COUNT_COUNT_WIDTH);
		break;
	case MBX_REG_TMR_DEADLINE:
		m->tmr_deadline = v;
		break;
	case MBX_REG_TMR_CMD:
		timer_command(m, v);
		break;
	case MBX_REG_EVT_TAIL:
		m->evt_tail = (uint16_t)mbx_field(v, MBX_EVT_TAIL_WORDS_LSB, MBX_EVT_TAIL_WORDS_WIDTH);
		break;
	default:
		break;
	}
}

static bool writable_ring(uint32_t off)
{
	for (unsigned k = 0; k < MBX_N_CH; ++k) {
		if (off >= tx_base[k] && off < tx_base[k] + 4u * tx_words[k]) {
			return true;
		}
	}
	return false;
}

void mbx_model_write(struct mbx_model *m, uint32_t byte_offset, uint32_t value, uint8_t strobes)
{
	uint32_t off = byte_offset & (MBX_WINDOW_BYTES - 4u);
	unsigned i = 0;
	unsigned e = 0;
	uint32_t reg = 0;
	m->writes++;
	if (strobes != 0xFu) {
		m->bus_err = sat16(m->bus_err);
		m->err = true;
		return;
	}
	if (off >= MBX_CH_BASE && off < MBX_CH_BASE + MBX_CH_STRIDE * MBX_N_CH) {
		write_channel(m, (off - MBX_CH_BASE) / MBX_CH_STRIDE, (off - MBX_CH_BASE) % MBX_CH_STRIDE, value);
	} else if (off >= MBX_IFF_BASE && off < MBX_IFF_BASE + MBX_IFF_STRIDE * MBX_N_IF) {
		write_interface_filter(m, (off - MBX_IFF_BASE) / MBX_IFF_STRIDE, (off - MBX_IFF_BASE) % MBX_IFF_STRIDE,
				       value);
	} else if (bound_at(off, &i, &e, &reg)) {
		write_bound(m, i, e, reg, value);
	} else if (pub_at(off, &i, &reg)) {
		m->pub[i][reg / 4u] = value & pub_mask(reg);
	} else if (face_at(off, &i, &reg)) {
		face_write(m, i, reg, value);
	} else if (off < MBX_REGISTER_SPACE_BYTES) {
		write_global(m, off, value);
	} else if (writable_ring(off)) {
		m->window[off / 4u] = value;
	}
	post(m);
}

const struct mbx_model_tx *mbx_model_tx_frame(const struct mbx_model *m, uint32_t k)
{
	if (k >= m->tx_sent || m->tx_sent - k > MBX_MODEL_TX_CAPTURE) {
		return NULL;
	}
	return &m->tx[k % MBX_MODEL_TX_CAPTURE];
}

const struct mbx_model_tmr_op *mbx_model_tmr_op(const struct mbx_model *m, uint32_t k)
{
	if (k >= m->tmr_ops || m->tmr_ops - k > MBX_MODEL_TMR_LOG) {
		return NULL;
	}
	return &m->tmr_log[k % MBX_MODEL_TMR_LOG];
}
