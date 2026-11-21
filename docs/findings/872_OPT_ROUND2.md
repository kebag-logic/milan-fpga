# Execution for 64x64 streams on two interfaces: round 2, three exact cuts measured (#872)

Status: **three exact-equivalent firmware cuts and two measurement groups**, for the owner's and the manager's rules
(#872). No product default, bound, gate rule or mailbox contract changed. Measured at `opt-exec-1`, which is
`origin/dev-soft-core-optimisation` `15168e14` with round 1's record ([872_OPT_ROUND1.md](872_OPT_ROUND1.md)) and
these commits; tsn-c-stack moves to `1c99aed` on its own `opt-exec-1`. Every figure names its receipt in the round
packet (the packet's `INDEX.md` lists them).

## Contents

- **[1. The harness groups no arm runs](#1-the-harness-groups-no-arm-runs)** -- an owed MRPDU and a retained receive, measured, and what each finds.
- **[2. The cuts](#2-the-cuts)** -- what each removes, and how each is shown to be an exact equivalent.
- **[3. The re-measure](#3-the-re-measure)** -- the differential against this head's base, and the loads.
- **[4. Designed, not built](#4-designed-not-built)** -- the sliced build, the memory bounds, and the next exact cuts.
- **[5. The Arty at this head](#5-the-arty-at-this-head)** -- round 1's finding F1, answered.
- **[6. Limits of round 2](#6-limits-of-round-2)**

## 1. The harness groups no arm runs

`scenario.named_groups` holds groups that `run.py --groups` reaches and no arm runs, measurements whose grading is not
ruled yet ([the harness README](../../tb/verilator/ctrl_service_budget/README.md#run-and-reproduce)).

**`srp-owed`, an owed MRPDU.** The load gate states `item.mrpdu` at a build of one's because no group staged it
([load_grade.py](../../tb/verilator/ctrl_service_budget/load_grade.py)). The group holds the egress from before the
links come up and sends a LeaveAll on both participants every JoinTime, so the SRP ring runs out of room and a build's
send is refused; lwSRP keeps its prepared PDU, and once the egress returns the poll resends it. The resend, the
poll's `mrpdu` item, is 11,531 / 9,118 / 9,487 CPU cycles at 1x1/1if, 8x8/1if and 8x8/2if, against statements of 735
/ 1,475 / 1,215 us. A refused resend while the ring is full costs 1,162 to 2,105 cycles a poll. The hold makes the MRP
timers' run-outs during it late by construction, so the group stays out of the arm until a ruling says how they are
graded.

**`srp-retained`, a retained receive retried.** The receive filter takes every SR class A Domain whose VID is in range
([srp_mbx.c](../../sw/firmware/ctrl/srp/srp_mbx.c) `interested_msrp`), and each Domain value is an attribute of its
own. A bridge's Domain declarations, one VID after another, take SRP's pool, and the poll retries the refused receive
once a centisecond (121, 121 and 132 retries). That legal flood exceeds four statements or more: at 1x1/1if the
retained item 31,827 cycles (stated 28,500), the record's apply 31,121 (28,500), the walk 6,229 (3,500) and the reclaim
6,110 (2,500); at 8x8/1if the retained item 92,416 (37,500), the apply 92,078 (37,500), the walk 27,669 (12,000), the
reclaim 16,533 (4,000), a build of one 167,456 (147,500), and one work pass of 224,926 cycles, over the 2.0 ms share;
at 8x8/2if the retained item 191,857 (36,500), the apply 193,255 (36,500), the walk 52,678 (6,000), the reclaim 30,872
(3,500), a build of one 296,082 (121,500), and 178 of 1,134 work passes over the share, the longest 387,823 cycles.
The costs grow with the Domain attributes registered, which only the pool bounds.

## 2. The cuts

| Cut | What it removes | Exact because | Shown by |
|---|---|---|---|
| The MAAP DA gate's mask ([maap_mbx.c](../../sw/firmware/ctrl/maap/maap_mbx.c) `declaring`) | a scan of every source in each interface's poll | `refresh_demand`, which asks every source anyway, files each answer under its source's interface (fixed at `acmp_init`); the mask by the count is the set the scan tested | `MaapHost.DeclaringMatchesTheSourceScan` against the scan after every pass of random sequences at one and two interfaces; three planted defects and two retargeted, caught |
| `acmp_declaring`'s state (tsn-c-stack `1c99aed`) | a 40-byte `memset` a source a poll | it reads only `dest_mac_valid`, which it now clears before the source port fills the state | `AcmpFresh.UnfilledDestinationReadsInvalid`; tsn-c-stack's own suite, 478 of 478 planted defects caught |
| The licence scan ([srp_mbx.c](../../sw/firmware/ctrl/srp/srp_mbx.c) `poll`) | the scan of every source of every interface, every pass | it is a fixed point once run, and each writer of what it reads marks its interface stale | every SRP arm, built with `CTRL_SRP_LICENCE_CHECK`, checks each skip against what the scan would have done (about 2 million skips, none wrong); two planted defects caught |

At 32x32/2if, round 1's profile put MAAP's demand chain at about 43 % of the service cycles; at 8x8/1if in
valid-destinations' `srp-talker-loss` it was about 31 %, of which the two MAAP cuts remove `memset` (6.5 %) and
`declaring` (1.7 %). The polls' base, a pass's own cost, is no load term (`load_grade.py`), so these cuts shorten the
passes and the rows more than they move the load.

## 3. The re-measure

**The differential.** Each graded group of the cut image is compared with the same group on this head's base, times
aside: every frame on the wire per channel and interface, every publication word's writes, the transmit commits, the
result, the refusals and each probe's status. At 1x1/1if and 8x8/1if the base is the flip train's re-measure, whose
images and scripts are byte-identical to this head's and whose logs a run here reproduced byte for byte.

| Point | Compared | Same | Different |
|---|---:|---:|---:|
| 1x1/1if | 37 | 37 | 0 |
| 8x8/1if | 8 | 8 | 0 |
| 8x8/2if | 11 | 11 | 0 |
| 32x32/2if (the scratch port) | 16 | 14 | 2 |

At 32x32/2if, `acmp-noresp`'s two interfaces time out a command within 0.1 ms and the cut sends them in the other
order, so the sequence_id the interfaces share swaps. In valid-destinations' `srp-talker-loss` every MAAP, ACMP and ADP
frame and every publication value is the same, but the DA gate opens each source from the sixth a script step earlier,
and the MRPDUs carry those Talkers earlier. That one is not resolved: the licence cut can only delay a licence, so it
is MAAP's side, `acmp_declaring` or the port of the mask onto #859's entry mapping, which has no host differential at
that shape. At 8x8/2if the lane's own mask leaves the same group the same in every frame and write.

**No regression at 1x1/1if and 8x8/1if.** ROM rises 88 bytes at both, inside the same block RAM (29 and 32 RAMB36);
SRAM is unchanged at 1x1/1if and 16 bytes larger at 8x8/1if (24 RAMB36). No group at either point exceeds a stated
cost or THE SHARE, on either side. The modelled load holds at 0.456 at 1x1/1if and rises 0.568 -> 0.572 at 8x8/1if:
three statements a 5 us step up (ACMP's declined offer, the walk and the tick), each still inside the gate's own
statement. `acmp_rx`, unchanged, sits 52 bytes later in the image, and its calls cost 2.2 % more on average: the
code's placement. The AECP response paths that rose are the stimulus's phase: a shorter pass lets a scripted command
land just after AECP's poll, or an edit just past THE PACE's millisecond, while the pass that answers is shorter.

**The loads**, round 1's model on the cut's costs (the gPTP reservation not included):

| Point | base | cut | cut, `item.mrpdu` restated | a pass's own cost, us (base / cut) |
|---|---:|---:|---:|---:|
| 1x1/1if | 0.456 | 0.456 | 0.447 | 240 / 240 |
| 8x8/1if | 0.568 | 0.572 | 0.547 | 330 / 310 |
| 8x8/2if | 0.605 | 0.597 | 0.573 | 330 / 310 |
| 16x16/2if | 0.741 | 0.732 | 0.682 | 495 / 455 |
| 32x32/2if | 1.111 | 1.091 | 0.980 | 855 / 770 |
| 64x64/2if (A), projected | 2.189 | 2.182 | 1.853 | 1570 / 1400 |

**Milestone one is not met**: at 32x32/2if the cut's load is 1.091, 1.191 with the 0.10 gPTP reservation against
0.70, and 1.080 with `item.mrpdu` restated as well. The exact cuts take 0.020 and 10 % of a pass's own cost; the
build of an MRPDU, lwSRP's, is unchanged.

## 4. Designed, not built

- **THE TRANSMIT's sliced build.** lwSRP builds within a capacity and sends what it omitted at the participant's next
  transmit opportunity, ahead of repeats, so a capacity a pass bounds a build's pass and spreads its declarations over
  JoinTimes. That changes what each MRPDU carries and when, so it is a rule, not an exact cut. `mrp_transmit` walks
  every attribute instance of the port to select and again for each open AttributeType to encode, so a capacity
  bounds the encoding and the insertion sort of the values it selects, not the walks. In
  valid-destinations' `srp-talker-loss` SRP's frames are at most 79, 275 and 512 bytes at 1x1/1if, 8x8/1if and
  32x32/2if, so a 512-byte cap binds nowhere (a capped run at 8x8/1if graded pass for pass as the uncapped one for
  its first 3.6 s). At 32x32/2if the heaviest build is one `build_mrpdu` of 198,400 CPU cycles for a 499-byte frame,
  in a tier-2 slice of 355,798, over the 2.0 ms share; with the three cuts that slice is 333,347. A 256-byte cap
  binds there: over the same 8.5 s of the group the worst pass is 196,831 cycles, inside the share, the heaviest
  builds 27 to 56 % shorter, the values a full PDU omits sent at the next opportunity, and the build passes' total
  11 % less, since a smaller PDU sorts fewer values.
- **Memory at scale.** SRP's pool by placement (each interface its own streams' attributes) takes 32x32/2if from 494
  medium blocks to 263 (-66 KB, 16 RAMB36) and 64x64/2if (A) from 942 to 487 (-128 KB, 32 RAMB36); the medium class
  sized to lwSRP's attribute instance (176 bytes on RV32, against a 256-byte payload) saves a further 21 KB and 38 KB.
  Each moves a bound, so each is a rule; the first needs the receive filter by placement too.
- **MAAP's demand, event-driven**: an epoch ACMP raises where an answer or a Listener changes, and its next expiry.
- **A one-entry `sources_of` memo**: the sources' StreamIDs are written only at `srp_mbx_init`, so it is exact by
  construction, and unlike a byte-7 index it leaves the planted comparison defects observable.

## 5. The Arty at this head

The Arty image at this head (#878's configuration on `15168e14`) was built (WNS +0.009 ns), loaded into the FPGA's
configuration memory over JTAG and read twice. **F1 does not persist**: AECP's timer slot ran twice in about 99 s since
boot, where the older image ran it about 500 times a second, and the loop is idle in 97 % of its passes' cycles.

## 6. Limits of round 2

- **The differential is a subset.** The cut ran, at 1x1/1if, arm A's 21 groups outside the store's windows and the
  four arms that reach the cuts' code (37 finished); at 8x8/1if, 8x8/2if and 32x32/2if the model's matched groups. The
  store's windows (78 groups of arm A) and the three AECP-notice arms were not run for the cut.
- **32x32/2if is not shown exact** in valid-destinations' `srp-talker-loss` (section 3).
- **The loads are the model's**, round 1's, with each cost scaled by the cut/base ratio measured over the groups both
  sides graded; 16x16/2if takes the geometric mean of 8x8/2if's and 32x32/2if's ratios.
- **32x32/2if is the scratch port of #859's shape**, with the MAAP mask carried onto its entry mapping.
