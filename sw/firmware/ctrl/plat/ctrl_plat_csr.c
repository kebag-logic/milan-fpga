// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// ctrl_plat_csr.c - the datapath CSR window in the split placement (see
// ctrl_plat_csr.h).

#include "ctrl_plat_csr.h"

#include "ctrl_plat_io.h"

static uint32_t rd(uintptr_t csr, uint32_t offset)
{
	return ctrl_plat_io_read32(csr + offset);
}

static void wr(uintptr_t csr, uint32_t offset, uint32_t value)
{
	ctrl_plat_io_write32(csr + offset, value);
}

bool ctrl_plat_csr_identity(uintptr_t csr, uint32_t *version)
{
	uint32_t id = rd(csr, CTRL_PLAT_CSR_ID);
	*version = rd(csr, CTRL_PLAT_CSR_VERSION);
	return id == CTRL_PLAT_MILAN_ID;
}

void ctrl_plat_csr_policy(uintptr_t csr, const struct ctrl_plat_policy *p)
{
	// Step 2: no fabric advertiser and no processor while the core validates
	wr(csr, CTRL_PLAT_CSR_ADP_CTRL, rd(csr, CTRL_PLAT_CSR_ADP_CTRL) & ~1u);
	wr(csr, CTRL_PLAT_CSR_PP_CTRL, rd(csr, CTRL_PLAT_CSR_PP_CTRL) & ~1u);
	// Step 3: the generated identity, the one the AEM image and ADP carry
	wr(csr, CTRL_PLAT_CSR_ADP_EID_LO, p->entity_id_lo);
	wr(csr, CTRL_PLAT_CSR_ADP_EID_HI, p->entity_id_hi);
	wr(csr, CTRL_PLAT_CSR_ADP_MID_LO, p->model_id_lo);
	wr(csr, CTRL_PLAT_CSR_ADP_MID_HI, p->model_id_hi);
	wr(csr, CTRL_PLAT_CSR_MAC_ADDR_LO, p->station_mac_lo);
	wr(csr, CTRL_PLAT_CSR_MAC_ADDR_HI, p->station_mac_hi);
	// the accept-all receive posture: station selection bypassed on a miss
	wr(csr, CTRL_PLAT_CSR_MAC_CTRL, rd(csr, CTRL_PLAT_CSR_MAC_CTRL) | p->mac_ctrl_set);
	wr(csr, CTRL_PLAT_CSR_TCAM_CTRL, p->tcam_ctrl);
	// the fabric's media policy for this shape
	wr(csr, CTRL_PLAT_CSR_AAF_CTRL, p->aaf_ctrl);
	wr(csr, CTRL_PLAT_CSR_LWSRP_VID, p->sr_vid);
	wr(csr, CTRL_PLAT_CSR_LWSRP_CTRL, p->lwsrp_ctrl_reset | CTRL_PLAT_LWSRP_LIVE);
	wr(csr, CTRL_PLAT_CSR_MAAP_CTRL, p->maap_ctrl);
	wr(csr, CTRL_PLAT_CSR_CRF_TX_CTRL, p->crf_tx_ctrl);
}

void ctrl_plat_csr_status(uintptr_t csr, struct ctrl_plat_status *s)
{
	// each low word first: reading it takes the pair's snapshot
	s->gm_lo = rd(csr, CTRL_PLAT_CSR_GM_LO);
	s->gm_hi = rd(csr, CTRL_PLAT_CSR_GM_HI);
	s->parent_lo = rd(csr, CTRL_PLAT_CSR_PARENT_LO);
	s->parent_hi = rd(csr, CTRL_PLAT_CSR_PARENT_HI);
	s->pdelay_ns = rd(csr, CTRL_PLAT_CSR_PDELAY);
	s->as_path = rd(csr, CTRL_PLAT_CSR_AS_PATH_CMD);
	s->clkv_stat = rd(csr, CTRL_PLAT_CSR_CLKV_STAT);
	s->gptp_lat = rd(csr, CTRL_PLAT_CSR_GPTP_LAT);
	s->id = rd(csr, CTRL_PLAT_CSR_ID);
	s->version = rd(csr, CTRL_PLAT_CSR_VERSION);
	s->ptp_ctrl = rd(csr, CTRL_PLAT_CSR_PTP_CTRL);
	s->adp_ctrl = rd(csr, CTRL_PLAT_CSR_ADP_CTRL);
	s->pp_ctrl = rd(csr, CTRL_PLAT_CSR_PP_CTRL);
	s->pp_stat = rd(csr, CTRL_PLAT_CSR_PP_STAT);
}

