[A655]

Closes #84
Closes #85

## Status

Five commits on `84-85-tu-pathtrace` from main `43acfbcc`. Head:
`2022d363fc622f6bbf4c312239fc3db741b4d29a`.

- Every repository gate passes at base and at head.
- The full parent consumer list passes 11/11 on a committed parent snapshot
  with four parent companion patches. So do milan_dp's `gptp` and
  `gptp-lat` legs and the other parent suites that run this engine.
- The companions ride the next gptp-processor pin adoption in milan-fpga
  (see "Parent companions").

## Description

### #84: the grandmaster role counts as synchronised

A grandmaster's own time is the domain's time. IEEE 1722-2016 4.4.4.7 makes
tu mark a discontinuity, not the role (see also Milan v1.2 4.3.5.2).

- `prog_become` now sets sync-ok (flags bit 3) together with the master bit,
  so the parent's tu is 0 during mastership.
- The Milan v1.2 Annex B.1.1 holdover stays. The parent arms it on a
  grandmaster change. Mastership arms it only when its commit replaces a peer
  grandmaster with thisClock.
- When the publication already names thisClock (from reset, or after a self
  publication), the mastership commit changes no grandmaster and arms no
  holdover. tu then falls at that commit unless an earlier holdover is still
  running.
- A Sync receipt timeout no longer clears a master's sync-ok. BECOME disarms
  the watch, but a timer expiry already queued behind BECOME's event cannot
  be recalled, so the receipt-timeout leg keeps bit 3 exactly where bit 1
  stands.
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

## Round 2 (review findings)

- **ROM budget** (R662-1-F01, R661-1-F2): the manager guide now states 1,015
  of 1,024 words (99.1%) with nine free, which is what the generator prints
  for all four images. A stale "88 percent full" comment now points to the
  guide instead of carrying a number.
- **Holdover wording** (R661-1-F3): the generator, the engine suite's
  phase-37 header and this description now say exactly when the Annex B.1.1
  holdover arms (above). The phase-37 header also moved above phase 38's
  (R661-1-R1).
- **Clause note** (R661-1-F4): the SlavePort pathTrace copy, with thisClock
  appended, is the published path that the parent serves to GET_AS_PATH
  (IEEE 1722.1-2021 7.4.41). Only the Announce transmit side has no reader on
  a single-port end station.
- **Parent companions** (R661-1-F1): the whole parent was searched for the old
  path shape, and every parent suite that runs this engine was run. The
  companion set grew from one patch to four (below).
- The RTL and all four ROM images are unchanged in Round 2; the four
  regenerated images are byte-identical to the committed ones.

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

## Parent companions

Four patches for milan-fpga dev `e9cbb676`. They apply cleanly in this order,
and every row cites its clause in the patch header.

| Patch | For | What it updates |
|---|---|---|
| `parent-adoption-gptp_shadow-85.patch` | #85 | `tb/verilator/gptp_shadow/sim_main.cpp:891, 930, 943, 1003`: path counts + 1, and the one-entry path ends with thisClock |
| `parent-adoption-milan_dp-85.patch` | #85 | `tb/verilator/milan_dp/sim_gptp.cpp:984, 1044, 1046, 1048, 1399, 1403, 1414, 1416, 1450` (count + 1; GET_AS_PATH length and cdl + 8 bytes) with two new thisClock-tail checks; `tb/verilator/milan_dp/sim_ax1x1gptp.cpp:938, 980, 982-984` (physical-rate leg) with one |
| `parent-adoption-milan_dp-82.patch` | #82 | boot and reset publication: the grandmaster reads thisClock, and its first publication arms the holdover (`sim_gptp.cpp:817-835`, `sim_ax1x1gptp.cpp:1149, 1197`) |
| `parent-adoption-milan_dp_gptp-84.patch` | #84 | physical-rate leg's loss and recovery arms (`sim_ax1x1gptp.cpp:344, 948, 1015, 1018, 1055`) |

#85 rows cite IEEE 802.1AS-2020 10.3.9.23 / 10.3.13.2.4 f) 5); #82 rows cite
10.3.13.2.4 b) and i) and Milan v1.2 Annex B.1.1; #84 rows cite IEEE
1722-2016 4.4.4.7 and Milan v1.2 4.3.5.2 and Annex B.1.1.

**For the owner's decision:**

- **The #82 patch.** The five expectations it changes already fail at this
  PR's base. They assert the boot state from before #82 (grandmaster 0).
- **The #84 patch changes harness logic, not only numbers.** After the peer is
  lost the station is grandmaster and synchronised:
  - CLKV "healthy" no longer implies the peer is elected, so the recovery wait
    now also requires the peer's grandmaster;
  - the loss window is split into three: tu 1 until the grandmaster change,
    the holdover, then tu 0;
  - new checks grade the 0.25 s holdover and the grandmaster identity.

Every new parent check fails under a planted defect:

| Planted defect | Checks it fails |
|---|---|
| thisClock not appended | path counts and lengths |
| the announcing source appended instead | thisClock-tail checks |
| the reset grandmaster is 0 | the #82 rows |
| the holdover is never armed | the holdover checks |
| becoming grandmaster clears sync-ok | the #84 role checks |
| the self publication keeps the departed grandmaster | "loss leaves this station grandmaster" |

## Parent consumer gates

The full consumer list ran on committed local parent snapshots at milan-fpga
dev `e9cbb676`, plus every parent suite that runs this engine.

| Gate | Base | Head, no companion | Head + four companions |
|---|---|---|---|
| C++ and Python idiom ratchets | pass | pass | pass |
| HDL analysis gate, RTL source lists | pass | pass | pass |
| End-station builder (all 103 gates, two legs) | pass | pass | pass |
| gPTP shadow suite and its mutation arm | pass, 309/309 | **fail, 305/309** | pass, 310/310 |
| Port contracts, naming, test evidence, docs, RTL lint | pass | pass | pass |
| milan_dp `gptp` and `gptp-lat` legs | **fail, 179/182** | **fail, 171/182** | pass, 185/185 each |
| Physical-rate gPTP suite (`milan_dp_gptp`) | **fail, 141/143** | **fail, 129/143** | pass, 155/155 and all four verifiers |
| Grandmaster-step suite (`milan_dp_gm_steps`) | not run | not run | pass, 190/190 and 6/6 controls |
| `gptp_plane`, `gptp_tables`, `gptp_txts` | not run | pass (one run; these suites compile none of the companion files) | same run |

The base failures are the #82 rows. `tsn_fuzz` also builds this engine, but
its field campaigns need an external traffic generator that is not present,
so they were skipped and not counted. Physical calibration and hardware
acceptance were not run.

## Definition of done

- [x] tu is 0 while this instance is grandmaster (#84)
- [x] The Annex B.1.1 holdover on a grandmaster change stays (#84)
- [x] Simulation cases and planted mutants for #84
- [x] Published path is the received pathSequence plus thisClock (#85)
- [x] Consistent with the grandmaster at every transition #82 grades (#85)
- [x] Simulation cases for a direct and a multi-hop grandmaster, with mutants (#85)
- [x] Repository gates pass at base and head
- [x] Full parent consumer list passes 11/11 at this head with the parent
      companions (they ride the next pin adoption)
- [x] milan_dp's gptp section and the other parent suites that run this
      engine pass with the companions
- [x] No port or parameter change seen by the parent
