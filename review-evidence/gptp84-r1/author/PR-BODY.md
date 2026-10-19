[A655]

Closes #84
Closes #85

## Status

Two commits on `84-85-tu-pathtrace` from main `43acfbcc`. Every repository
gate passes at base and head. The full parent consumer list passes 11/11 with
a seven-line parent companion for the gPTP shadow suite. That suite asserted
the received-only path, which #85 corrects. The companion rides the next
gptp-processor pin adoption in milan-fpga (see "Parent companion").

## Description

### #84: the grandmaster role counts as synchronised

A grandmaster's own time is the domain's time (IEEE 1722-2016 4.4.4.7: tu
marks a discontinuity, not the role; Milan v1.2 4.3.5.2).

- `prog_become` now sets sync-ok (flags bit 3) together with the master bit,
  so the parent's tu is 0 during mastership.
- The becoming-grandmaster commit still changes the published grandmaster
  identity, which arms the parent's 0.25 s holdover (Milan v1.2 Annex B.1.1).
  The parent is untouched, so that holdover stays.
- A Sync receipt timeout no longer clears a master's sync-ok. BECOME disarms
  the watch, but a timer expiry already queued behind BECOME's event cannot be
  recalled, so the receipt-timeout leg keeps bit 3 exactly where bit 1 stands.
- Handing mastership to a peer still clears sync-ok, in the same commit that
  names the new grandmaster.
- Unchanged: before mastership (no asCapable port yet) the self publication of
  #82 keeps its reset flags, so tu stays 1 there.

### #85: the published path is the received pathSequence plus thisClock

IEEE 802.1AS-2020 10.3.13.2.4 f) 5) and 10.3.9.23: a slave port copies the
received pathSequence and appends thisClock unless it is empty.

- The engine's path-staging write (region 3, word 7) now publishes count + 1
  with thisClock after the received entries. A directly attached grandmaster
  publishes [GM, thisClock].
- An absent PathTrace still publishes count 0.
- Eight or more received entries still publish their first eight: the
  publication carries eight entries, and widening it would be a port change.
- No port or parameter changes. The meaning of `pub_path_count_o` and
  `pub_path_o` changes as #85 requires: the count now includes thisClock.

## How to reproduce

```sh
make contract lint docs
make -C tb/verilator/ucpu
make -C tb/verilator/parser
make -C tb/verilator/engine        # four passes, then the mutation arm
make -C tb/verilator/gaskets
make -C tb/tsngen
make -C bench/arty test
```

## How to validate

- Engine suite at head: 1703/1703 on each of the three shipping passes and
  53/53 on the priority1 255 pass (base: 1642 and 46).
- Engine mutation arm at head: 72 of 72 planted defects caught, each failing
  every check it names (base: 58 of 58).
- New #84 cases: the first mastership, a takeover from a degraded parent while
  a Sync receipt timeout is queued behind it, every master cycle of the run,
  and every handover to a peer. Seven planted defects.
- New #85 cases: a direct grandmaster, a four-bridge grandmaster, seven and
  eight received entries, an absent PathTrace, and every committed peer path
  of the run. Nine planted defects, plus the existing path and transition
  checks of #82 updated to expect thisClock last.

## Parent companion

`parent-adoption-gptp_shadow-85.patch` updates four expectations in milan-fpga
`tb/verilator/gptp_shadow/sim_main.cpp`. Each follows IEEE 802.1AS-2020
10.3.9.23 / 10.3.13.2.4 f) 5), where the received pathSequence plus thisClock
is the path:

| Line | Expectation | Was | Now |
|---|---|---:|---:|
| 891 | published full path count | 3 | 4 |
| 930 | explicit one-entry PathTrace count, and a new check that its tail is thisClock | 1 | 2 |
| 943 | present path restored for servo controls | 3 | 4 |
| 1003 | better Announce preserves full path count | 3 | 4 |

The new tail check fails under two planted defects with the companion applied:
thisClock not appended, and the announcing source appended in its place.

## Parent consumer gates

The full consumer list ran on committed local parent snapshots at milan-fpga
dev `e9cbb676`. The gptp-processor gitlink was set to this base, to this head,
and to this head with the companion committed.

| Gate | Base | Head | Head + companion |
|---|---|---|---|
| C++ and Python idiom ratchets | pass | pass | pass |
| HDL analysis gate, RTL source lists | pass | pass | pass |
| End-station builder (all 103 gates, two legs) | pass | pass | pass |
| gPTP shadow suite and its mutation arm | pass, 309/309 | **fail, 305/309** | pass, 310/310 |
| Port contracts, naming, test evidence, docs, RTL lint | pass | pass | pass |

Without the companion, the four shadow checks above fail at this head. The #84
commit alone passes that suite 309/309.

## Definition of done

- [x] tu is 0 while this instance is grandmaster (#84)
- [x] The Annex B.1.1 holdover on a grandmaster change stays (#84)
- [x] Simulation cases and planted mutants for #84
- [x] Published path is the received pathSequence plus thisClock (#85)
- [x] Consistent with the grandmaster at every transition #82 grades (#85)
- [x] Simulation cases for a direct and a multi-hop grandmaster, with mutants (#85)
- [x] Repository gates pass at base and head
- [x] Full parent consumer list passes 11/11 at this head with the parent
      companion (rides the next pin adoption)
- [x] No port or parameter change seen by the parent
