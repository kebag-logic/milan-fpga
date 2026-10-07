#!/usr/bin/env python3
"""Recompute the three-way pass bound, the F6 tie and the MAILBOX_SPLIT.md
T_svc paragraph figures from the macro terms at the reviewed head.

Terms (path:line at d8060d87): loop/ctrl_loop.h:78-79 (EVENTS_PER_PASS 8,
RX_PER_PASS 2); mbx/mbx_contract.h:349,355 (RX_HDR_WORDS 2, EV_WORDS 4),
:533,:657 (ACMP 128 B, MAAP 64 B); adp/adp_mbx.h:118-121; acmp/acmp_mbx.h:
132-144; maap/maap_mbx.h:15-19; app/ctrl_app.h:62-66; ACMP_MAX_SINKS 16.
Passes taken: MAILBOX_SPLIT.md table (2, 10, 21, 8). T_svc 10 ms, ceiling 20 ms.
"""
EVP, RXP, HDR, EVW = 8, 2, 2, 4
ADP_SINK, ADP_HANDLER, ADP_POLL = 31, 4, 31
ADP_REC = 2 + HDR + 128 // 4
ACMP_EVENT, ACMP_SINK_WORK, ACMP_DISC, ACMP_HANDLER, ACMP_POLL, SINKS = 4, 23, 7, 51, 25, 16
ACMP_REC = 2 + HDR + 128 // 4
MAAP_EVENT = MAAP_RX = MAAP_POLL = 48
MAAP_REC = 2 + HDR + 64 // 4
for n_if in (1, 2):
    acmp = (EVP * (EVW + 2 + ADP_SINK + ACMP_EVENT) + SINKS * ACMP_SINK_WORK
            + RXP * (ADP_REC + max(ADP_HANDLER, ACMP_DISC)) + RXP * (ACMP_REC + ACMP_HANDLER)
            + n_if * ADP_POLL + ACMP_POLL)
    maap = EVP * (6 + MAAP_EVENT) + RXP * (20 + MAAP_RX) + n_if * MAAP_POLL
    share = EVP * MAAP_EVENT + RXP * (MAAP_REC + MAAP_RX) + n_if * MAAP_POLL
    app = acmp + share
    tie = acmp + maap - EVP * (EVW + 2)
    print(f"N_IF={n_if}: ACMP_MBX_PASS_MAX={acmp} MAAP_MBX_PASS_MAX={maap} share={share} "
          f"CTRL_APP_PASS_MAX={app} tie={tie} {'EQUAL' if app == tie else 'DIFFER'}")
    for what, passes in (("event", 2), ("acmp ring", 10), ("adp ring", 21), ("owed", 8)):
        acc = (passes + 1) * app
        ms = acc / 1000
        fit = "fits T_svc" if ms <= 10 else ("under ceiling" if ms <= 20 else "exceeds ceiling")
        print(f"   {what:10s} ({passes}+1)*{app} = {acc} accesses = {ms:.2f} ms at 1 us: {fit}")
print("two-way owed bound without MAAP: 9*1012 =", 9 * 1012, "-> 9.108 ms fits T_svc")
