// SPDX-License-Identifier: CERN-OHL-W-2.0
#ifndef CTRL_APP_AECP_H
#define CTRL_APP_AECP_H
#include "ctrl_app.h"
#include "aecp_mbx.h"
#include "aecp_nvm.h"

#define CTRL_APP_AECP_SLOT (CTRL_APP_MAAP_FIRST_SLOT + MBX_N_IF)
struct ctrl_app_aecp {
	struct ctrl_app *app;
	struct aecp_mbx *aecp;
	struct aecp_nvm *state;
	const struct aecp_ports *environment;
	const struct acmp_env *acmp_owner;
	struct aecp_ports ports;
	struct acmp_env acmp_ports;
	uint8_t input_events[ACMP_MAX_SINKS];
	uint32_t bindings;
	uint16_t start_index;
	bool start_pending, start_value;
};

// After ctrl_app_compose, before restore/open. The caller initializes state
// against aecp->core afterwards and wraps its port with acmp_nvm for bindings.
// SRP may attach after ctrl_app_open; it preserves this existing ACMP owner.
bool ctrl_app_compose_aecp(struct ctrl_app *, struct ctrl_app_aecp *, struct aecp_mbx *,
			  const struct aecp_config *, const struct aecp_ports *, struct aecp_nvm *);
// After ctrl_app_open and optional SRP attachment; requires store release.
bool ctrl_app_open_aecp(struct ctrl_app_aecp *);
// Event-loop input only. Input events wait behind any causal ACMP response.
void ctrl_app_aecp_changed(struct ctrl_app_aecp *, uint16_t, uint16_t, unsigned);
#endif
