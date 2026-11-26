// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
// The LED observer's platform ports. Compiled only into an image with LEDs.
#ifndef CTRL_PLAT_LEDS_PORTS_H
#define CTRL_PLAT_LEDS_PORTS_H

#include "ctrl_app_aecp.h"
#include "ctrl_plat_leds.h"
#include "srp_mbx.h"

// An input's bound state belongs to ACMP, not the datapath's stream window.
// Read the same member acmp_view returns, in the same single-threaded event
// loop. No copied state or mailbox read is needed for that one bit. The LED
// observer still checks the media-lock counters before declaring reception.
// An output needs GSI words 0 and 6, not a brief observation: word 0 selects
// the declaring owner, and word 6 carries the fabric extended flags. For a
// declaring output, use the same SRP Listener state as ctrl_app_aecp output().
static inline bool ctrl_plat_leds_stream(void *ctx, unsigned interface, uint16_t type, uint16_t index,
					struct aecp_stream_info *out)
{
#ifdef __cplusplus
	struct aecp_mbx *adapter = static_cast<struct aecp_mbx *>(ctx);
	struct ctrl_app_aecp *owner = static_cast<struct ctrl_app_aecp *>(adapter->environment->ctx);
#else
	struct aecp_mbx *adapter = ctx;
	struct ctrl_app_aecp *owner = adapter->environment->ctx;
#endif
	if (type == CTRL_PLAT_LEDS_STREAM_INPUT) {
		const struct acmp *acmp = &owner->app->acmp.acmp;
		if (index >= acmp->cfg.n_sinks) return false;
		out->bound = acmp->sinks[index].bound;
		return true;
	}
	const struct acmp_config *cfg = &owner->app->acmp.acmp.cfg;
	if (type != CTRL_PLAT_LEDS_STREAM_OUTPUT || index >= cfg->n_sources) return false;
	uint32_t request[4] = {mbx_place(type, MBX_GSI_REQ_TYPE_LSB, MBX_GSI_REQ_TYPE_WIDTH) |
				       mbx_place(index, MBX_GSI_REQ_INDEX_LSB, MBX_GSI_REQ_INDEX_WIDTH), 0u, 0u, 0u};
	uint64_t flags = 0u;
	uint64_t extended = 0u;
	if (mbx_win_read(interface, MBX_WIN_GSI, request, &flags) != MBX_STATUS_OK) return false;
	request[1] = mbx_place(6u, MBX_GSI_SEL_SEL_LSB, MBX_GSI_SEL_SEL_WIDTH);
	if (mbx_win_read(interface, MBX_WIN_GSI, request, &extended) != MBX_STATUS_OK) return false;
	out->flags_ex = (uint32_t)extended;
	if (((uint32_t)flags & 0x10000000u) != 0u) {
		const struct srp_interface *srp = owner->app->srp != NULL && index < CTRL_SRP_SOURCES
			? &owner->app->srp->ifs[cfg->source_interface[index]] : NULL;
		out->flags_ex = srp != NULL && srp->listener_present[index] ? 1u : 0u;
	}
	return true;
}

#endif
