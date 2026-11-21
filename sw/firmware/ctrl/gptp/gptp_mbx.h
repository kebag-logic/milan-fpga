// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// gptp_mbx.h - the gPTP end station ports on the mailbox and the loop
// (contract 2.5; #884, #665 F6).
//
// One gptp_port per interface. The adapter binds the gptp channel's receive
// ring (each record to its interface's port), an event sink (TIMESTAMP to the
// port that timed it, LINK to the port's portEnabled), a centisecond consumer
// (the ports' timers, on NOW_MS) and a poll (each port's gPTP publication,
// written only when its words moved, GPTP_STATE last with GEN moved). Its HAL
// sends on the gptp channel's transmit ring and drives each interface's PHC
// through `phc`, the platform's (gptp_phc_csr.h on the split).
//
// THE BOUND (ctrl_loop.h THE SHARE): a record costs the port's rx; an event,
// its ts or link; a centisecond, its tick; a poll, at most MBX_PUB_GPTP_WORDS
// bus writes an interface that moved. None waits on the fabric.

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

struct gptp_mbx {
	struct gptp_port port[MBX_N_IF];
	struct gptp_mbx_phc phc;
	uint32_t words[MBX_N_IF][MBX_PUB_GPTP_WORDS];   // the last publication written
	uint8_t gen[MBX_N_IF];
	uint32_t published;                             // publications written, all interfaces
	uint32_t foreign_if;                            // records or events naming no interface
};

// Initialise every port and bind the adapter to the loop; false when a table
// is full. cfg[i] is interface i's port (its clock identity, its MAC).
bool gptp_mbx_attach(struct gptp_mbx *g, struct ctrl_loop *l, const struct gptp_config cfg[MBX_N_IF],
		     const struct gptp_mbx_phc *phc);

// The publication's words of a port's state, in the contract's order (GPTP_GM_LO first), GEN as given.
void gptp_mbx_words(const struct gptp_pub *pub, uint8_t gen, uint32_t words[MBX_PUB_GPTP_WORDS]);

#ifdef __cplusplus
}
#endif

#endif
