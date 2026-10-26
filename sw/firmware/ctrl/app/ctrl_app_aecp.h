// SPDX-License-Identifier: CERN-OHL-W-2.0
#ifndef CTRL_APP_AECP_H
#define CTRL_APP_AECP_H
#include "ctrl_app.h"
#include "aecp_face.h"
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
	struct aecp_face *face;                 // contract 2.3's face, or NULL
	uint32_t live_map_writes;               // AMAP_LIVE_WRITE records' counts
	uint32_t bindings;
	uint16_t start_index;
	bool start_pending;
	bool start_value;
};

// After ctrl_app_compose, before restore/open. The caller initializes state
// against aecp->core afterwards and wraps its port with acmp_nvm for bindings.
// SRP may attach after ctrl_app_open; it preserves this existing ACMP owner.
bool ctrl_app_compose_aecp(struct ctrl_app *, struct ctrl_app_aecp *, struct aecp_mbx *,
			  const struct aecp_config *, const struct aecp_ports *, struct aecp_nvm *);
// The face block's owner (contract 2.3), once composed and before open: it was
// handed to ctrl_app_compose_aecp as the environment (&face->ports). Its events
// drive the Table 5.22 notifications, and the saved-state store's status is
// published through it before AECP opens and on every change.
bool ctrl_app_aecp_attach_face(struct ctrl_app_aecp *, struct aecp_face *);
// The saved-state store's status as the processor reported its restore and
// store to the CSRs: F_RESTORE, F_NVM and whether a persisted setting is not
// saved yet (#665, ruling 6410169666 item 4). The store's boot walk is
// synchronous, so BUSY is never set; its abort causes are the store's own code
// space (nvm_store.h), which the processor's RS_CAUSE and CAUSE codes do not
// share, so both stay 0.
struct nvm_status;
void ctrl_app_aecp_store_words(const struct nvm_status *, uint32_t *restore, uint32_t *nvm, bool *dirty);
// After ctrl_app_open and optional SRP attachment; requires store release.
bool ctrl_app_open_aecp(struct ctrl_app_aecp *);
// Event-loop input only. Input events wait behind any causal ACMP response.
void ctrl_app_aecp_changed(struct ctrl_app_aecp *, uint16_t, uint16_t, unsigned);
#endif
