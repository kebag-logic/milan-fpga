[A688c]

## Summary

Three receipt rules of IEEE 802.1AS-2011, as corrected by Cor1 and Cor2 (the edition Milan v1.2 profiles), in the generated microcode. Round 3 answers R719-2 (option (a)) and applies the R719-2 and R720-2 residue.

- **#89, 10.3.11 and Figure 10-13 (Cor1).** A sync receipt timeout ages the elected grandmaster exactly as an announce receipt timeout does: `currentTime >= syncReceiptTimeoutTime && gmPresent`.
  - The 375 ms watch is 3 x 125 ms (10.6.3.1; Milan v1.2 Table 4.2).
  - It restarts on every usable Sync/Follow_Up pair and on the adoption of a new grandmaster, so a grandmaster that never sends usable Sync is aged too.
  - Not usable: a Sync without its Follow_Up, a Follow_Up after the next Sync, a Follow_Up naming another sequenceId, and a Follow_Up later than followUpReceiptTimeout.
- **The watch belongs to the port, not to its role.** Cor1 strikes the parent condition from Figure 10-4, so any Sync an asCapable port takes refreshes syncReceiptTimeoutTime, and nothing else moves it.
  - Every expiry marks the port aged, whatever role it finds. A master is only marked: it keeps its sync-ok (#84).
  - Mastership stops neither the Sync watch nor a pending Sync's 125 ms Follow_Up watch (11.2.13). So a late Follow_Up pairs with nothing in the master role either.
  - While the mark stands, an Announce whose grandmaster would make gmPresent TRUE is aged at once, and the plane stays (or becomes) grandmaster.
  - As grandmaster the plane still pairs the aged peer's Sync and Follow_Up, steering and publishing nothing. The first usable pair clears the mark, and the peer's next Announce elects it again, once. If Sync then lapses again, the next expiry marks the port again, so one recovered pair cannot reopen election repeatedly.
- **gmPresent exactly.** gmPresent is TRUE only while the grandmaster's priority1 is below 255 (10.2.3.13; 10.3.12.1.4 g). A slave of a priority1 255 grandmaster is never aged by Sync, and an aged port still elects such a grandmaster.
  - **Round 3 (R719-2 F1, option (a)):** that grandmaster's Sync has still stopped, so its sync receipt timeout clears sync-ok (flags bit 3, from which the parent derives tu) and commits, while the peer stays elected. This keeps main's rule for the case that ages nothing. A master keeps sync-ok (#84).
  - The mark is a priority threshold, `0xFF << 3`. A vector's priority1 and the top three bits of its clockClass compare below it exactly when its priority1 is below 255. Its lowest set bit is sync-ok's, so the same value is the flag mask.
  - The timeout leg stays at 11 words and has no branch for the new case. The presence bit times the mark is zero for a master and the mark for an elected peer. That one value is both the ageing threshold and, through the microCPU's existing `MASK` (and-not) operation, the sync-ok clear. The leg then ends in the Pdelay exchange leg's existing flags-publishing tail.
  - Published flags bit 0 keeps its existing meaning.
- **#90, 11.2.15.3 and Figure 11-8 RESET.** lostResponses increments while it is at most allowedLostResponses (3), and only otherwise is asCapable cleared. Four consecutive losses keep asCapable; the fifth clears it. Both loss shapes count: no response, and a response without its Follow_Up.
- **#91, Figure 11-8 WAITING_FOR_PDELAY_RESP_FOLLOW_UP.** A second Pdelay_Resp carrying the outstanding sequenceId takes the exchange to RESET, from either responder. Its Follow_Up pairs with nothing, a third response cannot re-arm it, and the interval counts as a lost response. Per Cor2, the next request still waits for the 1 s interval.

No RTL file changes. No top-level port, parameter or register-map change. The ROM holds 1,021 of 1,024 words (main: 1,015), and seeded regression images hold 1,022; round 3 adds no word and moves no leg. All four tracked images are regenerated.

## Tests

The engine suite grows from 1,703 checks per shipping pass on main to 1,805; the seeded passes match. The priority1 255 pass grows from 53 to 59.

- **Phase 12** proves the takeover with the grandmaster still announcing, within 375 ms and one BMCA pass of the last usable pair.
- **Phase 19:** the receipt timeout queued behind the takeover commits after it, naming thisClock with sync-ok. This is main's check, restored now that a master's expiry commits again.
- **Phase 21** proves that a receipt timeout queued behind mastership still leaves the port aged.
- **Phase 39** covers a grandmaster adopted with no usable Sync, and each failure shape with Announce continuing: Sync stops, no Follow_Up, a Follow_Up after the next Sync, and the next sequenceId. Each is timed, held for 3 s of Announces without re-election, and recovered once.
- **Phase 40** covers re-ageing after one pair heard as master, mastership won by an Announce lapse, and a Sync pending at the takeover.
- **Phase 41 (priority1 255 pass):** the aged port refuses a priority1 1 Announce, elects a better priority1 255 peer and keeps it for 4 s without Sync, and then a priority1 1 Announce on that port makes this plane master at once.
- **Phase 42 (round 3, priority1 255 pass):** a priority1 255 peer's usable Sync raises sync-ok. When its Sync stops while its Announces continue, sync-ok still stands 350 ms after the last pair and is clear 380 ms after it. The peer stays elected, and sync-ok stays clear for 1 s more.
- **Phase 25** covers no response, no Follow_Up, a duplicated response and three responses: one and four losses keep asCapable, the fifth clears it, and duplicated exchanges complete nothing.

The mutation arm grows from 72 controls on main to 100, all caught, each on the named checks it lists. Round 3 adds two:

- a sync receipt timeout that ages nothing keeps sync-ok;
- a consumed pair leaves sync-ok down.

Round 3 also re-plants the controls the new leg moved, each on the same named checks. One control is replaced. "A queued receipt timeout ages a master" sent the expiry straight to BECOME. Now that the master's expiry commits, a second BECOME publishes the same record, so that mutant is equivalent. It is replaced by "an expiry takes a master's own vector for a peer's", which is caught on the restored phase-19 check.

## Gates

**This repository**, at this head and at base, every gate rc 0, each run on its own:
- `make contract`;
- the microCPU, parser (with its mutants), engine (with its mutation arm), gasket, tsngen and bench-tag suites;
- `make lint`, `make docs` and `make diagrams-check`;
- the out-of-context clock self-test (the synthesis flow itself needs a vendor tool not present here);
- the full `make`.

All four tracked images regenerate byte-identically with each consumer's own arguments.

**Reviewer probe, run unchanged at this head:** R719-2's priority1 255 sync-ok probe. From 1 s to 4 s after Sync stops, `syncok=0` with the priority1 255 peer still elected (`gm=0000000000000105`). At round 2 it read `syncok=1` throughout, and on main `syncok=0`.

**Parent consumer gates**, on a committed local milan-fpga snapshot of dev `97aab1d0` with this head as the gptp-processor gitlink and the companion change below: the full consumer list, plus tsn_fuzz `ptp` with its pinned field-campaign generator. Every gate returns 0:
- both idiom gates, the builder, and the RTL and port-contract checks;
- `milan_dp gptp` and `gptp-lat` (185/185 each);
- `milan_dp_gptp` (151 physical checks and every sub-arm with 0 failures; the scenario figure is unchanged);
- gm_steps;
- tsn_fuzz `ptp` (677 pass, 0 fail, artifact current).

The parent's `gptp_plane` suite, which the companion change also edits, passes as well. At base the same list passes.

## Parent companion change for the gitlink bump

The parent's suites encode the behaviour this change corrects:

- a peer elected on Announces alone stays selected past syncReceiptTimeout;
- asCapable falls at the fourth lost response;
- a drop-counter arm relies on a stale queue entry running a long handler.

A parent test and documentation change makes those suites pass at this head. It touches the milan_dp, gptp_plane and tsn_fuzz harnesses, and the parent documents that state the retired counts and the scenario length. It is attached to the lane handoff rather than committed here. It is unchanged from round 2. Its milan_dp `gptp` and tsn_fuzz parts also pass on the current gitlink, so they can land first.

Addresses #89, #90 and #91. Closing waits for the parent companion change, so this body does not use closing keywords.
