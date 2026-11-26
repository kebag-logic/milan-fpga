// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
// The LED observer's platform ports. Compiled only into an image with LEDs.
#ifndef CTRL_PLAT_LEDS_PORTS_H
#define CTRL_PLAT_LEDS_PORTS_H

#include "ctrl_app_aecp.h"
#include "ctrl_plat_leds.h"

// An input's bound state belongs to ACMP, not the datapath's stream window.
// Read the same member acmp_view returns, in the same single-threaded event
// loop. No copied state or mailbox read is needed for that one bit. The LED
// observer still checks the media-lock counters before declaring reception.
// An output keeps the complete stream port: its extended flags carry the
// Listener's registration and a brief observation cannot answer that rule.
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
	return adapter->environment->stream(owner, interface, type, index, out);
}

#endif
