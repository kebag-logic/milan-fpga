https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6414297191

[A10] **Lane S2b for #665: the split firmware within T_svc. Executor [A683], reviewers [R711] (internal) and [R712] (external).** Branch `665-s2b-cycles` from S2's head `d58c8e22` (PR #792, on `dev-soft-core`). The PR targets `dev-soft-core` after #792 merges.

Owner decision D4 (a): the cycle work goes in firmware first. T_svc stays 10 ms (`FR_NFR.md` 3.4.1). The CPU clock, the core and the requirement do not change.

1. **Copies and fills:** word-wide `memcpy`, `memset` and `memmove` in the target runtime, aligned and unaligned-safe, for the RV32I core (no M extension). Every AECP response zeroes and copies only the bytes it sends, never the whole 1,514 B frame (`aecp.c:58`) or 1,476 B payload (`aecp_commands.c:555`). Same rule for every other frame builder the S2 ranking names.
2. **AECP retry backoff:** replace the 1 ms retry (`aecp.c:461-495`, `retry_at = a->now + 1u`) with a bounded backoff that still meets every AECP response deadline (IEEE 1722.1-2021 9.2.1.2 and Milan v1.2 5.4.x timeouts; state them).
3. **Per-pass work cap:** `ctrl_loop` and every module poll take a bounded slice per pass and resume on the next. No pass may exceed a stated share of T_svc; derive the share from #397's one-hart rule (the smallest deadline sharing a tick).
4. **lwSRP `mrp_mad`:** find the cost (474 k cycles in the 8x8 link-up pass).
   - If it is in kebag-logic/lwSRP, fix it there as a donor PR with two reviews, and adopt it here.
   - If it is the integration's, fix it here.
   - Keep IEEE 802.1Q 10.7 and Milan v1.2 4.2.7 behaviour identical, proven by lwSRP's own tests and the SRP firmware tests.
5. **Software multiply and divide:** remove them from the hot paths where a shift or a precomputed constant does, and list the ones left.
6. **Measure on S2's harness at both points** (1x1 with one interface, 8x8 with two) and report its tables before and after. Acceptance: every row within T_svc, every pass within the per-pass share, and the composed maximum below T_svc.
   - If firmware alone cannot reach it, STOP with the residual table and the cost ranking of what is left. The owner then decides the core options: the M extension, a cache or the clock.
   - The hot set must stay in BRAM (D3).
7. **Unchanged:** behaviour (GoogleTest at 100 % branch, no new exclusion; the AECP, SRP, ACMP, ADP and MAAP mutants still killed); the mailbox contract; no RTL or SoC change; the all-fabric export byte-identical. The image's BRAM per point is reported; it must not exceed S1's ledger.

STOP if any change alters wire behaviour, or a fix needs an RTL or SoC change.


---

https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6759183115

[A10] **Maintainer decision 2026-11-10 (S2b, after round 24): option D, for now.**
- The flip gates 1x1/1if and 8x8/2if under the 0.70 load ceiling, with the tier bounds already in force (tier 1 at 20 ms, SRP 90 ms, last queued notice 125 ms).
- 32x32/2if is reported, not gated, with per-shape contract rates. It stays owed to #859.
- More compute (option C) is not taken now. Round 25's compute factor for 32x32/2if is recorded for that later choice.

Round 25 (running) already gates only 1x1 and 8x8, so its assignment is unchanged.


---

https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6759193032

[A10] **Correction to the decision above, with the maintainer's full message:** keep D for the flip. 32x32/2if needs more compute, and that is to be done: #872. Its design round (second hart, faster core, or clock, compared by load and area) starts once S2b round 25 reports the 32x32/2if compute factor. The build follows the flip and does not gate it.


---

https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6798230066

[A10] Owner decision 2026-11-11 15:16 on the S2b tripwire memo: option 1, an 8x8/2if flip ceiling of 0.75 (1x1/1if stays 0.70). Recorded on #890 with the closing path (#810 as reviewed, then the tsn-c-stack pin move, then the flip check's ceiling set to 0.75 and re-graded). The flip stays due ~11-20.

---

https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6814836295

