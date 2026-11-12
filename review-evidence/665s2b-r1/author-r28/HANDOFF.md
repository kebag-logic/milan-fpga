# [A683zm] #665 lane S2b, round 28 (HANDOFF)

**Status: REVIEW READY** at `66f713267f201d1a00d7f711e04b3a996d804dee` (`665-s2b-cycles`), five commits on round 27's `e7e2b7444a9859b058deff0d9edb575f2fb1946f`. No merge, rebase, force or amend; nothing pushed. No RTL, mailbox contract, donor or submodule change.

- Authority: the round 28 ruling (#665 issuecomment-6805157674), items 1 to 7.
- TAKEN: issuecomment-6805358380 (`TAKEN-COMMENT.md`), 2026-11-11 20:3x CET. REVIEW READY: issuecomment-6813034799 (`REVIEW-READY-COMMENT.md`), 2026-11-12 03:57 CET. Nothing else posted.

| Commit | Subject |
|---|---|
| `24ea9c04` | Put the firmware's compiler extensions behind one platform header with a portable C11 fallback, align the AECP response buffer with _Alignas, and hold both with a portable arm and its plants (#665) |
| `71e905fb` | Hold a TX record's commit to the move that record started, report a failed move for the record it carried, and resume a notice at the recipient whose frame was lost, with driver, fan-port and AECP tests and a planted defect for each rule (#665) |
| `5a19b0ca` | Hold 1x1/1if's long-window load at this tree's pin as well as with tsn-c-stack#32, hold each point's flip to decision D's tier bounds by every source in the flip check, and state the harness comments' issues and behaviour in place of comment IDs and round labels (#665) |
| `19f16f80` | Record the platform header and the files whose counts grew in the firmware coverage ratchet, through fw_coverage.py --write (#665) |
| `66f71326` | Restate two of 1x1/1if's costs with tsn-c-stack#32 from this round's legs, and state in section 13 the re-grade on this image, both columns held, the rows by every source the flip check holds and round 16's margin at 8x8/2if deferred to #890 (#665) |

## Contents

1. Outcome against the ruling
2. Changes (file:line, reason)
3. New checks, planted mutants and failing words
4. Measurement: the re-grade at both points
5. Gates
6. Findings, deviations and open questions
7. Run history

## 1. Outcome against the ruling

| Item | Outcome |
|---|---|
| 1. The merge gate at the pin | `5a19b0ca`. `load_grade.py --check` holds 1x1/1if at this tree's pin and with tsn-c-stack#32, each at most 0.70 (`COLUMNS`), names the column in each finding and prints `HELD 1x1/1if at the pin: the load 0.463, its ceiling 0.70` and `HELD 1x1/1if with tsn-c-stack#32: the load 0.450, its ceiling 0.70`. The control "a rise at the pin alone" (an ACMP record at 2,000 us in the pin's column only, the pin's load 0.807) is refused by name; `--selftest` 24 of 24. R711-6's `probe_1x1_column.py` and R712-6's `probe_pin_1x1.py` print the refusal (`receipts/gates/lane/probe_r711_1x1_column.log`, `probe_r712_pin_1x1.log`). Section 13 names both columns' margins |
| 2. Record commits | `71e905fb` (section 2): a TX record's commit judges only the move that record started; a failed move is reported for its record (`mbx_tx_commit` false, `mbx_tx_begin` LOST and nothing started); the fan port reports it for its frame; `fan_end` keeps its commit's result; the notice resumes at the recipient whose frame was lost, its sequence_id given back; `mbx.h` states it. Driver tests T4 and T5 (T2 extended), the AECP test, nine plants caught (section 3) |
| 3. Round 16's margin at 8x8/2if | Deferred to the 8x8/2if flip under #890 (the owner's decision of 2026-11-11 there sets that point's flip ceiling to 0.75), cited in section 13. 1x1/1if keeps it: this image's heaviest 1x1/1if work pass is 160,618 cycles (`backlog`), 39,382 under the share; at 8x8/2if 192,237 (`backlog`), 7,763 under, the margin met at this layout (`receipts/legs/heaviest-work-passes.txt`). `flip_grade.FLIP` stays 0.70: #890's decision makes the 0.75 a small change of its own after the pin move, with no change to this head |
| 4. Decision D's tier bounds | `5a19b0ca`. `flip_grade.py --check` holds the rows by every source (R4 20 ms, R5 and R6 90 ms, the first queued notice 20 and the last 125 ms) at 1x1/1if and 8x8/2if (`rows_grade.py`), `--point` for one; 129 self-test controls and five harness mutants. **1x1/1if (finding, not a STOP):** R4 73.02 ms against 20 (+53.02; SRP's records ahead of AECP's 16.50 ms, the other channels' records 10.96, the retained retries 9.00); R5 37.19 and R6 32.69 ms within 90; the first queued notice 20 ms within 20, the last 22 within 125. `--point 1x1/1if` exits 1 at this head. The proposed issue's text is `ROWS-FINDING.md`. 8x8/2if stays with #890: R4 489.97, R5 162.96, R6 149.57 ms, the first queued notice 22 against 20, the last 62 within 125 |
| 5. Portable C | `24ea9c04`. `_Alignas(64)` (C++ `alignas` for the tests); `CTRL_CC_NOINLINE` and `ctrl_cc_ptr_load`/`_store` behind `CTRL_CC_GNU` in `plat/ctrl_cc.h` with the portable fallback (`memcpy` for the link). `git grep __attribute__ -- sw/firmware/ctrl ':!*/test/*'` shows only that header (`receipts/gates/lane/attribute_grep.log`); the `portable` arm holds it. Image-neutral alone: 8x8/2if arm A's three images byte-identical to round 27's and the `control` log byte-identical (`receipts/item5/`) |
| 6. Docs and residue | R712-6 F3's sentence; the comment IDs and round labels of R711-6 RES-1 and R712-6 RESIDUE-1 replaced; #890 and #891 named (the PR body, `answers.py`); R712-6 RESIDUE-2's round 26 block heading (now in `evidence/ROUND-HISTORIES.md`) |
| 7. Gates | The full clean-clone pass at `66f71326`, once: every gate rc 0 but the flip check, which exits 1 by design, and `elaborate-gates-1`, whose first run timed out a LiteX simulation under load and whose second run is rc 0 (section 5) |

## 2. Changes (file:line, reason)

| Commit | File:line | Change | Reason |
|---|---|---|---|
| `24ea9c04` | `sw/firmware/ctrl/plat/ctrl_cc.h` (new, 61 lines) | `CTRL_CC_GNU` (1 where `__GNUC__`, a build may set it), `CTRL_CC_NOINLINE` (GNU `noinline`, nothing with 0), `ctrl_cc_ptr_load`/`ctrl_cc_ptr_store` (GNU `may_alias` in place, `memcpy` with 0) | item 5: one platform header outside the protocol code, a portable C11 fallback; the one file of the firmware outside `test/` that names a compiler extension |
| `24ea9c04` | `sw/firmware/ctrl/aecp/aecp.h:50-56`, `:292` | `AECP_LINE`: `_Alignas(64)` in C, `alignas(64)` where a C++ test reads the header (g++ has no `_Alignas`); the response buffer `AECP_LINE uint8_t response[...]` | item 5: C11's alignment for the buffer |
| `24ea9c04` | `sw/firmware/ctrl/port/ctrl_pool.c:17`, `:118-121`, `:124`, `:192` | the link through `ctrl_cc_ptr_load`/`_store`; the `may_alias` typedef removed | item 5 |
| `24ea9c04` | `sw/firmware/ctrl/srp/srp_mbx.c:6`, `:62`, `:943`, `:953` | `static CTRL_CC_NOINLINE` for `same`, `reclaim`, `build_mrpdu` | item 5 |
| `24ea9c04` | `sw/firmware/ctrl/test/ctrl_arms.py:35-62` (`arm_portable`), `test_ctrl_firmware.py:177` | the `portable` arm: a scan of every `.c`, `.h` and `.S` of the tree outside `test/` for `__attribute__`/`__builtin_` but `plat/ctrl_cc.h` (`[FAIL] Portable.CompilerExtensionsOnlyInThePlatformHeader: <file>:<line> ...`), and the port arm's tests built with `-DCTRL_CC_GNU=0` | item 5's verification as a gate, and the fallback run |
| `24ea9c04` | `sw/firmware/ctrl/test/test_port_loop.cpp:296-314` | `Pool.P10AFreedBlocksLinkIsWrittenOverItsClientsBytes`: two blocks filled by their client, freed, handed back last first, the second through the link the free wrote | the pool's link had no test that can fail for an unwritten link (R711-6 S3, R712-6 S1); both the GNU and the fallback path |
| `24ea9c04` | `sw/firmware/ctrl/test/ctrl_mutants.py:223-230`, `:932` | three plants (section 3); the `portable` arm in the campaign's arm table | |
| `24ea9c04` | `sw/firmware/ctrl/README.md:472`, `:481`; `plat/README.md:5` | the `portable` arm's row; `ctrl_cc.h` named | |
| `71e905fb` | `sw/firmware/ctrl/mbx/mbx.c:80-85` | `TX_MOVED` (0x400, an immediate's bit past every record's words, `_Static_assert`) in `tx_ring.moving` | item 2: a record holds whether the mover carries it |
| `71e905fb` | `mbx.c:515-534` (`mbx_tx_commit`) | the mover's wait and its ERR judged only for a record whose move it is (`(moving & TX_MOVED) != 0u && !mbx_dma_wait()`); the head advanced by the record's words | item 2: a word-loop record never inherits an earlier ERR (the mover holds ERR until its next start) |
| `71e905fb` | `mbx.c:545-549` (`mbx_tx_begin`) | a record before it that its move failed: `MBX_STATUS_LOST`, nothing started | item 2: a failed move is reported for the record it carried |
| `71e905fb` | `mbx.c:571-585` | `moving \|= TX_MOVED` where the mover starts; `t->moving` stored once | |
| `71e905fb` | `sw/firmware/ctrl/mbx/mbx.h:43`, `:182-199` | `MBX_STATUS_LOST`; the contract of `mbx_tx_send`, `mbx_tx_begin` and `mbx_tx_commit` restated: a commit judges its own move and no other, a failed move reported for its record (`commit` false, `begin` LOST, nothing started) | item 2: state the behaviour in `mbx.h` |
| `71e905fb` | `sw/firmware/ctrl/aecp/aecp.h:142-148`, `:187-194` | `enum aecp_fan` (TAKEN, REFUSED, LOST); `fan` and `fan_end` return it; the contract: a frame not delivered is reported for that frame | item 2 |
| `71e905fb` | `aecp/aecp_mbx.c:19-41` | `fan` maps `mbx_tx_begin`'s LOST to `AECP_FAN_LOST`; `fan_end` reports a failed last commit (`AECP_FAN_LOST`, no completion kept) | item 2: `fan_end` does not discard its commit's result |
| `71e905fb` | `aecp/aecp.c:601-686` (`fan_out`) | the recipient held uncommitted (`held`, `held_r`); a lost frame, from the next fan or from `fan_end`, resumes the notice at its recipient and gives back the sequence_id it did not spend | item 2: the notice resumes at the recipient whose move failed (IEEE 1722.1-2021 7.5.2) |
| `71e905fb` | `sw/firmware/ctrl/test/test_mbx_dma_driver.cpp:20-35`, `:171-188`, `:331-337`, `:352-410`; `ctrl_arms.py:240-247` | T2 extended (the begin after a failed move LOST, nothing started); T4 and T5 (section 3); the unit arm links `aecp_mbx.c` over the DMA driver and the window's HAL with stubbed AECP core and loop | item 2's driver and fan-port tests |
| `71e905fb` | `sw/firmware/ctrl/test/test_aecp.cpp:1418-1477` | `FanModel` (a fan port that commits at the next call and loses one numbered frame) and `Core.ANoticeWhoseFrameWasLostSendsItToItsRecipientAgain`; the two Mailbox tests read the enum | item 2's AECP test |
| `71e905fb` | `mbx_dma_mutants.py:18-50`, `aecp_fan_mutants.py:15-75`, `aecp_retry_mutants.py:161-163` | plants (section 3); `mover-transmit-error-committed` and `retry-notice-lost-to-a-full-queue` re-anchored on the new lines | a planted defect for each rule |
| `71e905fb` | `tb/verilator/ctrl_service_budget/poll_items.py:28-100` | `FAN_NOW`/`FAN_BEFORE`, the harness's cost plant `notice-fan-out-as-it-was`, re-anchored on the new walk (the old one keeps today's lost-frame report) | the plant must apply to the tree |
| `71e905fb` | `sw/firmware/ctrl/README.md:482`, `aecp/README.md:123` | the unit arm's T4/T5; the lost frame's resume | |
| `5a19b0ca`, `66f71326` | `tb/verilator/ctrl_service_budget/load_grade.py:10-23` (docstring), `:168` (`COLUMNS`), `:173` (`ROW_HEADERS`), `:244-247` (`parsed`), `:326-359` (`below_pin`, `findings`), `:362-366` (`ceiling`), `:369-388` (`report`), `:391-394` (`held`), `:420-429` (the control), `:542`, the `--check` output | the merge gate holds each `CEILING` point in both columns, each named (`1x1/1if: the load L at the pin is over its ceiling 0.70`); `--check` prints `HELD` per column; the control "a rise at the pin alone"; the contract parsed once a text (the checks plant it many times) | item 1 |
| `5a19b0ca` | `tb/verilator/ctrl_service_budget/rows_grade.py` (new): `BOUNDS` :64, `ROW_COSTS` :72, `SOURCES` :75, `header` :90 (`arithmetic` :111, no `eval`), `demand` :184, `solve` :240, `rows` :262, `unsourced` :283, `findings` :300, `report` :315 | the rows by every source: R4, R5, R6 by round 22's method (THE DRAIN as `ctrl_loop.h` states it), the GM events bounded by IEEE 802.1AS-2011's intervals, the queued notices at `aecp_mbx.h`'s derived bounds; tier bounds 20/90/90/20/125 ms | item 4 |
| `5a19b0ca` | `tb/verilator/ctrl_service_budget/flip_grade.py:3-23` (docstring), `:56-68` (`report`), `:70-146` (`controls`, `row_controls`), `:152-168` (`row_control_names`), `:170-175`, `:177-205` (`main`, `--point`) | the flip check holds both points' rows (`--point` for one); the rows' controls (section 3) | item 4 |
| `5a19b0ca` | `selftest_mutants.py:29`, `:471-482` | five mutants (section 3) | the self-test counts the new controls |
| `5a19b0ca` | `README.md:131-150`, the mutant table, `:1395-1396` | both columns held; the rows by every source; the controls | |
| `5a19b0ca` | `load_grade.py`, `flip_grade.py`, `poll_grade.py:3`, `:32`, `:38`, `:57`, `poll_items.py:3`, `:19`, `:116`, `:120`, `selftest_polls.py:3` | each comment ID and round label replaced by the issue and the behaviour (`#665`, `#890`, "option D", "the cuts' stated costs") | item 6, RESIDUE |
| `5a19b0ca` | `answers.py:101-103` | the unknown command's workaround names #891 | item 6, RES-2; R712-6 S2 |
| `19f16f80` | `sw/firmware/gtest/coverage.ratchet` | recorded through `fw_coverage.py --write` (section 6, D3) | `fw_coverage.py --check` refuses a measured file the ratchet does not record: `plat/ctrl_cc.h` |
| `66f71326` | `tb/verilator/ctrl_service_budget/load_grade.py:114`, `:141-145`, `:148`, `:151` | `STATED_US_DONOR['1x1/1if']`: `event.ACMP` 165 to 170, `build` 910 to 920; the tables' provenance | this round's legs, the table rule (section 4) |
| `66f71326` | `docs/design/SPLIT_CONTROL_MEMORY.md:2077`, `:2082-2085`, `:2073`, `:2131`, `:2133`, `:2141`, `:2143-2147`, `:2153-2157`, `:2170`, `:2178`, `:2180` | section 13: both columns held and named; the rows by every source the flip check holds and their result; R712-6 F3's sentence; the pool's link through `ctrl_cc.h`; the fan-out control's fixture; the record-move and portable-C paragraphs; the re-grade on this image; the table's columns; the least margins, the heaviest passes and round 16's margin deferred to #890; the load bullet | items 1, 3, 4, 6 and 7 |
| `66f71326` | `rows_grade.py:3-5`, `:17`, `README.md:146` | the queued notices named as the loop search's stated bounds | |

