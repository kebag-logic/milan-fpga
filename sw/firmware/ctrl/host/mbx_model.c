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
//               grandmaster, lowest slot, tick;
//   KL_mbx      the register file, the GM_LO snapshot, the sticky ERR, the
//               refusal of a partial write, the interrupt levels, the
//               publication block (its fields masked, a hole reading 0 and
//               taking no write, the stream_id driven only while SID_VALID).

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
	return false;
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
	} else {
		m->tick_count = 0;
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
	memset(m, 0, sizeof *m);
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
			       ones(MBX_BINDING_SID_VALID_LSB, MBX_BINDING_SID_VALID_WIDTH);
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
	for (unsigned k = 0; k < MBX_N_PUB_SINKS; ++k) {
		const uint32_t *e = w + (MBX_PUB_SINK_BASE + MBX_PUB_SINK_STRIDE * k) / 4u;
		uint32_t binding = e[MBX_PUB_SINK_REG_BINDING / 4u];
		out->bound[k] = mbx_field(binding, MBX_BINDING_BOUND_LSB, MBX_BINDING_BOUND_WIDTH) != 0u;
		if (mbx_field(binding, MBX_BINDING_SID_VALID_LSB, MBX_BINDING_SID_VALID_WIDTH) != 0u) {
			out->sid[k] = ((uint64_t)e[MBX_PUB_SINK_REG_SID_HI / 4u] << 32) | e[MBX_PUB_SINK_REG_SID_LO / 4u];
		}
	}
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
