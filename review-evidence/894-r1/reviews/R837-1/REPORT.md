[R837] NEGATIVE - exact head 12180198b087d4cfdd531d0de5d3753211b35616

# R837-1: internal independent review of PR #902 (issue #894, THE TIERS)

- Role: cleared-context internal reviewer, round R837-1.
- Exact head reviewed: `12180198b087d4cfdd531d0de5d3753211b35616`, tree `120938b3c677bc899acc258fbde163e7cba0688a`.
- Whole lane diff reviewed: `66f713267f201d1a00d7f711e04b3a996d804dee..12180198`, 12 commits, both rounds: round 1 (`04d3c1cc`, `f9442a10`, never reviewed before) and round 2 (`3f469cef`..`12180198`).
- PR #902: base `665-s2b-cycles` (stacked), not draft, open.
- Authority: #894's body, scope and acceptance. Also the STOP ruling (issuecomment-6813855717: the `aecp_ready` change under conditions (a)-(d), and the slice rule), the owner's option A (issuecomment-6814835849) and the round 3 ruling on F1 (issuecomment-6839847820).
- Requirement and interface sources: FR_NFR.md 3.4.1; IEEE 1722.1-2021 7.5.2, 9.3.5.2.6 and 9.3.5.4; Milan v1.2 4.3.2, 5.4.5.1 and 5.4.5.2; IEEE 802.1Q-2018 10.7.
- Public evidence: the author packet at `61a7204d` (`review-evidence/894-r1/author`), the REVIEW READY comment on #894 and the PR body. The PR body is byte-identical to the packet's `PR-BODY.md`.

## Verdict summary

The tiers in `ctrl_loop.c` are built as the ruling describes. The owed-notice queue meets conditions (a) to (d) for notices that fit its 128-byte slot. The resumed SRP build sends the frames of the build made whole. The slice rule reproduces 1,200 us. `flip_grade.py --check --point 1x1/1if` passes, the load is 0.470 at the pin, and every lane plant I re-ran was caught.

The verdict is still NEGATIVE, for two MAJOR findings:

- **R837-1-1.** The every-source R4 row assumes that every AECP command's notice fits the owed-notice slot. A legal command does not: ADD_AUDIO_MAPPINGS or REMOVE_AUDIO_MAPPINGS with 11 or more mappings. For such a burst, the lane's own tier model at the built slice and orders puts R4 at 20.70 ms, over tier 1's 20 ms.
- **R837-1-2.** A timer's MRPDU no longer holds FR_NFR 3.4.1's 20 ms by every source: it is 29.00 ms at 1x1/1if. The compile-time bound that held it was removed, and the requirement row was rewritten in-lane to "an open decision" that no ruling has taken.

There are also three MINOR documentation findings, one RESIDUE and two SUGGESTIONs.

## Findings

### R837-1-1 MAJOR - Conformance, RTL, Robustness, Tests - R4 by every source does not count notices longer than an owed-notice slot

**Artifacts**
- `sw/firmware/ctrl/aecp/aecp.h:249`: `AECP_OWED_BYTES 128u`.
- `sw/firmware/ctrl/aecp/aecp.c:390`: `owe()` refuses a response longer than a slot.
- `sw/firmware/ctrl/aecp/aecp.c:281-285`: `aecp_ready` is false while `notify` is set.
- `sw/firmware/ctrl/aecp/aecp_maps.c:220-224` and `:60-71`: ADD/REMOVE_AUDIO_MAPPINGS answer with a body of 8 + 8·count, count up to `AECP_MAP_PAGE` (176). Identical mappings in one command are accepted (`conflict()` is false for equal mappings).
- `tb/verilator/ctrl_service_budget/rows_tiers.py:587`: `BUILT = Design(0, 'aecp-first', 'srp-first', 'queue')` applies the queue rule to every record of R4's burst. No source or control in the model names `AECP_OWED_BYTES` or a notice longer than a slot.

