// SPDX-License-Identifier: CERN-OHL-W-2.0
#ifndef CTRL_AECP_MBX_H
#define CTRL_AECP_MBX_H
#include "aecp.h"
#include "ctrl_loop.h"

#ifdef __cplusplus
extern "C" {
#endif

// A notice's last frame keeps a completion (aecp_ports.fan_end, for a walk
// that reached its last recipient), and a notice waits while the queue is
// full; a power of two, so its wrap is a mask.
#define AECP_MBX_COMPLETIONS 32u
// THE RETRY's notices (ctrl_loop.h, #665), each to every registration of every interface, at what a round spends of its
// pass: a notice, 365 us to 32 recipients and 255 us to 16, and once a round AECP_ROUND_COLD_US, what its first attempt
// pays cold. Each is the line C + n x W over every round the CPU budget harness measured, plus 5 %, rounded up to 5 us
// (#665: a stated cost is an upper bound, and the harness fails a round over C + n x W + k x AECP_ATTEMPT_US,
// round_grade.py). A round takes as many as what its pass has left holds (aecp.c, scan): four in a pass of its own at
// 8x8/2if, seven at 1x1/1if, and fewer beside refused attempts, each charged AECP_ATTEMPT_US.
// The one exception to the 5 %: the cold cost at 8x8/2if is 185 us, 2.7 % over the most measured, 180.16 us (a round
// of no notice beside two refused attempts, on the image that merged dev-soft-core 0fb66211), because 185 us is the
// most THE RETRY's search holds the first notice to AECP_QUEUED_FIRST_MS at: 186 us already fails it, since its binding
// pass, a build of one (1,215 us) carrying a round's cold start, five refused attempts and a notice beside THE SHARE's
// margin, is then over THE SHARE, which at 185 us it fills exactly: 185 + 5 x 34 + 1,215 + 365 + 65 = 2,000 us (#665,
// decided 2026-11-13; FR_NFR.md 3.4.1). It expires at the 8x8/2if flip: #890 closes only with a measured cold cost of
// at most 176.1 us, or on a new owner decision.
#define AECP_NOTICE_US (MBX_N_IF == 1u ? 255u : 365u)
#define AECP_ROUND_COLD_US (MBX_N_IF == 1u ? 85u : 185u)
// A round sets the next one's earliest start. Two milliseconds, a pass, lets a row of passes given whole carry a queue.
// While records wait and the client yields it is two passes, and a round takes AECP_ROUND_YIELD_NOTICES: the rows a
// composed burst holds have the CPU those passes leave. Each round that builds beside records spends a yield, whatever
// else its pass carried, and with AECP_ROUND_YIELDS spent the client stands firm, at most AECP_ROUND_FIRM_NOTICES a
// round beside records: a round of four is shorter than the pace, so an ordinary pass stands between two. One
// interface yields none and caps none: its bound has no room for either, and its records wait no longer than two
// interfaces'.
#define AECP_ROUND_PACE_MS 2u
// THE PACE (#894, #904): an ADD or REMOVE_AUDIO_MAPPINGS that is checked holds AECP's next record in its ring, never
// dropped, until AECP_PACE_MS after the edit was taken (aecp_mbx.c, ready; the core stamps aecp.edited_ms). An edit's
// record grows with its mappings, so the rows that count every AECP command as the largest legal one, R4L and txL,
// take at most one a pace; the pace is the tier model's, the smallest that holds txL within the MRP timer budget at
// 1x1/1if, at most 13 ms (paced_rows.py, choice). The gate reads the core's clock, which each pass's poll moves on, so
// a held record is taken at most two passes late, and a burst of AECP_REGISTRATIONS edits answers its last within 15
// paces, their passes and its own row, inside the 240 ms response time of IEEE 1722.1-2021 9.3.2.6.
#define AECP_PACE_MS 8u
#define AECP_ROUND_YIELD_PACE_MS 4u
#define AECP_ROUND_YIELD_NOTICES 1u
#define AECP_ROUND_FIRM_NOTICES (MBX_N_IF == 1u ? AECP_NOTICES_MOST : 4u)
#define AECP_ROUND_YIELDS (3u * (MBX_N_IF - 1u))
// The bound of FR_NFR.md 3.4.1 on notices queued behind one another, under THE TIERS (ctrl_loop.h; #894, #665, the
// decision of 2026-11-09 and decision D). A queue's first notice is tier 1's and commits within AECP_QUEUED_FIRST_MS of
// its port's answer, 20 ms at 1x1/1if; every notice queued behind it is tier 2's, its rounds a slice each behind tier 1
// and SRP's records, and commits within AECP_QUEUED_MS, the last queued notice's 125 ms, half of the 250 ms a
// controller waits on an AECP command (IEEE 1722.1-2021 9.3.2.6). The rows by every source hold both at the built
// design's slice (tb/verilator/ctrl_service_budget/rows_tiers.py, flip_grade.py --design built), and the CPU budget
// harness holds every measured queue to them. At 8x8/2if the stated 22 and 62 ms stand: its rows by every source do not
// fit and are reported, not held (#894, the owner's decision of 2026-11-12, owed to #872).
#define AECP_QUEUED_FIRST_MS (MBX_N_IF == 1u ? 20u : 22u)
#define AECP_QUEUED_MS (MBX_N_IF == 1u ? 125u : 62u)
// The owed-notice queue's slots an integrator gives AECP (aecp_config.owed, #894): the AECP channel's burst at one
// interface, so its last record never waits on a full queue; none at two, whose ledger has no room for them
// (docs/design/SPLIT_CONTROL_MEMORY.md section 5), so there the next record waits for every notice, as before.
#define AECP_MBX_OWED_SLOTS (MBX_N_IF == 1u ? MBX_CH_AECP_RATE_BURST : 0u)
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