void ctrl_plat_csr_sink_format(uintptr_t csr, unsigned n, uint64_t format)
{
	// the window's words by their offset from its selection
	const uintptr_t window = csr + CTRL_PLAT_CSR_STRM_SEL;
	uint32_t selection = ctrl_plat_io_read32(window);
	// dir 0, the listener contexts: index n
	ctrl_plat_io_write32(window, n & 0xFu);
	ctrl_plat_io_write32(window + (CTRL_PLAT_CSR_STRMW_FMT_LO - CTRL_PLAT_CSR_STRM_SEL), (uint32_t)format);
	ctrl_plat_io_write32(window + (CTRL_PLAT_CSR_STRMW_FMT_HI - CTRL_PLAT_CSR_STRM_SEL), (uint32_t)(format >> 32));
	ctrl_plat_io_write32(window, selection);
}

// IEEE 1722.1-2021 7.2.6: a STREAM_INPUT's descriptor_type, descriptor_index,
// current_format and avb_interface_index, by offset in its descriptor
enum { STREAM_INPUT = 5u, TYPE_AT = 0u, INDEX_AT = 2u, FORMAT_AT = 74u, INTERFACE_AT = 126u };
// IEEE 1722-2016 Table 6: the AAF subtype, a stream format's first byte
#define AAF_SUBTYPE 0x02u

static uint32_t be32(const uint8_t *p)
{
	return ((uint32_t)p[0] << 24) | ((uint32_t)p[1] << 16) | ((uint32_t)p[2] << 8) | p[3];
}

bool ctrl_plat_csr_sink_context(const uint8_t *value, size_t length, uint16_t configuration, uint16_t in_force,
				uint64_t *format)
{
	if (length < INTERFACE_AT + 2u) {
		return false;
	}
	*format = ((uint64_t)be32(value + FORMAT_AT) << 32) | be32(value + FORMAT_AT + 4u);
	// type and index are the descriptor's first two words; the interface's two bytes are 0 or not
	uint32_t key = be32(value + TYPE_AT);
	return configuration == in_force && (key >> 16) == STREAM_INPUT && (key & 0xFFFFu) != 0u &&
	       value[FORMAT_AT] == AAF_SUBTYPE && (value[INTERFACE_AT] | value[INTERFACE_AT + 1u]) == 0u;
}

bool ctrl_plat_csr_tod(uintptr_t csr, uint64_t *ns)
{
	wr(csr, CTRL_PLAT_CSR_PTP_CMD, CTRL_PLAT_PTP_SNAPSHOT);
	for (volatile uint32_t spin = CTRL_PLAT_SNAPSHOT_SPIN; spin != 0u; spin = spin - 1u) {
	}
	for (unsigned tries = 0; tries < CTRL_PLAT_TOD_TRIES; ++tries) {
		uint32_t hi = rd(csr, CTRL_PLAT_CSR_TOD_RD_HI);
		uint32_t lo = rd(csr, CTRL_PLAT_CSR_TOD_RD_LO);
		if (rd(csr, CTRL_PLAT_CSR_TOD_RD_HI) == hi) {
			*ns = ((uint64_t)hi << 32) | lo;
			return true;
		}
	}
	return false;
}

#ifdef CTRL_PLAT_LAT_WRITABLE
uint32_t ctrl_plat_csr_set_lat(uintptr_t csr, uint16_t ingress_ns, uint16_t egress_ns)
{
	wr(csr, CTRL_PLAT_CSR_PTP_ILAT, ingress_ns);
	wr(csr, CTRL_PLAT_CSR_PTP_ELAT, egress_ns);
	return rd(csr, CTRL_PLAT_CSR_GPTP_LAT);
}
#endif
