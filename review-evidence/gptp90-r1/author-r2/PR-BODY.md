[A688b]

## Summary

Three receipt rules of IEEE 802.1AS-2011, as corrected by Cor1 and Cor2 (the edition Milan v1.2 profiles), in the generated microcode. Round 2 answers R719-1 and R720-1.

- **#89, 10.3.11 and Figure 10-13 (Cor1).** A sync receipt timeout ages the elected grandmaster exactly as an announce receipt timeout does: `currentTime >= syncReceiptTimeoutTime && gmPresent`.
  - The 375 ms watch is 3 x 125 ms (10.6.3.1; Milan v1.2 Table 4.2).
  - It restarts on every usable Sync/Follow_Up pair and on the adoption of a new grandmaster, so a grandmaster that never sends usable Sync is aged too.
  - Not usable: a Sync without its Follow_Up, a Follow_Up after the next Sync, a Follow_Up naming another sequenceId, and a Follow_Up later than followUpReceiptTimeout.
- **The watch belongs to the port, not to its role (round 2, R719-1 F1 and F2).** Cor1 strikes the parent condition from Figure 10-4, so any Sync an asCapable port takes refreshes syncReceiptTimeoutTime, and nothing else moves it.
  - Every expiry marks the port aged, whatever role it finds. A master is only marked: it keeps its sync-ok (#84).
  - Mastership stops neither the Sync watch nor a pending Sync's 125 ms Follow_Up watch (11.2.13). So a late Follow_Up pairs with nothing in the master role either.
  - While the mark stands, an Announce whose grandmaster would make gmPresent TRUE is aged at once, and the plane stays (or becomes) grandmaster.
  - As grandmaster the plane still pairs the aged peer's Sync and Follow_Up, steering and publishing nothing. The first usable pair clears the mark, and the peer's next Announce elects it again, once. If Sync then lapses again, the next expiry marks the port again, so one recovered pair cannot reopen election repeatedly.
- **gmPresent exactly (round 2, R720-1 F1).** gmPresent is TRUE only while the grandmaster's priority1 is below 255 (10.2.3.13; 10.3.12.1.4 g). A slave of a priority1 255 grandmaster is never aged by Sync, and an aged port still elects such a grandmaster.
  - One compare asks both questions: the mark is a priority threshold, and a vector's {priority1, clockClass, clockAccuracy} compares below it exactly when its priority1 is below 255.
  - Published flags bit 0 keeps its existing meaning.
- **#90, 11.2.15.3 and Figure 11-8 RESET.** lostResponses increments while it is at most allowedLostResponses (3), and only otherwise is asCapable cleared. Four consecutive losses keep asCapable; the fifth clears it. Both loss shapes count: no response, and a response without its Follow_Up.
- **#91, Figure 11-8 WAITING_FOR_PDELAY_RESP_FOLLOW_UP.** A second Pdelay_Resp carrying the outstanding sequenceId takes the exchange to RESET, from either responder. Its Follow_Up pairs with nothing, a third response cannot re-arm it, and the interval counts as a lost response. Per Cor2, the next request still waits for the 1 s interval.

No RTL file changes. No top-level port, parameter or register-map change. The ROM holds 1,021 of 1,024 words (round 1: 1,018; main: 1,015); seeded regression images hold 1,022. All four tracked images are regenerated.

## Tests

The engine suite grows from 1,703 checks per shipping pass on main to 1,805; the seeded passes match. The priority1 255 pass grows from 53 to 57.

- **Phase 12** proves the takeover with the grandmaster still announcing, within 375 ms and one BMCA pass of the last usable pair.
- **Phase 39** covers a grandmaster adopted with no usable Sync, and each failure shape with Announce continuing: Sync stops, no Follow_Up, a Follow_Up after the next Sync, and the next sequenceId. Each is timed, held for 3 s of Announces without re-election, and recovered once.
- **Phase 40 (round 2)** covers what the reviewers probed:
  - one usable pair heard as master, then Sync lost again: the grandmaster's Announce 624 ms after that pair elects nothing, while one 124 ms after a lone pair re-elects it;
  - mastership won by an Announce lapse leaves the Sync watch running, so Sync stopping just before it ages the next Announce;
  - a Sync pending at the takeover keeps its Follow_Up watch: its Follow_Up 200 ms later pairs with nothing, and one 60 ms later is heard and lets the next Announce re-elect.
- **Phase 41 (round 2, priority1 255 pass):** the aged port refuses a priority1 1 Announce, elects a better priority1 255 peer and keeps it for 4 s without Sync, and then a priority1 1 Announce on that port makes this plane master at once.
- **Phase 21** now proves that a receipt timeout queued behind mastership still leaves the port aged.
- **Phase 25** covers no response, no Follow_Up, a duplicated response and three responses: one and four losses keep asCapable, the fifth clears it, and duplicated exchanges complete nothing.

The mutation arm grows from 72 controls on main to 98, all caught, each on the named checks it lists. Round 2 adds seven:

- only an expiry that ages a slave marks the port (the round-1 rule);
- mastership stops the Sync receipt watch;
- mastership stops the Follow_Up watch;
- mastership voids the pending Sync;
- sync receipt ageing ignores gmPresent;
- an aged port refuses a priority1 255 grandmaster;
- an aged Announce is dropped rather than aged.

The receipt-rule controls now live in `tb/verilator/engine/receipt_mutants.py`, which keeps the arm under the parent's module length limit.

## Gates

**This repository** at this head, every gate rc 0, each run on its own: `make contract`; the microCPU, parser (with its mutants), engine (with its mutation arm), gasket, tsngen and bench-tag suites; `make lint`, `make docs` and `make diagrams-check`; the out-of-context clock self-test (the synthesis flow itself needs a vendor tool not present here); and the full `make`.

**Reviewer probes, run unchanged at this head:**

- R719-1 re-ageing probe: no late Announce re-elects the aged grandmaster (0 of 3 rounds), and the control round still re-elects.
- R719-1 pending-Sync probe: the next Announce elects nothing.
- R720-1 priority1 255 probe: the plane stays the peer's slave for all 6 s.

**Parent consumer gates**, on a committed local milan-fpga snapshot of dev `97aab1d0` with this head as the gptp-processor gitlink and the companion change below: the full consumer list, including the milan_dp `gptp` and `gptp-lat` legs and both idiom gates, plus tsn_fuzz `ptp` with its pinned field-campaign generator. Every gate returns 0: both idiom gates, the builder, the RTL and port-contract checks, `milan_dp gptp` and `gptp-lat` (185/185 each), `milan_dp_gptp` (151 physical checks and every sub-arm with 0 failures), gm_steps, and tsn_fuzz `ptp` (677 pass, 0 fail, artifact current). At base the same list passes, tsn_fuzz `ptp` included.

## Parent companion change for the gitlink bump

The parent's suites encode the behaviour this change corrects:

- a peer elected on Announces alone stays selected past syncReceiptTimeout;
- asCapable falls at the fourth lost response;
- a drop-counter arm relies on a stale queue entry running a long handler.

A parent test and documentation change makes those suites pass at this head. It touches the milan_dp, gptp_plane and tsn_fuzz harnesses, and the parent documents that state the retired counts and the scenario length (now the patched run's own figure). It is attached to the lane handoff rather than committed here. Its milan_dp `gptp` and tsn_fuzz parts also pass on the current gitlink, so they can land first.

The tsn_fuzz campaign was not on the round-1 consumer list. At the round-1 head it already failed the same two Announce-only adoption checks, for the same #89 reason, so its edit belongs with this change.

Addresses #89, #90 and #91. Closing waits for the parent companion change, so this body does not use closing keywords.