## 3. New checks, planted mutants and failing words

**Firmware** (each caught in this round's subset runs, `receipts/plants/`, and again by the campaigns of the gate pass):

| Plant | Campaign, arm | Planted defect | Refused by, with its words |
|---|---|---|---|
| `mover-commit-judges-every-record` | control, `unit` | the commit waits on the mover and judges its ERR for every record (`!mbx_dma_wait()`, the earlier rule) | `MbxDma.T4ARecordTheWordLoopWroteInheritsNoEarlierMovesError`: "T4 a frame off a word sent after a failed move is committed" |
| `mover-move-not-held-its-own` | control, `unit` | `moving \|= TX_MOVED` removed: no record holds its move | `MbxDma.T2AMoveEndingInErrorIsNotCommitted`: "T2 a move that ends in ERR is refused" |
| `mover-lost-record-reported-as-bad` | control, `unit` | `mbx_tx_begin` returns BAD for the record before it (the earlier rule) | T2: "T2 a begin that finds the record before it ended in ERR reports it lost"; T5: "T5 the fan after a frame whose move failed reports that frame lost" |
| `mover-fan-lost-reported-as-refused` | control, `unit` | `aecp_mbx.c`'s `fan` maps LOST to REFUSED | T5: "T5 the fan after a frame whose move failed reports that frame lost" |
| `mover-fan-end-commit-discarded` | control, `unit` | `(void)mbx_tx_commit(MBX_CH_AECP);` in `fan_end` (the earlier rule, R712-6 F2) | T5: "T5 fan_end reports a last frame whose move failed lost" |
| `mover-transmit-error-committed` (re-anchored) | control, `unit` | the commit's wait result ignored | T2: "T2 a move that ends in ERR is refused" |
| `notice-lost-frame-skipped` | AECP | the walk resumes past a lost frame (`lost = false`, the earlier rule) | `Core.ANoticeWhoseFrameWasLostSendsItToItsRecipientAgain`: "was lost is delivered once to each recipient, in order" |
| `notice-lost-frame-sequence-spent` | AECP | the lost recipient's sequence_id not given back | the same test: "was lost carries its recipient's addresses and sequence" |
| `notice-lost-last-frame-dropped` | AECP | `fan_end`'s LOST ignored by `fan_out` | the same test: "was lost is delivered once to each recipient, in order" |
| `notice-lost-frame-resumed-at-the-next` | AECP | the held recipient recorded one past itself | the same test: "was lost is delivered once to each recipient, in order" |
| `retry-notice-lost-to-a-full-queue` (re-anchored) | AECP | `fan_end`'s REFUSED (no room for the completion) not owed | `Mailbox.ANoticeWithNoRoomStaysOwed`: "a notice with no room for its completion stays owed" |
| `portable-attribute-in-the-srp-adapter` | control, `portable` | `static __attribute__((noinline)) bool same(` back in `srp_mbx.c` | `Portable.CompilerExtensionsOnlyInThePlatformHeader`: "srp/srp_mbx.c:62 a compiler extension outside plat/ctrl_cc.h" |
| `portable-fallback-link-unwritten` | control, `portable` | the fallback's `memcpy` store of the link removed | `Pool.P10AFreedBlocksLinkIsWrittenOverItsClientsBytes` built with `CTRL_CC_GNU=0`: "P10 then the one freed before it, through the link its free wrote" |
| `pool-link-unwritten` | control, `port` | `ctrl_cc_ptr_store(ptr, bin->free_head);` removed | the same test (GNU path): the same words |

The fallback plant first escaped with 0 checks failed: no pool test could fail for an unwritten link while the freed block still held its old link, so `Pool.P10` writes the client's bytes over the block before the free; it then failed at once with a crash, and reads the list head before the second allocation so the failure is named.

**The harness** (`run.py --self-test`, `load_grade.py --selftest`, `flip_grade.py --selftest`):

| Check or control | Holds |
|---|---|
| the load gate refuses a rise at the pin alone | an ACMP record's cost raised to 2,000 us in the pin's column only: the pin's load at 1x1/1if 0.807, refused as `1x1/1if: the load 0.807 at the pin is over its ceiling 0.70`, the donor's column unrefused (R711-6's and R712-6's probes print the same) |
| the flip check refuses each row at each point over its bound, and passes it within | R4, R5, R6, first, last at 1x1/1if and 8x8/2if: a bound a hundredth of a ms under W refused, over W passed |
| the flip check refuses each source not counted | every term of each solved row left out in turn must shorten its W |
| the flip check refuses a stated cost not read | an SRP record's cost raised in the pin's column lengthens R5 |
| the flip check refuses the rows read on the column graded with tsn-c-stack#32 | the rows' costs are the pin's |
| the flip check refuses the last queued notice past its bound | `AECP_QUEUED_PASSES` planted in a copy of `aecp_mbx.h` (70 at one interface): `1x1/1if last` refused |
| the flip check refuses a source the rows do not count | each source of the docstring's list counted in every solved row (links in R5) |
| the flip check refuses the tier bounds or the points not decision D's | 20, 90, 90, 20, 125 ms at 1x1/1if and 8x8/2if |

| Harness mutant | Planted defect | Caught by |
|---|---|---|
| load: 1x1/1if held with tsn-c-stack#32 alone (earlier rule) | `load_grade.COLUMNS` the donor's only | the load gate refuses a rise at the pin alone |
| rows: the rows by every source not held | `rows_grade.findings` finds nothing | the flip check refuses 1x1/1if R4 over its bound |
| rows: SRP's rows held to T_svc's 20 ms | R5 and R6 bound 20 | the flip check refuses the tier bounds or the points not decision D's |
| rows: the grandmaster events left out of a row's window | `demand` without `gm` | the flip check refuses a source the rows do not count |
| rows: read on the column graded with tsn-c-stack#32 | `rows_grade.costs` on the donor's column | the flip check refuses the rows read on the column graded with tsn-c-stack#32 |

`load_grade.py --selftest`: 24 of 24 (23 before). `flip_grade.py --selftest`: 129 of 129 (6 before: the load's six and the rows' 123). The harness self-test: 0 failures, 201 `MUTANT caught` (196 before).

## 4. Measurement: the re-grade at both points

**The image** (`receipts/rom/rom.txt`): item 2 grows every image by 112 to 120 B (8x8/2if arm A 122,328 to 122,440 B; the `answering-every-port` arm 122,636 to 122,748 B; arm B 122,488 to 122,608 B; 1x1/1if arm A 107,112 to 107,232 B; with tsn-c-stack#32 at 1x1/1if 107,568 to 107,680 B). Arm A's 8x8/2if image with tsn-c-stack#32 is 122,896 B, refused by the ledger: `allocation over budget: 58 RAMB36 (rom 122896 bytes in 124928, ...) exceeds the 57.5-RAMB36 budget ledgered for 8x8, two interfaces` (`receipts/rom/D8-image.log`). Before committing item 2 I cut its code from +136 B to +112 B at 8x8/2if (an immediate's bit for `TX_MOVED`, `t->moving` stored once) to fit that ledger; the last 16 B would have needed changes that obscure the protocol code, so the column with tsn-c-stack#32 at 8x8/2if is not re-measured (deviation D1, section 6).

**The legs** (each a fresh build on its own clean clone of `71e905fb`, the firmware's final tree: the later commits change only the harness's Python, docs, the coverage ratchet and the stated-cost table, none a recorded build input; the donor column's at 1x1/1if on a scratch clone with round 26's port of tsn-c-stack#32, its stack tree `ff86a1d1...`, byte-identical to round 27's; `receipts/legs/`):

| Leg | Groups | Refusals | Budget misses | Work passes over the share | Heaviest work pass | Least row margin |
|---|---:|---:|---|---|---|---|
| GA8, arm A, 8x8/2if | 93 | 0 | 6 of 996, 3 of 136 paths | 0 of 272,475 | 192,237 (`backlog`), 7,763 under | 6.515 ms (`backlog-adp@verify-aged2-6`, 13.485 ms) |
| GA1, arm A, 1x1/1if | 94 | 0 | 6 of 945, 3 of 87 | 0 of 184,496 | 160,618 (`backlog`) | 10.434 ms |
| GN8, the `answering-every-port` arm, 8x8/2if | 16 | 0 | 0 of 736 | 0 of 14,350 | 186,213 (`notice-every-2`) | 4.018 ms (`notice-burst-6`, 15.982 ms) |
| GN1, the same, 1x1/1if | 16 | 0 | 0 of 280 | 0 of 22,114 | 160,222 (`notice-burst-6`) | 8.349 ms |
| GB8, GB1, arm B's `aecp` group | 1, 1 | 0 | 0 of 39, 0 of 25 | 0 of 131, 0 of 110 | 119,134, 63,670 | |
| D1, tsn-c-stack#32, 1x1/1if | 19 | 0 | 6 of 141, 3 of 81 | 0 of 10,249 | 156,237 (`backlog-adp`) | 11.748 ms |

The six misses are round 27's three egress-held paths (tsn-c-stack#26). Every save is durable within its stated worst case (8x8/2if `save-second` 22,110 ms of 22,150, `save-starved` 12,089 of 12,110; 1x1/1if 6,030 of 6,070 and 4,048 of 4,070).

The two arm A legs ran with helper runs on the same build (`scripts/a683zm_helper.py`): each took the tail of the leg's queue in run.py's own order, stopped each duplicate the leg's own run then started (its Vsim, by PID, its argument the leg's own `results-rest/<group>.txt`: 49 at 1x1/1if, 54 at 8x8/2if, none of them a group whose only run it was), and merged and regraded the leg again once every run had ended (`legs/GA8-helper.txt`, `GA1-helper.txt`). My leg runner first merged without the group its build run carried; arm B's two legs were merged and regraded again by hand (`scripts/remerge.sh`). Each leg's final regrade is rc 0.

**The costs** (round 26's parsers, `receipts/costs/`; the table rule of round 27, `tools/tables28.py`: each cost the larger of this measurement and the committed table's; `costs/tables28-against-e7e2b744.txt`): the pin's column unchanged at both points, and `poll_grade.py`'s; with tsn-c-stack#32 at 1x1/1if `event.ACMP` 165 to 170 us and `build` 910 to 920 (`66f71326`); the 8x8/2if column with tsn-c-stack#32 kept (no D8 leg). The load: 1x1/1if 0.4631 at the pin and 0.4503 with tsn-c-stack#32 (0.237 and 0.250 under 0.70); 8x8/2if 0.8152 and 0.7191; 32x32/2if 2.150 and 1.659 (reported).

**The cost controls** on this image (`receipts/controls/`), each caught: `notice-fan-out-as-it-was` (its fixture re-anchored on the new walk) an AECP item of 29,968 cycles against 27,000; `srp-compared-by-memcmp` an SRP record's apply of 37,494 against 36,500; `polls-rebuild-in-the-base` a polls base of 74,399 against 28,000; `polls-rebuild-twice` a rebuild item of 113,443 against 63,000.

**The rows by every source** (`flip_grade.py --check`, `receipts/gates/lane/flip_check_exits_1.log`):

| Point | R4 (20 ms) | R5 (90 ms) | R6 (90 ms) | First queued notice (20 ms) | Last queued notice (125 ms) |
|---|---:|---:|---:|---:|---:|
| 1x1/1if | **73.02** | 37.19 | 32.69 | 20 | 22 |
| 8x8/2if | **489.97** | **162.96** | **149.57** | **22** | 62 |

## 5. Gates

The full gate pass ran once, at `66f713267f201d1a00d7f711e04b3a996d804dee`, each workflow job and gate part on a fresh clean clone of it, never piped (`receipts/gates/`: `workflows/` the job drivers, every step's log and rc, each job's tree check, `not_run.json` with every reason and `verify-table.md`; `sweep/`; `lane/`; `dispatch.txt` and `queue-as-started.txt`). Every gate rc 0 but the flip check, which exits 1 by design, and `elaborate-gates-1`, run twice (its first run's LiteX simulation timed out under the pool's load, result unknown; the second rc 0).

| Gate | Where it ran | Result | Receipt |
|---|---|---|---|
| Every `run:` step of `rtl-fast.yml`, `rtl.yml`, `elaborate.yml` and `docs.yml` (the four a pull request to `dev-soft-core` triggers) | each job its own clone (`run_wf.py`), the firmware jobs and the elaborate jobs with the LiteX venv, on the session pool | **139 steps rc 0, 226 not run, each with its reason, 0 bad** (`verify_wf.py`, rc 0; `elaborate-gates-1`'s steps from its second run) | `workflows/verify-table.md` |
| `rtl-fast.yml`: `changes`, `verilator-lint`, `bdd-conformance`, `yosys-tool`, `yosys-elaboration`, `publication-census`, `split-cdc`, `rtl-fast` | 01:49 to 02:40 | every step rc 0; `behave` 508 scenarios, 2,330 steps passed | `workflows/drivers/rtl-fast-*.driver.log` |
| `firmware-unit` | 01:44 to 02:14 | every step rc 0: `test_ctrl_firmware.py --require-rv32 --self-test` PASS (the `portable` arm among its arms); the saved-state store gate's 455 tests; `fw_coverage.py --check` PASS (39 files) | `workflows/logs/rtl-fast__firmware-unit__ci_step_1{0,1,2}.log` |
| `firmware-control-mutants` | 01:15 to 01:53 | **680 of 680 caught** (672 before: the five new mover and fan-port plants, the three portable and pool plants), `test_ctrl_firmware: PASS` | `..._firmware-control-mutants__ci_step_9.log`, `workflows/mutant-counts.txt` (each campaign's every `[ok]` line) |
| `firmware-aecp-mutants` | 01:15 to 01:35 | 224 `[ok]` (220 before: the four lost-frame plants), `test_ctrl_firmware: PASS` | `..._firmware-aecp-mutants__ci_step_9.log`, `workflows/mutant-counts.txt` (each campaign's every `[ok]` line) |
| `firmware-srp-mutants` | 01:16 to 01:40 | 340 `[ok]`, `test_ctrl_firmware: PASS` | `..._firmware-srp-mutants__ci_step_9.log`, `workflows/mutant-counts.txt` (each campaign's every `[ok]` line) |
| `firmware-boundary` | 01:16 to 01:44 | `ctrl_boundary: PASS`: 3,333 compiled sources, 0 findings | `..._firmware-boundary__ci_step_9.log` |
| `firmware-verilator` | 01:35 to 01:51 | `ctrl_boundary: PASS`: 1,123 compiled sources, 0 findings | `..._firmware-verilator__ci_step_14.log` |
| `rtl.yml`: `full-ci-gate`, `yosys-tool`, `yosys-shards` 0/4 to 3/4 | 02:18 to 02:40 | every step rc 0 | `workflows/drivers/rtl-*.driver.log` |
| `elaborate.yml`: `elaborate-gates-0`, `elaborate` | 01:40 to 02:05 | every step rc 0 | `workflows/drivers/elaborate-*.driver.log` |
| `elaborate.yml`: `elaborate-gates-1` | 01:42 to 02:18, again 02:47 to 03:22 on a fresh clone | first run: every step rc 0 but `gate_19`, the LiteX simulations' aggregate, rc 92: `TIMEOUT test_soc_timing_cuts (900s wall clock - result UNKNOWN, not a failure)` on the loaded session pool, 7 of 8 passed. Second run: every step rc 0, `gate_19` 8 of 8 passed (`test_soc_timing_cuts` PASS). Both runs' logs are kept (`workflows/logs/` holds the second run's, `workflows/first-elaborate-gates-1/` the first's) | `workflows/logs/elaborate__elaborate-gates-1__gate_19.log`, `workflows/rerun-elaborate-gates-1/` |
| `docs.yml`: `wire-accountability`, `docs-check-no-git`, `docs-gates-0` (43 steps), `docs-gates-1`, `docs-gates-2`, `docs-check` | 01:16 to 02:37 | every step rc 0; `docs-check-no-git` removes `.git`, so the runner's own tree check after it cannot run (as in rounds 25 to 27) | `workflows/drivers/docs-*.driver.log` |
| The full sweep (`rtl.yml`'s `verilator-shards` suites), `scripts/run_all_suites.sh` as four `native-shards.py` units, MemoryMax 10G, `-j4 --no-print-directory`, shard 2 (`capture_coherence`) on four CPUs | 02:13 to 03:55 on the session pool, 96-103, 104-111, 112-115, 120-127 (deviation D4) | **65 suites, 65 passed, 0 failed, 0 timed out; 2,613,726 checks, 0 in-suite failures** (shard 0: 15 suites, 360,992 checks; shard 1: 17, 1,946,931; shard 2: 17, 284,228, `capture_coherence` with "41 builds on 4 worker(s)" passed within its budget; shard 3: 16, 21,575); every shard's preflight PASS (suite cancellation among them: no #833 re-run). Tree after: clean in shards 0 to 2; in shard 3 the two `TEST_RESULTS.md` files the `tsn_fuzz` campaign writes in place show a new date stamp only, their counts unchanged (`sweep/shard-3-tree-after.diff`) | `sweep/` |
| `git diff --check` against the merge base `1d6bf555` and against round 27's `e7e2b744` | lane clone a | rc 0, no output | `lane/diffcheck_*.log` |
| `check_py_idiom.py`, `check_cpp_idiom.py`, `check_baremetal_only.py --check`, `docs_check.py` | lane clone a | rc 0 (`docs_check`: 0 findings across 217 md files) | `lane/` |
| `ctrl_hot.py --self-test`, `--check` | lane clone a | rc 0 | `lane/ctrl_hot_*.log` |
| The harness self-test (`run.py --self-test`) | lane clone a | **`self-test: 0 failures`**, 201 `MUTANT caught` (the five new among them) | `lane/harness_selftest.log.tail` |
| `load_grade.py --selftest`, `--check` | lane clone a | 24 of 24 controls refused; `RESULT: PASS`, `HELD 1x1/1if at the pin: the load 0.463`, `HELD 1x1/1if with tsn-c-stack#32: the load 0.450` | `lane/load_*.log` |
| `flip_grade.py --selftest`, `--check`, `--check --point 1x1/1if`, `--check --point 8x8/2if` | lane clone a | 129 of 129 controls refused; **each `--check` rc 1 by design**: 8x8/2if's load and rows, and `OVER 1x1/1if R4: by every source 73.02 ms, over its bound 20 ms` (the finding) | `lane/flip_*.log` |
| R711-6's `probe_1x1_column.py`, R712-6's `probe_pin_1x1.py` | lane clone a | rc 0, each pin-only rise refused: `1x1/1if: the load 20.407 at the pin is over its ceiling 0.70`, `... 1.461 ...`; `... 0.807 ...` | `lane/probe_*.log` |
| `git grep -n __attribute__ -- sw/firmware/ctrl ':!*/test/*'` | lane clone a | only `sw/firmware/ctrl/plat/ctrl_cc.h:31` and `:32` | `lane/attribute_grep.log` |
| `ctrl_service_hooks/run.py --self-test`, `nvm_split_target/run.py --self-test` | lane clone a | rc 0 each | `lane/hooks_selftest.log`, `lane/target_selftest.log` |
| `test_ctrl_nvm.py --require-rv32 --self-test --jobs 8` | lane clone c | rc 0: 455 tests, all 121 planted defects reddened | `lane/nvm_selftest.log` |
| `gen_mailbox.py --check --crosscheck`, `--selftest`; `lint_rtl.py --check`; `test_soc_options.py`; `test_ctrl_memory.py` | lane clone a | rc 0 each | `lane/` |
| `test_builder.py --require-rv32` | lane clone b, 01:15 to 01:48 | rc 0, `ALL GATES PASS EXCEPT 2 NOT RUN` (the same two arms as round 14's, each with the tool's reason) | `lane/test_builder.log` |
| `ctrl_split_boot` at 1x1, 8x8, `--native-controls`, `--self-test` | lane clone c | `ctrl_split_boot: PASS (0 finding(s))` at both shapes; 6 of 6 native controls; 3 of 3 plants | `lane/boot_*.log` |
| `cd tests && behave` | lane clone a | 508 scenarios, 2,330 steps passed | `lane/behave.log.tail` |
| `make -C tb/verilator/milan_dp twin` | lane clone a | rc 0 | `lane/twin.log.tail` |
| The harness at both points (S2's harness): every recorded group of arm A, of the `answering-every-port` arm and arm B's `aecp` group at 1x1/1if and 8x8/2if, regraded at the head against a fresh build of each point there (deviation D5) | each leg's own clone at the head | each fresh build's three images byte-identical to the leg's (objcopy and ELF) and its sample log byte-identical (`acmp-cmd`, `notice-burst-0`, `aecp`); every regrade rc 0: 0 refusals; GA8 93 groups, 6 of 996 (3 of 136 paths); GA1 94, 6 of 945 (3 of 87); GN8 0 of 736; GN1 0 of 280; GB8 0 of 39; GB1 0 of 25; 0 passes over the share in every leg | `receipts/head/` |

The lane clones' trees after their gates and every job's tree check are clean (`lane/tree-after-*.txt`, empty). Memory: every gate ran in a unit of its own with MemoryMax 10G; host MemAvailable stayed at or above 36 GB.

## 6. Findings, deviations and open questions

- **F1, a finding for the flip (item 4): 1x1/1if misses tier 1 at R4 by every source**, 73.02 ms against 20. THE DRAIN takes SRP's records ahead of AECP's, and round 23's tier design is not built. Not a STOP by the ruling. Proposed issue: `ROWS-FINDING.md`.
- **D1, deviation: the column with tsn-c-stack#32 at 8x8/2if is not re-measured.** Item 7 re-grades both points; at the pin both are, and with tsn-c-stack#32 1x1/1if is. Arm A's 8x8/2if image with tsn-c-stack#32 is over that point's ledger at this head (16 B past the granule), so that leg cannot build: the column keeps its committed costs, which `load_grade.py` reports (it gates only 1x1/1if) and the flip check does not read (it reads the pin). The pin move meets the same ledger.
- **D2: `flip_grade.FLIP` stays 0.70 at 8x8/2if.** #890's owner decision (2026-11-11) sets that point's flip ceiling to 0.75 "with no change to S2b's reviewed head", in a small change after the pin move; item 3 asks only that section 13 cite it.
- **D3: the coverage ratchet** (`19f16f80`) was recorded through `fw_coverage.py --write` because the new header is measured: every file at 100 %, and the counts of files earlier rounds grew are recorded with it (the ratchet had not been written since; it refuses only drops). Found by an early `fw_coverage.py --check` on a clean clone of `5a19b0ca` (`receipts/early/`), before the gate pass.
- **D4, deviation: the sweep's shards ran on the shared session pool**, not on ranges `cpu_ranges.py pick` booked. From 01:15 the release lane's holds kept 0-95 booked (`milan-hold883-*`), so no 8-CPU range came free in an hour; at 02:13 the launcher was stopped by its PID and `native-shards.py` started the four shard units on 96-103, 104-111, 112-115 (shard 2, `capture_coherence`, on four CPUs) and 120-127, MemoryMax 10G each, MemAvailable 51 GB. Every gate job ran on the pool too. The pool is counted busy by every booking, so this took no booked CPU from another lane; it slowed the pool's other sessions.
- **D5: the harness at the head through fresh builds.** `build.FIRMWARE_TREES` digests `sw/firmware/gtest` with the firmware, so `19f16f80`'s ratchet made the legs' builds stale for `--reuse-build` at the head (`logs/head-*.log`: `REFUSED reused build is stale: tree:firmware changed`). As round 25 did for a test-only commit, each leg was built fresh on its own clone at the head with one sample group, its images, inputs and sample log compared with the leg's build, and every recorded group regraded against the fresh build (`scripts/head_sample.sh`, `receipts/head/`).
- **Interpretation (item 4): which rows.** "R4, R5 and R6 (tier 1 20 ms, SRP 90 ms, last notice 125 ms)": R4 is tier 1's row and R5 and R6 SRP's, solved by round 22's method; tier 1 also holds the first queued notice (round 23, item 3) and the last queued notice has its own 125 ms, so both are held too, at `aecp_mbx.h`'s stated bounds the loop search holds the loop to.
- **Interpretation (item 4): the model.** Round 22's method (its receipts' `arrivals2.py`, THE DRAIN as built, every source) ported into the tree with the current constants and this tree's pin costs; one change: the grandmaster event is bounded by its IEEE 802.1AS-2011 intervals, as the load gate's term is, where round 22 charged one an interface every ordinary pass (with today's stated GM cost of 320 us at 8x8/2if that alone made R4 unbounded there). A LINK event's cost, which no load table states, is `rows_grade.ROW_COSTS` (150 and 300 us, this round's measurement 145 and 300).
- **Item 2's design.** `MBX_STATUS_LOST` is a new driver status, returned only by `mbx_tx_begin`; `mbx_tx_send`'s own failed move stays BAD (it reports its own record). The fan port's result became `enum aecp_fan`, so the AECP core resumes at the held recipient without a second port call per recipient. The existing T2 expectation (BAD for a begin after a failed move) became LOST: a contract change, stated in `mbx.h`, not a weakened test.
- **The item 5 receipt** (`receipts/item5/`) is a scratch clone of `e7e2b744` with the portable change alone; `24ea9c04` differs from it only in where one comment of `ctrl_pool.c` sits, and a comment move was shown image-neutral on the full change (`receipts/item5/image-identity.txt` and the r2/r3 rebuild below).
- **Live `dev-soft-core`** moved to `764482b4` (PR #874) after the merge base `1d6bf555`; `git merge-tree --write-tree HEAD origin/dev-soft-core` merges cleanly. The candidate merge is the manager's.

## 7. Run history

- 2026-11-11 20:24 CET start; origin and head `e7e2b744` verified; the ruling, R711-6 and R712-6 read; #890's owner decision (15:16) read.
- 20:3x TAKEN posted (issuecomment-6805358380).
- 20:4x to 21:10 items 2 and 5 in firmware, their tests and plants; quick image builds on scratch clones: item 5 alone byte-identical to round 27's GA8 images (`Q5A8`); item 2 first +136 B at 8x8/2if, cut to +112 B (an immediate's bit for `TX_MOVED`, `t->moving` stored once; rebuilt twice, `r2` and `r3`, the second after a comment move, with identical objcopy images), the unit, port, portable and AECP core and mailbox arms PASS, each new plant caught on a subset campaign (`receipts/plants/` holds the reruns after two plants needed fixing: the sequence plant first failed to compile under -Werror, `(void)held_r;` kept it building; the fallback-link plant escaped with 0 checks failed until `Pool.P10` wrote the client's bytes). `24ea9c04` and `71e905fb` committed 21:08.
- 21:14 the legs started at `71e905fb` on booked ranges: GA8 48-55, GA1 56-63, GN8 and GN1 40-47, D1 with arm B and the fan-out control 0-7; 21:31 the other three cost controls on 32-39; 21:34 helper runs for GA8 (80-87) and GA1 (24-31).
- 21:1x to 21:27 items 1, 4 and 6 in the harness (the row model ported from round 22's receipts; `eval` replaced after the idiom gate refused it; the model's inputs bundled to keep six parameters; the firmware header paths moved into the load gate, already classified for the boundary gate's builder scan); the harness self-test 0 failures, 201 mutants caught (263 s, rc 21:32); `5a19b0ca` committed 21:28.
- 21:2x arm B's legs merged and regraded again by hand (the runner's merge had left out the build run's group).
- 21:43 an early `fw_coverage.py --check` on a clean clone of `5a19b0ca` refused the new header (not in the ratchet), every file at 100 %; 21:48 `--write` there, `19f16f80` (21:53); 21:56 the firmware suites on that clone PASS, 68 arms.
- 22:09 D1 rc 0; 22:54 GN8; 23:05 GN1; 00:00 GA1 (its helper's re-merge); 00:58 GA8. The costs: D1 22:10, G1 00:17, G8 01:11. 21:56 arm A's 8x8/2if image with tsn-c-stack#32 built alone and refused by the ledger (`receipts/rom/D8-image.log`).
- 01:12 the table rule applied: the pin's column unchanged, the donor's 1x1/1if two costs restated; section 13 written; `66f71326` committed 01:14.
- 01:15 the final gate pass at `66f71326`: the sweep launcher (waiting for four free ranges) and the gate dispatcher (`scripts/a683zm_disp.py 4 6 22`, every job its own unit, MemoryMax 10G, a booked range when one is free, else the session pool).
- 01:15 to 02:13 no booked range came free: the release lane's holds kept 0-95 (`milan-hold883-*`), so every gate job ran on the session pool, and at 02:13 the sweep's launcher was stopped by its PID and its four shards launched there by `native-shards.py` (96-103, 104-111, 112-115 for shard 2, 120-127; MemAvailable 51 GB), each unit's affinity checked (deviation D4).
- 02:29 the harness's head regrades from the legs' builds refused them as stale (the ratchet's tree is digested); 02:30 to 02:56 a fresh build of each point at the head with a sample, its images and sample log byte-identical, every leg regraded rc 0 (D5).
- 02:40 `verify_wf.py` found `elaborate-gates-1`'s `gate_19` rc 92 (`test_soc_timing_cuts` past its 900 s wall clock on the loaded pool); 02:47 to 03:22 that job run again on a fresh clone, every step rc 0; 03:23 `verify_wf.py` rc 0 with the second run's logs, the first run's kept aside.
- 03:27 to 03:55 the four shards ended, rc 0 each, 65 suites passed.
- 03:5x the receipts collected and scrubbed of host paths, this file and `PR-BODY.md` written, `receipts/INDEX.md` generated (666 files, none over 200 KB, no host path), REVIEW READY posted (issuecomment-6813034799).
