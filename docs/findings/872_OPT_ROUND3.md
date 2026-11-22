# Execution for 64x64 streams on two interfaces: round 3, the firmware levers folded and held egress graded (#872)

Status: **the donor lane's firmware levers folded, the 32x32/2if difference resolved as time, and THE TRANSMIT's held
run-outs graded**, for the manager's round 3 order and rulings (#872, 2026-11-21). No product default, bound or mailbox
contract changed; the one gate rule that changed, the held run-out's, is the ruled one (rule 2). Measured at
`opt-exec-1`, round 2's record ([872_OPT_ROUND2.md](872_OPT_ROUND2.md)) and these commits; tsn-c-stack `115df0b` and
lwSRP `343c610`, each on its own `opt-exec-1`. Every figure names its receipt in the round packet.

## Contents

- **[1. The 32x32/2if difference](#1-the-32x322if-difference)** -- exact at the shape and in situ; what moves is time.
- **[2. The fold](#2-the-fold)** -- the donor lane's levers, the attribute key as a build option, the hot list.
- **[3. Held run-outs](#3-held-run-outs)** -- the ruled grade, and srp-owed in arm A.
- **[4. The re-measure](#4-the-re-measure)** -- 1x1/1if and 8x8/1if against the base, and the loads.
- **[5. Scale](#5-scale)** -- 32x32/2if and 64x64/2if on the fold, and a build's cost a value.
- **[6. Waiting on a decision](#6-waiting-on-a-decision)** -- the Domain cap's bank, the owed MRPDU's restatement, 1x1/1if's 0.003.
- **[7. Limits of round 3](#7-limits-of-round-3)**

## 1. The 32x32/2if difference

Round 2 left valid-destinations' `srp-talker-loss` at 32x32/2if unresolved: the DA gate opened each source from the
sixth about a script step earlier with the three cuts. It is time, not function.

- A host differential at #859's 32x32 shape, its generated contract with 33 sources and sinks, compares the MAAP gate's
  mask and its SRC_SID marks with the base scan after every pass: 48 random configurations, 11,520 passes, no
  difference, and 3 of 3 planted defects caught.
- Round 2's three-lever image, each lever checked against the base procedure at every call, ran the whole group, 1,110M
  sys cycles, without a mismatch; the same image with one planted defect stops at the first call it changes.
- The base reruns byte for byte. Each change alone, and all three together, give every MAAP, ACMP and ADP frame and
  every publication value of the base. A source's DA gate opens only once its SRC_SID is written, one word a poll, so
  each change moves the openings by 0.1M to 1.8M cycles, and where an opening crosses its interface's join opportunity
  the Talker goes out a JoinTime later or earlier. Every Talker declaration is within 200 ms in every run.
- Two refused probes are the harness's window: the step waits for SRP's next frame on either interface, so interface
  1's frame ends interface 0's probe. Interface 0's frames came 180 and 190 ms after their commands.

## 2. The fold

The donor lane's levers are folded as ruled: L6 everywhere, lwSRP's lookup buckets (L3) and transmit merge (L4) on only
from 16x16, its timer wheel (L5) off. The attribute key the buckets carry is a build option too (`LWSRP_ATTR_KEY`,
lwSRP `8645ce2`), set by the buckets and the scale option: at 1x1 and 8x8 lwSRP's objects are byte-identical to the
previous pin's, which keeps 8x8/1if's `declaring-outputs` image in its bank (131,064 bytes of 131,072). The split image's
hot list is relearned by its recorded procedure (267 entries). tsn-c-stack's full suite passes with 482 of 482 planted
defects caught; lwSRP's suites pass in all four profiles and its reversals end with no failure.

## 3. Held run-outs

THE TRANSMIT's grade judges a run-out that is late by its bound, and whose owner's transmit opportunity fell while the
testbench held the egress, again from the egress's return: `held` where the owner's frame or build comes within
JoinTime, 200 ms, of the return, and late past it ([the harness README](../../tb/verilator/ctrl_service_budget/README.md);
IEEE 802.1Q-2018 10.7.11, Milan v1.2 Table 4.3; #872's rulings of 2026-11-21, rule 2, on #894's held-egress
precedent). A held run-out passes and is named, as is a join interval that ends on its frame. `srp-owed` moves into arm
A. Round 2's `srp-owed` logs regrade with 3, 3 and 6 run-outs held at 1x1/1if, 8x8/1if and 8x8/2if, each owner's frame
0.4 to 4.2 ms after the return, and nothing failing. The harness self-test passes with seven new planted defects caught.

## 4. The re-measure

Every arm and every group of the fold's image was measured at 1x1/1if and 8x8/1if, and every leg exits clean. During
the round the base legs round 2 compared against were removed from the host, so the comparison is read from what
survives: round 1's load model with its two lost inputs rebuilt from round 2's saved model, which reproduces round 2's
base loads exactly, and the fold's costs over the groups round 2 compared, against round 2's saved base costs over
them. The differential is against round 2's cut, which round 2 showed the same as its base.

| | 1x1/1if | 8x8/1if |
|---|---|---|
| groups compared, the same in every frame and publication write | 38 of 38 | 8 of 8 |
| ROM, every arm | about 256 bytes more, 29 RAMB36 before and after | about 256 bytes more, 32 RAMB36 before and after |
| SRAM | unchanged | at most 16 bytes more, 24 RAMB36 |
| modelled load, base -> fold | 0.456 -> 0.459 | 0.568 -> 0.561 |

8x8/1if's placement regression of round 2 is gone. 1x1/1if rises 0.003: ACMP's set-bit walk (L6) costs, at two sinks,
about what the two-sink loop did (ACMP's record, its event and its ADP tap 3 to 11 % dearer against round 2),
and MAAP's and SRP's records, which the walk does not reach, moved by the code's placement. The hot list is already
learned at 1x1/1if, so learning it again does not move it.

At 8x8/1if the largest legal AECP command's group, `aecp-largest-notice`, has 2 of its 106 work passes over THE SHARE,
the longest 224,893 cycles, AECP's map code 71,081 of it. It is in the base as well: rerun on round 2's base build, 2
of 108, the longest 222,104.

## 5. Scale

32x32/2if and a built 64x64/2if point ran the fold with lwSRP's lookup buckets and transmit merge on. The 64x64/2if
point (64 stream instances a direction, 32 on each interface) is a scratch port that lifts, in scratch only, the
product limits the point meets; its image takes 199.5 RAMB36.

| Point | Largest build of one, CPU cycles | Its values and frame | Passes over THE SHARE | Modelled load, base -> fold |
|---|---:|---|---|---:|
| 32x32/2if | 102,393 | 17 values, 484 bytes | none; the longest 197,310 cycles | 1.111 -> 0.955 |
| 64x64/2if | 198,328 | 33 values, 932 bytes | 8 of 18,012 in `srp-talker-loss` | 2.189 -> 1.569 |

The transmit merge halves the largest 32x32/2if build (round 2: 198,400 cycles for 499 bytes). A build's cost a value
grows with the values, from about 4,400 cycles a value at 4 to 17 values to about 6,200 at 17 to 33, which sizes the
sliced build's capacity from the measured builds: 16 values a build keeps a 64x64/2if build near 93,000 cycles and
puts an interface's 33 declarations on the wire in three JoinTimes, inside the 600 ms after a LeaveAll. 64x64/2if is
still over the load's 0.70 on one hart.

**The owed MRPDU at its largest.** The valid-destinations arm's `srp-owed-declared` declares every source's Talker
beside a registered Listener, then holds the egress under a bridge's LeaveAll for every MSRP attribute type, so the
poll resends the run's largest SRP frame: 122 bytes and 5 values at 1x1/1if in 17,866 cycles, 402 bytes and 19 values
at 8x8/1if in 38,359, well under the build that made each frame (43,414 and 116,581). Its cost hardly moves with the
frame's size. Under that LeaveAll an SRP record's apply exceeds its statement at both points (34,404 cycles against
28,500 at 1x1/1if, 64,347 against 37,500 at 8x8/1if), a stimulus no arm stages.

## 6. Waiting on a decision

- **The Domain cap** (rule 4: the adopted value and at least one other kept, the oldest other evicted and withdrawn,
  refusals counted) is built and tested, its two-declarer scenario identical and 4 of 4 planted defects caught, but at
  8x8/1if the image no longer fits its 56-RAMB36 budget (131,776 bytes of ROM in 131,072). It waits on the bank or a
  trim, and so do the measurements ruled after it.
- **The owed MRPDU restated** (rule 1) at its measured resend, 195 us at 1x1/1if and 405 at 8x8/1if, moves #894's
  ruled slice at 1x1/1if from 950 us to 900, a product constant, so it waits on a decision. Restating 8x8/1if alone
  leaves the slice at 950.
- **1x1/1if's 0.003** over its base under the ruled fold.

## 7. Limits of round 3

- **The base is round 2's saved one.** The base legs were removed from the host; the loads and the differential are
  read against round 2's saved base costs and its cut, not a fresh base.
- **The loads are the model's**, with each cost scaled by the fold/base ratio over the groups both sides graded and
  the built 64x64/2if point entered as measured.
- **32x32/2if and 64x64/2if are scratch ports.** They ran arm A's matched groups and `srp-talker-loss`; the owed
  MRPDU was not staged at them.
- **One hart.** No two-hart image of the fold was measured.
