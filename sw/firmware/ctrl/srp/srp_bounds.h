// SPDX-License-Identifier: CERN-OHL-W-2.0
// Mailbox accesses per SRP pass, excluding CPU work and external port work.
#ifndef CTRL_SRP_BOUNDS_H
#define CTRL_SRP_BOUNDS_H
#include "ctrl_loop.h"

// A reset of an interface's participants publishes LICENCE (every licence
// closed) and TALKER_DECL (every declaration withdrawn) before it destroys
// them. The next pass's poll builds new ones, publishing SR_DOMAIN (the
// default), IDLE_SLOPE and TALKER_DECL as it declares again, once each (the
// publication block, contract 2.2). Destroying and building in one pass took
// 110,000 cycles of the 200,000 share at 8x8/2if on the split CPU, and a pass
// of link changes would have built once per record (#665, the share in
// ctrl_loop.h): any number of resets of a pass builds once, and SRP's receive
// waits until it has, so no record meets an interface with no participants.
// A poll builds one interface at most: both links changing together built
// both in one pass of 2.08 ms. The other is built on the next pass, first,
// and the interface whose build waited goes first after that, so an
// interface whose build keeps failing delays the other's by one pass at most.
// The poll reads whether the interface with the turn builds before it visits
// any interface, so the rule holds whichever index has the turn.
#define SRP_MBX_PUB_WITHDRAW 2u
#define SRP_MBX_PUB_REOPEN 3u
#define SRP_MBX_PUB_RESET (SRP_MBX_PUB_WITHDRAW + SRP_MBX_PUB_REOPEN)
// LINK reset snapshots RX_HEAD once, then publishes its withdrawal. Tick
// callbacks make no mailbox access.
#define SRP_MBX_EVENT_MAX (1u + SRP_MBX_PUB_WITHDRAW)
// Readiness reads nothing past the head the ring's mark read; a refused receive
// reads NOW_MS once.
#define SRP_MBX_RX_MAX 1u
#define SRP_MBX_RX_RECORD_MAX (2u + MBX_RX_HDR_WORDS + (MBX_CH_SRP_MAX_FRAME_BYTES + 3u) / 4u)
// Each interface reads LINK, may snapshot RX_HEAD, and may read NOW_MS for
// retained reception. A poll sends at most SRP_MBX_POLL_FRAMES bounded frames,
// the frame a build left owed. THE TRANSMIT's call has a pass given whole
// (ctrl_loop.h), with no poll beside it: SRP_MBX_TRANSMIT_FRAMES, both of an
// interface's MRPDUs, and the next such pass the next interface's, so a pass
// never carries every participant's (#665, the share in ctrl_loop.h; lwSRP's
// periodic transmission built all four at two interfaces in one pass of 8.7 ms
// on the split core).
#define SRP_MBX_POLL_FRAMES 1u
#define SRP_MBX_TRANSMIT_FRAMES 2u
#define SRP_MBX_TX_MAX (2u + MBX_TX_HDR_WORDS + (MBX_CH_SRP_MAX_FRAME_BYTES + 3u) / 4u)
// Each interface may also publish: a reset's five writes (a poll that sees
// the link change itself withdraws; a later poll builds), a Domain adoption's
// SR_DOMAIN, IDLE_SLOPE and TALKER_DECL, and LICENCE before each licence
// change it reports, at most two per source (an owed stop, then the new
// level). A re-creation that is refused and retried writes less than the
// reset's term, and that poll reports no licence change on the interface (its
// VLAN is not yet sent again), so the term funds it.
#define SRP_MBX_PUB_POLL_MAX (SRP_MBX_PUB_RESET + 3u + 2u * MBX_N_PUB_SOURCES)
#define SRP_MBX_POLL_MAX (MBX_N_IF * (4u + SRP_MBX_PUB_POLL_MAX) + SRP_MBX_POLL_FRAMES * SRP_MBX_TX_MAX)
// The loop's own reads of SRP's ring a pass: the mark it reads as it takes its
// events (rx_order), and the head a pass given whole reads for its row.
#define SRP_MBX_LOOP_READS 2u
#define SRP_MBX_PASS_MAX (SRP_MBX_LOOP_READS + CTRL_LOOP_EVENTS_PER_PASS * (MBX_EV_WORDS + 2u + SRP_MBX_EVENT_MAX) + \
    CTRL_LOOP_RX_PER_PASS * (SRP_MBX_RX_RECORD_MAX + SRP_MBX_RX_MAX) + SRP_MBX_POLL_MAX)
#endif
