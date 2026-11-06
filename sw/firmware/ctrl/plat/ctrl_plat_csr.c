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
