[A683zm]

## Contents

- **[Status](#status)** — REVIEW READY at the head below: round 28's seven items. 1x1/1if's long-window load is held for merge at this tree's pin and with tsn-c-stack#32; a failed record move is reported for its own record and a notice resumes at the recipient whose frame was lost; the firmware's compiler extensions sit behind one platform header; each point's flip is held to decision D's tier bounds, which 1x1/1if misses at R4 (a finding).
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — Round 28 item by item and the re-grade on its image; round 27 as it stood; what holds at this head; where the round histories went.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Checkout, submodules and environment.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What is left, and the decisions for the owner.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

REVIEW READY at `66f713267f201d1a00d7f711e04b3a996d804dee`, five commits on round 27's head `e7e2b744` (`665-s2b-cycles` -> `dev-soft-core`). No merge, no rebase, no force, no amend. No RTL, mailbox contract, donor or submodule change; the firmware changes are items 2 and 5.

The round 28 ruling (#665 issuecomment-6805157674) is the last round before S2b's merge: items 1 to 7 of R711-6's and R712-6's findings (both NEGATIVE at `e7e2b744`, MINOR only), and nothing else.

- **1x1/1if: 0.463 at the pin and 0.450 with tsn-c-stack#32**, each held at 0.70 for merge by `load_grade.py --check`, which exits 0.
- **8x8/2if: 0.815 at the pin**, held by the flip check (0.719 with tsn-c-stack#32), which exits 1 at this head; the 8x8/2if flip waits on #890.
- **Decision D's tier bounds**, held for each point's flip by `flip_grade.py --check`: 1x1/1if misses tier 1 at R4 (73.02 ms by every source against 20 ms), a finding the ruling asks reported; R5, R6 and the queued notices fit there.
- 32x32/2if, reported: the more-compute image, #872: 1.659 (2.150 at the pin), 2.37x the compute for 0.70.

The full gate pass ran once, on clean clones of this head, every gate rc 0 but the flip check, which exits 1 by design ([How to validate](#how-to-validate)).

## Linked Issue / roles

Relates to #665
Relates to #882 (its three acceptance items were met in round 27)
Relates to #890 (the 8x8/2if flip, which this lane's flip check holds)
Relates to #891 (the 14-bit AEM command_type the harness works around)

Executor: `[A683zm]`
Internal cleared-context reviewer: `[R711]`
External reviewer: `[R712]`

## Description

### Round 28

**The ruling** (issuecomment-6805157674, on R711-6 and R712-6, both NEGATIVE at `e7e2b744`, MINOR only): the last round before S2b's merge, items 1 to 7 and nothing else.

| Item | At this head |
|---|---|
| 1. The merge gate at the pin (R711-6 F1 = R712-6 F1) | `5a19b0ca`. `load_grade.py --check` holds 1x1/1if in both columns, this tree's pin (the image that merges) and with tsn-c-stack#32 (the load the pin move owes), each at most 0.70 (`load_grade.COLUMNS`); a point over its ceiling is named with its column (`1x1/1if: the load L at the pin is over its ceiling 0.70`), and `--check` prints a `HELD` line for each. At this head 0.463 at the pin and 0.450 with tsn-c-stack#32, `RESULT: PASS`. A new control plants a pin-only rise (an ACMP record, a cost the donor's walk may state lower, raised to 2,000 us in the pin's column alone: the pin's load 0.807) and the gate must refuse it naming the pin's column: `--selftest` 24 of 24. R711-6's `probe_1x1_column.py` and R712-6's `probe_pin_1x1.py` now each print the refusal, `1x1/1if: the load ... at the pin is over its ceiling 0.70`. Section 13's margin names both columns |
| 2. Record commits (R712-6 F2) | `71e905fb`. A TX record holds whether the record mover carries it (`TX_MOVED` in `tx_ring.moving`), and its commit waits on the mover and judges its ERR only then: a record the word loop wrote never inherits an earlier ERR, which the mover holds until its next start. A failed move is reported for the record it carried: `mbx_tx_commit` is false, and `mbx_tx_begin`, which commits the record before its own, returns the new `MBX_STATUS_LOST` and starts nothing. The AECP fan port reports it for its frame (`enum aecp_fan`: TAKEN, REFUSED, LOST), from the next `fan` or from `fan_end`, which no longer discards its commit's result and keeps no completion for a lost last frame; `fan_out` resumes the notice at the recipient whose frame was lost and gives back the sequence_id it did not spend (IEEE 1722.1-2021 7.5.2; Milan v1.2 5.4.5.1). `mbx.h` states it. Tests: the driver's T4 (an ERR, then a frame off a word, sent whole and in halves, which must commit; then a frame on a word moved again) and T5 (the fan port over the DMA driver: the fan after a failed move LOST, nothing started; a failed last frame LOST from `fan_end`, no completion; each sent again), T2 extended; the AECP core's `ANoticeWhoseFrameWasLostSendsItToItsRecipientAgain` (a middle frame lost, reported by the next fan, and a last frame lost, reported by `fan_end`). Nine plants, each caught by its test's words (HANDOFF section 3). The image grows 112 to 120 B (8x8/2if arm A 122,328 to 122,440 B, the `answering-every-port` arm 122,636 to 122,748 B, each within its ledger). With tsn-c-stack#32, arm A's 8x8/2if image is 122,896 B, 58 RAMB36 against the 57.5 ledgered there: that column's 8x8/2if leg does not build at this head and keeps its committed costs, and the pin move that carries tsn-c-stack#32 meets the same ledger |
| 3. Round 16's margin at 8x8/2if (R711-6 F2) | Deferred to the 8x8/2if flip under #890, whose owner decision of 2026-11-11 sets that point's flip ceiling to 0.75; section 13 cites it. 1x1/1if keeps the margin: its heaviest work pass at this image is 160,618 cycles (`backlog`), 39,382 under the share. At 8x8/2if this image's heaviest is 192,237 cycles (`backlog`), 7,763 under the share, so the margin holds at this layout (round 26's image gave 193,609, 99 short): it moves with the image, which is why the ruling defers it. `flip_grade.FLIP` keeps 0.70 at this head: #890's decision applies the 0.75 in a change of its own once the pin moves |
| 4. Decision D's tier bounds (R711-6 F3) | `5a19b0ca`. `flip_grade.py --check` holds each point's flip to the rows by every source (`rows_grade.py`): R4 at tier 1's 20 ms, R5 and R6 at SRP's 90 ms, the first queued notice at 20 ms and the last at 125 ms, at 1x1/1if and 8x8/2if (`--point` for one). R4, R5 and R6 are round 22's method on this tree's pin costs (the smallest W in which the record's own work and every source's arrival bound fit, THE DRAIN as `ctrl_loop.h` states it, the grandmaster events at their IEEE 802.1AS-2011 intervals); the queued notices are `aecp_mbx.h`'s derived bounds, which the loop search holds. Self-test controls for each row at each point (over and within its bound), each source left out, the pin's column read, a planted queued-notice derivation and the bounds themselves: 129 of 129, and five harness mutants caught. **The 1x1/1if result, a finding:** R4 is 73.02 ms by every source against tier 1's 20 ms (+53.02 ms; its largest terms SRP's records ahead of AECP's, 16.50 ms, the other channels' records, 10.96 ms, and the retained retries, 9.00 ms): THE DRAIN takes SRP's records first, and round 23's tier design, a tier-1 record served before any tier-2 work, is not built. R5 is 37.19 ms and R6 32.69 ms within SRP's 90; the first queued notice is held at 20 ms, its bound, and the last at 22 ms within 125. So `flip_grade.py --check --point 1x1/1if` exits 1 at this head, and the 1x1/1if flip cannot pass it until R4 fits; the finding is for an issue of its own, the manager's to open. The flip at 1x1/1if must pass `flip_grade.py --check --point 1x1/1if`; 8x8/2if stays with #890 (R4 489.97 ms, R5 162.96 and R6 149.57 ms by every source, the first queued notice stated at 22 ms against tier 1's 20 and the last at 62 within 125) |
| 5. Portable C (R711-6 F4) | `24ea9c04`. `_Alignas(64)` for the AECP response buffer (`alignas(64)` where a C++ test reads `aecp.h`, which g++ requires); `noinline` and `may_alias` behind `CTRL_CC_GNU` in `sw/firmware/ctrl/plat/ctrl_cc.h`, outside the protocol code, with a portable C11 fallback (nothing for `CTRL_CC_NOINLINE`, `memcpy` for the pool's link). `git grep __attribute__ -- sw/firmware/ctrl ':!*/test/*'` shows only that header, and a new firmware arm, `portable`, holds it: a scan for `__attribute__` and `__builtin_` outside `test/` but `ctrl_cc.h`, and the port arm's tests built with `CTRL_CC_GNU=0`. A pool test that can fail for an unwritten link (`Pool.P10`) and three plants. The change alone is image-neutral: `e7e2b744` with it builds 8x8/2if arm A's three images byte-identical to round 27's (objcopy sha256 `5b2317d8...`, `be42e7c9...`, `57b60044...`) and its `control` group's log byte for byte, so it restates no cost |
| 6. Docs and residue | R712-6 F3's sentence (152 B at the pin and 160 B with tsn-c-stack#32); the new harness comments' issue-comment IDs and round labels replaced by the issue and the behaviour; #890 and #891 named where this body said "the flip-gate issue" and "its own issue", and at the harness's unknown command (`answers.py`) |
| 7. Gates | The full clean-clone pass at this head, once ([How to validate](#how-to-validate)): every gate rc 0 but the flip check, which exits 1 by design; `elaborate-gates-1` ran twice, its first run's LiteX simulation timing out under the session pool's load |

**The re-grade on this image** (item 7; the legs at `71e905fb`, every group of arm A and of the `answering-every-port` arm at both points, arm B's `aecp` group and the column with tsn-c-stack#32 at 1x1/1if; then regraded at the head):

| Leg | Groups | Refusals | Budget misses | Work passes over the share | Heaviest work pass, CPU cycles | Least row margin |
|---|---:|---:|---|---|---|---|
| Arm A, 8x8/2if | 93 | 0 | 6 of 996 instances, 3 of 136 paths | 0 of 272,475 | 192,237 (`backlog`), 7,763 under | 6.515 ms (13.485 ms, an AECP record in a save's verify window opened at the age limit) |
| Arm A, 1x1/1if | 94 | 0 | 6 of 945, 3 of 87 | 0 of 184,496 | 160,618 (`backlog`) | 10.434 ms |
| The `answering-every-port` arm, 8x8/2if | 16 | 0 | 0 of 736 | 0 of 14,350 | 186,213 (`notice-every-2`) | 4.018 ms (15.982 ms, `notice-burst-6`) |
| The `answering-every-port` arm, 1x1/1if | 16 | 0 | 0 of 280 | 0 of 22,114 | 160,222 (`notice-burst-6`) | 8.349 ms |
| Arm B's `aecp` group, 8x8/2if and 1x1/1if | 1 and 1 | 0 | 0 of 39, 0 of 25 | 0 of 131, 0 of 110 | 119,134 and 63,670 | |
| Arm A with tsn-c-stack#32, 1x1/1if | 19 | 0 | 6 of 141, 3 of 81 | 0 of 10,249 | 156,237 (`backlog-adp`) | |

The six misses at each arm A point and with tsn-c-stack#32 are the three egress-held paths of tsn-c-stack#26, as in round 27. Each save is durable within its stated worst case (8x8/2if `save-second` 22,110 ms against 22,150; 1x1/1if 6,030 against 6,070). **The costs** (round 26's parsers, each cost the larger of this measurement and the committed table's): no cost at the pin moves at either point, nor `poll_grade.py`'s; with tsn-c-stack#32 at 1x1/1if ACMP's timer slot rises 165 to 170 us and THE TRANSMIT's build 910 to 920 (`66f71326`), which leave that column at 0.450. The four cost controls are refused on this image (an AECP item of 29,968 cycles against 27,000; an SRP record's apply of 37,494 against 36,500; a polls base of 74,399 against 28,000; a rebuild item of 113,443 against 63,000).

**The load at this head** (`load_grade.py --check`, `flip_grade.py --check`):

| Point | Load at the pin | Load with tsn-c-stack#32 | Held by | Compute for 0.70 | Its three largest terms |
|---|---:|---:|---|---:|---|
| 1x1/1if | 0.463 | 0.450 | the load gate, 0.70 in both columns, for merge | 1.00x | SRP's channel 0.150, ACMP's records 0.053, the TICK's consumers 0.047 (with tsn-c-stack#32) |
| 8x8/2if | **0.815** | 0.719 | the flip check, 0.70 at the pin | 1.16x at the pin | SRP's channel 0.219, ACMP's records 0.088, ACMP's owed frame 0.070 (at the pin) |
| 32x32/2if | 2.150 | 1.659 | reported: the more-compute image, #872 | 2.37x | SRP's channel 0.519, owed MRPDUs 0.299, THE TRANSMIT's builds 0.150 (with tsn-c-stack#32) |

**The rows by every source at this head** (`flip_grade.py --check`):

| Point | R4 (tier 1, 20 ms) | R5 (SRP, 90 ms) | R6 (SRP, 90 ms) | First queued notice (20 ms) | Last queued notice (125 ms) |
|---|---:|---:|---:|---:|---:|
| 1x1/1if | **73.02** | 37.19 | 32.69 | 20 | 22 |
| 8x8/2if | **489.97** | **162.96** | **149.57** | **22** | 62 |

Each W in ms by every source at this tree's pin; bold misses its bound. The largest terms of 1x1/1if's R4: SRP's records ahead of AECP's 16.50 ms, the other channels' records 10.96, the retained retries 9.00.

### Round 27 (at `e7e2b744`)

**The ruling** (issuecomment-6788828284, on [A683zf]'s STOP at `0b37f3d2`, issuecomment-6788757307):

| Item | At this head |
|---|---|
| 1. #882 first | `e5baac61`. The CPU budget harness's `get_avb_info` row sent GET_AS_PATH (`0x0028`) with descriptor_index 9, which no image has, and timed its NO_SUCH_DESCRIPTOR as GET_AVB_INFO. It now sends GET_AVB_INFO (`0x0027`) on AVB_INTERFACE 0 with its four-byte command (IEEE 1722.1-2021 7.4.40.1; Milan v1.2 5.4.2.23). Every row that ends at a response states its command or message type and its status (`answers.py`; IEEE 1722.1-2021 Table 7-141 for AEM and MVU, Table 8-3 for ACMP), and the grader holds the probe's own response, the one answering its sequence_id, to both: another type or status is an unexpected response, which fails the run. A row that states a status other than SUCCESS is a refusal row, named `<row>, refused <status>`; the run refuses a row that states no response, or a refusal its row does not name. **SUCCESS is asserted in arm B** (`answering-ports`), whose observation ports answer; in arm A the test SoC's datapath is held idle, so the face block's window read finds no answer within its bound and GET_AVB_INFO answers ENTITY_MISBEHAVING, a named refusal (GET_COUNTERS is the same case, and was measured as an unnamed refusal before). Arm B's `aecp` group is now one of the load gate's legs at both points. The other refusal rows: PROBE_TX (TALKER_DEST_MAC_FAIL: the source has no stream destination in that group, Milan v1.2 Tables 5.42 and 5.43), GET_TX_CONNECTION (NOT_SUPPORTED, Milan v1.2 5.5.4.4, Table 5.48) and the unknown AEM command (NOT_IMPLEMENTED). Eighteen self-test checks and ten mutants, among them the plant restoring the refused command, caught |
| The baseline | On unchanged firmware, each of round 26's legs rebuilt byte-identical to its build (objcopy and ELF), its sample log byte-identical; the `aecp` group run again in arm A, in arm B and with tsn-c-stack#32 at both points; every other recorded group regraded under the new checks. 0 refusals; the tallies round 26's (8x8/2if: 93 groups, 6 misses of 996 probe instances, 3 of 136 paths, the three egress-held paths, tsn-c-stack#26; 1x1/1if: 94, 6 of 945, 3 of 87; the notice arm 0 of 736 and 0 of 280; no pass over the share); the `aecp` group's heaviest AECP record 21,201 cycles at 8x8/2if (arm B) and 15,838 at 1x1/1if, under the AECP record's stated 265 and 205 us. The figures that changed (#882's item 3), each a row's time on interface 0: at 8x8/2if `get_avb_info` 0.338 ms in arm A, refused ENTITY_MISBEHAVING (0.316 as GET_AS_PATH before), and 0.341 ms in arm B, SUCCESS; `get_counters` 0.255 in arm A, refused as before, and 0.284 in arm B; at 1x1/1if `get_avb_info` 0.118 in arm A (0.095 before) and 0.143 in arm B; the costs' notice instance counts (35 to 41 at 8x8/2if, 29 to 32 at 1x1/1if, arm B's notices), and the 1x1/1if ADP event with tsn-c-stack#32 measured 9,482 cycles (9,940 before), under the 110 us its column states. **No stated cost moves**, so the load is round 26's |
| 2. One cut | The gap at 8x8/2if, 0.019, is under 0.03. The cut, of this tree's share of SRP's record: the record path's StreamID and MAC comparisons with their last byte compared where they are called, `same` only on a match; a sink's `capture` only where its kind was or is one; `ctrl_mem.c`'s `memcmp` four bytes a turn where the two alignments differ. **Measured on a scratch image and not committed.** On the same groups at 8x8/2if the heaviest SRP record went from 34,361 to 33,741 cycles (the `answering-every-port` arm's `notice-every-3`) and from 33,260 to 33,251 in arm A (`backlog-owed`): stated 365 to about 355 us, 8x8/2if about 0.713 with tsn-c-stack#32 and 0.809 at the pin, over 0.70 either way; closing it takes the heaviest record to 31,428. The cut takes about as much from the second heaviest record as from the heaviest, so the heaviest's excess of some 11,000 cycles is not in its reach; and it adds 152 B at the pin and 160 B with tsn-c-stack#32, which takes arm A's image with tsn-c-stack#32 over the 8x8/2if ledger (122,936 B in 122,880), so the graded column's leg would not build; the pin move that carries tsn-c-stack#32 would meet the same ledger. The same image moved the heaviest work pass of those groups by -15,987 to +2,056 cycles. With no firmware change there is no firmware mutant |
| 3. The gate pass | The full clean-clone pass at this head ([How to validate](#how-to-validate)) |
| 4. The outcome | 8x8/2if over and 1x1/1if under: the lane splits. `load_grade.py --check` holds 1x1/1if for merge (`load_grade.CEILING`). 8x8/2if is held by `flip_grade.py`, a separately invoked check that reads the pin's column (`load_grade.STATED_US`) through `load_grade.load`: `--check` exits 1 at this head, `OVER 8x8/2if: the load 0.815 at the pin is over the flip ceiling 0.70`; `--selftest` refuses all six of its controls, the over-ceiling row among them, and four more mutants hold the split in the harness self-test. The manager opened the flip-gate issue, #890 |
| 5. Tripwire | Fires. The memo's figures: the baseline 0.719 with tsn-c-stack#32 and 0.815 at the pin; after the cut about 0.713 and 0.809; the movement between images on the same groups, the heaviest work pass -15,987 to +2,056 cycles |
| 6. The donor | tsn-c-stack, lwSRP and the donor clone untouched; the graded column's legs apply round 26's port of tsn-c-stack#32 in a scratch build, byte-identical to round 26's image. The flip check reads the pin, `70936b77` here. tsn-c-stack#34 (tsn-c-stack#32) merged on the stack's `main` at `715589c` during this round, by its own review; the pin move is its own lane |
| 7. S9 (#870) | Its `KL_mbx` round had not landed by the measurement (its round 3 posted REVIEW READY afterwards and is in review): the grade uses the harness's own access cycles, and #890 carries #870's |

**The load at round 27's head `e7e2b744`** (as its gates then stood):

| Point | Load at the pin | Load with tsn-c-stack#32 | Held by | Compute for 0.70 | Its three largest terms |
|---|---:|---:|---|---:|---|
| 1x1/1if | 0.463 | 0.450 | the load gate, 0.70, for merge | 1.00x | SRP's channel 0.150, ACMP's records 0.053, the TICK's consumers 0.047 (graded) |
| 8x8/2if | **0.815** | 0.719 | the flip check, 0.70 at the pin | 1.16x at the pin | SRP's channel 0.219, ACMP's records 0.088, ACMP's owed frame 0.070 (at the pin) |
| 32x32/2if | 2.150 | 1.659 | reported: the more-compute image, #872 | 2.37x | SRP's channel 0.519, owed MRPDUs 0.299, THE TRANSMIT's builds 0.150 (graded) |

**Three findings** (none changed here): the firmware keeps 14 bits of AEM command_type (`aecp.c:428`, `& 0x3fff`), so `0x7FF0` is answered NOT_IMPLEMENTED under `0x3FF0` (#891; the harness's unknown command is `0x3FF0`, a reserved value under `0x4000`, until it is fixed); no arm measures GET_AVB_INFO, GET_COUNTERS or GET_STREAM_INFO with their window reads answered (arm A's are refused at the window's bound, arm B's stubs read no window); and no row measures a talker's PROBE_TX answered SUCCESS.

### What holds at this head

The acceptance of this lane's assignment (S2b, #665: the split firmware within T_svc, cycle work in firmware, owner decision D4 a), read at this head:

- **The rows by measurement** (the CPU budget harness on this head's image, every group of arm A and of the `answering-every-port` arm, and arm B's `aecp` group, at 1x1/1if and 8x8/2if): every row is within its bound except the three egress-held paths (`backlog.owed`, `backlog.owed_behind0` to `3`, `backlog-owed.service.aecp.last`, tsn-c-stack#26): 6 misses of 996 probe instances in 93 groups at 8x8/2if, and of 945 in 94 groups at 1x1/1if. 0 refusals, no `STATED` line, every row's response the one it states. The `answering-every-port` arm: 16 groups at each point, 0 misses of 736 and 280, every queued notice within its bound. Arm B's `aecp` group: 0 misses of 39 and 25.
- **The pass share** (2.0 ms): 0 of 272,475 work passes over it at 8x8/2if and 0 of 184,496 at 1x1/1if; 0 of 14,350 and 0 of 22,114 in the `answering-every-port` arm. The heaviest at 8x8/2if is 192,237 cycles (`backlog`), 7,763 under, round 16's margin met at this layout and deferred to #890 by the ruling; at 1x1/1if 160,618, 39,382 under.
- **The bounds that hold by construction:** the queued notices at `aecp_mbx.h`'s stated bounds, which the loop search holds the loop to (the first 22 ms at 8x8/2if and 20 at 1x1/1if; the last 62 and 22 ms within their 70 and 25 ms ceilings); every pass's polls base and each heavy item within its stated cost (`poll_grade.py`), each SRP record's own apply within its retry's, every round within its own (`round_grade.py`), and every pass given whole to a build or an aged step within its own (`whole_grade.py`), each a gate over every group at both points.
- **The long-window load:** 1x1/1if within its ceiling in both columns, held for merge; 8x8/2if over it, held by the flip check.
- **Decision D's tier bounds by every source, for the flip:** at 1x1/1if R5, R6 and both queued notices fit.
- **What does not hold:** 1x1/1if's R4 by every source (73.02 ms against tier 1's 20); at 8x8/2if R4, R5 and R6 by every source and the first queued notice (22 ms against 20), with #890; every row at 32x32/2if; the long-window load at 8x8/2if.

### The round histories

Rounds 12 to 26's Description sections, and the decisions their Known limitations listed, are in the evidence packet `evidence/ROUND-HISTORIES.md` (round 26's moved there in this round, as round 27's body gave it, its load block headed with the head it describes).

## Authoritative references

- The round 28 ruling (#665 issuecomment-6805157674); R711-6 (PR comment, issuecomment-6805132259) and R712-6 (issuecomment-6799611250), the reviews it answers; #890 and its owner decision of 2026-11-11 (the 8x8/2if flip ceiling 0.75); #891.
- Decision D (#665 issuecomment-6759183115 and issuecomment-6759193032: the flip gates 1x1/1if and 8x8/2if under 0.70 with the tier bounds in force) and the round 23 ruling (issuecomment-6732443213: tier 1 20 ms, SRP 90 ms, the last queued notice 125 ms; the every-source count is the bound).
- IEEE 1722.1-2021 7.5.2 (a notice to each registered controller, its own sequence_id) and 9.2.1.1; Milan v1.2 5.3.4.2 and 5.4.5.1. The record mover's register contract (`sw/firmware/ctrl/plat/mbx_dma.h`: ERR set by a refused start or an error response, cleared by the next accepted start) and `hdl/milan/mailbox/KL_mbx_dma.sv`.
- C11 (ISO/IEC 9899:2011) 6.7.5 (`_Alignas`) and 6.5 paragraph 7 (the effective-type rule the pool's link meets through `memcpy` in the fallback); `sw/firmware/ctrl/README.md` ("Portable C11 for the on-chip RISC-V, and for a hard core").
- The round 27 ruling (#665 issuecomment-6788828284) and the earlier rulings where round 28 leaves them; the round 16 ruling (issuecomment-6634982529, item 2: every pass class at least 6,490 cycles under the share).
- The protocol timers the arrival bounds cite: Milan v1.2 5.5.2.3 and Table 5.26, 5.6.3.5.3, 5.6.3.5.9 and Table 5.50, 5.6.4.5, 5.4.5.2 and Table 5.22, 5.4.5.3; IEEE 1722.1-2021 6.2.2.5; IEEE 1722-2016 B.3.4.1, B.3.4.2 and Table B.8; IEEE 802.1Q-2018 10.7.4.1 and Table 10-7, Milan v1.2 Table 4.3; IEEE 802.1AS-2011 (+Cor1/Cor2) 10.7.2.2, 10.7.3.2 and 11.5.2.2, the edition Milan v1.2 profiles.
- `sw/mailbox/mailbox.yaml`, each channel's `rate` and `tick_ms`; `docs/design/SPLIT_CONTROL_MEMORY.md` section 13 (the long-window load, the rows by every source) and section 5 (the ledger); `tb/verilator/ctrl_service_budget/README.md`; `sw/firmware/ctrl/README.md`, `sw/firmware/ctrl/aecp/README.md`, `sw/firmware/ctrl/plat/README.md`.
- `docs/reference/FR_NFR.md` 3.4.1; `sw/firmware/ctrl/loop/ctrl_loop.h` (THE SHARE, THE DRAIN, THE RETRY, THE TRANSMIT, THE STEP); `sw/firmware/ctrl/aecp/aecp.h` and `aecp_mbx.h`; `sw/firmware/ctrl/mbx/mbx.h`.

## How to get into the same state

```sh
git fetch origin
git checkout 66f713267f201d1a00d7f711e04b3a996d804dee
git submodule update --init protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack third_party/verilog-axis
```

The harness's prerequisites are in `tb/verilator/ctrl_service_budget/README.md`: the product LiteX tree, the pinned RV32 SDK and Verilator, with `COURSIER_MODE=offline` and `SBT_OPTS=-Dsbt.offline=true`.

## How to validate

```sh
python3 -B tb/verilator/ctrl_service_budget/load_grade.py --check
python3 -B tb/verilator/ctrl_service_budget/load_grade.py --selftest
python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --selftest
python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check --point 1x1/1if
python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check
python3 -B tb/verilator/ctrl_service_budget/run.py --self-test
git grep -n __attribute__ -- sw/firmware/ctrl ':!*/test/*'
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 0/4
python3 sw/firmware/gtest/fw_coverage.py --check
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir /tmp/budget-8x8 --record-budget-findings --record-share-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir /tmp/budget-1x1 --record-budget-findings --record-share-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir /tmp/budget-8x8-notice --variant answering-every-port --record-budget-findings --record-share-findings
```

Expected result at this head:
- `load_grade.py --check` prints the load table and exits 0 (`RESULT: PASS`) with `HELD 1x1/1if at the pin: the load 0.463, its ceiling 0.70` and `HELD 1x1/1if with tsn-c-stack#32: the load 0.450, its ceiling 0.70`; the 8x8/2if row's ceiling reads "the flip check, 0.70 at the pin". `--selftest`: `load gate: 24 of 24 planted controls refused`.
- `flip_grade.py --selftest` exits 0, `flip check: 129 of 129 planted controls refused`. `flip_grade.py --check --point 1x1/1if` exits 1 at this head, `OVER 1x1/1if R4: by every source 73.02 ms, over its bound 20 ms`: the finding above. `flip_grade.py --check` exits 1 by design, 8x8/2if's load and rows over with them: it is no merge gate.
- The harness self-test reports 0 failures, 201 mutants caught (five new).
- `git grep -n __attribute__ -- sw/firmware/ctrl ':!*/test/*'` prints only `sw/firmware/ctrl/plat/ctrl_cc.h`'s two lines.
- The firmware gate PASS, its `portable` arm among its arms; `fw_coverage.py --check` PASS over 39 files.
- The 8x8 and 1x1 runs: as the re-grade's table above (0 refusals, no pass over the share, no `STATED` line, every row within its bound but the three egress-held paths).

The evidence at this head, each on a clean clone of it, never piped:

- **Every `run:` step of the four workflows a pull request to `dev-soft-core` triggers**, each job on its own fresh clone: 139 steps ran, every one rc 0 (`elaborate-gates-1`'s from its second run, below), 0 steps without an rc or a reason; 226 are not run, each with its reason (hosted orchestration, artifact upload and collection, apt and sudo installs whose pinned tools this host carries, `physical-gptp`, which runs only on a schedule, and `rtl.yml`'s `verilator-shards` suites, which run here as the full sweep below).
  - `rtl-fast.yml`, all 14 jobs: `changes`, `verilator-lint`, `bdd-conformance` (508 scenarios and 2,330 steps passed), `yosys-tool`, `yosys-elaboration`, `publication-census`, `split-cdc`, `rtl-fast`; `firmware-unit` (`test_ctrl_firmware.py --require-rv32 --self-test` PASS, the `portable` arm among its arms; the saved-state store gate's 455 tests; `fw_coverage.py --check` PASS over 39 files); `firmware-control-mutants` (680 of 680 caught), `firmware-aecp-mutants` (224 `[ok]`), `firmware-srp-mutants` (340 `[ok]`); `firmware-boundary` and `firmware-verilator` (`ctrl_boundary: PASS`, 0 findings).
  - `rtl.yml`: `full-ci-gate`, `yosys-tool`, `yosys-shards` 0/4 to 3/4.
  - `elaborate.yml`: `elaborate-gates-0`, `elaborate`, and `elaborate-gates-1` (its first run's LiteX simulation aggregate, `gate_19`, exited 92: `test_soc_timing_cuts` passed its 900 s wall clock on the loaded session pool, result unknown, 7 of 8 passed; the job ran again on a fresh clone, every step rc 0, 8 of 8 passed; both runs' logs are kept).
  - `docs.yml`: `wire-accountability`, `docs-check-no-git` (its three steps rc 0; the job removes `.git`, so the runner's own tree check after it cannot run), `docs-gates-0` (43 steps), `docs-gates-1`, `docs-gates-2`, `docs-check`.
- **The full sweep**, `scripts/run_all_suites.sh` as four shard units on clean clones: 65 suites, 65 passed, 0 failed, 0 timed out, 2,613,726 checks, 0 in-suite failures; every shard's preflight PASS (suite cancellation among them), so no re-run; the shard holding `capture_coherence` on four CPUs. The shards ran on the shared session pool: the release lane's holds kept every bookable range for the hour before.
- **The lane's own gates** on clean clones: `git diff --check` against the merge base `1d6bf555` and against round 27's head; `check_py_idiom.py`, `check_cpp_idiom.py`, `check_baremetal_only.py --check`, `docs_check.py` (0 findings); `ctrl_hot.py --self-test` and `--check`; the harness self-test (`self-test: 0 failures`, 201 mutants caught); `load_grade.py --selftest` (24 of 24) and `--check` (PASS, both columns held); `flip_grade.py --selftest` (129 of 129) and `--check`, `--point 1x1/1if` and `--point 8x8/2if` (each exits 1, as above); R711-6's and R712-6's column probes (each pin-only rise refused); `git grep __attribute__` (the platform header only); `ctrl_service_hooks` (28 of 28 checks, 96 of 96 mutants) and `nvm_split_target` self-tests; `test_ctrl_nvm.py --require-rv32 --self-test` (121 planted defects reddened); `gen_mailbox.py --check --crosscheck` and `--selftest`; `lint_rtl.py --check`; `test_soc_options.py`; `test_ctrl_memory.py`; `test_builder.py --require-rv32` (every gate passes; the same two arms as before do not run, each with the tool's reason); `ctrl_split_boot` at 1x1 and 8x8 (PASS, 0 findings), its native controls (6 of 6) and its plants (3 of 3); `cd tests && behave` (508 scenarios, 2,330 steps passed); `make -C tb/verilator/milan_dp twin` (0 findings). Each clone's tree is clean after them.
- **The harness at both points**: every recorded group of arm A, of the `answering-every-port` arm and arm B's `aecp` group at 1x1/1if and 8x8/2if, regraded at this head against a fresh build of each point made there, whose images and sample log are byte-identical to the leg's: 0 refusals; 6 misses of 996 probe instances (3 of 136 paths) at 8x8/2if and of 945 (3 of 87) at 1x1/1if, the three egress-held paths; 0 of 272,475 and 0 of 184,496 work passes over the share; the notice arm 0 of 736 and 0 of 280; arm B 0 of 39 and 0 of 25. (The coverage ratchet's commit changes a tree the builds digest, so the legs' own builds refuse reuse at the head.)

## Known limitations / out of scope

- **Round 28's decisions, for the owner and the manager:**
  1. **1x1/1if misses tier 1 at R4 by every source** (73.02 ms against 20; [Round 28](#round-28), item 4): THE DRAIN takes SRP's records ahead of AECP's and round 23's tier design, a tier-1 record served before any tier-2 work with tier-2 work in bounded slices, is not built. The ruling makes it a finding for the 1x1/1if flip, which must pass `flip_grade.py --check --point 1x1/1if`; it is for an issue of its own.
  2. **8x8/2if waits on #890**: its load (0.815 at the pin, 0.719 with tsn-c-stack#32), its rows by every source, and round 16's margin there, which the ruling defers to that flip. #890's owner decision sets that point's flip ceiling to 0.75 in a change of its own after the pin move; this head keeps `flip_grade.FLIP` at 0.70.
  3. **The column with tsn-c-stack#32 is not re-measured at 8x8/2if**: arm A's image with tsn-c-stack#32 is 122,896 B at this head, 58 RAMB36 against the 57.5 ledgered for 8x8, two interfaces (16 B over the granule; 122,776 B at round 27), so its leg does not build and the column keeps its committed costs there. The pin move that carries tsn-c-stack#28, tsn-c-stack#31 and tsn-c-stack#32 meets the same ledger: arm A's 16 B, and the `answering-every-port` arm's, 204 B over at round 27 and 112 B more with item 2.
  4. **The firmware coverage ratchet** is recorded again through `fw_coverage.py --write` for the new platform header: every file stays at 100 % of lines and branches, and the counts of the files earlier rounds grew are recorded with it (the ratchet refuses only a drop).
- **Round 27's decisions, where round 28 leaves them:** SUCCESS for GET_AVB_INFO asserted in arm B, the arm whose observation ports answer; AEM command_type at or above `0x4000` answered under another command_type (`aecp.c` keeps 14 bits; #891, the harness's unknown command `0x3FF0` until it lands); PROBE_TX's SUCCESS measured by no row; the cut of SRP's record measured and not committed.
- **Live `dev-soft-core`** has moved since the merge base `1d6bf555` to `764482b4` (PR #874, lwSRP's transmit path); `git merge-tree` merges this head with it with no conflict. The candidate merge is the manager's to validate.
- **`AECP_NOTICE_US`** (365 us at two interfaces) and **`AECP_NOTICES_MOST`** (40 at two interfaces, against 136 in the 32x32/2if model, #866) are unchanged; the queued-notice bounds and their search are stated for them.
- **A refused SRP record's give-up** past 1 s with a change pending waits at most the centisecond for the retry the change allows (`sw/firmware/ctrl/srp/README.md`).
- **No group stages** a retained record's retry, an owed MRPDU or a registration's probe, nor a failed record move (the driver and AECP tests do): each is stated at the cost of the measured work that holds it.
- **The three egress-held rows** stay with tsn-c-stack#26.
- **The drafts** (lwSRP, tsn-c-stack) are measured staged and are not pinned here.
- **The platform image's hot list:** four entries name the size fixture's callbacks and place nothing in that image.
- **No fabric option outlives the switch-over:** nothing here adds one. The hybrid-XIP arm still misses T_svc on every path, so D3's rule stands.
- The earlier rounds' decisions for the owner and the manager are in `evidence/ROUND-HISTORIES.md`.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (#665 stays open: this lane is one part of it)
- [x] New or changed behavior has self-checking tests (the driver's T4 and T5 and T2 extended, the AECP lost-frame test, the pool's P10, the `portable` arm, nine firmware plants and three for portable C; the load gate's pin control; the rows' 123 controls and five harness mutants)
- [x] Required local verification bar passes (the full pass at this head, every gate rc 0 but the flip check, which exits 1 by design)
- [ ] Self-test evidence is posted in a PR comment
- [ ] No undocumented requirement or interface change remains (the 8x8/2if flip, round 16's margin there and the tier bounds await #890 and the owner; 1x1/1if's R4 misses tier 1, a finding; the pin move owes the 8x8/2if ledger more bytes)
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed (`mbx.h`'s record contract, `aecp.h`'s fan port, the firmware, AECP and platform READMEs, the harness README, section 13: both columns held, the rows by every source, the re-grade)
- [ ] Post-merge containment will be checked before the Issue moves to Done

