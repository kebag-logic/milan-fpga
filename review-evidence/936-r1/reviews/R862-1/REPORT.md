[R862] NEGATIVE - exact head 7cfb8a0499941e56682f0c2f63326d120f5b7d9e

External independent review, round R862-1, issue #936 / PR #944. Tree `eb5a313b02b3669d9529500c0369c62dca697b50`; source base `70f4056f`. All nine commits and 22 changed files were examined. This is a source-head verdict, not a current-dev merge-candidate verdict.

Public reconstruction: [issue and frozen acceptance](https://github.com/kebag-logic/milan-fpga/issues/936), [held-egress ruling](https://github.com/kebag-logic/milan-fpga/issues/936#issuecomment-6938589620), [REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/936#issuecomment-6953386992), [PR](https://github.com/kebag-logic/milan-fpga/pull/944), [immutable evidence archive](https://github.com/kebag-logic/milan-fpga/tree/a1853df5239bf79c53bab731215350dbfe33c2f6/review-evidence/936-r1), [BRAM ruling](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6892332745), [batch rule](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6939574513). Local `public-contract.json` and the two owner-rule receipts preserve the consulted public text.

The declaration-change implementation and requested mutation checks pass this review. One MAJOR acceptance-evidence gap remains: no CPU-budget measurement covers a real SRP declaration change through to its STREAM_OUTPUT notice's last recipient. Two wording residues do not affect the verdict.

## Findings

### R862-1-F1: MAJOR; Conformance, Robustness, Tests, Docs

**Artifact:** `sw/firmware/ctrl/app/ctrl_app_aecp.c:207`; `tb/verilator/ctrl_service_budget/talker_window.py:61`; `tb/verilator/ctrl_service_budget/notice_window.py:103`; `tb/verilator/ctrl_service_budget/build.py:213`; PR #944 acceptance/CPU-budget claims; archived `author-r1/receipts/final/budget/{vd-1x1,vd-8x8-1if}/results-summary.json`.

**Title:** The new SRP-to-STREAM_OUTPUT notification path has no event-to-commit budget check.

**Authority/evidence:** Issue #936 expressly requires the CPU service-budget harness to show the notice rows within their bounds. `docs/reference/FR_NFR.md:351` defines event occurrence as the start and the last required recipient's TX commitment as the end; its asynchronous-notification row at line 410 applies the project budget. The held-egress ruling exempts seven existing rows, not this new path.

`valid-destinations` exercises real declaration/withdrawal work, but its probes end at SRP transmission, register no unsolicited recipients, and leave the stream observation unanswered. Both published summaries contain zero timed notices. `answering-later` instead starts from `retry_port_answers` for a STREAM_INPUT notice following BIND_RX. `answering-every-port` includes STREAM_OUTPUT notices, but injects them directly with `aecp_changed`, substitutes observation callbacks, and starts timing when those callbacks answer. It bypasses the new declaration record and both delivery polls. The host tests prove forwarding, not target CPU elapsed time. The twin checks ordered values/recipients, not a 20 ms declaration-to-notice interval. No measured bound joins the missing interval to the measured delivery interval. The PR acknowledges that no row times the newly triggered notice, yet marks this acceptance criterion met.

**Impact:** A delay or loss specific to the new handoff under load can leave the published CPU notice rows green. No over-budget delivery was demonstrated here; the defect is the missing required proof, including the loaded case, and the unsupported acceptance claim. Reusing AECP's scheduler does not measure the upstream handoff or successful output observation in this causal path.

**Required outcome:** Before approval, establish the complete budget for a real Talker declaration and withdrawal through the SRP record and bridge to the last registered controller's STREAM_OUTPUT GET_STREAM_INFO commit, at 1x1/1if and 8x8/1if. Use an answering observation and the required concurrent work/recipient population. Grade the applicable single-notice or queued-notice bound without restarting the origin to hide handoff delay. A focused harness row or an equally explicit measured composition proof can close this; no general harness redesign or unrelated RTL repair is requested. Correct the acceptance claim to the resulting evidence. A missing or delayed notification must fail a named check. This is #936's frozen acceptance, not unrelated new scope.

**Verification:** Publish exact-image identity, event origin, recipient count, final commit, elapsed time, applicable bound and passing receipts. A disposable dropped/delayed-output-notice control must fail the new check for that reason. Re-review those artifacts.

### R862-1-R1: RESIDUE; Docs

**Artifact:** `sw/litex/ctrl_memory.py:247`, added source comment.

**Authority/evidence:** The owner's 2026-10-15 source-comment rule prohibits lane labels in new source comments. This addition says `debt owed to S14`.

**Impact:** Wording only; ledger values and checks are unaffected.

**Exact required fix:** In that comment replace `debt owed to S14` with `debt owed to the cold-code and descriptor move to QSPI (#665 decision D3)`. Preserve numeric values and executable strings.

**Verification:** Inspect the added comment against the source-comment rule. No executable check changes. This residue does not unclean a lens.

### R862-1-R2: RESIDUE; Docs

**Artifact:** PR #944, `Known limitations / out of scope`, first bullet; `tb/verilator/milan_dp/README.md:1382`, owed-to cell for `stream-output-0-dest-mac`.

**Authority/evidence:** The same PR identifies the face defect as opened under #943, while these prose locations still say no issue owns it.

**Impact:** Stale ownership wording only. #943 itself is a known out-of-scope defect, not a finding of this review.

**Exact required fix:** In the PR bullet replace `no issue owns it yet` with `tracked by #943`; replace the README cell `#665 (no issue owns it yet)` with `#943`. This request applies to prose only, not executable owed-row predicates or generated receipts.

**Verification:** Both prose locations name #943; predicates and measurements remain untouched. This residue does not unclean a lens.

## Independent results by lens

**Conformance:** `srp_mbx.c:261` and `:339` implement the accepted trigger rule from Milan v1.2 5.4.5.1/5.4.5.2, Table 5.22, IEEE 1722.1-2021 7.5.2 and IEEE 802.1Q's declaration model. The release reference is `protocol-processor/hdl/top/protocol_processor_top.sv:3679`. XOR detects declared/withdrawn sources; `kept` restricts type and VID changes to continuing declarations; `advertise` uses the successfully retained type, not the desired type of a refused swap. Failed creation returns before advancing the shown snapshot. Reset retains it, avoiding notices for unchanged re-creation. No new missed/duplicate trigger found. Timing acceptance remains unproved under F1.

**[R862] PASS RTL - `srp_mbx.h:83`, `srp_mbx.c:347`, `ctrl_app_srp.c:63`, `ctrl_app_aecp.c:207`, `sw/litex/ctrl_memory.py:254` - checked single-owner state flow, bounded masks/indexing, publication order, attachment lifetime and memory effects against the mailbox/application contracts.** The firmware paths in this sentence are under `sw/firmware/ctrl/{srp,app}`. No RTL, clock crossing, mailbox ABI or gitlink changes occur. The existing single-threaded loop owns the new state; source count is bounded below 32. SRP delivery consumes each interface mask, successful attach clears the application mask, and AECP consumes it into type 6/event bit 0. Existing AECP pending/retry/fan-out retains refused observations and addresses all registrations. No synchronous SRP reentry or separate architectural defect found. F1 concerns missing timing acceptance evidence, not a demonstrated scheduler failure.

**Robustness:** Examined refusal, unchanged periodic declaration, type-swap refusal/retry, VID adoption versus priority-only change, link reset/re-creation, stale composition records, source/interface isolation and AECP retry/fan-out. Each mask transfers to the next owner before being cleared; pending changes coalesce as existing AECP events do. Baseline suites and mutations below pass. The complete loaded timing case remains open under F1.

**Tests:** Independently executed Talker and `SrpGate.*` suites at 1x1/1if and 8x8/2if, plus the new AECP app test at one and two interfaces: **50 baseline cases, zero failures/skips**. All 12 `talker-notice-*` definitions were rerun at each SRP point (24 kills), plus all four `app-output-notice-*` definitions at two interfaces (4 kills). Each kill required its unchanged named assertion diagnostic; compile refusals never counted. Raw logs and results are included. The twin's exact owed row requires four frames in the expected controller/order/state sequence and admits only the stated destination-MAC payload difference. Published exact-head receipts show `output-notice-dropped` refused against both the unplanted split and the other placement; `vanished-owed` fails its intended checks too. F1 is the remaining test gap.

**Docs:** Checked SRP/AECP/twin READMEs, plant inventory, memory tables and public acceptance/evidence claims. They describe the handoff and memory change consistently. The exact-head twin is not green as a whole: its known stale `split-talker-failed` row and `srp-plus-k` plant belong to #935. No clean-twin claim is inferred from that run. F1 concerns a technical acceptance claim, not wording residue. R1/R2 are wording only.

## Budget and memory dispositions

**1x1 held-egress growth is not a defect of this PR under the frozen ruling.** The seven existing misses rise 0.132 to 0.151 ms behind the deliberately held 60 ms egress. #936's public ruling treats them as the base's exempt rows. There is no 1x1 ledger to pass or fail; none is invented here. The growth remains reported. At 8x8/1if all seven fit the published ledger, with 0.13570 to 0.31397 ms remaining. These are the only budget misses in the supplied arm-A summaries; no measured work-pass share miss is reported.

**The 21 refused 8x8/1if retry rounds are not an independently blocking PR defect under the stated reporting contract.** The new output events cause the attempts. Their 11,922 to 12,537 cycles exceed the reported one-interface 11,900 estimate by 22 to 637 cycles. This fixture never answers the observation; that is not evidence of a stuck product port. `ctrl_service_budget/README.md:49` explicitly reports 8x8/1if costs against the 1x1 cost set. The published 1x1 result stays within that estimate, and no service/share overrun is measured from these attempts. These figures do not validate 11,900 as an upper bound at 8x8; the composition statement survey must account for them. They cannot substitute for F1's successful-delivery measurement.

**The absent real-declaration notice row must be closed before approval (F1).** Existing notice measurements are valid but narrower: eight retried STREAM_INPUT rows at each point, maxima 8.30084/8.24574 ms against 20 ms, and 192 injected queued notices at 1x1, maximum 27.07272 ms against 140 ms. The known refusal of `answering-every-port` at 8x8/1if is pre-existing, not newly filed here.

**Memory debt is authorized and measured.** The #665 owner ruling permits measured overflow rounded to the next half RAMB36 as cold-code/descriptor debt. The final 8x8/2if fixture needs 126,824 B ROM (59.0); its answering-every-port and valid-destinations arms need 127,132/126,992 B, beyond 59.0's 126,976 B. The 59.5 entry is supported, not an arbitrary test relaxation. Platform two-interface `ctrl_plat` figures are 19,136/20,416 B (+64 B each); one-interface figures remain 17,536/18,240 B. Symbol-qualified overrides and half-tile-past refusal remain in the tests. Published final/b496c99e hashes match for all 24 platform artifacts and six fixture images. The six release comparisons against the base match, including both `bios.bin` files and debug-stripped ELFs. Whole debug ELFs differ by build paths and are not claimed byte-identical. Product ROM banks are unchanged. These receipts do not prove physical fit or timing.

## Reviewer-owned coverage ledger

All paths refer to the exact reviewed head. Firmware abbreviations below identify the artifacts expanded in the lens results above.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | `srp_mbx.c:261`, `ctrl_app_aecp.c:207`, `docs/reference/FR_NFR.md:351`, `notice_window.py:103`, public acceptance/budget receipts | R862-1 applied; no clean covering round | 7cfb8a0499941e56682f0c2f63326d120f5b7d9e |
| RTL | CLEAN | `srp_mbx.h:83`, `srp_mbx.c:347`, `ctrl_app_srp.c:63`, `ctrl_app_aecp.c:207`, `sw/litex/ctrl_memory.py:254`, image receipts | R862-1 | 7cfb8a0499941e56682f0c2f63326d120f5b7d9e |
| Robustness | UNCLEAN (F1) | `srp_talker.cpp:631`, `srp_gate.hpp:348`, `test_aecp.cpp:755`, `aecp.c:814`, `talker_window.py:61` | R862-1 applied; no clean covering round | 7cfb8a0499941e56682f0c2f63326d120f5b7d9e |
| Tests | UNCLEAN (F1) | 28 mutation receipts, six baseline receipts, `twin_compare.py:476`, `twin_plants.py:112`, CPU notice probes | R862-1 applied; no clean covering round | 7cfb8a0499941e56682f0c2f63326d120f5b7d9e |
| Docs | UNCLEAN (F1; residues do not affect cleanliness) | SRP/AECP/twin READMEs, `SPLIT_CONTROL_MEMORY.md:544`, `MARK_II_AREA_PLAN.md:1088`, public contract/receipts | R862-1 applied; no clean covering round | 7cfb8a0499941e56682f0c2f63326d120f5b7d9e |

## Reproduction, limits and pending duties

`focused.py CHECKOUT PACKET all` runs the three focused campaigns concurrently, four compile jobs each, under a foreground supervisor (12 jobs maximum). `receipt_audit.py EXTRACTED_AUTHOR_RECEIPTS` checks published hashes and budget/twin receipt consistency; it does not execute target simulations. `verify_tree.py CHECKOUT` hashes every tracked blob directly, checks kinds/modes and the full index against the commit, and verifies the five required submodule checkouts/gitlinks. All passed: 1,632 superproject entries and 1,238 required-submodule entries match. The unrelated `external` gitlink remains uninitialized as supplied. No source fixes, commits, pushes, GitHub writes or changes in another checkout were made. Disposable sources/builds are confined to packet `scratch/`.

The public archive is `a1853df5239bf79c53bab731215350dbfe33c2f6`, under `review-evidence/936-r1/author-r1/receipts`. Final exact-head firmware/docs/image receipts are distinguished from b496c99e's campaigns/boundary/selected split-firmware suites and 77c1aad7's arm-A images. The final commit changes documentation and an unread reason string; final image hash comparisons were checked. These are the author's executions. **No manager source bank ran at this head; none is claimed.** The reviewer reran only the focused checks stated above, not full parent/processor, synthesis, builder or timing banks. No new twin or CPU-budget target simulation was run. Standards clause quotations, public scope decisions, repository normative requirements and the pinned reference were checked; downloading the complete Milan PDF returned HTTP 403, so no fresh full-text standards audit is claimed.

The manager owns hosted/local-replica acceptance and must distinguish executed jobs from skipped contexts. No hosted context was used here as execution evidence. Two POSITIVE independent reviews are required before freezing a constituent; this verdict does not meet that condition. After F1 closes and is independently re-reviewed, composition must resolve #935/#932 conflicts, remeasure CPU budgets/statements/ROM, validate the actual live-dev candidate (supplied live dev `e275d7950ef3385753e6a15d2e191ba855b171ed`), publish receipts, and complete train review, required gates and containment under explicit merge authorization. #943 and the named pre-existing face gaps remain outside these findings. Physical calibration is **NOT RUN**; field skips and simulations are not hardware proof.

**Prior-public-finding reconciliation:** After saving this independent verdict and ledger, queried PR reviews, all conversation comments and inline review comments. There are no submitted reviews, no inline comments, and only the two manager review-start comments. Thus no prior public review finding exists to resolve or retain at this head. `pr-review-audit.json` and the empty `pr-inline-comments.jsonl` record that check. No other reviewer's report informed this verdict. The other independent round remains the manager's responsibility; it is not assumed complete.

R862-1 FINISHED
