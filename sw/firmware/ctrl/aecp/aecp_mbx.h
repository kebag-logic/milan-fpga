// SPDX-License-Identifier: CERN-OHL-W-2.0
#ifndef CTRL_AECP_MBX_H
#define CTRL_AECP_MBX_H
#include "aecp.h"
#include "ctrl_loop.h"

#ifdef __cplusplus
extern "C" {
#endif

// Every core frame is at least 38 bytes: two header words plus ten payload
// words. One extra entry distinguishes a full completion queue from empty.
#define AECP_MBX_COMPLETIONS (MBX_CH_AECP_TX_WORDS / 12u + 1u)
struct aecp_mbx_completion {
	uint32_t cookie;
	uint16_t end;
};
struct aecp_mbx {
	struct aecp core;
	struct aecp_ports ports;
	const struct aecp_ports *environment;
	struct ctrl_loop *loop;
	unsigned slot;
	uint16_t tag;
	uint32_t deadline;
	bool armed;
	struct aecp_mbx_completion completions[AECP_MBX_COMPLETIONS];
	unsigned completion_head, completion_count;
	uint32_t stale_expiries;
};

// Does not touch the mailbox. environment supplies the observation, change
// and START ports; its transport/time fields are not used by this adapter.
bool aecp_mbx_init(struct aecp_mbx *, const struct aecp_config *,
		   const struct aecp_ports *environment, unsigned timer_slot);
bool aecp_mbx_attach(struct aecp_mbx *, struct ctrl_loop *);
// After the mailbox contract is checked and saved-state release permits AECP.
void aecp_mbx_open(struct aecp_mbx *);

#ifdef __cplusplus
}
#endif
#endif
