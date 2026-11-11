[A683zj]

## Contents

- **[Status](#status)** — REVIEW READY at the head below, the lane split as the round 27 ruling's item 4 directs: 1x1/1if's long-window load (0.450 with tsn-c-stack#32) is held for merge; 8x8/2if (0.815 at the pin, 0.719 with tsn-c-stack#32) moves to a flip check that fails at this head; #882's harness fix is in, and the baseline it leaves moves no stated cost.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — Round 27 item by item (#882, the cut, the split); round 26's cuts; what holds at this head; where the round histories went.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Checkout, submodules and environment.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What is left, and the decisions for the owner.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

REVIEW READY at `e7e2b7444a9859b058deff0d9edb575f2fb1946f`, two commits on round 26's head `0b37f3d2` (`665-s2b-cycles` -> `dev-soft-core`). No merge, no rebase, no force, no amend. No firmware, RTL, mailbox contract, donor or submodule change in round 27.

The round 27 ruling (#665 issuecomment-6788828284) is S2b's last load round: #882 first, its re-measure the baseline; one cut of SRP's record if the baseline gap at 8x8/2if is at most 0.03; the full gate pass; then REVIEW READY if both points are at or under 0.70, the lane split if only 8x8/2if is over, STOP if 1x1/1if is.

- **1x1/1if: 0.450** with tsn-c-stack#32 (0.463 at the pin), held for merge by `load_grade.py --check`, which exits 0.
- **8x8/2if: 0.815 at the pin**, held by the flip check, `flip_grade.py --check`, which exits 1 at this head (0.719 with tsn-c-stack#32, the column graded until round 27). The flip at 8x8/2if waits on the flip-gate issue the manager opens.
- 32x32/2if, reported: the more-compute image, #872: 1.659 (2.150 at the pin), 2.37x the compute for 0.70.

The ruling's tripwire (item 5) fires: S2b's load work ends here. The full gate pass ran once, on clean clones of this head, every gate rc 0 but the flip check, which exits 1 by design ([How to validate](#how-to-validate)).

## Linked Issue / roles

Relates to #665
Relates to #882 (its three acceptance items are met here; [Round 27](#round-27))

Executor: `[A683zj]`
Internal cleared-context reviewer: `[R711]`
External reviewer: `[R712]`

## Description

### Round 27

**The ruling** (issuecomment-6788828284, on [A683zf]'s STOP at `0b37f3d2`, issuecomment-6788757307):

| Item | At this head |
|---|---|
| 1. #882 first | `e5baac61`. The CPU budget harness's `get_avb_info` row sent GET_AS_PATH (`0x0028`) with descriptor_index 9, which no image has, and timed its NO_SUCH_DESCRIPTOR as GET_AVB_INFO. It now sends GET_AVB_INFO (`0x0027`) on AVB_INTERFACE 0 with its four-byte command (IEEE 1722.1-2021 7.4.40.1; Milan v1.2 5.4.2.23). Every row that ends at a response states its command or message type and its status (`answers.py`; IEEE 1722.1-2021 Table 7-141 for AEM and MVU, Table 8-3 for ACMP), and the grader holds the probe's own response, the one answering its sequence_id, to both: another type or status is an unexpected response, which fails the run. A row that states a status other than SUCCESS is a refusal row, named `<row>, refused <status>`; the run refuses a row that states no response, or a refusal its row does not name. **SUCCESS is asserted in arm B** (`answering-ports`), whose observation ports answer; in arm A the test SoC's datapath is held idle, so the face block's window read finds no answer within its bound and GET_AVB_INFO answers ENTITY_MISBEHAVING, a named refusal (GET_COUNTERS is the same case, and was measured as an unnamed refusal before). Arm B's `aecp` group is now one of the load gate's legs at both points. The other refusal rows: PROBE_TX (TALKER_DEST_MAC_FAIL: the source has no stream destination in that group, Milan v1.2 Tables 5.42 and 5.43), GET_TX_CONNECTION (NOT_SUPPORTED, Milan v1.2 5.5.4.4, Table 5.48) and the unknown AEM command (NOT_IMPLEMENTED). Eighteen self-test checks and ten mutants, among them the plant restoring the refused command, caught |
| The baseline | On unchanged firmware, each of round 26's legs rebuilt byte-identical to its build (objcopy and ELF), its sample log byte-identical; the `aecp` group run again in arm A, in arm B and with tsn-c-stack#32 at both points; every other recorded group regraded under the new checks. 0 refusals; the tallies round 26's (8x8/2if: 93 groups, 6 misses of 996 probe instances, 3 of 136 paths, the three egress-held paths, tsn-c-stack#26; 1x1/1if: 94, 6 of 945, 3 of 87; the notice arm 0 of 736 and 0 of 280; no pass over the share); the `aecp` group's heaviest AECP record 21,201 cycles at 8x8/2if (arm B) and 15,838 at 1x1/1if, under the AECP record's stated 265 and 205 us. The figures that changed (#882's item 3), each a row's time on interface 0: at 8x8/2if `get_avb_info` 0.338 ms in arm A, refused ENTITY_MISBEHAVING (0.316 as GET_AS_PATH before), and 0.341 ms in arm B, SUCCESS; `get_counters` 0.255 in arm A, refused as before, and 0.284 in arm B; at 1x1/1if `get_avb_info` 0.118 in arm A (0.095 before) and 0.143 in arm B; the costs' notice instance counts (35 to 41 at 8x8/2if, 29 to 32 at 1x1/1if, arm B's notices), and the 1x1/1if ADP event with tsn-c-stack#32 measured 9,482 cycles (9,940 before), under the 110 us its column states. **No stated cost moves**, so the load is round 26's |
| 2. One cut | The gap at 8x8/2if, 0.019, is under 0.03. The cut, of this tree's share of SRP's record: the record path's StreamID and MAC comparisons with their last byte compared where they are called, `same` only on a match; a sink's `capture` only where its kind was or is one; `ctrl_mem.c`'s `memcmp` four bytes a turn where the two alignments differ. **Measured on a scratch image and not committed.** On the same groups at 8x8/2if the heaviest SRP record went from 34,361 to 33,741 cycles (the `answering-every-port` arm's `notice-every-3`) and from 33,260 to 33,251 in arm A (`backlog-owed`): stated 365 to about 355 us, 8x8/2if about 0.713 with tsn-c-stack#32 and 0.809 at the pin, over 0.70 either way; closing it takes the heaviest record to 31,428. The cut takes about as much from the second heaviest record as from the heaviest, so the heaviest's excess of some 11,000 cycles is not in its reach; and it adds 152 B at the pin and 160 B with tsn-c-stack#32, which takes arm A's image with tsn-c-stack#32 over the 8x8/2if ledger (122,936 B in 122,880), so the graded column's leg would not build; the pin move that carries tsn-c-stack#32 would meet the same ledger. The same image moved the heaviest work pass of those groups by -15,987 to +2,056 cycles. With no firmware change there is no firmware mutant |
| 3. The gate pass | The full clean-clone pass at this head ([How to validate](#how-to-validate)) |
| 4. The outcome | 8x8/2if over and 1x1/1if under: the lane splits. `load_grade.py --check` holds 1x1/1if for merge (`load_grade.CEILING`). 8x8/2if is held by `flip_grade.py`, a separately invoked check that reads the pin's column (`load_grade.STATED_US`) through `load_grade.load`: `--check` exits 1 at this head, `OVER 8x8/2if: the load 0.815 at the pin is over the flip ceiling 0.70`; `--selftest` refuses all six of its controls, the over-ceiling row among them, and four more mutants hold the split in the harness self-test. The flip-gate issue is the manager's to open |
| 5. Tripwire | Fires. The memo's figures: the baseline 0.719 with tsn-c-stack#32 and 0.815 at the pin; after the cut about 0.713 and 0.809; the movement between images on the same groups, the heaviest work pass -15,987 to +2,056 cycles |
| 6. The donor | tsn-c-stack, lwSRP and the donor clone untouched; the graded column's legs apply round 26's port of tsn-c-stack#32 in a scratch build, byte-identical to round 26's image. The flip check reads the pin, `70936b77` here. tsn-c-stack#34 (tsn-c-stack#32) merged on the stack's `main` at `715589c` during this round, by its own review; the pin move is its own lane |
| 7. S9 (#870) | Its `KL_mbx` round had not landed by the measurement (its round 3 posted REVIEW READY afterwards and is in review): the grade uses the harness's own access cycles, and the flip-gate issue carries #870's |

**The load at this head** (`load_grade.py --check`, `flip_grade.py --check`):

| Point | Load at the pin | Load with tsn-c-stack#32 | Held by | Compute for 0.70 | Its three largest terms |
|---|---:|---:|---|---:|---|
| 1x1/1if | 0.463 | 0.450 | the load gate, 0.70, for merge | 1.00x | SRP's channel 0.150, ACMP's records 0.053, the TICK's consumers 0.047 (graded) |
| 8x8/2if | **0.815** | 0.719 | the flip check, 0.70 at the pin | 1.16x at the pin | SRP's channel 0.219, ACMP's records 0.088, ACMP's owed frame 0.070 (at the pin) |
| 32x32/2if | 2.150 | 1.659 | reported: the more-compute image, #872 | 2.37x | SRP's channel 0.519, owed MRPDUs 0.299, THE TRANSMIT's builds 0.150 (graded) |

**Three findings** (none changed here; for new issues): the firmware keeps 14 bits of AEM command_type (`aecp.c:428`, `& 0x3fff`), so `0x7FF0` is answered NOT_IMPLEMENTED under `0x3FF0` (the harness's unknown command is `0x3FF0`, a reserved value under `0x4000`, until it is fixed); no arm measures GET_AVB_INFO, GET_COUNTERS or GET_STREAM_INFO with their window reads answered (arm A's are refused at the window's bound, arm B's stubs read no window); and no row measures a talker's PROBE_TX answered SUCCESS.

### Round 26 (the cuts, at `0b37f3d2`; unchanged by round 27)

**The ruling** (issuecomment-6779973927, on [A683ze]'s STOP at `3a1d14c2`, issuecomment-6778599191): the 8x8/2if load was 0.747 with tsn-c-stack#32 graded, against the 0.70 ceiling, and round 26 closes the 0.047 with firmware cost cuts, the mailbox contract unchanged: (1) the donor merged with `main` and re-graded; (2) AECP's owed frame, a notice to 32 recipients, cut per recipient; (3) SRP's record cut the same way; (4) the exit, both held points at most 0.70 with the margin stated; (5) STOP otherwise, with what closes the gap and its cost; (6) the 32x32/2if row labelled "the more-compute image, #872".

| Item | At this head |
|---|---|
| 1. The donor | tsn-c-stack's `main` (`9deb0dd`, tsn-c-stack#33 with the tsn-c-stack#31 mask work) merged into `32-acmp-dirty-walk` by a merge commit, `dd8b026f`, and `9043b926` on it, not pushed (`DONOR-HANDOFF.md`, `DONOR-PR-BODY.md` with the keyword line for tsn-c-stack#32). The one source conflict is the release loop: tsn-c-stack#31 reads each sink's word of the mask, tsn-c-stack#32 marks only the released sinks; both now. `9043b926` restores both parents' plant orders, which the merge's table had put out of the order the entity self-test reads. On a clean clone of `9043b926`: the stack's CI steps rc 0 on Linux (28 of 28 gates, the campaign 470 caught, 0 escaped) and bare-metal; the differential test passes at 1, 8, 32 and 33 sinks; the host benchmark at 32 sinks 2,294 to 279 cycles at -O2. The merged head's change ported to this tree's pin is byte-identical to round 25's port, so the graded column is the merged head's; this round measures it again on this round's image |
| 2. AECP's owed frame | `46069672`, `f19c32d9`. A notice to the registered controllers is built once and each recipient's frame only addressed: its destination MAC, its interface's source MAC, its `controller_entity_id` and its `sequence_id` stored byte by byte from the registration (`aecp.c`, `address`; IEEE 1722.1-2021 7.5.2 and 9.3; Milan v1.2 5.4.5.1 sets the recipients), the walk stepping through each interface's used registrations by their mask (`fan_out`). A recipient 805 to 639 cycles at 8x8/2if; the heaviest notice 340 to 270 us there, 225 to 210 at 1x1/1if. Two firmware tests (each recipient's fields, interface and sequence across both interfaces, the asker and a freed registration left out, a notice stopped by backpressure and resumed; the same through the fan port's alternating frames) and eight plants in the AECP campaign, all caught. The cost control `notice-fan-out-as-it-was` (the old fan-out, verbatim) fails the harness's AECP item at the head |
| 3. SRP's record | `61fef2bb`, `f19c32d9`. StreamID and MAC equality on SRP's record path (the receive filter, the indications, the registrar walk) by `same`, from the last byte, not `memcmp` (one talker's StreamIDs differ in their unique ID, IEEE 802.1Q-2018 35.2.2.8.2); a pool block's link read and written in place. The heaviest SRP record 405 to 365 us at 8x8/2if (the `answering-every-port` arm's; arm A's with tsn-c-stack#32 350 us), 250 at 1x1/1if, unchanged (the arm's 23,645 cycles round to it). The retained retry's rule is unchanged and stated at the record's cost. A firmware test (a Listener whose StreamID differs from a source's in its first byte alone, or its last) and three plants, caught at both interface counts, and two existing plants re-anchored on `same`. A new harness check holds each SRP record's own apply to its retry's stated cost (`poll_grade.RECORD`), and the cost control `srp-compared-by-memcmp` fails it at the head |
| 4. The exit | Not met: 0.719 at 8x8/2if (below) |
| 5. STOP | Fires; what closes it is below |
| 6. The 32x32/2if row | Labelled "reported: the more-compute image, #872" (`load_grade.PENDING`, decision D, issuecomment-6759183115). Its row is round 25's, not measured again: 1.659 with tsn-c-stack#32, 2.37x the compute for 0.70, the factor #872 takes |

**How the costs were measured.** The harness now traces each pass's parts (`poll_items.PART_SPANS`), so the gate's own legs are the measurement: every group of arm A and of the `answering-every-port` arm at 1x1/1if and 8x8/2if, and arm A's groups but the save windows with tsn-c-stack#32 applied at the pin in a scratch build. The three costs the cuts move (an SRP record, its retained retry, a notice) are this measurement; every other cost is the larger of it and the committed table's, and in the donor's column also the committed donor column's. `poll_grade.STATED_US` takes the AECP item (210 and 270 us) and the retained item (250 and 365 us) from the same legs, so every measured pass is held to them.

**The load at this head** (`load_grade.py --check`):

| Point | Load at the pin | Load with tsn-c-stack#32 (graded, owed to the pin move) | Ceiling | Compute for 0.70 | Its three largest graded terms | A pass's own cost, us |
|---|---:|---:|---:|---:|---|---:|
| 1x1/1if | 0.463 | 0.450 | 0.70 | 1.00x | SRP's channel 0.150, ACMP's records 0.053, the TICK's consumers 0.047 | 180 |
| 8x8/2if | 0.815 | **0.719** | 0.70 | 1.03x | SRP's channel 0.219, AECP's owed frame 0.062, ACMP's records 0.061 | 275 |
| 32x32/2if | 2.150 | 1.659 | reported: the more-compute image, #872 | 2.37x | SRP's channel 0.519, owed MRPDUs 0.299, THE TRANSMIT's builds 0.150 | 590 |

At 8x8/2if the cuts take SRP's channel from 0.243 to 0.219 and AECP's owed frame from 0.076 to 0.062; the TICK's consumers rise 0.007 (the first finding below).

**What closes 8x8/2if** (0.719 against 0.70, 0.019 to find), each option alone, by the gate's own terms:

| Option | Change | Burst and sustained rate it implies |
|---|---|---|
| SRP's refill | 2 to 2.19 ms | burst 32 records unchanged; sustained 500 to 457 records a second |
| AECP's refill | 5 to 6.09 ms | burst 16; 200 to 164 a second |
| ACMP's refill | 5 to 6.91 ms | burst 16; 200 to 145 a second |
| ADP's refill | 10 to 18.9 ms | burst 8; 100 to 53 a second |
| MAAP's refill | none reaches 0.70 alone | |
| Compute | 1.03x | |
| An SRP record, its retry with it | 365 to 333 us (-8.7 %) | 2,628 cycles of the arm's heaviest record (34,361), whose code is lwSRP's for 19,511 and this tree's for 14,850: 18 % of this tree's share |
| A notice to 32 recipients | 270 to 175 us (-35 %) | a recipient's floor is about 640 cycles whatever the mailbox driver's record path (measured: 630 to 654) |
| An ACMP record | 305 to 210 us (-31 %) | |

A third cut of this tree's share of the SRP record (SRP's adapter 7,725 cycles, the copies, fills and compares in `ctrl_mem.c` 5,509, the pool 1,518) could close it alone, but at no margin: each new image moves a measured worst case by up to 7,620 cycles (the findings below). lwSRP's 19,511 are a donor change, as tsn-c-stack#32 was.

**Two findings** (both found by the legs and placed with `3a1d14c2`'s image, rebuilt byte for byte and run on this round's harness):

1. **A centisecond's consumers** measured 48,549 cycles at 8x8/2if (`notice-every-1`, four of lwSRP's periodic-transmission timers in one centisecond) against 41,816 for `3a1d14c2`'s image in the same group, which is round 25's own figure. The pass that holds it runs fewer instructions and more cycles at this image, in code the cuts do not change (lwSRP's `mrp_mad` +2,983, the copies +3,339); no data symbol moved, and 362 of 448 functions moved by -188 to +312 B. The table states 510 us (440 before), 0.007 of the load.
2. **The heaviest 8x8/2if work pass** is 193,609 cycles (`backlog`), 6,391 under the 2.0 ms share and **99 cycles short of the 6,490 round 16 asks of every pass class** (issuecomment-6634982529, item 2). `3a1d14c2`'s image gives 185,989 there, a different pass: the cuts move what coincides in a pass, and the same group's heaviest moved 7,620 cycles, more than the swing the margin assumes. No pass is over the share. 1x1/1if's heaviest is 158,176, 41,824 under.

The SRP and AECP passes' costs at this head are in section 13 of `docs/design/SPLIT_CONTROL_MEMORY.md`, with the trace of the arm's heaviest SRP record and both findings.

### What holds at this head

The acceptance of this lane's assignment (S2b, #665: the split firmware within T_svc, cycle work in firmware, owner decision D4 a), read at this head:

- **The rows by measurement** (the CPU budget harness, every group of arm A and of the `answering-every-port` arm, and arm B's `aecp` group, at 1x1/1if and 8x8/2if): every row is within its bound except the three egress-held paths (`backlog.owed`, `backlog.owed_behind0` to `3`, `backlog-owed.service.aecp.last`, tsn-c-stack#26): 6 misses of 996 probe instances in 93 groups at 8x8/2if, and of 945 in 94 groups at 1x1/1if. 0 refusals, no `STATED` line, and every row's response the one it states. The `answering-every-port` arm: 16 groups at each point, 0 misses of 736 and 280 probe instances, every queued notice within its bound. Arm B's `aecp` group: 0 misses of 39 and 25.
- **The pass share** (2.0 ms): 0 of 264,961 work passes over it at 8x8/2if and 0 of 178,192 at 1x1/1if; 0 of 14,133 and 0 of 21,631 in the `answering-every-port` arm. The heaviest at 8x8/2if is 193,609 cycles (`backlog`), 99 cycles short of round 16's margin (round 26's second finding, unchanged).
- **The bounds that hold by construction:** the first queued notice, 22 ms at 8x8/2if and 16 ms at 1x1/1if (THE RETRY's search); the last queued notice at 1x1/1if, 22 ms within its 25 ms ceiling; every pass's polls base and each heavy item within its stated cost (`poll_grade.py`), each SRP record's own apply within its retry's, every round within its own (`round_grade.py`), and every pass given whole to a build or an aged step within its own (`whole_grade.py`), each a gate over every group at both points.
- **The long-window load:** 1x1/1if within its ceiling, held for merge; 8x8/2if over it, held by the flip check.
- **What does not hold:** R4, R5 and R6 by every source at either point, the last queued notice at 8x8/2if (74 ms against 70 at THE DRAIN's derived pass count), every row at 32x32/2if, the long-window load at 8x8/2if, and round 16's margin on the heaviest 8x8/2if pass. Round 23's tier design waits for a load under the ceiling.

### The round histories

Rounds 12 to 25's Description sections, and the decisions their Known limitations listed, are in the evidence packet `evidence/ROUND-HISTORIES.md` (round 26's, carried unchanged).

## Authoritative references

- The round 27 ruling (#665 issuecomment-6788828284) and [A683zf]'s STOP it answers (issuecomment-6788757307); #882 and its three acceptance items.
- IEEE 1722.1-2021 7.4.40 and 7.4.40.1 (GET_AVB_INFO, `0x0027`), 7.4.41 (GET_AS_PATH, `0x0028`), Table 7-126 (AEM command_type), Table 7-141 (AEM status codes), 9.2.1.2 (the AEM AECPDU), Table 8-1 and Table 8-3 (ACMP message types and status codes); Milan v1.2 5.4.2.23 and 5.4.2.24, 5.4.3.1 (MVU) and Table 5.19, 5.5.4.4 and Table 5.48 (GET_TX_CONNECTION), Tables 5.42 and 5.43 (PROBE_TX's answer).
- The round 26 ruling (#665 issuecomment-6779973927) and [A683ze]'s STOP it answers (issuecomment-6778599191); decision D (issuecomment-6759183115 and issuecomment-6759193032); kebag-logic/tsn-c-stack#32, and tsn-c-stack#28 and tsn-c-stack#31, which the same pin move carries.
- IEEE 1722.1-2021 7.5.2 and 9.3 (the AECP frame and its unsolicited notification); Milan v1.2 5.3.4.2 and 5.4.5.1 (at most 16 registered controllers an AVB interface, each notified), 5.4.5.2 and Table 5.22 (COUNTERS_CHANGED and its holdoff), 5.4.5.3 (the registration probe's 250 ms retry).
- IEEE 802.1Q-2018 35.2.2.8.2 (a StreamID: the talker's MAC and a unique ID), clause 10 for lwSRP's participant (10.7.4.1 and Table 10-7, JoinTime); Milan v1.2 Table 4.3.
- The round 16 ruling (issuecomment-6634982529, item 2: every pass class at least 6,490 cycles under the share); the round 25 ruling (issuecomment-6751196896) and the earlier rulings, where round 26 leaves them.
- The protocol timers the arrival bounds cite: Milan v1.2 5.5.2.3 and Table 5.26, 5.6.3.5.3, 5.6.3.5.9 and Table 5.50, 5.6.4.1; IEEE 1722.1-2021 6.2.2.5; IEEE 1722-2016 B.3.4.2 and Table B.8; IEEE 802.1AS-2011 (+Cor1/Cor2) 10.7.2.2, 10.7.3.2 and 11.5.2.2, the edition Milan v1.2 profiles.
- `sw/mailbox/mailbox.yaml`, each channel's `rate` and `tick_ms`; `docs/design/SPLIT_CONTROL_MEMORY.md` section 5 (the ledger), section 13 (the polls by source, the long-window load, the two cuts) and section 14 (the 32x32/2if costs); `tb/verilator/ctrl_service_budget/README.md`; `sw/firmware/ctrl/srp/README.md` and `sw/firmware/ctrl/aecp/README.md`.
- `docs/reference/FR_NFR.md` 3.4.1 and 3.4.2; `sw/firmware/ctrl/loop/ctrl_loop.h` (THE SHARE, THE STEP, THE RETRY, THE TRANSMIT, THE TICK's cap); `sw/firmware/ctrl/aecp/aecp.h`.
- The earlier rounds' rulings and decisions are cited in `evidence/ROUND-HISTORIES.md`.

## How to get into the same state

```sh
git fetch origin
git checkout e7e2b7444a9859b058deff0d9edb575f2fb1946f
git submodule update --init protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack third_party/verilog-axis
```

The harness's prerequisites are in `tb/verilator/ctrl_service_budget/README.md`: the product LiteX tree, the pinned RV32 SDK and Verilator, with `COURSIER_MODE=offline` and `SBT_OPTS=-Dsbt.offline=true`.

## How to validate

```sh
python3 -B tb/verilator/ctrl_service_budget/load_grade.py --check
python3 -B tb/verilator/ctrl_service_budget/load_grade.py --selftest
python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --selftest
python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check
python3 -B tb/verilator/ctrl_service_budget/run.py --self-test
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir /tmp/budget-8x8 --record-budget-findings --record-share-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir /tmp/budget-1x1 --record-budget-findings --record-share-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir /tmp/budget-8x8-ports --variant answering-ports --groups aecp --record-budget-findings --record-share-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir /tmp/budget-8x8-notice --variant answering-every-port --record-budget-findings --record-share-findings
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 0/4
```

Expected result at this head:
- `load_grade.py --check` prints the load table and exits 0 (`RESULT: PASS`): 1x1/1if at 0.450 against 0.70; the 8x8/2if row's ceiling reads "the flip check, 0.70 at the pin". `--selftest`: `load gate: 23 of 23 planted controls refused`.
- `flip_grade.py --selftest` exits 0, `flip check: 6 of 6 planted controls refused`. `flip_grade.py --check` exits 1 by design, `OVER 8x8/2if: the load 0.815 at the pin is over the flip ceiling 0.70`: it is no merge gate.
- The harness self-test reports 0 failures, the rows' eighteen checks and fourteen new mutants among them.
- The 8x8 and 1x1 runs: 0 refusals, no pass over the share, no `STATED` line, every row's response the one it states, every row within its bound but the three egress-held paths. Arm B's `aecp` group: GET_AVB_INFO and GET_COUNTERS SUCCESS, 0 refusals.

The evidence at this head, each on a clean clone of it, never piped:

- **Every `run:` step of the four workflows a pull request to `dev-soft-core` triggers**, each job on its own fresh clone: 139 steps ran, every one rc 0; 226 are not run, each with its reason (hosted orchestration, artifact upload and collection, apt and sudo installs whose pinned tools this host carries, `physical-gptp`, which runs only on a schedule, and `rtl.yml`'s `verilator-shards` suites, which run here as the full sweep below); 0 steps without either.
  - `rtl-fast.yml`, all 14 jobs: `changes`, `verilator-lint`, `bdd-conformance` (508 scenarios and 2,330 steps passed), `yosys-tool`, `yosys-elaboration`, `publication-census`, `split-cdc`, `rtl-fast`; `firmware-unit` (`test_ctrl_firmware.py --require-rv32 --self-test` PASS, the saved-state store gate's 455 tests, `fw_coverage.py --check` PASS over 38 files); `firmware-control-mutants` (672 of 672 caught), `firmware-aecp-mutants` (220 arms `[ok]`), `firmware-srp-mutants` (340 `[ok]`); `firmware-boundary` and `firmware-verilator` (`ctrl_boundary: PASS`, 0 findings).
  - `rtl.yml`: `full-ci-gate`, `yosys-tool`, `yosys-shards` 0/4 to 3/4.
  - `elaborate.yml`: `elaborate-gates-0`, `elaborate-gates-1`, `elaborate`.
  - `docs.yml`: `wire-accountability`, `docs-check-no-git` (its three steps rc 0; the job removes `.git`, so the runner's own tree check after it cannot run), `docs-gates-0` (43 steps), `docs-gates-1`, `docs-gates-2`, `docs-check`.
- **The full sweep**, `scripts/run_all_suites.sh` as four shard units on clean clones: 65 suites, 65 passed, 0 failed, 0 timed out, 2,613,726 checks, 0 in-suite failures; every shard's preflight PASS (suite cancellation among them), so no re-run.
- **The lane's own gates** on a clean clone: `git diff --check` against the merge base `1d6bf555` and against round 26's head; `check_py_idiom.py`, `check_cpp_idiom.py`, `check_baremetal_only.py --check`, `docs_check.py` (0 findings); `ctrl_hot.py --self-test` and `--check`; the harness self-test (`self-test: 0 failures`, the rows' eighteen checks and fourteen new mutants caught); `load_grade.py --selftest` (23 of 23) and `--check` (PASS); `flip_grade.py --selftest` (6 of 6) and `--check` (exits 1: `OVER 8x8/2if: the load 0.815 at the pin is over the flip ceiling 0.70`); `ctrl_service_hooks` (28 of 28 checks, 96 of 96 mutants) and `nvm_split_target` self-tests; `test_ctrl_nvm.py --require-rv32 --self-test` (121 planted defects reddened); `gen_mailbox.py --check --crosscheck` and `--selftest`; `lint_rtl.py --check`; `test_soc_options.py`; `test_ctrl_memory.py`; `test_builder.py --require-rv32` (every gate passes; the same two arms as round 14's do not run, each with the tool's reason); `ctrl_split_boot` at 1x1 and 8x8 (PASS, 0 findings), its native controls (6 of 6) and its plants (3 of 3, and 8 of 8 placement controls); `cd tests && behave` (508 scenarios, 2,330 steps passed); `make -C tb/verilator/milan_dp twin` (0 findings). The clone's tree is clean after them.
- **The harness at both points**: every recorded group of arm A, of the `answering-every-port` arm and arm B's `aecp` group at 1x1/1if and 8x8/2if, regraded at this head from builds that resolve every recorded input unchanged here: 0 refusals; 6 misses of 996 probe instances (3 of 136 paths) at 8x8/2if and of 945 (3 of 87) at 1x1/1if, the three egress-held paths; 0 of 264,961 and 0 of 178,192 work passes over the share; the notice arm 0 of 736 and 0 of 280; arm B 0 of 39 and 0 of 25.

## Known limitations / out of scope

- **Round 27's decisions, for the owner and the manager:**
  1. **8x8/2if waits on the flip check** (0.815 at the pin, 0.719 with tsn-c-stack#32); the flip-gate issue carries it, with the options the ruling's item 5 names (a flip ceiling, a per-source refill, compute, #872 early, or an lwSRP donor cut, 57 % of the heaviest SRP record's cycles) and #870's access cycles.
  2. **The cut was measured and not committed** ([Round 27](#round-27), item 2): it reaches about 0.713 and does not fit the 8x8/2if ledger with tsn-c-stack#32; there is no firmware change and so no firmware mutant this round. That is a deviation from item 2, which asks for the cut's mutant, and the manager's to accept or overturn: committing the cut would put the pin move's 8x8/2if arm A image over its ledger for about 0.006 of load.
  3. **SUCCESS for GET_AVB_INFO is asserted in arm B**, the arm whose observation ports answer; arm A, the image as linked, states the face's refusal. No arm measures the face's window reads answered.
  4. **AEM command_type at or above `0x4000`** is answered under another command_type (`aecp.c` keeps 14 bits), a firmware finding for its own issue.
  5. **PROBE_TX's SUCCESS** is measured by no row: `acmp-cmd`'s source has no stream destination.
- **Round 26's decisions, for the owner** ([Round 26](#round-26-the-cuts-at-0b37f3d2-unchanged-by-round-27)), where round 27 leaves them:
  1. **8x8/2if is 0.019 over 0.70** after both cuts, graded with tsn-c-stack#32. Each alone closes it: SRP's refill 2 to 2.19 ms, AECP's 5 to 6.09 ms, ACMP's 5 to 6.91 ms or ADP's 10 to 18.9 ms (each burst unchanged); 1.03x the compute; or an SRP record 365 to 333 us, a notice 270 to 175 us or an ACMP record 305 to 210 us. The SRP record's code is 57 % lwSRP's.
  2. **Round 16's margin at 8x8/2if**: the heaviest work pass is 99 cycles short of 6,490 under the share at this head, and a group's heaviest moved 7,620 cycles between images on the same harness. Holding it by construction is round 16's own alternative, a per-pass record cap for the records class, or a margin restated from that swing.
  3. **A centisecond's consumers** at 8x8/2if rose to 510 us at this image in code the cuts do not change (stalls on the same work, not attributed further here).
  4. **32x32/2if** is reported, not gated: the more-compute image, #872 (decision D), 2.37x.
  5. **The pin move** that carries tsn-c-stack#28, tsn-c-stack#31 and tsn-c-stack#32 owes the 8x8/2if `answering-every-port` arm 204 bytes of `rom`: with tsn-c-stack#32 the arm's image is 123,084 bytes, past its 122,880-byte granule. The graded column's costs that only that arm stages are the pin's.
- **`AECP_NOTICE_US`** (365 us at two interfaces), the stated notice THE RETRY's rounds are sized by, is unchanged: the notice it covers is cheaper now (270 us measured), so it bounds it with more room; lowering it reopens the queued-notice bounds and their search.
- **`AECP_NOTICES_MOST`** caps the notices a datapath reset can leave pending at 40 at two interfaces whatever the shape, against 136 in the 32x32/2if model; the queued-notice bounds and their search are stated for 40 (#866).
- **A refused SRP record's give-up** past 1 s with a change pending waits at most the centisecond for the retry the change allows (`sw/firmware/ctrl/srp/README.md`).
- **No group stages** a retained record's retry, an owed MRPDU or a registration's probe: each is stated at the cost of the measured work that holds it (an SRP record, a build of one, a response).
- **The three egress-held rows** stay with tsn-c-stack#26.
- **The drafts** (lwSRP, tsn-c-stack) are measured staged and are not pinned here.
- **The platform image's hot list:** four entries name the size fixture's callbacks and place nothing in that image.
- **No fabric option outlives the switch-over:** nothing here adds one. The hybrid-XIP arm still misses T_svc on every path, so D3's rule stands.
- The earlier rounds' decisions for the owner and the manager are in `evidence/ROUND-HISTORIES.md`.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (#665 stays open: this lane is one part of it; #882's three items are met here)
- [x] New or changed behavior has self-checking tests (the rows' eighteen checks and ten mutants; the flip check's six controls and four mutants)
- [x] Required local verification bar passes (the full pass at this head, every gate rc 0 but the flip check, which exits 1 by design)
- [ ] Self-test evidence is posted in a PR comment
- [ ] No undocumented requirement or interface change remains (8x8/2if's flip, round 16's margin and the 32x32/2if image await the owner; the pin move owes the arm's 204 bytes)
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed (section 13: every row's response, the baseline, the cut, the split and the load at this head; the harness README: the rows' rule, the refusal rows, arm B's leg, the flip check)
- [ ] Post-merge containment will be checked before the Issue moves to Done