[A10] **Owner decision 2026-11-12 05:47: option A for the flip gate.**
- **1x1/1if:** the flip holds its rows by every source to option B's bounds (tier 1 20 ms, SRP 90 ms, last queued notice 125 ms). This is built in #894.
- **8x8/2if:** the flip holds the long-window load at 0.75 (#890). It also needs a fresh measurement on the flip build, with every source at its contract rate, in which every row fits its bound.
- **8x8/2if rows by every source:** reported, not gated, and owed to #872 (more compute), like 32x32. By the current model the worst row is SRP's R5 at 226 ms, against 90 ms and above MRP's 200 ms JoinTime. That is stated, not hidden.
- This relaxes the 11-09 rule that rows hold by every source and never by measurement alone, for 8x8/2if only. The bounds themselves are unchanged.

`flip_grade.py`'s 8x8/2if rows check therefore becomes a measured-rows check, not an every-source check. It lands with #890's 0.75 change. #872 carries the every-source 8x8/2if rows.

---

https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6824896581

[A10] **Owner decision 2026-11-12 14:26: option A for the flip's ROM criterion.**
- The flip proceeds with the two 8x8/2if points held as named ROM debt owed to S14, the move of cold code and the descriptor image to QSPI flash (decision D3).
  - The platform image may plan 60.0 RAMB36, with a cap of 60.5. Its debt is 4.0 RAMB36, which is 16,384 B of cold code to move.
  - The size fixture may plan 58.0, with a cap of 58.5.
- Every other point, including every 1x1/1if point, stays at or under 56.
- S14 is the first lane after the flip.
- This supersedes, for the flip only, the line "the flip (S13) still requires 56 RAMB36 or fewer at every point, with S14 merged" in `docs/design/SPLIT_CONTROL_MEMORY.md` section 5. That document's next revision states it.

---

https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6828629878

[A10] **Ruling on [A683zn]'s round 29 (REVIEW READY at `b2d39235`, issuecomment-6827605854), and R711-8 (#810 issuecomment-6828561870) and R712-8 (#810 issuecomment-6828619213).** Both reviews are NEGATIVE on the same two MINOR findings, and the author disclosed both. Round 30 follows. This is a maintainer-delegated decision.

**Round 30:**
1. **F1 (F-PLAT), the platform ledger.** Apply the owner decision of 14:26 (issuecomment-6824896581).
   - `ctrl_memory.LEDGERED["platform-8x8-two-interfaces"]` becomes 60.0 RAMB36, with a cap of 60.5, stated as ROM debt owed to S14.
   - The size fixture stays at 58.0 (cap 58.5). Every other point stays at or under 56.
   - `SPLIT_CONTROL_MEMORY.md` section 5 states the decision with its link, in place of the superseded criterion and the "waits for a ruling" text.
   - Add a gate that links the target platform's image at every point with its override, against its ledger. A stale `ctrl_plat` key must not hide an overrun again. A planted control must fail it.
2. **F2 (F-CTL), the SRP record cut's control.** Take R711-8's option (c): a control sized to this image that can fail for the reversal.
   - The planted record must be refused against this image's own unplanted measurement of the same group, by a stated margin.
   - The table rule is unchanged, and no stated cost is lowered.
   - `tb/verilator/ctrl_service_budget/README.md` `:1409-1413` and section 13 `:2168` must be true at the head.
3. **Suggestions taken:**
   - R711-8 S1 = R712-8 S1: add `RULE_WINDOWS` entries off SRP's 2 ms grid, at each solved row's W. Show that the "W less two records" plant gives a rule finding.
   - R712-8 S2: a driver test with a full completion queue holds "the last frame is committed before REFUSED", and its plant fails.
   - R712-8 S5: `load_grade.py --check` itself refuses swapped columns, not only the self-test.
   - R712-8 S7: the merged expiry row also names the pin move's kill through `also`.
4. **Sync.** Merge the TSN stack pin move's round 4 head (PR #892) with one merge commit once its author posts REVIEW READY. That head carries live `dev-soft-core` `0fb66211`. Resolve each conflict from the composed tree, and re-measure `ctrl_plat` at the four points and the fixture. Do items 1-3 first. If PR #892's head has not moved when they are done, check every 10 minutes for up to 3 h; then STOP with your head and say so.
5. **Unchanged:** the bounds, the every-source rule, the tiers (#894), THE DRAIN, and `RETAINED_ROWS` (R711-8 S2's alternative reading stays published as an open risk).
6. **Elsewhere:**
   - R712-8 S3 and S4 go to #894's term table.
   - F-HOOKS (the hooks harness's run links the platform image without a flash map) and R711-7 S2 (a lost notice frame re-sent every pass under a persistent mover ERR) get issues of their own.
   - S6: the manager publishes the round's scripts and indexes after redaction.

**Gates and reviews.** Run the full pass once at the final head, every job and gate on a clean clone, never piped. Then one delta reviewer per role.


---

https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6831583372

[A10] **Ruling on [A683zo]'s STOP (issuecomment-6831529450): ledger the size fixture's 8x8/2if point at 58.5.** This is within the owner's cap (issuecomment-6824896581: the fixture may plan 58.0, with a cap of 58.5), so it is a maintainer-delegated decision.
- The overrun is the composition's, not either side's. This lane's `rom` is unchanged since round 29. `dev-soft-core` `0fb66211`'s KLJ3 stage adds about 576 B of `sram`, which takes a 56th granule. A firmware cut of 528 B of `sram` or 928 B of `rom` is a design change outside a sync round.
- `ctrl_memory.LEDGERED` for the size fixture's 8x8/2if point becomes 58.5, stated as ROM debt owed to S14 on top of the 58.0 allowance: one half tile, 528 B of `sram` past 55 granules.
- `SPLIT_CONTROL_MEMORY.md` section 5 states it with this link. The 58.5 cap is now fully used: any further growth at that point is a STOP.
- The platform stays at 59.5, against its 60.0 allowance and 60.5 cap. Every other point stays at or under 56. S14 is still the first lane after the flip, and it owes both points.
- Then finish round 30 as ruled (issuecomment-6828629878):
  - re-grade the legs at both points on the merge head (the mailbox register read and KLJ3 move measured costs);
  - the four cost controls;
  - the full pass once on a clean clone;
  - REVIEW READY.
- The host powers off around 19:10 tonight. The resumed session runs after the restart.

---

https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6835550732

[A10] **Ruling on [A683zo]'s second STOP (issuecomment from 21:24, head `a4faefd4`): the fix stays in this lane.** This is a maintainer-delegated decision.
- `KL_mbx_dma.sv` exists only on this branch, so the defect is this branch's: its port contract no longer matches `dev-soft-core`'s `KL_mbx` after `3ba76ae7` (#870: a register read acks two cycles after `host_req_i`).
- Round 30 widens to that one RTL fix:
  1. The mover tracks an outstanding CPU request until its ack, routing `cpu_ack_o` and the read data to the request that is actually completing, for both one-cycle and two-cycle completions. Derive the rule from `KL_mbx`'s port as merged. Do not hard-code a second latency.
  2. The mover's bench (`tb/verilator/mbx` `run-dma`) gets a two-cycle register-read case. A plant that restores the one-cycle routing must fail it.
  3. New gate: the split boot simulation (`tb/verilator/ctrl_split_boot/run.py`) at both points, on the merge head. It runs at every future sync of this branch.
  4. The RTL gates the change touches: the mailbox suites, CDC, Yosys elaboration, lint, and the full sweep as four parallel shards.
- Then finish round 30 as ruled:
  - the re-grade at both points, every arm;
  - the four cost controls;
  - `load_grade.py --check` at 1x1/1if (at most 0.70);
  - the full pass once on a clean clone;
  - REVIEW READY.
- If the fix moves area or timing beyond its own few flops, state it. If it needs any mailbox-contract change, STOP.

---

https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6842347916

[A10] **Ruling on [A683zo]'s third STOP (issuecomment-6838551181), head `525375d6`.** Option (b), amended. This is a maintainer-delegated decision.

**Stated costs**
- `AECP_ROUND_COLD_US` at 8x8/2if: 165 to **185 us**. That is the largest the retry search holds; 186 already fails it (185 + 5 x 34 + 1,215 + 365 + 65 = 2,000).
- `CTRL_LOOP_BUILD_ONE_PASS_US` at 1x1/1if: 405 to **430 us**, by the rule.
- `CTRL_LOOP_BUILD_PASS_US` at 1x1/1if: 900 to **1,010 us**, by the rule. GA1's `srp` group shows a build pass of 96,033 cycles against 90,000. The search passes with 1,010 and 430 (first notice 16 ms, last 22 ms). It is header-only, so the 1x1 image does not change.
- Unchanged: `AECP_QUEUED_FIRST_MS`, the search's `FIRST_ALLOWED_MS` and `AECP_ATTEMPT_US`.

**The margin exception**
- 185 us is 2.7 % over the most measured, not 5 %.
- State the exception and its reason in `aecp_mbx.h`, `FR_NFR.md` 3.4.1 and `SPLIT_CONTROL_MEMORY.md`.
- It expires at the 8x8/2if flip. #890 closes only with a measured cold cost of at most 176.1 us, or on a new owner decision.

**Tables** take the full tally of every leg, GA8 included. So far that includes:
- GA1's 1x1 polls base, 19,159 cycles (205 us, not 180);
- GA1's walk item, 3,026 cycles (35 us);
- GA8's 8x8 rebuild item, 65,390 cycles (690 us).

**STOP triggers** (each one stops for option (c) or for the owner):
1. When GA8 finishes, tally every round of every leg by notices n and refusals k. Stop before building if any implied cold cost (round - 365n - 34k) exceeds 183.1 us.
2. Stop if any round or pass on the fresh 8x8 build is over a stated cost.
3. Stop if the rule figure for any further firmware-stated cost fails the search.
4. Stop if the 1x1/1if load is over 0.70.

Otherwise proceed as proposed:
- GA8, GN8, GB8 and the four controls run again on a fresh 8x8 build.
- The 1x1 legs are graded on a fresh build after an image and sample byte-compare.
- Then restate the tables, run the load gate, run the full pass once on a clean clone, and post REVIEW READY.

**Rationale**
- (a) breaks the 22 ms bound of the 2026-11-08 decision (`FR_NFR.md` 3.4.1) and moves further from tier 1's 20 ms.
- (c) is of unknown size against this week's 1x1/1if flip. The cold cost is an 8x8 constant, and the 8x8 flip waits on #890.
- GN8's rounds fit roughly 191.6 + 28.3k us. The stated 185 + 34k covers k = 2 by 2.0 %, k = 4 by 5.3 % and the search's binding k = 5 by about 6.6 %.
- That fit would put a round with k = 0 or 1 over the stated line. No receipt shows one, which is why trigger 1 tallies by k.


---

https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6845315282

[A10] **Owner decision (2026-11-13 06:47):** "8x8 is a must, 2if parts an option, but keep it going."
- The flip needs 8x8 as well as 1x1/1if: at least 8x8/1if.
- The two-interface parts are optional. A blocker at 2if only may be deferred to #890 as tracked debt instead of costing a new round.
- #810 continues in its current scope; nothing is re-scoped now.
- Consequence: the flip check must also hold the rows at 8x8/1if. #894 models only 1x1/1if so far, so modelling the 8x8/1if point is its next step after round 4.

---

https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6850895861

[A683zp] REVIEW READY
Commit: 084cf7a8455e9fa8e24a0e5bcf57c9557816c819
Changed: round 31, docs only, three one-line commits on round 30's head 325514224bcc356a6b43843f1003c2323f09de25, as the manager's ruling on R711-9 (#810 issuecomment-6850590935) and R712-9 (#810 issuecomment-6850656712) sets them. No code, cost, bound, ledger figure or gate changes.
- f150b8cb, R712-9-F1: `docs/design/SPLIT_CONTROL_MEMORY.md:442` names what dev-soft-core `0fb66211` carries as `6eacd76d` does: #874, #880 (with KLJ3, #823), #889 and #888. `:455-456` state both regions' smallest margins at the pin move's merge: 288 B of `rom` at the platform's 1x1/2if (112,352 B in 112,640) and 16 B of `sram` at the platform's 8x8/2if (114,672 B in 56 granules of 2,048), whose next granule would plan 59.5 against the 59.0 its override held there.
- 47e44d73, R712-9-F2: section 13 `:2323` states arm A's least margin at this head from round 30's re-grades only: at most 8.162 ms at 8x8/2if (group `backlog-adp@program-aged2-7`, instance `service.aecp.last.if1`, at 11.838 ms) and at most 9.992 ms at 1x1/1if (group `backlog-adp@verify-aged2-5`, instance `service.aecp.last.if0`, at 10.008 ms), each the least of the windows opened at the age limit, the figure the re-grade prints. It says round 30 did not re-derive arm A's least over all its rows nor the `answering-every-port` arm's at either point, and labels 6.246, 8.973, 9.080 and 11.006 ms as round 29's. `:2331` cites only the two round-30 figures.
- 084cf7a8, R711-9 RES-2: `sw/litex/ctrl_memory.py:257`, `:265`: "ROM debt owed to the hybrid XIP work (#665 decision D3)" in place of "owed to S14". Reason strings only.
Validation: at 084cf7a8, each rc 0, never piped: `git diff --check 32551422 HEAD` (no output); `python3 -B scripts/docs_check.py` (0 findings); `python3 -B scripts/check_doc_style.py` (OK); `python3 -B scripts/check_em_dash.py --base 32551422` (0 findings over 5 added lines) and `--selftest`; `python3 -B scripts/check_py_idiom.py` (every count within its budget); `python3 -B sw/litex/test_ctrl_memory.py` (`RESULT: PASS`, 0 failures); `grep -n 'owed to S14' sw/litex/ctrl_memory.py` (no match). `git diff e5f88a8e HEAD -- docs/design/SPLIT_CONTROL_MEMORY.md` keeps both of `6eacd76d`'s statements. No leg re-run.
Acceptance criteria: the ruling's three items met, one commit each, with the receipts above. The lane's other criteria stand as round 30's REVIEW READY (issuecomment-6848807388) states them; the tree differs from `5bea2597`'s only in these docs and two reason strings.
Open risks/questions: arm A's least over all its rows and the `answering-every-port` arm's least margins are not re-derived at this head (round 30's re-grades print no table of rows); section 13 says so. Section 13's 8x8/2if heaviest work pass (183,244 cycles) is round 30's figure, unchanged here, and is not in round 30's published verdict lines. `SPLIT_CONTROL_MEMORY.md:141` keeps "owed to S14" in prose, outside item 3's reason strings. The Docs lens must be covered again at this head. Nothing pushed; PR body and handoff are with the manager.