**Authority and evidence**
- The issue's acceptance 1 requires every row by every source within its tier's bound. The STOP ruling built the 1x1/1if design on "AECP taking its next record while a command's notice is owed".
- The firmware keeps a notice longer than a slot in the response buffer and holds the next record behind it. The lane's own test shows this: `test_aecp.cpp:805-815`, `Queued.ALongerNoticeWaitsInTheResponseBufferBehindTheQueue`, uses a 12-mapping ADD_AUDIO_MAPPINGS (142 B > 128) and asserts `EXPECT_FALSE(aecp_ready(&a))`.
- How a 16-command burst of such commands is built: each command is 38 + 8 + 8·11 = 134 B or more, and ADD and REMOVE of one mapping alternate so that each changes state and notifies. That burst gets the rule before the queue (`--aecp notify`).
- The tier model, at the built slice and orders with that rule, gives R4 = **20.70 ms against 20 ms** (+0.70). The queue rule at the same settings gives 12.71 ms. The only change between the two runs is the AECP rule. Receipts: `receipts/rows-tiers-1x1-notify-rule-slice1200.txt`, `receipts/rows-tiers-1x1-queue-rule-slice1200.txt`, `receipts/rows-tiers-1x1-notify-rule-R4-terms.txt`.
- The 20.70 ms charges each long notice at the stated 210 us, a cost measured on notices of 128 B or less. The real figure is therefore no smaller.

**Impact**
- The flip check's 1x1/1if PASS (R4 12.71 ms) holds only for commands whose notices fit a slot. It does not hold by every source.
- The tier-1 bound can be exceeded by an admissible controller burst at the contract rate (16 records). The acceptance criterion this lane exists for is not shown.

**Required outcome**
Either:
- every notice a state-changing command can cause at 1x1/1if is taken by the owed-notice queue (for example, a slot sized to the longest notifying response at the point, or long notices queued another way), with R4 recomputed; or
- the every-source R4 counts the long-notice source and still fits 20 ms.

In both cases:
- `rows_tiers.py` gets a control that fails when the long-notice source is dropped;
- a firmware test drives a burst of long-notice commands.

**Verification**
- `flip_grade.py --check --point 1x1/1if` passes with the source counted.
- `rows_tiers.py --selftest` refuses the new control.
- The new firmware test fails on the current slot size, or on a planted defect that drops the long-notice path.

### R837-1-2 MAJOR - Conformance, Docs - a timer's MRPDU over FR_NFR 3.4.1's 20 ms by every source, the requirement rewritten to an undecided bound

**Artifacts**
- `docs/reference/FR_NFR.md:396` (the SRP/MRP row): before this lane it said every MRPDU a timer makes owed is "committed within 20 ms ... by construction (`CTRL_LOOP_SRP_MS`, `CTRL_LOOP_TX_MS`)". It now says "which bound holds it under the tiers is an open decision on #894". The row's third column still reads "The bound is T_svc; it fits each".
- `sw/firmware/ctrl/loop/ctrl_loop.c`: the lane deletes `_Static_assert(CTRL_LOOP_TX_MS <= CTRL_LOOP_T_SVC_MS, ...)`, and `ctrl_loop.h` deletes `CTRL_LOOP_TX_MS`.
- `tb/verilator/ctrl_service_budget/rows_tiers.py:464-467`: `TX_BOUND_MS`, `tx_row`, reported only.
- Mirrored in `sw/firmware/ctrl/srp/README.md:238` and in `docs/design/SPLIT_CONTROL_MEMORY.md` (the "THE TIERS" section and the "What is left" bullet).

**Authority and evidence**
- `receipts/flip_grade.py_--check_--point_1x1_1if.txt`: `tx (reported) | 29.00 | 20 | +9.00` with `RESULT: PASS`.
- The issue's scope says "The bounds (20, 90 and 125 ms) and the every-source rule are not changed in this lane".
- AGENTS.md section 2: an Issue cannot silently override a normative requirement, and a conflict is published and marked as needing a decision.
- The conflict is published (PR body "Open risks", REVIEW READY "The MRPDU row"). No ruling on #894 decides it:
  - 6813855717 rules the five rows and the slice;
  - 6814835849 rules the five rows at 1x1/1if and 8x8/2if's rows;
  - 6839847820 rules only on F1.
