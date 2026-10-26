// SPDX-License-Identifier: CERN-OHL-W-2.0
// The AECP owner's platform face on contract 2.3 (#665): what the processor
// wrapper's AECP faces carried in the fabric placement, in the mailbox's face
// block.
//   changed   writes each setting the core changed (class F) into the block of
//             every interface it concerns and commits it, waiting at most
//             MBX_FACE_ACK_CYCLES for the datapath's acknowledgement, before
//             the port returns
//   applied   false while a commit waits for its acknowledgement or an
//             interface owes a publication; while a change waits, whether
//             its commits are taken. Acknowledged state is the only state a
//             controller sees: false after a change, the command waits, the
//             change undone, behind IN_PROGRESS, so every response, read and
//             notification reports the values in force; true within
//             AECP_WAIT_MS, it is done again and answered SUCCESS, then
//             notified, else it fails, changing nothing. While a change waits
//             nothing is written: each interface it reaches is owed. While
//             false, the core takes no change, until the acknowledgement
//             returns and the interface is published again (aecp_face_poll)
//             (docs/ARCHITECTURE_HW_SW_SPLIT.md section 1; Milan v1.2 5.4.5.2;
//             IEEE 1722.1-2021 7.5.2, 9.3.2.6)
//   counters  GET_COUNTERS' 32 quadlets and counters_valid through the CTR window
//   stream    GET_STREAM_INFO's words through the GSI window (kind 0), and an
//             output's streaming level from the SRP owner's LICENCE
//   avb       GET_AVB_INFO's words through the GSI window (kind 1)
//   format    SET_STREAM_FORMAT's verdict through the GSI window (kind 0, selector 15)
// Every window read is bounded (mbx_win_read); a read that finds no answer
// fails its port. random and path are the platform's, forwarded.
#ifndef CTRL_AECP_FACE_H
#define CTRL_AECP_FACE_H
#include "aecp.h"
#include "mbx.h"

#ifdef __cplusplus
extern "C" {
#endif

struct aecp_face {
	struct aecp_ports ports;                // the environment ports this face answers
	const struct aecp_ports *platform;      // random and path
	struct aecp *core;                      // the values the settings carry
	bool owed[MBX_N_IF];                    // a commit the datapath has not taken: publish again
	bool ready;                             // F_CTRL.READY
	bool dirty;                             // F_AECP.DYN_DIRTY
	uint32_t restore;                       // F_RESTORE, as the saved-state store last reported it
	uint32_t nvm;                           // F_NVM
	uint32_t commits;                       // commits the datapath acknowledged
	uint32_t late;                          // commits it did not acknowledge within the bound
	uint32_t unanswered;                    // window reads with no answer within the bound
};

// Does not touch the mailbox. platform supplies random and path.
void aecp_face_init(struct aecp_face *, const struct aecp_ports *platform);
// The core whose settings the face publishes, once composed (before open).
void aecp_face_attach(struct aecp_face *, struct aecp *core);
// The saved-state store's restore and status words (F_RESTORE, F_NVM) and
// whether a persisted setting is not saved yet (F_AECP.DYN_DIRTY). Published
// at once once the face is open, else by aecp_face_open.
void aecp_face_status(struct aecp_face *, uint32_t restore, uint32_t nvm, bool dirty);
// Publish every setting with F_CTRL.READY set, on every interface: after the
// saved state is applied, before AECP opens (Milan v1.2 5.6.1). True once every
// interface acknowledged it; false leaves the others owed, and AECP stays
// closed until a later call or poll publishes them.
bool aecp_face_open(struct aecp_face *);
// Publish again, whole, each owed interface whose block is free; true while
// one is still owed.
bool aecp_face_poll(struct aecp_face *);

#ifdef __cplusplus
}
#endif
#endif
