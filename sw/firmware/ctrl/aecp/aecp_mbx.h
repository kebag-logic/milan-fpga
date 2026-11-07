// SPDX-License-Identifier: CERN-OHL-W-2.0
#ifndef CTRL_AECP_MBX_H
#define CTRL_AECP_MBX_H
#include "aecp.h"
#include "ctrl_loop.h"

#ifdef __cplusplus
extern "C" {
#endif

// A notice's last frame keeps a completion (aecp_ports.fan_end), and a notice
// waits while the queue is full; a power of two, so its wrap is a mask.
#define AECP_MBX_COMPLETIONS 32u
// THE RETRY's notices (ctrl_loop.h, #665), each to every registration of every interface, at what a round spends of its
// pass: a recipient's share, in quarter microseconds, and the notice's own, 320 us to 32 recipients and 220 us to 16,
// and once a round AECP_ROUND_COLD_US, what its first attempt pays cold, the line over the rounds measured (CPU budget
// harness). A round takes as many as what its pass has left holds (aecp.c, scan): five in a pass of its own at 8x8/2if,
// eight at 1x1/1if, and fewer beside refused attempts, each charged AECP_ATTEMPT_US.
#define AECP_RECIPIENT_QUARTER_US 25u
#define AECP_NOTICE_US (MBX_N_IF * AECP_REGISTRATIONS * AECP_RECIPIENT_QUARTER_US / 4u + 120u)
#define AECP_ROUND_COLD_US (MBX_N_IF * 80u)
// A round sets the next one's earliest start. Two milliseconds, a pass, lets a row of passes given whole carry a queue.
// While records wait and the client yields it is two passes, and a round takes AECP_ROUND_YIELD_NOTICES: the rows a
// composed burst holds have the CPU those passes leave. Each round that builds beside records spends a yield, whatever
// else its pass carried, and with AECP_ROUND_YIELDS spent the client stands firm, at most AECP_ROUND_FIRM_NOTICES a
// round beside records: a round of four is shorter than the pace, so an ordinary pass stands between two. One
// interface yields none and caps none: its bound has no room for either, and its records wait no longer than two
// interfaces'.
#define AECP_ROUND_PACE_MS 2u
#define AECP_ROUND_YIELD_PACE_MS 4u
#define AECP_ROUND_YIELD_NOTICES 1u
#define AECP_ROUND_FIRM_NOTICES (MBX_N_IF == 1u ? AECP_NOTICES_MOST : 4u)
#define AECP_ROUND_YIELDS (3u * (MBX_N_IF - 1u))
// The bound of FR_NFR.md 3.4.1 on notices queued behind one another (the owner's ruling of 2026-11-06, #665), every
// constant above in it. The first retried notice commits within AECP_NOTICE_MS of its port's answer. Every notice
// queued behind it commits within AECP_QUEUED_MS: the 8 ms spacing, then AECP_QUEUED_PASSES passes of THE SHARE for
// AECP_NOTICES_MOST notices at the point's own recipient count, 60 ms at 8x8/2if and 20 ms at 1x1/1if, each its
// ceiling. The passes come from a search of what the loop may be made to do (ctrl_retry_search.py, a gate): each pass
// charged all of THE SHARE, at most THE DRAIN's passes, an interface's builds, the aged steps, a retry's due time
// anywhere in the spacing and every count of refusing ports, charged to every round. aecp_mbx.c holds AECP_QUEUED_MS
// to its ceiling.
#define AECP_QUEUED_PASSES (MBX_N_IF == 1u ? 6u : 26u)
#define AECP_QUEUED_MS (AECP_RETRY_MAX_MS + AECP_QUEUED_PASSES * CTRL_LOOP_SHARE_US / 1000u)
#define AECP_QUEUED_CEILING_MS (MBX_N_IF == 1u ? 20u : 60u)
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
	unsigned yields;         // the rounds of this queue that gave way to waiting records
};

// Does not touch the mailbox. environment supplies the observation, change
// and START ports; its transport/time fields are not used by this adapter.
bool aecp_mbx_init(struct aecp_mbx *, const struct aecp_config *,
		   const struct aecp_ports *environment, unsigned timer_slot);
// Binds the AECP channel, a sink, a poll and THE RETRY's client (ctrl_loop.h),
// and holds the core's due retries for that client (aecp.retry_hold, #665).
// False, binding nothing, when any of them is taken or its table is full.
bool aecp_mbx_attach(struct aecp_mbx *, struct ctrl_loop *);
// After the mailbox contract is checked and saved-state release permits AECP.
void aecp_mbx_open(struct aecp_mbx *);

#ifdef __cplusplus
}
#endif
#endif