- By measurement the row holds (the MRPDU margin of 1.052 ms against 20 in the author's harness table). The owner's 2026-11-09 rule is that rows hold by every source, never by measurement alone. That rule was relaxed for 8x8/2if only.

**Impact**
- The head would land a design whose own every-source model puts a normative 20 ms row 9 ms over at the gated point.
- The requirement text that held it now defers to a decision that does not exist.
- AGENTS.md section 7 cannot be met while a requirement decision is open.

**Required outcome**
- A recorded maintainer or owner decision on #894 naming the bound a timer's MRPDU is held to under the tiers at 1x1/1if, and whether by every source or by measurement.
- FR_NFR 3.4.1's MRP row (all three columns), the srp README and SPLIT_CONTROL_MEMORY state exactly that decision.
- The flip check, or the named gate, holds the row to it.

**Verification**
- The decision is linked from FR_NFR.md:396.
- The named gate passes and refuses a plant over the ruled bound.

### R837-1-3 MINOR - Docs - the 1x1/1if slice stated as 1.05 ms in the mailbox split design

**Artifacts**
- `docs/design/MAILBOX_SPLIT.md:347`: "SRP's records in a slice from the pass's start (1.05 ms at 1x1/1if, 1.3 ms at 8x8/2if)".
- The code: `sw/firmware/ctrl/loop/ctrl_loop.h:268`, `CTRL_LOOP_SLICE_US (MBX_N_IF == 1u ? 1200u : 1300u)`.

**Evidence**
- The figure is the one the rule chose before the image under the tiers was measured again (SPLIT_CONTROL_MEMORY "THE TIERS": "at the datapath costs alone ... the rule picked 1,050 us").
- Commit `8cc3e5d3` moved the slice to 1,200 us. `ctrl_loop.h`, SPLIT_CONTROL_MEMORY, the harness README and the PR body say 1,200 us. This line was not updated.

**Impact:** an authoritative design document states the wrong tier-2 slice for the gated point.

**Required outcome:** MAILBOX_SPLIT.md:347 states 1.2 ms (or 1,200 us) at 1x1/1if.

**Verification:** `grep -n "1.05 ms" docs/design/MAILBOX_SPLIT.md` is empty, and the docs gates pass.

### R837-1-4 MINOR - Docs - 8x8/2if's rows and flip still called an open owner question after the owner decided them

**Artifacts**
- `docs/reference/FR_NFR.md:373` ("its rows by every source do not fit under the tiers, an owner question on #894").
- `docs/design/SPLIT_CONTROL_MEMORY.md:2046` ("an owner question on #894").
- `sw/firmware/ctrl/aecp/README.md:120` ("at 8x8/2if the stated figures are an owner question on #894").
- `sw/firmware/ctrl/aecp/aecp_mbx.h:40-41` ("its rows by every source do not fit, an owner question (#894)").
- `tb/verilator/ctrl_service_budget/flip_grade.py:15` ("8x8/2if's is an owner question (#894)").
- `tb/verilator/ctrl_service_budget/README.md:151` ("fails at 8x8/2if, an owner question on #894").

**Authority:** the owner decision of 2026-11-12 05:47 (#894 issuecomment-6814835849, option A):
- 8x8/2if's flip holds the long-window load at 0.75 (#890), plus a fresh measurement in which every row fits;
- 8x8/2if's rows by every source are reported, not gated, and owed to #872.

**Impact**
- The requirements document and its mirrors describe a decided requirement as undecided, and they do not state the rule that now governs 8x8/2if.
- F1 (the 8x8/2if ledger) is a different, genuinely open question. SPLIT_CONTROL_MEMORY.md:2184 about F1 is not part of this finding.

**Required outcome:** each listed line states the owner's decision with its link, in place of "an owner question".

**Verification:** grep of the six artifacts, and the docs gates.

### R837-1-5 MINOR - Docs - the Domain-adoption invariant (Milan v1.2 4.3.2) is stated where a sliced build does not hold it

**Artifacts**
- `sw/firmware/ctrl/srp/README.md:239`: "A Domain adopted in that call is sent in it, so no poll sees the new VID unlicensed between the adoption and its MVRP commit (Milan 4.3.2)".
- `sw/firmware/ctrl/srp/srp_mbx.c:1093-1094`, the same claim in the transmit client's comment.
- `sw/firmware/ctrl/loop/ctrl_loop.h:313`: `CTRL_LOOP_BUILD_MOST` is 1 at 8x8/2if.

**Evidence: reviewer probe** (`scripts/probe_srp_domain_slice.cpp`, `scripts/run_srp_probe.py`, `receipts/probe-srp-domain-slice.txt`, run at one and two interfaces)
- Scenario: a VID-moving Domain adoption with a licensed Talker.
- Built whole (2 MRPDUs a slice), no slice boundary falls between adoption and MVRP commit.
- Sliced at 1 MRPDU a slice, a slice ends with the MSRP sent, the MVRP owed and `vlan_sent` false (`gap=1`).
- In the fixture, no SRP poll ran in that gap (`polled=0`): the resumed slice followed as the next pass given whole.
- The licence changes were identical (1 revoke and 1 grant in each case), and the lane's byte comparison (`ABuildResumedAcrossSlicesSendsTheFramesOfTheBuildMadeWhole`) passes.
- With a tier-1 record held between the two slices, an ordinary pass and its polls can stand in the gap.

**Impact**
- A cited protocol invariant is stated unconditionally, but at 8x8/2if the loop does not hold it.
- I established no wire or licence divergence, so this finding is not a Conformance defect.

**Required outcome:** the README and comment state when the adoption and its MVRP share a slice (1x1/1if, `CTRL_LOOP_BUILD_MOST` 2) and what holds when they do not (8x8/2if). Alternatively, the build keeps an adoption's MVRP in the adoption's slice.

**Verification:** a test of a sliced adoption with an ordinary pass between the slices, asserting the stated property.

### R837-1-6 RESIDUE - Docs - new review-round identifiers in source comments

**Artifact:** `receipts/comment-rule-new-round-refs.txt`, 14 lines the lane adds in 9 non-Markdown files. Examples: `sw/firmware/ctrl/loop/ctrl_loop.h` (THE TIERS block and the `CTRL_LOOP_SLICE_US` comment), `sw/firmware/ctrl/aecp/aecp_mbx.h`, `sw/firmware/ctrl/srp/srp_mbx.c:1093`, and `rows_tiers.py` (5 lines). Each cites "#665 round 23".

**Authority:** owner rule of 2026-10-15. Source comments cite issue and requirement IDs and never review rounds. Existing instances are tracked by #746; these are new.

**Exact fix:** in each listed line, replace "#665 round 23" (and "round 23") with the issue and decision name only, for example "#665, option B (the two tiers)". The fix changes no code, figure or claim.

### R837-1-7 SUGGESTION - Tests - `least_margin` ranks a row with no solution above solved rows

- Artifact: `tb/verilator/ctrl_service_budget/rows_tiers.py:595-597`. A row with no W scores -1.0, which beats any solved row missing by more than its bound.
- Effect: at 8x8/2if, `slice_choice` returns 650 us (-2.07, the last queued notice unsolved), whereas the best fully solved slice is 1,250 us (-4.18) (`receipts/slice-rule-reproduction.txt`).
- It is used only at 1x1/1if (`rows_tiers.py:764`), where every grid slice solves, so the shipped choice is unaffected.
- Suggestion: rank an unsolved row below every solved one.

### R837-1-8 SUGGESTION - Tests - the owed-notice behave layer is an offline model

- Artifact: `tests/steps/aecp_owed_notice_steps.py`. Its rules are pinned to source strings and replayed by a Python model.
- Condition (d) is met by `Queued.*` in `test_aecp.cpp`, which runs the firmware.
- Suggestion: a scenario that drives the built firmware would keep the behave layer from merely restating the implementation.

## Prior public findings

- PR #902 carries no prior review findings at this head: 0 reviews, 0 review comments, and only the two review-start comments.
- Round 1's head `f9442a10` was never reviewed. I reviewed its two commits as part of the whole diff.
- On #894, F1 (the 8x8/2if size fixture over its 57.5 ledger) is the author's open risk, ruled OPEN at this head (issuecomment-6839847820). I did not grade it. I checked only its stated bytes against the author receipt `receipts/gates/harness-8x8-clean-head-build.txt`:
  - rom 123,544 B against the 58.0 plan's 124,928 B;
  - 664 B over a 57.5-RAMB36 rom of 122,880 B;
  - 1,104 B over the 122,440 B before the tiers.
  These are consistent with SPLIT_CONTROL_MEMORY.md:2184.
- F2 and F3 (8x8/2if) are measured, not gated, and not graded.

## Focus items checked

1. **THE TIERS** (`ctrl_loop.c:247-336`):
   - Tier 1 takes the first channel (AECP, `first_ch`) past `CTRL_LOOP_RX_PER_PASS` to `CTRL_LOOP_DRAIN_RECORDS` while the pass has spent at most `CTRL_LOOP_DRAIN_US`. The other tier-1 channels are served only once its take left none (`sweep = l->rx_left == 0u`).
   - SRP is served only when `tier1_done`, in a slice ending `start + CTRL_LOOP_SLICE_US - CTRL_LOOP_SRP_UNIT_US`.
   - Build and round run as tier-2 slices of a pass given whole. The round runs only once SRP is `drained`, except a queue's first notice (`round_one`/`retry_first`).
   - Mailbox reads: the ordinary pass's tier-1 test uses `rx_left`, which is set as the take runs (`service_rx`, `ctrl_loop.c:169`). `tier1_holds()` reads the rings only in the pass-given-whole decision after another pass given whole, with a tier-2 client bound, as HANDOFF.md:14 states. The ADP and ACMP access bounds (`ADP_MBX_LAT_*`, `ACMP_MBX_LAT_*`) pass in my firmware run.
   - Widths and wrap: `slice_end` and `round_of` use signed differences of `uint32_t`. In `reset_interface`, `(tx_resume - 1u) / 2u` with `tx_resume` 0 never equals an index. The owed-queue counts are 8-bit and guarded by `owed_slots > 0xffu`.
2. **The owed-notice queue and conditions (a)-(d)** (`aecp.c:281-285`, `owe` at `:388`, the record's turn at `:509`, `notices`/`transmit` at `:719-743`):
   - (a) The FIFO head is drained one notice per poll, each recipient's `sequence` is incremented per notice, and the requester is skipped.
   - (b) The response is sent in the record's turn (`transmit(a, false)` never drains the queue), and notices are sent only from the poll.
   - (c) `aecp_ready` is false while the queue is full. The model counts the depth (`rows_tiers.py:767-780`).
   - (d) `Queued.*` and the behave feature both pass (`receipts/behave-aecp-owed.txt`).
   - IEEE 1722.1-2021 9.3.5.4 and Milan v1.2 5.4.5.2 are read as the ruling reads them.
   - The scratch use of the response buffer in `fan_out` is safe: the queue drains only after `respond()` has sent it, and never while START is pending (`aecp_poll` returns earlier).
   - Gap: notices longer than a slot (R837-1-1).
3. **The resumed SRP build** (`srp_mbx.c:1098-1139, 894-895`):
   - `tx_resume` records the next participant, and the resumed slice skips the declarations already made, then makes them again for the interface. A reset clears a resume on its interface.
   - At 1x1/1if `CTRL_LOOP_BUILD_MOST` is 2, so no build is split.
   - The 802.1Q-2018 10.7 transmit opportunity is per participant, and MSRP and MVRP may leave in consecutive slices.
   - Milan 4.3.2: see R837-1-5.
4. **The slice rule**, reproduced by `scripts/slice_rule.py`, which computes the margin itself from `rows_tiers.rows()` (`receipts/slice-rule-reproduction.txt`):
   - On the stated 50 us grid at 1x1/1if: **1,200 us, least relative margin 0.2673, the last queued notice binding**. 1,050 us gives 0.2610 and 1,300 us gives 0.2650, matching the PR's figures.
   - On a 10 us grid the best is 1,170 us at 0.2675, a 0.0002 difference. The 50 us grid is stated in `ctrl_loop.h` and SPLIT_CONTROL_MEMORY.
   - At 8x8/2if the ruling chooses no slice, and 1,300 us is kept.
5. **Rows, load and costs:**
   - `flip_grade.py --check --point 1x1/1if` rc 0: R4 12.71, R5 54.59, R6 52.85, first 14.60, last 91.59, tx 29.00 (reported).
   - `--design as-built` rc 1. `flip_grade.py --check` (both points) rc 1, as stated.
   - `load_grade.py --check` rc 0: 0.470 at the pin, 0.457 with tsn-c-stack#32.
   - The cost rises in `load_grade.STATED_US` and `poll_grade.STATED_US` match the author's measured table (`author/receipts/measure/costs-8cc3e5d3-1x1.txt`: record.aecp 235, event.ADP 115, events_none 30, base 160). They are stated at the larger value.
   - The donor column keeps base 155 at 1x1/1if, because `base` is in `load_grade.WALK`, the costs #32 moves.
6. **Planted defects**, re-run on disposable copies (`scripts/run_lane_mutants.py`):
   - Loop tiers: 17 of 17 caught (`receipts/lane-mutants-ctrl.txt`).
   - Owed-queue and fan-out rows: 31 of 31 caught (`receipts/lane-mutants-aecp.txt`).
   - Resumed-build rows: 4 of 4 caught at two interfaces, the interface count the author's driver uses (`receipts/lane-mutants-srp.txt`).
   - At one interface, which the driver does not run for these rows, `build-reclaim-left-to-the-next-slice` escapes. At 1x1/1if no build is split, so this is noted, not filed.
   - `rows_tiers.py --selftest` refuses 509 of 509, `flip_grade.py --selftest` 319 of 319, and `load_grade.py --selftest` 24 of 24.
7. **The gate pass on 12180198** (author receipts):
   - `receipts/gates/lane-summary.txt`: every lane gate has the expected rc at the head.
   - `receipts/gates/dispatch.txt`: every job rc 0 except the expected refusal of the 8x8/2if clean build (F1).
   - The `elaborate-gates-1` gate_19 rerun is present: head 12180198, dirty 0, `LITEX_SIM_TIMEOUT=1800`, 8 of 8, rc 0.
   - The reruns of the three sweep suites killed by the wall clock are present: `milan_dp`, `milan_dp_gm_steps`, `milan_dp_render`, each head 12180198, dirty 0, make rc 0 and verdict rc 0, with log hashes.
   - The sweep shards record 0 in-suite failures.

## Reviewer-run evidence at this head

- `test_ctrl_firmware.py --require-rv32 --jobs 4`: PASS, 62 arm verdicts and 0 failures, including the port/loop, AECP core (132 checks at 1 and 2 interfaces), SRP and RV32 arms (`receipts/fw-suites.txt`).
- `behave features/aecp_owed_notices.feature`: 3 scenarios pass.
- `git diff --check 66f71326..12180198` is clean.
- Hosted: no check run, status or workflow run exists at this head (`receipts/hosted-evidence.txt`). Nothing hosted is claimed.
- Restoration:
  - The clone is at `12180198`, tree `120938b3`, and `git diff HEAD --quiet` holds.
  - The index is unchanged.
  - The gitlinks are unchanged: protocol-processor `a9e84b66`, gptp-processor `135afd04`, lwSRP `08ee86e8`, tsn-c-stack `70936b77`, verilog-axis `48ff7a7e`, external `efeb541a`.
  - Interpreter caches the session created in the clone were removed.
  - Every probe and plant ran on copies under the packet's scratch directory.

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R837-1-1, R837-1-2) | #894 acceptance 1-3 and rulings 6813855717, 6814835849 and 6839847820; FR_NFR.md:367-396; aecp.c conditions (a)-(d) against IEEE 1722.1-2021 7.5.2, 9.3.5.2.6 and 9.3.5.4 and Milan v1.2 5.4.5.1-5.4.5.2; srp_mbx.c transmit against 802.1Q-2018 10.7 and Milan 4.3.2; flip/load receipts | R837-1 | 12180198b087d4cfdd531d0de5d3753211b35616 |
| RTL | UNCLEAN (R837-1-1) | ctrl_loop.c:169-336 (tiers, slices, rx_left, holds, round_of, slice_end, whole_runs); ctrl_loop.h interface (`ctrl_transmit_fn` and its callers); aecp.c queue state and fan_out buffer use; srp_mbx.c:891-895 and 1098-1139; widths and wrap arithmetic | R837-1 | 12180198b087d4cfdd531d0de5d3753211b35616 |
| Robustness | UNCLEAN (R837-1-1) | long-notice commands (aecp_maps.c:220-224); queue full and zero slots; reset during a resumed build (srp_mbx.c:895, ABuildResumed… reset arm); no-clock paths; probe of a sliced Domain adoption | R837-1 | 12180198b087d4cfdd531d0de5d3753211b35616 |
| Tests | UNCLEAN (R837-1-1) | test_port_loop.cpp L22/L23/L26/L27 (`:1330`, `:1400`, `:1591`, `:1665`); test_aecp.cpp `Queued.*`; srp_mbx.cpp:1584; aecp_owed_mutants, loop_step_mutants.tier_mutants and srp_transmit_mutants re-run; rows_tiers, flip and load self-tests; slice reproduction; behave layer | R837-1 | 12180198b087d4cfdd531d0de5d3753211b35616 |
| Docs | UNCLEAN (R837-1-2, R837-1-3, R837-1-4, R837-1-5) | FR_NFR.md 3.4.1; SPLIT_CONTROL_MEMORY.md section 13 ("THE TIERS", "What is left"); MAILBOX_SPLIT.md:340-352; aecp/README.md:111-131; srp/README.md:230-245; ctrl_service_budget/README.md; PR body against the packet; source-comment rule scan | R837-1 | 12180198b087d4cfdd531d0de5d3753211b35616 |

## Real limits

- **Harness self-test.** I started a re-run of the CPU budget harness self-test (`run.py --self-test`). It was terminated from outside by signal 15 (rc 143) before its summary (`receipts/harness-selftest.txt`, partial). Up to that point it shows the `rows:` built-design plant caught. For this gate I rely on the author's receipt (`harness_selftest rc=0`).
- **Not rebuilt.** I did not rebuild or re-run the CPU budget harness legs at either point. The measured tables and image identities are the author's receipts.
- **Long notices not measured.** R837-1-1's 20.70 ms comes from the lane's own tier model with the AECP rule for long notices. The longer notice's own cost was not measured.
- **Not run by me:** the parent, PP, gPTP, Yosys and builder banks; the full control, AECP and SRP mutant campaigns (only the lane's rows); Docker/act; hosted contexts.
- **No hardware.** Physical calibration was not run. Field skips are not hardware proof.
- **Specification text.** IEEE and Milan clause readings are taken from the ruling's citations and the tree's requirement documents. No specification text was available here.

## Pending manager duties

- Validate the current-dev merge candidate (source base `66f71326`, live dev `b7d69295`) with the builder and native banks, and publish the receipts. Own the hosted and act acceptance. No hosted context has run at this head.
- Obtain the maintainer or owner decision R837-1-2 asks for, and the round 3 work on F1 (issuecomment-6839847820).
- Carry R837-1-6 to the residue checklist.
- Re-review the corrected head with every lens again. The findings above leave every lens unclean at `12180198`.

R837-1 FINISHED
