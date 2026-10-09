// SPDX-License-Identifier: CERN-OHL-W-2.0
// Mailbox accesses per SRP pass, excluding CPU work and external port work.
#ifndef CTRL_SRP_BOUNDS_H
#define CTRL_SRP_BOUNDS_H
#include "ctrl_loop.h"

// A reset of an interface's participants publishes LICENCE (every licence
// closed), SR_DOMAIN (the default) and IDLE_SLOPE once each (the publication
// block, contract 2.2).
#define SRP_MBX_PUB_RESET 3u
// LINK reset snapshots RX_HEAD once, then publishes. Tick callbacks make no
// mailbox access.
#define SRP_MBX_EVENT_MAX (1u + SRP_MBX_PUB_RESET)
// Readiness reads IRQ_STATUS; a refused receive reads NOW_MS once.
#define SRP_MBX_RX_MAX 2u
#define SRP_MBX_RX_RECORD_MAX (2u + MBX_RX_HDR_WORDS + (MBX_CH_SRP_MAX_FRAME_BYTES + 3u) / 4u)
// Each interface reads LINK, may snapshot RX_HEAD, and may check IRQ_STATUS
// and NOW_MS for retained reception. The transmit loop calls mrp_transmit
// at most twice per interface; each call sends at most one bounded frame.
#define SRP_MBX_TX_MAX (2u + MBX_TX_HDR_WORDS + (MBX_CH_SRP_MAX_FRAME_BYTES + 3u) / 4u)
// Each interface may also publish: a reset's three writes, a Domain
// adoption's SR_DOMAIN and IDLE_SLOPE, and LICENCE before each licence change
// it reports, at most two per source (an owed stop, then the new level).
#define SRP_MBX_PUB_POLL_MAX (SRP_MBX_PUB_RESET + 2u + 2u * MBX_N_PUB_SOURCES)
#define SRP_MBX_POLL_MAX (MBX_N_IF * (4u + SRP_MBX_PUB_POLL_MAX + 2u * SRP_MBX_TX_MAX))
#define SRP_MBX_PASS_MAX (CTRL_LOOP_EVENTS_PER_PASS * (MBX_EV_WORDS + 2u + SRP_MBX_EVENT_MAX) + \
    CTRL_LOOP_RX_PER_PASS * (SRP_MBX_RX_RECORD_MAX + SRP_MBX_RX_MAX) + SRP_MBX_POLL_MAX)
#endif
