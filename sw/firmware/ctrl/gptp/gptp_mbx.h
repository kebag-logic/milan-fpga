// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// gptp_mbx.h - the gPTP end station ports on the mailbox and the loop
// (contract 2.5; #884, #665 F6).
//
// One gptp_port per interface. The adapter binds the gptp channel's receive
// ring (each record to its interface's port, its ingress stamp first: the
// record's eight-octet trailer, KL_ctrl_split's), an event sink (TIMESTAMP,
// an egress stamp, to the port that launched it; LINK to the port's
// portEnabled) and a centisecond consumer (the ports' timers, on NOW_MS),
// and no poll: each of the three publishes the port it ran, in the pass that
// ran it, so a pass that ran none of them costs nothing (#884, R2-5). Its HAL
// sends on the gptp channel's transmit ring and drives each interface's PHC
// through `phc`, the platform's (the CSR's PTP block on the split,
// ctrl_plat_csr.h).
//
// THE PUBLISHED SNAPSHOT (#884's ruling of 2026-11-21, item 7). A port's
// state is published whenever anything GET_AVB_INFO or GET_AS_PATH
// answers moved: the adapter writes the narrowed words (GPTP_GM_LO,
// GPTP_GM_HI, then GPTP_STATE with GEN moved) and keeps the whole state as
// the snapshot of that GEN. The AECP owner answers both commands' gPTP fields from the
// snapshot (gptp_mbx_snapshot), so its answers are the publication the
// datapath holds, and the adapter raises both changes itself (the
// datapath's detectors are off under gPTP in firmware): AVB_INFO when the
// grandmaster, the neighbor delay, the domain or asCapable moved, AS_PATH
// when the path trace did (Milan v1.2 Table 5.22).
//
// THE BOUND (ctrl_loop.h THE SHARE): a record costs the port's ts and rx; an
// event, its ts or link; a centisecond, every port's tick; each, for a port
// that moved, MBX_PUB_GPTP_WORDS bus writes and the AECP owner's notice.
// None waits on the fabric.

#ifndef GPTP_MBX_H
#define GPTP_MBX_H

#include "ctrl_loop.h"
#include "gptp.h"
#include "mbx.h"

#ifdef __cplusplus
extern "C" {
#endif

struct gptp_mbx_phc {
	void *ctx;
	void (*adjfine)(void *ctx, unsigned interface, int32_t addend);
	void (*step)(void *ctx, unsigned interface, int64_t delta_ns);
};

// a gptp record's trailer: the frame's ingress stamp, most significant octet first; all ones: no stamp
#define GPTP_MBX_TRAILER 8u
#define GPTP_MBX_NO_STAMP UINT64_MAX
// the AECP owner's change notice: ctrl_app_aecp_changed's events for an AVB_INTERFACE
#define GPTP_MBX_AVB_INFO 2u
#define GPTP_MBX_AS_PATH 4u

struct gptp_mbx_aecp {
	void *ctx;
	void (*changed)(void *ctx, unsigned interface, unsigned events);
};

struct gptp_mbx {
	struct gptp_port port[MBX_N_IF];
	struct gptp_mbx_phc phc;
	struct gptp_mbx_aecp aecp;
	struct gptp_pub snap[MBX_N_IF];                 // the state at the last GEN published
	bool snap_v[MBX_N_IF];
	uint8_t gen[MBX_N_IF];
	uint32_t published;                             // publications written, all interfaces
	uint32_t foreign_if;                            // records or events naming no interface
	uint32_t rx_stamped;                            // event messages received with their stamp
	uint32_t rx_unstamped;                          // event messages received with none (never expected)
	uint32_t rx_short;                              // records too short to hold a trailer
	uint32_t ts_foreign;                            // TIMESTAMP records that are no egress stamp
	uint32_t notices;                               // AECP change notices raised
};

// Initialise every port and bind the adapter to the loop; false when a table
// is full. cfg[i] is interface i's port (its clock identity, its MAC).
bool gptp_mbx_attach(struct gptp_mbx *g, struct ctrl_loop *l, const struct gptp_config cfg[MBX_N_IF],
		     const struct gptp_mbx_phc *phc);

// The publication's words of a port's state, in the contract's order (GPTP_GM_LO first), GEN as given.
void gptp_mbx_words(const struct gptp_pub *pub, uint8_t gen, uint32_t words[MBX_PUB_GPTP_WORDS]);

// The AECP owner's change notice; set once the owner is composed (before the loop's first pass).
void gptp_mbx_notify(struct gptp_mbx *g, const struct gptp_mbx_aecp *aecp);

// The snapshot interface i last published (its GEN's state), or NULL before the first publication.
const struct gptp_pub *gptp_mbx_snapshot(const struct gptp_mbx *g, unsigned interface);

// Which of GPTP_MBX_AVB_INFO and GPTP_MBX_AS_PATH moved from a to b.
unsigned gptp_mbx_changes(const struct gptp_pub *a, const struct gptp_pub *b);

// GET_AVB_INFO's and GET_AS_PATH's gPTP fields from interface i's snapshot (struct aecp_face_gptp's ports;
// ctx the struct gptp_mbx). The propagation delay is served unsigned, a negative measurement as 0, as the
// fabric plane's public bank serves it; the path is empty while there is no grandmaster, as the datapath's.
void gptp_mbx_avb(void *ctx, unsigned interface, uint64_t *gm, uint32_t *pdelay, uint8_t *domain, bool *as_capable);
bool gptp_mbx_path(void *ctx, unsigned interface, uint64_t *out, size_t capacity, size_t *count);

#ifdef __cplusplus
}
#endif

#endif
