[A683zn]

## Contents

- **[Status](#status)** — REVIEW READY at the head below: round 29, the sync onto the TSN stack's pin move and round 28's review findings. The pin move is merged once; the rows by every source charge SRP's retained retry at its own rule; a refusal in a notice's fan-out is pinned against a loss and a completion waits for the whole walk; the 8x8/2if size fixture is ledgered at 58.0; both points are re-graded on the composed image. The tier rows stay red, with #894.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — Round 29 item by item and the re-grade on the composed image; round 28 as it stood; what holds at this head; where the round histories went.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Checkout, submodules and environment.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What is left, and the decisions for the owner and the manager.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

REVIEW READY at `b2d39235ab9bba85d7e560b5f5f78fb4be528960` (`665-s2b-cycles` -> `dev-soft-core`): one merge commit of the TSN stack pin move's head `bfe7a9d6` (PR #892) into round 28's head `66f71326`, then seven ordinary commits. No rebase, no force, no amend. The tsn-c-stack submodule is at `715589c`, the pin move's; no change to tsn-c-stack, lwSRP or any donor. No RTL or mailbox-contract change.

The ruling on round 28 (#665 issuecomment-6813183455) makes round 29 the sync onto the pin move, with R711-7's and R712-7's findings on round 28's delta and the pin move's own handover; the tier rows go to #894.

- **1x1/1if: 0.486 at the pin and 0.483 in the column with tsn-c-stack#32**, each held at 0.70 for merge by `load_grade.py --check`, which exits 0. The pin now carries tsn-c-stack#32, and both columns are measured on the composed image.
- **8x8/2if: 0.816 at the pin**, held by the flip check (0.767 in the second column), which exits 1; the 8x8/2if flip waits on #890.
- **Decision D's tier bounds by every source**, held for each point's flip by `flip_grade.py --check`: 1x1/1if misses tier 1 at R4, 66.12 ms against 20 ms; R5, R6 and the queued notices fit there. The rows stay red; the tiers are #894's.
- 32x32/2if, reported: the more-compute image, #872, round 25's row unchanged: 1.659 (2.150 at the pin).

The full gate pass ran once, on clean clones of this head ([How to validate](#how-to-validate)).

## Linked Issue / roles

Relates to #665
Relates to #892 (the TSN stack pin move, merged here)
Relates to #894 (the tier rows by every source, model first)
Relates to #890 (the 8x8/2if flip, which this lane's flip check holds)
Relates to #882 (its three acceptance items were met in round 27)
Relates to #891 (the 14-bit AEM command_type the harness works around)

Executor: `[A683zn]`
Internal cleared-context reviewer: `[R711]`
External reviewer: `[R712]`

## Description

### Round 29

**The ruling** (#665 issuecomment-6813183455, on [A683zm]'s round 28 REVIEW READY at `66f71326`): round 29 is the sync onto the TSN stack's pin move, PR #892, and the tier rows go to #894. With it, R711-7's and R712-7's findings on round 28's delta (#810 issuecomment-6813519183 and R712-7), and the pin move's handover (#665 issuecomment-6813799445).

| Item | At this head |
|---|---|
| 1. The merge | `e96b9120`, one merge commit of the pin move's head `bfe7a9d6` into `66f71326` (`git merge --no-ff`), the tsn-c-stack submodule at `715589c`. The seven conflicts #890's lane recorded, each resolved from the composed tree: `ctrl_plat` at each point measured by `ctrl_plat_image.py` in the composed build, 17,472 / 19,008 / 18,112 / 20,288 B (`PLAT_*`; the platform override's key 20,288 B), neither side's; `acmp-expiry-reads-the-clock-twice` anchored on the composed code (715589c's `dirty_if` mark) and refused by `AcmpCore.TimerPortBudgets`; `coverage.ratchet` through `fw_coverage.py --write`; the docs with both sides' facts, the figures restated from the composed headers (`MAILBOX_SPLIT.md`: S2b's one 20 ms bound with the pin's 2,754-access pass; the four-module table and `CTRL_APP_PASS_MAX`, 4,840 and 4,980, from the service-bounds probe); and `__lshrdi3` out of the hot list, in `ctrl_split_hot.txt` (the merge) and in the link script's copy of it (`2cc852fa`), which `ctrl_hot.py` holds equal and which the merge alone left refused (`ORDER`, `LINKED`). No conflict needed a protocol or mailbox-contract change |
| 2. The 8x8/2if size fixture | `459a8d70`. 58.0 RAMB36, its cause stated in the ledger: a TX record's commit judges its own move (+112 to 120 B an image) and, with the pin move, arm A's image is 123,112 B of `rom`, past 57.5's 122,880; at 58.0 it holds 124,928, 1,816 B to spare (the `answering-every-port` arm 123,420 B, 1,508 to spare). `test_ctrl_memory.py` holds the entry, its own image refused at 58.5 |
| 3. The re-grade | Both points at the composed head ([below](#the-re-grade-on-the-composed-image)). The pin carries tsn-c-stack#32 here (its `src/` and `include/` equal the donor's `9043b926`), so each point's legs serve both of the load gate's columns, each kept the larger of the measurement and its own committed costs; the 8x8/2if column with tsn-c-stack#32 that round 28 could not build is measured |
| 4. No tier change | The bounds (20, 90, 125 ms), the every-source rule and THE DRAIN are unchanged; no tier structure. The rows stay red: [#894](https://github.com/kebag-logic/milan-fpga/issues/894) |
| 6, 8 F1. The rows by every source | `446d3310`. SRP's retained retry is charged at its own rule (`srp_mbx.c`: one a centisecond, `retry_spent` given back by the centisecond's consumer): one before the window's first centisecond and one after each it holds, `min(passes, floor(W/10) + 2)` (`rows_grade.retained_retries`). SRP's records ahead of R4's are counted over W less R4's own record (`rows_grade.srp_window`), not less AECP's whole burst. **The scope:** a retained record holds SRP's channel, each up to `SRP_RX_RETRY_MS` (1,000 ms), SRP's storage rule and not the CPU's service, so SRP's own rows, R5 and R6, are solved with no record of theirs refused for storage, and count neither the hold nor the retry; R4's record is AECP's, which no SRP record holds, and counts the retries (`RETAINED_ROWS`). With the hold counted, each of the 31 SRP records ahead of R5's or R6's, refused in turn, would hold it 1,000 ms: no W under 2,000 ms. **The datapath change records** (COUNTERS_CHANGED, AVB_INFO_CHANGED, AS_PATH_CHANGED, AMAP_LIVE_WRITE) are named as excluded with the reason (`EXCLUDED`): no group stages them, so no cost of theirs is stated, and the method charges stated costs only; the notices they mark are counted, and their dispatch is #894's to stage. `rows_grade.rule_findings` holds each rule against the tree (the retry's lines in `srp_mbx.c`, the counts at six windows, every event type of the contract counted or excluded), and the flip self-test plants the earlier rules: the once-a-pass retry, refused and lengthening 1x1/1if's R4, and the shortened SRP window, refused and shortening it; with them a retry counted in an SRP row, the retry's rule planted out of `srp_mbx.c`, and a datapath event dropped from the list (131 of 131 controls; six harness mutants). R4 by every source at 1x1/1if: 66.12 ms; my independent re-derivation (`receipts/rows/`, its constants from a compiled probe of the headers) gives the same to the hundredth at both points. The reviewers' figures reconcile exactly: R711-7's 58.18 ms is W less the row's own record with `floor(W/10) + 1` retries, R712-7's 58.94 ms the whole W with `floor(W/10) + 1`; neither counts the retry a window can hold before its first centisecond (on round 28's costs that rule gives 59.19 ms) |
| 7, 8 F2. The fan-out's resume and completion | `bdb0ae52`. A refusal is not a loss: `AECP_FAN_REFUSED` means the frame before was delivered, so the walk resumes at the refused frame's own recipient, or, for a completion queue with no room, past the last; `Core.ARefusedFrameIsSentToItsRecipientAndNoOneElseAgain` (a ring full at the second frame, a completion queue full after the last) asserts each recipient has the notice once, in order, at its own sequence_id, and refuses both of R711-7's planted defects. `fan_end` keeps a completion only for a walk that reached its last recipient (`whole`): a walk left owed at a recipient, lost or refused there, keeps none, and the resumed walk's end keeps the notice's one (Milan v1.2 5.4.5.2); `aecp_mbx.c`'s comment is true at the code. Driver test T6 (no completion after a mid-walk loss, exactly one after the resumed walk) and the core test's completion count, each refusing a plant that restores the old rule. The ratchet records `aecp_mbx.c`'s new branch (`6188ab6b`) |
| 8 S1, S2 | The receipts' `INDEX.md` is generated after every redaction and verified against the files present (`receipts/INDEX-verify.txt`). The load gate refuses `COLUMNS` with a name bound to the other column's table (`a column's name bound to the other's table`; 25 of 25 controls), and a harness mutant swaps them |
| 8 S3 | For #894: noted in the handoff, no change |
| 9. ACMP's poll at 1x1/1if | The pin move's redelivery makes the 1x1/1if ACMP item 11,359 CPU cycles at its heaviest (`backlog-owed`; the pin move measured 10,974), so `poll_grade.py` states it 120 us (65 before), and the load gate and the rows read it there, in both columns (`item.acmp`) |
| The first gate pass | At `7f50ee6a` it found three things this round's changes broke, fixed in `b2d39235`: the firmware-boundary gate refused `flip_grade.py`, which now named the SRP adapter's path (it reads it from `load_grade.RETRY_RULE`, a classified module); the C and C++ idiom gate found one new multi-declarator line in the AECP test's fan model; and the hooks self-test's "the plants apply" refused H-ACMP's two plants, whose anchor the pin move's redelivery had changed (re-anchored on the composed `on_frame`; the self-test shows each applies, 28 of 28 checks; the hooks harness's own run cannot build, at this head as at round 28's, so neither is shown caught by a run: a finding below). The full pass then ran again, once, at this head |
| 5. Gates | The full clean-clone pass at this head ([How to validate](#how-to-validate)) |

### The re-grade on the composed image

The legs at `2cc852fa`, the firmware's final tree (the later commits change only the harness's graders and tables, docs, and nothing a build records), each a fresh build on its own clean clone; then each regraded at this head with its build reused (`--reuse-build`, which refuses unless every recorded input resolves unchanged):

| Leg | Groups | Refusals | Budget misses | Work passes over the share | Heaviest work pass, CPU cycles | Least row margin |
|---|---:|---:|---|---|---|---|
| Arm A, 8x8/2if | 93 | 0 | 7 of 996 instances, 4 of 136 paths | 0 of 274,456 | 186,522 (`srp`), 13,478 under | 8.973 ms (11.027 ms, an AECP record in a save's verify window opened at the age limit) |
| Arm A, 1x1/1if | 94 | 0 | 7 of 945, 4 of 87 | 0 of 169,480 | 163,134 (`backlog-owed`) | 11.006 ms |
| The `answering-every-port` arm, 8x8/2if | 16 | 0 | 0 of 736 | 0 of 14,946 | 177,446 (`notice-every-2`) | 6.246 ms (13.754 ms, `notice-burst-2`) |
| The `answering-every-port` arm, 1x1/1if | 16 | 0 | 0 of 280 | 0 of 20,920 | 168,216 (`notice-every-3`), 31,784 under | 9.080 ms |
| Arm B's `aecp` group, 8x8/2if and 1x1/1if | 1 and 1 | 0 | 0 of 39, 0 of 25 | 0 of 136, 0 of 110 | 118,326 and 61,240 | |

The seven misses at each arm A point are round 28's six egress-held instances and the ACMP command behind the owed input, which the pin move's redelivery now answers (62.57 ms at 8x8/2if and 62.14 at 1x1/1if; unanswered before): the three rows of tsn-c-stack#26. Each save is durable within its stated worst case (8x8/2if `save-second` 22,110 ms against 22,150, `save-starved` 12,089 against 12,110; 1x1/1if 6,030 against 6,070 and 4,048 against 4,070). The heaviest work pass at 8x8/2if is 13,478 cycles under the share, round 16's 6,490 met at this layout (deferred to #890 by the round 28 ruling either way). **The costs** (round 26's parsers; each cost the larger of this measurement and the committed table's; `poll_grade.py`'s held unless a measured instance is over one): at 1x1/1if ACMP's owed frame 65 to 120 us, an SRP record and its retained retry 250 to 260, a centisecond 125 to 130; at 8x8/2if AECP's timer slot 95 to 100; in the column with tsn-c-stack#32, the walk's costs measured here: ACMP's owed frame 35 to 120 at 1x1/1if and 40 to 165 at 8x8/2if, the polls' base 245 to 285 at 8x8/2if. The cost controls: `notice-fan-out-as-it-was`, `polls-rebuild-in-the-base` and `polls-rebuild-twice` refused (an AECP item of 31,747 cycles against 27,000; a polls base of 70,031 against 28,000; a rebuild item of 100,273 against 63,000); `srp-compared-by-memcmp` escapes (below). The legs ran first on the oversubscribed session pool, and when the scratch volume filled, the unfinished groups of two legs ran again on another volume and GA8's `save-second`, whose log the full disk cut, ran again from the start; the evidence packet's handoff states each step.

**The load at this head** (`load_grade.py --check`, `flip_grade.py --check`):

| Point | Load at the pin | Load with tsn-c-stack#32 | Held by | Compute for 0.70 | Its three largest terms |
|---|---:|---:|---|---:|---|
| 1x1/1if | 0.486 | 0.483 | the load gate, 0.70 in both columns, for merge | 1.00x | SRP's channel 0.156, ACMP's records 0.053, the TICK's consumers 0.047 (with tsn-c-stack#32) |
| 8x8/2if | **0.816** | 0.767 | the flip check, 0.70 at the pin | 1.17x at the pin (1.10x with tsn-c-stack#32) | SRP's channel 0.219, ACMP's records 0.088, ACMP's owed frame 0.070 (at the pin) |
| 32x32/2if | 2.150 | 1.659 | reported: the more-compute image, #872 | 2.37x | SRP's channel 0.519, owed MRPDUs 0.299, THE TRANSMIT's builds 0.150 (with tsn-c-stack#32) |

**The rows by every source at this head** (`flip_grade.py --check`), each W in ms at this tree's pin, bold over its bound:

| Point | R4 (tier 1, 20 ms) | R5 (SRP, 90 ms) | R6 (SRP, 90 ms) | First queued notice (20 ms) | Last queued notice (125 ms) |
|---|---:|---:|---:|---:|---:|
| 1x1/1if | **66.12** | 35.95 | 28.67 | 20 | 22 |
| 8x8/2if | **346.15** | **144.15** | **135.80** | **22** | 62 |

The largest terms of 1x1/1if's R4: SRP's records ahead of AECP's 16.64 ms, the other channels' records 10.58, AECP's owed frames 7.14; the retained retries are 2.08 ms (round 28's model charged 9.00 at its once-a-pass rule). The independent re-derivation gives every solved row at both points to the hundredth (the evidence packet's `receipts/rows/`).

**Two findings, for the manager:**
- **The target platform's 8x8/2if image plans 59.5 RAMB36 against its ledgered 59.0** (ruling 6505997821), and has since at least round 27: its `rom` needs 128,264 B at this head (127,664 at `66f71326`, 127,544 at `e7e2b744`) against the 126,976 its 59.0 holds. Every link of it was refused first by the stale `ctrl_plat` key, and no gate links that image with its override, so its tiles were never read. The ledger stays 59.0; proposed issue text in the evidence packet (`PLATFORM-LEDGER-FINDING.md`).
- **The cost control `srp-compared-by-memcmp` escapes on this image**: the old comparisons planted give `notice-every-2` an SRP record of 35,908 cycles (37,494 on round 28's image), under the 36,500 its stated 365 us allows; unplanted the same group's is 32,866. The image made the record some 1,500 cycles cheaper, and the table rule keeps round 26's stated cost. Restating it from this image would refuse the plant but lowers a stated cost against the table rule: left for a ruling. The other three controls are refused.

### Round 28 (at `66f71326`)

**The ruling** (issuecomment-6805157674, on R711-6 and R712-6, both NEGATIVE at `e7e2b744`, MINOR only): the last round before S2b's merge, items 1 to 7 and nothing else.

| Item | At this head |
|---|---|
| 1. The merge gate at the pin (R711-6 F1 = R712-6 F1) | `5a19b0ca`. `load_grade.py --check` holds 1x1/1if in both columns, this tree's pin (the image that merges) and with tsn-c-stack#32 (the load the pin move owes), each at most 0.70 (`load_grade.COLUMNS`); a point over its ceiling is named with its column (`1x1/1if: the load L at the pin is over its ceiling 0.70`), and `--check` prints a `HELD` line for each. At this head 0.463 at the pin and 0.450 with tsn-c-stack#32, `RESULT: PASS`. A new control plants a pin-only rise (an ACMP record, a cost the donor's walk may state lower, raised to 2,000 us in the pin's column alone: the pin's load 0.807) and the gate must refuse it naming the pin's column: `--selftest` 24 of 24. R711-6's `probe_1x1_column.py` and R712-6's `probe_pin_1x1.py` now each print the refusal, `1x1/1if: the load ... at the pin is over its ceiling 0.70`. Section 13's margin names both columns |
| 2. Record commits (R712-6 F2) | `71e905fb`. A TX record holds whether the record mover carries it (`TX_MOVED` in `tx_ring.moving`), and its commit waits on the mover and judges its ERR only then: a record the word loop wrote never inherits an earlier ERR, which the mover holds until its next start. A failed move is reported for the record it carried: `mbx_tx_commit` is false, and `mbx_tx_begin`, which commits the record before its own, returns the new `MBX_STATUS_LOST` and starts nothing. The AECP fan port reports it for its frame (`enum aecp_fan`: TAKEN, REFUSED, LOST), from the next `fan` or from `fan_end`, which no longer discards its commit's result and keeps no completion for a lost last frame; `fan_out` resumes the notice at the recipient whose frame was lost and gives back the sequence_id it did not spend (IEEE 1722.1-2021 7.5.2; Milan v1.2 5.4.5.1). `mbx.h` states it. Tests: the driver's T4 (an ERR, then a frame off a word, sent whole and in halves, which must commit; then a frame on a word moved again) and T5 (the fan port over the DMA driver: the fan after a failed move LOST, nothing started; a failed last frame LOST from `fan_end`, no completion; each sent again), T2 extended; the AECP core's `ANoticeWhoseFrameWasLostSendsItToItsRecipientAgain` (a middle frame lost, reported by the next fan, and a last frame lost, reported by `fan_end`). Nine plants, each caught by its test's words (HANDOFF section 3). The image grows 112 to 120 B (8x8/2if arm A 122,328 to 122,440 B, the `answering-every-port` arm 122,636 to 122,748 B, each within its ledger). With tsn-c-stack#32, arm A's 8x8/2if image is 122,896 B, 58 RAMB36 against the 57.5 ledgered there: that column's 8x8/2if leg does not build at this head and keeps its committed costs, and the pin move that carries tsn-c-stack#32 meets the same ledger |
| 3. Round 16's margin at 8x8/2if (R711-6 F2) | Deferred to the 8x8/2if flip under #890, whose owner decision of 2026-11-11 sets that point's flip ceiling to 0.75; section 13 cites it. 1x1/1if keeps the margin: its heaviest work pass at this image is 160,618 cycles (`backlog`), 39,382 under the share. At 8x8/2if this image's heaviest is 192,237 cycles (`backlog`), 7,763 under the share, so the margin holds at this layout (round 26's image gave 193,609, 99 short): it moves with the image, which is why the ruling defers it. `flip_grade.FLIP` keeps 0.70 at this head: #890's decision applies the 0.75 in a change of its own once the pin moves |
| 4. Decision D's tier bounds (R711-6 F3) | `5a19b0ca`. `flip_grade.py --check` holds each point's flip to the rows by every source (`rows_grade.py`): R4 at tier 1's 20 ms, R5 and R6 at SRP's 90 ms, the first queued notice at 20 ms and the last at 125 ms, at 1x1/1if and 8x8/2if (`--point` for one). R4, R5 and R6 are round 22's method on this tree's pin costs (the smallest W in which the record's own work and every source's arrival bound fit, THE DRAIN as `ctrl_loop.h` states it, the grandmaster events at their IEEE 802.1AS-2011 intervals); the queued notices are `aecp_mbx.h`'s derived bounds, which the loop search holds. Self-test controls for each row at each point (over and within its bound), each source left out, the pin's column read, a planted queued-notice derivation and the bounds themselves: 129 of 129, and five harness mutants caught. **The 1x1/1if result, a finding:** R4 is 73.02 ms by every source against tier 1's 20 ms (+53.02 ms; its largest terms SRP's records ahead of AECP's, 16.50 ms, the other channels' records, 10.96 ms, and the retained retries, 9.00 ms): THE DRAIN takes SRP's records first, and round 23's tier design, a tier-1 record served before any tier-2 work, is not built. R5 is 37.19 ms and R6 32.69 ms within SRP's 90; the first queued notice is held at 20 ms, its bound, and the last at 22 ms within 125. So `flip_grade.py --check --point 1x1/1if` exits 1 at this head, and the 1x1/1if flip cannot pass it until R4 fits; the finding is #894's (the tier rows, model first). **Superseded:** these rows charged SRP's retained retry once a pass and cut SRP's window by AECP's whole burst; round 29 corrects both ([Round 29](#round-29)), and 73.02 ms is not this head's figure. The flip at 1x1/1if must pass `flip_grade.py --check --point 1x1/1if`; 8x8/2if stays with #890 (R4 489.97 ms, R5 162.96 and R6 149.57 ms by every source, the first queued notice stated at 22 ms against tier 1's 20 and the last at 62 within 125) |
| 5. Portable C (R711-6 F4) | `24ea9c04`. `_Alignas(64)` for the AECP response buffer (`alignas(64)` where a C++ test reads `aecp.h`, which g++ requires); `noinline` and `may_alias` behind `CTRL_CC_GNU` in `sw/firmware/ctrl/plat/ctrl_cc.h`, outside the protocol code, with a portable C11 fallback (nothing for `CTRL_CC_NOINLINE`, `memcpy` for the pool's link). `git grep __attribute__ -- sw/firmware/ctrl ':!*/test/*'` shows only that header, and a new firmware arm, `portable`, holds it: a scan for `__attribute__` and `__builtin_` outside `test/` but `ctrl_cc.h`, and the port arm's tests built with `CTRL_CC_GNU=0`. A pool test that can fail for an unwritten link (`Pool.P10`) and three plants. The change alone is image-neutral: `e7e2b744` with it builds 8x8/2if arm A's three images byte-identical to round 27's (objcopy sha256 `5b2317d8...`, `be42e7c9...`, `57b60044...`) and its `control` group's log byte for byte, so it restates no cost |
| 6. Docs and residue | R712-6 F3's sentence (152 B at the pin and 160 B with tsn-c-stack#32); the new harness comments' issue-comment IDs and round labels replaced by the issue and the behaviour; #890 and #891 named where this body said "the flip-gate issue" and "its own issue", and at the harness's unknown command (`answers.py`) |
| 7. Gates | The full clean-clone pass at this head, once ([How to validate](#how-to-validate)): every gate rc 0 but the flip check, which exits 1 by design; `elaborate-gates-1` ran twice, its first run's LiteX simulation timing out under the session pool's load |

**The re-grade on round 28's image** (item 7; the legs at `71e905fb`, every group of arm A and of the `answering-every-port` arm at both points, arm B's `aecp` group and the column with tsn-c-stack#32 at 1x1/1if; then regraded at the head):

| Leg | Groups | Refusals | Budget misses | Work passes over the share | Heaviest work pass, CPU cycles | Least row margin |
|---|---:|---:|---|---|---|---|
| Arm A, 8x8/2if | 93 | 0 | 6 of 996 instances, 3 of 136 paths | 0 of 272,475 | 192,237 (`backlog`), 7,763 under | 6.515 ms (13.485 ms, an AECP record in a save's verify window opened at the age limit) |
| Arm A, 1x1/1if | 94 | 0 | 6 of 945, 3 of 87 | 0 of 184,496 | 160,618 (`backlog`) | 10.434 ms |
| The `answering-every-port` arm, 8x8/2if | 16 | 0 | 0 of 736 | 0 of 14,350 | 186,213 (`notice-every-2`) | 4.018 ms (15.982 ms, `notice-burst-6`) |
| The `answering-every-port` arm, 1x1/1if | 16 | 0 | 0 of 280 | 0 of 22,114 | 160,222 (`notice-burst-6`) | 8.349 ms |
| Arm B's `aecp` group, 8x8/2if and 1x1/1if | 1 and 1 | 0 | 0 of 39, 0 of 25 | 0 of 131, 0 of 110 | 119,134 and 63,670 | |
| Arm A with tsn-c-stack#32, 1x1/1if | 19 | 0 | 6 of 141, 3 of 81 | 0 of 10,249 | 156,237 (`backlog-adp`) | |

The six misses at each arm A point and with tsn-c-stack#32 are the three egress-held paths of tsn-c-stack#26, as in round 27. Each save is durable within its stated worst case (8x8/2if `save-second` 22,110 ms against 22,150; 1x1/1if 6,030 against 6,070). **The costs** (round 26's parsers, each cost the larger of this measurement and the committed table's): no cost at the pin moves at either point, nor `poll_grade.py`'s; with tsn-c-stack#32 at 1x1/1if ACMP's timer slot rises 165 to 170 us and THE TRANSMIT's build 910 to 920 (`66f71326`), which leave that column at 0.450. The four cost controls are refused on this image (an AECP item of 29,968 cycles against 27,000; an SRP record's apply of 37,494 against 36,500; a polls base of 74,399 against 28,000; a rebuild item of 113,443 against 63,000).

**The load at round 28's head** (as its gates then stood):

| Point | Load at the pin | Load with tsn-c-stack#32 | Held by | Compute for 0.70 | Its three largest terms |
|---|---:|---:|---|---:|---|
| 1x1/1if | 0.463 | 0.450 | the load gate, 0.70 in both columns, for merge | 1.00x | SRP's channel 0.150, ACMP's records 0.053, the TICK's consumers 0.047 (with tsn-c-stack#32) |
| 8x8/2if | **0.815** | 0.719 | the flip check, 0.70 at the pin | 1.16x at the pin | SRP's channel 0.219, ACMP's records 0.088, ACMP's owed frame 0.070 (at the pin) |
| 32x32/2if | 2.150 | 1.659 | reported: the more-compute image, #872 | 2.37x | SRP's channel 0.519, owed MRPDUs 0.299, THE TRANSMIT's builds 0.150 (with tsn-c-stack#32) |

**The rows by every source at round 28's head** (superseded by round 29's rules):

| Point | R4 (tier 1, 20 ms) | R5 (SRP, 90 ms) | R6 (SRP, 90 ms) | First queued notice (20 ms) | Last queued notice (125 ms) |
|---|---:|---:|---:|---:|---:|
| 1x1/1if | **73.02** | 37.19 | 32.69 | 20 | 22 |
| 8x8/2if | **489.97** | **162.96** | **149.57** | **22** | 62 |

Each W in ms by every source at this tree's pin; bold misses its bound. The largest terms of 1x1/1if's R4: SRP's records ahead of AECP's 16.50 ms, the other channels' records 10.96, the retained retries 9.00.

### What holds at this head

The acceptance of this lane's assignment (S2b, #665: the split firmware within T_svc, cycle work in firmware, owner decision D4 a), read at this head:

- **The rows by measurement** (the CPU budget harness on the composed image, every group of arm A and of the `answering-every-port` arm, and arm B's `aecp` group, at 1x1/1if and 8x8/2if): every row is within its bound except the three egress-held rows of tsn-c-stack#26 (`backlog.owed`, `backlog.owed_behind0` to `3`, `backlog-owed.service.aecp.last`, and the ACMP command behind the owed input, `backlog-owed.service.acmp.last`, which the pin move's redelivery now answers at 62 ms): 7 misses of 996 probe instances in 93 groups at 8x8/2if, and of 945 in 94 groups at 1x1/1if. 0 refusals, no `STATED` line, every row's response the one it states. The `answering-every-port` arm: 16 groups at each point, 0 misses of 736 and 280, every queued notice within its bound. Arm B's `aecp` group: 0 misses of 39 and 25.
- **The pass share** (2.0 ms): 0 of 274,456 work passes over it at 8x8/2if and 0 of 169,480 at 1x1/1if; 0 of 14,946 and 0 of 20,920 in the `answering-every-port` arm. The heaviest at 8x8/2if is 186,522 cycles (`srp`), 13,478 under, round 16's margin met at this layout and deferred to #890 by the round 28 ruling; at 1x1/1if 168,216 (`notice-every-3`), 31,784 under.
- **The bounds that hold by construction:** the queued notices at `aecp_mbx.h`'s stated bounds, which the loop search holds the loop to (the first 22 ms at 8x8/2if and 20 at 1x1/1if; the last 62 and 22 ms within their 70 and 25 ms ceilings); every pass's polls base and each heavy item within its stated cost (`poll_grade.py`), each SRP record's own apply within its retry's, every round within its own (`round_grade.py`), and every pass given whole to a build or an aged step within its own (`whole_grade.py`), each a gate over every group at both points.
- **The long-window load:** 1x1/1if within its ceiling in both columns, held for merge; 8x8/2if over it, held by the flip check.
- **Decision D's tier bounds by every source, for the flip:** at 1x1/1if R5, R6 and both queued notices fit.
- **What does not hold:** 1x1/1if's R4 by every source (66.12 ms against tier 1's 20, #894); at 8x8/2if R4, R5 and R6 by every source and the first queued notice (22 ms against 20), with #890 and #894; every row at 32x32/2if; the long-window load at 8x8/2if; the platform image's 8x8/2if ledger (59.5 against 59.0); and the cost control of the SRP record cut on this image.

### The round histories

Rounds 12 to 27's Description sections, and the decisions their Known limitations listed, are in the evidence packet `evidence/ROUND-HISTORIES.md` (round 27's moved there in this round, as round 28's body gave it).

## Authoritative references

- The ruling on round 28 (#665 issuecomment-6813183455); R711-7 (#810 issuecomment-6813519183) and R712-7, the reviews it folds in; the pin move's REVIEW READY (#665 issuecomment-6813799445) and PR #892; #894 (the tier rows); #890 and its owner decision of 2026-11-11; #891.
- Decision D (#665 issuecomment-6759183115 and issuecomment-6759193032) and the round 23 ruling (issuecomment-6732443213: tier 1 20 ms, SRP 90 ms, the last queued notice 125 ms; the every-source count is the bound).
- IEEE 1722.1-2021 7.5.2 (a notice to each registered controller, its own sequence_id) and 9.2.1.1; Milan v1.2 5.4.5.1 and 5.4.5.2 (the counters' notice and its holdoff). The record mover's register contract (`sw/firmware/ctrl/plat/mbx_dma.h`) and `hdl/milan/mailbox/KL_mbx_dma.sv`.
- `sw/firmware/ctrl/srp/srp_mbx.c` (the retained receive and its retry: `retry_spent`, `SRP_RX_RETRY_MS`); `sw/mailbox/mailbox.yaml` (each channel's `rate`, `tick_ms`, `event_types`, `counters_changed`).
- The protocol timers the arrival bounds cite: Milan v1.2 5.5.2.3 and Table 5.26, 5.6.3.5.3, 5.6.3.5.9 and Table 5.50, 5.6.4.5, 5.4.5.2 and Table 5.22, 5.4.5.3; IEEE 1722.1-2021 6.2.2.5; IEEE 1722-2016 B.3.4.1, B.3.4.2 and Table B.8; IEEE 802.1Q-2018 10.7.4.1 and Table 10-7, Milan v1.2 Table 4.3; IEEE 802.1AS-2011 (+Cor1/Cor2) 10.7.2.2, 10.7.3.2 and 11.5.2.2, the edition Milan v1.2 profiles.
- `docs/design/SPLIT_CONTROL_MEMORY.md` sections 3 and 5 (the ledger) and 13 (the long-window load, the rows by every source); `docs/design/MAILBOX_SPLIT.md` (the ACMP pass bound and the service tables); `tb/verilator/ctrl_service_budget/README.md`; `sw/firmware/ctrl/README.md`, `sw/firmware/ctrl/aecp/README.md`; `sw/firmware/ctrl/aecp/aecp.h` and `aecp_mbx.h`; `sw/firmware/ctrl/loop/ctrl_loop.h`; `docs/reference/FR_NFR.md` 3.4.1.

## How to get into the same state

```sh
git fetch origin
git checkout b2d39235ab9bba85d7e560b5f5f78fb4be528960
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
python3 -B sw/firmware/ctrl/test/ctrl_hot.py --check
python3 sw/litex/test_ctrl_memory.py
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 0/4
python3 sw/firmware/gtest/fw_coverage.py --check
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir /tmp/budget-8x8 --record-budget-findings --record-share-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir /tmp/budget-1x1 --record-budget-findings --record-share-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir /tmp/budget-8x8-notice --variant answering-every-port --record-budget-findings --record-share-findings
```

Expected result at this head:
- `load_grade.py --check` prints the load table and exits 0 (`RESULT: PASS`) with `HELD 1x1/1if at the pin: the load 0.486, its ceiling 0.70` and `HELD 1x1/1if with tsn-c-stack#32: the load 0.483, its ceiling 0.70`. `--selftest`: `load gate: 25 of 25 planted controls refused`.
- `flip_grade.py --selftest` exits 0, `flip check: 131 of 131 planted controls refused`. `flip_grade.py --check --point 1x1/1if` exits 1, `OVER 1x1/1if R4: by every source 66.12 ms, over its bound 20 ms; the largest term srp 16.64 ms`, and prints no rule finding: the finding #894 holds. `flip_grade.py --check` exits 1 by design, 8x8/2if's load and rows over with them: it is no merge gate.
- The harness self-test reports 0 failures, 207 mutants caught (six new).
- `ctrl_hot.py --check`: `hot list: 207 entries, in the recorded order`. `test_ctrl_memory.py` PASS, the size fixture's entry at 58.0.
- The firmware gate PASS; `fw_coverage.py --check` PASS over 39 files.
- The 8x8 and 1x1 runs: as the re-grade's table above (0 refusals, no pass over the share, no `STATED` line, every row within its bound but the three egress-held rows of tsn-c-stack#26).

The evidence at this head, each on a clean clone of it, never piped:

- **Every `run:` step of the four workflows a pull request to `dev-soft-core` triggers**, each job on its own fresh clone: 139 steps ran, every one rc 0, 0 steps without an rc or a reason; 226 are not run, each with its reason (hosted orchestration, artifact upload and collection, apt and sudo installs whose pinned tools this host carries, `physical-gptp`, which runs only on a schedule, and `rtl.yml`'s `verilator-shards` suites, which run here as the full sweep below).
  - `rtl-fast.yml`, all 14 jobs: `changes`, `verilator-lint`, `bdd-conformance` (508 scenarios and 2,330 steps passed), `yosys-tool`, `yosys-elaboration`, `publication-census`, `split-cdc`, `rtl-fast`; `firmware-unit` (`test_ctrl_firmware: PASS`; the saved-state store gate; `fw_coverage.py --check` PASS over 39 files); `firmware-control-mutants` (696 of 696 caught), `firmware-aecp-mutants` (227 `[ok]`), `firmware-srp-mutants` (340 `[ok]`); `firmware-boundary` and `firmware-verilator` (`ctrl_boundary: PASS`, 0 findings).
  - `rtl.yml`: `full-ci-gate`, `yosys-tool`, `yosys-shards` 0/4 to 3/4.
  - `elaborate.yml`: `elaborate-gates-0`, `elaborate`, and `elaborate-gates-1` (its first run's LiteX simulation aggregate exited 92: `test_soc_timing_cuts` passed its 900 s wall clock on the loaded session pool, result unknown, 7 of 8 passed, 0 failed; the job ran again on a fresh clone and a booked range, every step rc 0, 8 of 8 passed; both runs' logs are kept).
  - `docs.yml`: `wire-accountability`, `docs-check-no-git` (the job removes `.git`, so the runner's own tree check after it cannot run), `docs-gates-0`, `docs-gates-1`, `docs-gates-2`, `docs-check`.
- **The full sweep**, `scripts/run_all_suites.sh` as four shard units on clean clones and booked ranges: 65 suites, 65 passed, 0 failed, 0 timed out, 2,613,726 checks, 0 in-suite failures; every shard's preflight passes (suite cancellation among them), so no re-run; the shard holding `capture_coherence` on four CPUs. In one shard the `tsn_fuzz` campaign rewrites the date stamp of two `TEST_RESULTS.md` files in place, as before.
- **The lane's own gates** on clean clones: `git diff --check` against the merge base `1d6bf555` and against round 28's head; `check_py_idiom.py`, `check_cpp_idiom.py`, `check_baremetal_only.py --check`, `docs_check.py` (0 findings); `ctrl_hot.py --self-test` and `--check`; the harness self-test (`self-test: 0 failures`, 207 mutants caught); `load_grade.py --selftest` (25 of 25) and `--check` (PASS, both columns held); `flip_grade.py --selftest` (131 of 131) and `--check`, `--point 1x1/1if` and `--point 8x8/2if` (each exits 1, as above); the independent re-derivation of the rows (each solved row equal to the flip check's to the hundredth); R711-7's fan-out probe (its refused-mid-walk plant fails the new refusal test), R712-7's rows re-derivation and column probe (the swap now refused), and R711-6's and R712-6's column probes (each pin-only rise refused); `ctrl_service_hooks` (28 of 28 checks, 96 of 96 mutants) and `nvm_split_target` self-tests; `test_ctrl_nvm.py --require-rv32 --self-test` (121 planted defects reddened); `gen_mailbox.py --check --crosscheck` and `--selftest`; `lint_rtl.py --check`; `test_soc_options.py`; `test_ctrl_memory.py`; `test_builder.py --require-rv32` (every gate passes; the same two arms as before do not run, each with the tool's reason); `ctrl_split_boot` at 1x1 and 8x8 (PASS, 0 findings), its native controls and its plants; `cd tests && behave` (508 scenarios, 2,330 steps passed); `make -C tb/verilator/milan_dp twin`. Each clone's tree is clean after them.
- **The harness at both points**: this head changes a test file in a tree the harness's builds digest, so each leg was built fresh at this head with one sample group: every image byte-identical to the leg's build (objcopy and ELF) and every sample log byte-identical; every recorded group of arm A, of the `answering-every-port` arm and arm B's `aecp` group at 1x1/1if and 8x8/2if then regraded against the fresh build: 0 refusals; 7 misses of 996 probe instances (4 of 136 paths) at 8x8/2if and of 945 (4 of 87) at 1x1/1if; 0 of 274,456 and 0 of 169,480 work passes over the share; the notice arm 0 of 736 and 0 of 280; arm B 0 of 39 and 0 of 25.
- **A first pass** at `7f50ee6a`, this head's parent, found the three things `b2d39235` fixes ([Round 29](#round-29)); the pass above is the one at this head.

## Known limitations / out of scope

- **Round 29's decisions, for the owner and the manager:**
  1. **The tier rows stay red** ([#894](https://github.com/kebag-logic/milan-fpga/issues/894)): 1x1/1if's R4 by every source is 66.12 ms against tier 1's 20, with the corrected retry and window; THE DRAIN takes SRP's records ahead of AECP's. #894 itemises every term at both points first.
  2. **The retained record's hold is out of SRP's rows' scope** (R712-7 F1's question): SRP's storage rule (up to `SRP_RX_RETRY_MS` a refused record) is not the CPU's service; R5 and R6 count neither the hold nor the retry, R4 counts the retry. If the hold is ruled in scope, R5 and R6 carry up to 31 records x 1,000 ms, no W under 2,000 ms.
  3. **The platform image's 8x8/2if ledger**: it plans 59.5 RAMB36 against its ruled 59.0, since at least round 27, unseen while its `ctrl_plat` key was stale; proposed issue text in the evidence packet (`PLATFORM-LEDGER-FINDING.md`).
  4. **The SRP record cut's cost control escapes on this image**: the old comparisons cost 35,908 cycles in `notice-every-2`, under the 365 us the table rule keeps (this image's unplanted record there is 32,866). A ruling on restating that cost from this image's measurement would restore it.
  5. **The hooks harness's own run cannot build** (pre-existing, at round 28's head too): it links a provisional target-platform image with no flash map, which the image tool refuses. Its self-test, the lane's gate, passes; proposed for an issue of its own.
  6. **8x8/2if waits on #890**: its load (0.816 at the pin), its rows, round 16's margin there and the 0.75 flip ceiling #890's decision sets in a change of its own; this head keeps `flip_grade.FLIP` at 0.70.
- **Round 28's decisions, where round 29 leaves them:** the 8x8/2if column with tsn-c-stack#32 is measured here (the pin carries #32, and the fixture's ledger is 58.0).
- **Live `dev-soft-core`** has moved since the merge base `1d6bf555` to `38967e26` (PRs #874, #880, #889); `git merge-tree` reports conflicts with this head in seven paths (`SPLIT_CONTROL_MEMORY.md`, `ctrl_nvm`'s README, `nvm_store.c` and `nvm_mutants.py`, `gtest`'s README and ratchet, `ctrl_memory.py`). The candidate merge is the manager's.
- **Suggestions carried, not taken:** R711-7 S2 (a lost notice frame re-sent every pass under a persistent mover ERR, with no bound) for an issue of its own; R711-7 S3 to S5 and R712-7 S3 (the rows' AECP records a pass, `drained`'s assumption, the walk inside `CTRL_LOOP_TICK_US`, the notices the records ahead cause) for #894's itemisation; R711-7 S6 (a resume across interfaces) not taken.
- **The datapath change records** (COUNTERS_CHANGED, AVB_INFO_CHANGED, AS_PATH_CHANGED, AMAP_LIVE_WRITE) are excluded from the rows with the reason: no group stages them, so no cost is stated; #894 stages them.
- **`AECP_NOTICE_US`** (365 us at two interfaces) and **`AECP_NOTICES_MOST`** (40 at two interfaces, against 136 in the 32x32/2if model, #866) are unchanged.
- **No group stages** a retained record's retry, an owed MRPDU or a registration's probe, nor a failed record move (the driver and AECP tests do): each is stated at the cost of the measured work that holds it.
- **The three egress-held rows** stay with tsn-c-stack#26.
- **No fabric option outlives the switch-over:** nothing here adds one.
- The earlier rounds' decisions for the owner and the manager are in `evidence/ROUND-HISTORIES.md`.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (#665 stays open: this lane is one part of it)
- [x] New or changed behavior has self-checking tests (the core test of a refusal against a loss, the lost-frame test's completion count, driver test T6, four firmware plants; the rows' rule checks, six rule controls and six harness mutants; the load gate's column binding control)
- [x] Required local verification bar passes (the full pass at this head, every gate rc 0 but the flip check, which exits 1 by design)
- [ ] Self-test evidence is posted in a PR comment
- [ ] No undocumented requirement or interface change remains (the tier rows await #894; the 8x8/2if flip awaits #890; the platform image's 8x8/2if ledger and the SRP cut's control await a ruling)
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed (`aecp.h`'s fan port, the AECP and firmware READMEs, `MAILBOX_SPLIT.md`'s service tables, section 3's and 5's ledger, section 13's rows, re-grade and load, the harness README)
- [ ] Post-merge containment will be checked before the Issue moves to Done
