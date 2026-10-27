[A688]

## Summary

Three receipt rules of IEEE 802.1AS-2011, as corrected by Cor1 and Cor2 (the edition Milan v1.2 profiles), in the generated microcode.

- **#89, 10.3.11 and Figure 10-13 (Cor1).** A sync receipt timeout now ages the elected grandmaster, exactly as an announce receipt timeout does: `currentTime >= syncReceiptTimeoutTime && gmPresent`.
  - The 375 ms watch is 3 x 125 ms (10.6.3.1; Milan v1.2 Table 4.2).
  - It restarts on every usable Sync/Follow_Up pair and on the adoption of a new grandmaster. So a grandmaster that never sends usable Sync is aged too.
  - Not usable: a Sync without its Follow_Up, a Follow_Up after the next Sync, and a Follow_Up naming another sequenceId.
- **#89, no oscillation and automatic recovery.** Cor1 strikes the parent condition from Figure 10-4, so any Sync an asCapable port takes refreshes the port's sync receipt time, whatever its role.
  - An aged port keeps a mark; while it stands, the peer's Announces are aged at once and the plane stays grandmaster.
  - As grandmaster it still pairs that peer's Sync and Follow_Up, steering and publishing nothing.
  - The first usable pair clears the mark, and the peer's next Announce elects it again, once.
- **#90, 11.2.15.3 and Figure 11-8 RESET.** lostResponses increments while it is at most allowedLostResponses (3), and only otherwise is asCapable cleared. Four consecutive losses keep asCapable; the fifth clears it. Both loss shapes count: no response, and a response without its Follow_Up.
- **#91, Figure 11-8 WAITING_FOR_PDELAY_RESP_FOLLOW_UP.** A second Pdelay_Resp carrying the outstanding sequenceId takes the exchange to RESET, from either responder.
  - Its Follow_Up pairs with nothing, and a third response cannot re-arm it.
  - The interval counts as a lost response. Per Cor2, the next request still waits for the 1 s interval.

No RTL file changes. No top-level port, parameter or register-map change. The ROM holds 1,018 of 1,024 words, six free (1,015 before). All four tracked images are regenerated.

## Tests

The engine suite grows from 1,703 to 1,799 checks per shipping pass; the seeded passes match and the priority1 255 pass is unchanged.

- **Phase 12** now proves the takeover. With the grandmaster still announcing, the plane becomes grandmaster within 375 ms and one BMCA pass of the last usable pair, naming thisClock with sync-ok.
- **A new end-of-run phase** covers:
  - a grandmaster adopted with no usable Sync;
  - each failure shape with Announce continuing: Sync stops, no Follow_Up, a Follow_Up after the next Sync, and the next sequenceId. Each is timed against the watch, held for 3 s of Announces without re-election, and recovered once;
  - Sync every 250 ms keeping the plane deferring;
  - a Follow_Up 60 ms after its Sync being used.
- **Phase 25** covers no response, no Follow_Up, a duplicated response and three responses. In each, one loss and four losses keep asCapable and the fifth clears it. Duplicated exchanges complete nothing.
- **Adapted phases.** Phases that encoded the old flag-only timeout now re-elect the grandmaster after hearing its Sync. Their #68, #75 and #84 properties are unchanged.

The mutation arm grows from 72 to 91 controls, all caught. Every one of the 106 new or changed checks is failed by at least one planted mutant. The named controls include:

- the receipt timeout leg as main shipped it;
- adoption without the watch;
- an aged port taking Announces;
- a master steering on, or not hearing, its aged peer's Sync;
- watches of the wrong length;
- a refresh expiring the watch;
- loss limits at the first, fourth and sixth loss;
- the old re-arm, and a reset that a third response undoes.

## Gates

**This repository**, at base and at head, every gate rc 0, each run on its own:

- `make contract`;
- the microCPU, parser (with its mutants), engine, gasket, tsngen and bench-tag suites;
- `make lint`, `make docs` and `make diagrams-check`;
- the out-of-context clock self-test (the synthesis flow itself needs a vendor tool not present here);
- the full `make`.

At head, the engine suite passes 1,799 checks in the shipping pass and in each seeded pass, and its mutation arm passes 92 of 92.

**Parent consumer gates**, on a scratch milan-fpga at dev `97aab1d0` with this head as the gptp-processor gitlink:

- At head, 12 of the 15 listed gates pass, gm_steps included.
- The milan_dp `gptp` and `gptp-lat` legs and `milan_dp_gptp` fail only on parent expectations of the behavior this change corrects.
- At base, all 15 pass.
- With the companion parent test change below, those three legs pass at this head, as does the plane suite with its mutation campaign.

## Parent companion change for the gitlink bump

The parent's datapath and plane suites encode the behavior this change corrects:

- A peer elected on Announces alone stays selected past syncReceiptTimeout.
- asCapable falls at the fourth lost response.
- A drop-counter arm relies on a stale queue entry running a long handler.

A five-file parent test change makes those suites pass at this head. It has been verified, and is attached to the lane handoff rather than committed here. The milan_dp `gptp` leg also passes with it on the current gitlink, so that part can land first.

Addresses #89, #90 and #91. Closing waits for the parent companion change, so this body does not use closing keywords.
