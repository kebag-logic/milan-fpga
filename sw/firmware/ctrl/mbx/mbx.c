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

#include "mbx_hal.h"
#include "mbx_wire.h"

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

static uint16_t counter(uint32_t byte_offset)
{
	return (uint16_t)mbx_field(mbx_hal_read32(byte_offset), 0u, MBX_INDEX_BITS);
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
	if (!caps_match(mbx_hal_read32(MBX_REG_ID), mbx_hal_read32(MBX_REG_CAPS))) {
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
	mbx_hal_write32(MBX_REG_OWN_EID_LO, (uint32_t)entity_id);
	mbx_hal_write32(MBX_REG_OWN_EID_HI, (uint32_t)(entity_id >> 32));
}

void mbx_filter_open(uint32_t channel_mask)
{
	mbx_hal_write32(MBX_REG_FILTER_EN, mbx_place(channel_mask, MBX_FILTER_EN_OPEN_LSB, MBX_FILTER_EN_OPEN_WIDTH));
}

void mbx_filter_set_maap_range(uint64_t base, uint16_t count)
{
	mbx_hal_write32(MBX_REG_MAAP_BASE_LO, (uint32_t)base);
	mbx_hal_write32(MBX_REG_MAAP_BASE_HI,
			mbx_place((uint32_t)(base >> 32), MBX_MAAP_BASE_HI_ADDR_LSB, MBX_MAAP_BASE_HI_ADDR_WIDTH));
	mbx_hal_write32(MBX_REG_MAAP_COUNT, mbx_place(count, MBX_MAAP_COUNT_COUNT_LSB, MBX_MAAP_COUNT_COUNT_WIDTH));
}

bool mbx_filter_set_own_mac(unsigned interface, uint64_t mac)
{
	if (interface >= MBX_N_IF) {
		return false;
	}
	mbx_hal_write32(iff_reg(interface, MBX_IFF_REG_OWN_MAC_LO),
			mbx_place((uint32_t)mac, MBX_OWN_MAC_LO_MAC_LSB, MBX_OWN_MAC_LO_MAC_WIDTH));
	mbx_hal_write32(iff_reg(interface, MBX_IFF_REG_OWN_MAC_HI),
			mbx_place((uint32_t)(mac >> 32), MBX_OWN_MAC_HI_MAC_LSB, MBX_OWN_MAC_HI_MAC_WIDTH));
	return true;
}

uint16_t mbx_filter_mismatch(void)
{
	return (uint16_t)mbx_field(mbx_hal_read32(MBX_REG_FILTER_MISMATCH), MBX_FILTER_MISMATCH_COUNT_LSB,
				   MBX_FILTER_MISMATCH_COUNT_WIDTH);
}

static uint32_t rx_word(unsigned ch, uint32_t index)
{
	return mbx_hal_read32(rx_base[ch] + 4u * (index & (rx_words[ch] - 1u)));
}

// Release everything up to RX_HEAD.
static enum mbx_status rx_resync(unsigned ch, uint16_t head)
{
	rx_tail[ch] = head;
	mbx_hal_write32(ch_reg(ch, MBX_CH_REG_RX_TAIL), head);
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
	for (uint32_t i = 0; i < payload; ++i) {
		uint32_t word = rx_word(ch, (uint32_t)tail + MBX_RX_HDR_WORDS + i);
		uint32_t n = len - 4u * i;
		ring_lanes_unpack(word, &f->bytes[4u * i], n > 4u ? 4u : n);
	}
	f->len = (uint16_t)len;
	f->interface = (uint8_t)mbx_field(w0, MBX_RXREC_W0_IF_LSB, MBX_RXREC_W0_IF_WIDTH);
	f->arrival_ms = mbx_field(w1, MBX_RXREC_W1_ARRIVAL_MS_LSB, MBX_RXREC_W1_ARRIVAL_MS_WIDTH);
	rx_tail[ch] = (uint16_t)(tail + record);
	mbx_hal_write32(ch_reg(ch, MBX_CH_REG_RX_TAIL), rx_tail[ch]);
	return MBX_STATUS_OK;
}

static void tx_word(unsigned ch, uint32_t index, uint32_t value)
{
	mbx_hal_write32(tx_base[ch] + 4u * (index & (tx_words[ch] - 1u)), value);
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
	for (uint32_t i = 0; i < payload; ++i) {
		uint32_t n = (uint32_t)len - 4u * i;
		tx_word(ch, (uint32_t)head + MBX_TX_HDR_WORDS + i, ring_lanes_pack(&frame[4u * i], n > 4u ? 4u : n));
	}
	tx_head[ch] = (uint16_t)(head + record);
	tx_seq = (uint16_t)(tx_seq + 1u);
	mbx_hal_write32(ch_reg(ch, MBX_CH_REG_TX_HEAD), tx_head[ch]);
	return MBX_STATUS_OK;
}

static uint32_t evt_word(uint32_t index)
{
	return mbx_hal_read32(MBX_EVT_BASE + 4u * (index & (MBX_EVT_WORDS - 1u)));
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
	mbx_hal_write32(MBX_REG_EVT_TAIL, evt_tail);
	return true;
}

uint32_t mbx_now_ms(void)
{
	return mbx_hal_read32(MBX_REG_NOW_MS);
}

void mbx_timer_arm(unsigned slot, uint16_t tag, uint32_t deadline_ms)
{
	mbx_hal_write32(MBX_REG_TMR_DEADLINE, deadline_ms);
	mbx_hal_write32(MBX_REG_TMR_CMD, mbx_place(slot, MBX_TMR_CMD_SLOT_LSB, MBX_TMR_CMD_SLOT_WIDTH) |
					 mbx_place(tag, MBX_TMR_CMD_TAG_LSB, MBX_TMR_CMD_TAG_WIDTH) |
					 mbx_place(MBX_TMR_OP_ARM, MBX_TMR_CMD_OP_LSB, MBX_TMR_CMD_OP_WIDTH));
}

void mbx_timer_cancel(unsigned slot)
{
	mbx_hal_write32(MBX_REG_TMR_CMD, mbx_place(slot, MBX_TMR_CMD_SLOT_LSB, MBX_TMR_CMD_SLOT_WIDTH) |
					 mbx_place(MBX_TMR_OP_CANCEL, MBX_TMR_CMD_OP_LSB, MBX_TMR_CMD_OP_WIDTH));
}

void mbx_tick_enable(bool enable)
{
	mbx_hal_write32(MBX_REG_TICK_CTL, mbx_place(enable ? 1u : 0u, MBX_TICK_CTL_EN_LSB, MBX_TICK_CTL_EN_WIDTH));
}

bool mbx_link_up(unsigned interface)
{
	uint32_t up = mbx_field(mbx_hal_read32(MBX_REG_LINK), MBX_LINK_UP_LSB, MBX_LINK_UP_WIDTH);
	return ((up >> interface) & 1u) != 0u;
}

uint64_t mbx_gm_id(unsigned interface, uint8_t *domain)
{
	// GM_LO first: reading it snapshots GM_HI and DOMAIN for the next reads
	uint32_t lo = mbx_hal_read32(if_reg(interface, MBX_IF_REG_GM_LO));
	uint32_t hi = mbx_hal_read32(if_reg(interface, MBX_IF_REG_GM_HI));
	uint32_t dom = mbx_hal_read32(if_reg(interface, MBX_IF_REG_DOMAIN));
	if (domain != NULL) {
		*domain = (uint8_t)mbx_field(dom, MBX_DOMAIN_NUMBER_LSB, MBX_DOMAIN_NUMBER_WIDTH);
	}
	return ((uint64_t)mbx_field(hi, MBX_GM_HI_ID_LSB, MBX_GM_HI_ID_WIDTH) << 32) |
	       (uint64_t)mbx_field(lo, MBX_GM_LO_ID_LSB, MBX_GM_LO_ID_WIDTH);
}

uint32_t mbx_irq_status(void)
{
	return mbx_hal_read32(MBX_REG_IRQ_STATUS);
}

void mbx_irq_enable(uint32_t mask)
{
	mbx_hal_write32(MBX_REG_IRQ_ENABLE, mask);
}

void mbx_irq_clear_err(void)
{
	mbx_hal_write32(MBX_REG_IRQ_STATUS, mbx_place(1u, MBX_IRQ_STATUS_ERR_LSB, MBX_IRQ_STATUS_ERR_WIDTH));
}
