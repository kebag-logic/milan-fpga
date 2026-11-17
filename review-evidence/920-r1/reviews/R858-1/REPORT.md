[R858] POSITIVE - exact head bd252db1d73511307c0ecb78470f0d15d0c3ea9b

External independent review R858-1 of issue #920 / PR #938. Tree: `2cc90eb47ddd00d5bd7d1d5edb6c7ec0937b509a`. No BLOCKER, MAJOR or MINOR finding remains from this review. One grouped wording RESIDUE is recorded below. All five source-review lenses are CLEAN. This verdict does not declare the issue complete or authorize a merge; the outstanding acceptance and manager duties are stated below.

The review reconstructed the task from AGENTS.md, CONTRIBUTING.md and docs/README.md, then the frozen issue, public scope decisions, linked persistence authorities, the full `659d7687..bd252db1` diff and history, and public executable receipts. The independent verdict and ledger were written before reading the PR discussion. That discussion contained only the two review-start notices: there were no prior public review findings to resolve or retain. No other review report was used.

Authority: [issue #920](https://github.com/kebag-logic/milan-fpga/issues/920), [rehearsal finding 13](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6899519003), [the three-mechanism ruling, item 1](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6899740728), and [the timing, cost and merge-scope decision](https://github.com/kebag-logic/milan-fpga/issues/920#issuecomment-6910219988). Repository authorities examined include REQUIREMENTS.md's saved-state requirements, SAVED_STATE_SNAPSHOT_OWNERSHIP.md, SAVED_STATE_MATERIALIZATION.md including DR2a/DR2b/DR2c, SAVED_STATE_FASTCONNECT.md sections 6.2 and 7, layout 3, and the loop's THE STEP contract. The review applies the supplied owner's proportional-save-time rule and #818's +0.030 ns setup / 0 ns hold floor.

The public evidence source is [archive 4a3e37f80640ec17ab6acffbe5cf8c4ac587c5dc](https://github.com/kebag-logic/milan-fpga/tree/4a3e37f80640ec17ab6acffbe5cf8c4ac587c5dc/review-evidence/920-r1), specifically its author-r1 and author-r2 executable receipts, plus the issue's REVIEW READY comment. `receipts/public-evidence-manifest.json` identifies the 37 selected receipts whose published hashes were independently checked; `receipts/evidence-check.json` records the independent tally, timing and image-size checks. These are author source receipts, not a manager source bank.

[R858] RESIDUE Docs — R858-1-F1 — `sw/firmware/ctrl_nvm/test/test_nvm_write.cpp:155` and `tb/verilator/ctrl_service_budget/save_burst.py:5` — New source comments contain an issue-comment identifier.

- Authority/evidence: the owner's 2026-10-15 source-comment rule requires behavior/reason with issue and requirement IDs, without issue-comment IDs. Both added comments contain `issuecomment-6899740728`.
- Impact: wording policy only. The defect changes no measurement, figure, test, executable behavior, conformance claim or privacy rule.
- Required outcome / exact fix: in test_nvm_write.cpp replace `#920 (#665, the ruling of issuecomment-6899740728, item 1)` with `#920 (#665, save-burst ruling, item 1)`; in save_burst.py replace `THE TARGET (#665, the ruling of issuecomment-6899740728, item 1)` with `THE TARGET (#920; #665, save-burst ruling, item 1)`. Keep the substantive behavior and Milan 5.3.13 explanation.
- Verification: inspect the two comment-only changes and search the newly added source comments for the forbidden identifier. The generated findings-page wording in run.py is permitted by the owner rule. Existing source-comment residue is outside this delta and remains #746's.

[R858] PASS Conformance — `sw/firmware/ctrl/aecp/aecp_nvm.h:10`, `aecp_nvm.c:135`, `sw/firmware/ctrl_nvm/nvm_store.c:532`, and archive `author-r1/receipts/cause/`, `author-r2/receipts/harness/save-groups-*.txt` — Cause, scope and save target checked against #920 and the ruling.

The base defect is established independently of the timing adjustment: names begin at ID 222, so ordinals 34 onward exceed the old 256-bit queue. The base unit receipt delivers 34 of 39 marks; the 1x1 save replay loses precisely names 34–38; the 8x8 replay records eight load-access traps. The base board console goes from dirty to pending to backed/clean with no pending work or failed-attempt indication before the cut, yet those five names restore as defaults. This supports a missing owner mark, rather than an unfinished flash operation. The board receipt is cause evidence on the old image, not hardware validation of the fix.

The owner now allocates 36 words over layout 3's 1,129 IDs, counts only newly set bits, decrements on delivery, and checks the shape's name bound statically. The write-path changes implement precisely the permitted capture join, immediate next-save start and input-free pass stepping. First-dirty delay, failed-attempt backoff, step duration, age, tiers, pace, slot sequence, blank check, verification and format remain intact. The capture admits an uncaptured record behind its cursor through a second walk; it never takes an already captured record again on that walk. A later change to that record remains dirty for the next save. Save work remains proportional to records/container bytes and media operations, without a shape-independent timing shortcut.

| Published measurement on the merge's code | 1x1/1if | 8x8/1if |
|---|---:|---:|
| Latest burst name durable after its response | 1,107.785 ms | 1,370.301 ms |
| Burst names / verified saves / missing at cut | 39 / 1 / 0 | 107 / 6 / 0 |
| Change during a save durable after its response | 165.045 ms | 663.104 ms |
| Steps from first verify to next erase | 19, expected 19 | 59, expected 59 |

Both target scenarios meet 5,000 ms. The tested executable code at `d66b4045` is unchanged at the exact reviewed head: the subsequent delta modifies only SPLIT_CONTROL_MEMORY.md and ctrl_nvm/README.md. The starved and datasheet-maximum cases remain separately stated, including values above 10 seconds at 8x8; the ruling explicitly does not make them this target gate.

[R858] PASS RTL — `sw/firmware/ctrl_nvm/nvm_store.c:635`, `nvm_store.c:893`, `sw/firmware/ctrl/loop/ctrl_loop.c`, `sw/firmware/ctrl/aecp/aecp_nvm.c:172`, and `receipts/merge-resolutions.diff` — Architecture, bounds, loop integration and all four merge resolutions checked.

The full requested diff, including inherited changes, was examined; there is no gateware or submodule-pin change. The pending-word indexing, unsigned masks, count/bit invariant, capture cursor, finite rewind, reset initialization and signed wrap-safe deadline comparison are consistent. The loop calls the store at most once in a pass taking no input; a short unowed pass creates no debt, while an owed pass retains the existing defer/age behavior. No new CDC or clock/reset domain is introduced.

Merge `d66b4045529fbba7b483aadbbea15ad75bd1ccf9` preserves both parents in its four conflicts: the enlarged pending array and the compressed name runs coexist in aecp_nvm.h; ctrl_memory.py, ctrl_memory_ledger.py and the memory design document retain #895's 60.5-RAMB36 entry and incorporate #920's measured sizes. The merged ctrl_plat figures are 17,664 / 19,200 / 18,304 / 20,480 bytes. All eight ROM entries grow 296–304 bytes and fit; the largest platform image is 132,040 of 133,120 ROM bytes, with SRAM 114,352 of 114,688 bytes. No cap was silently raised beyond the recorded 60.5 entry.

The regrades contain 98 groups at 1x1 and 97 at 8x8/1if, zero refusals, and zero of 132,926 / 231,039 work passes over the share. The seven misses at each point are the specified held-egress rows behind the scenario's 60 ms hold, not new CPU-decided row misses. The 8x8/1if exit 1 records the ruled #914 stated-cost lines: polls 25,015/22,500 cycles, ACMP item 7,277/5,500, declined offer 2,338/2,000. It is not represented as an unconditional rc-0 harness result. The independent load check reproduces 0.517 against 0.70 at 1x1.

[R858] PASS Robustness — `sw/firmware/ctrl_nvm/nvm_store.c:548`, `nvm_store.c:692`, `nvm_store.c:797`, `sw/firmware/ctrl_nvm/test/test_nvm_write.cpp:164`, `:239`, `:341`, `:830`, `:859`, and `cut_probe.cpp` — Power cuts, repeated changes, recovery, timeout/backoff, no-room and disabled/HELD behavior checked.

The capture and subsequent save retain independent dirty/inflight ownership; commit clears only the completed inflight set, and stale status heals only when no dirty work remains. Failed attempts retain their captured set and backoff; reset reconstructs authority from whole accepted containers. Existing tests exercise blank/one/two-slot starts, malformed/truncated records, invalid ordering, boundary IDs and widths, media refusal/timeouts, retry exhaustion, unchanged values, capacity, and cuts within erase/program effects and verify.

The added reviewer probe saves a highest-ID change, joins a lower-ID change behind the capture cursor, and changes the already captured high record again. It cuts and reboots at every service boundary through both saves and compares the entire restored state against three independently constructed snapshots. All nine active phases and all three sequences were reached. Both flash ports pass: 845 / 823 boundaries at 1x1 and 2,125 / 2,103 at 8x8, 5,896 boundaries total (`receipts/cut-probe.log`). This supplements the suite's partial-media-effect tests; it does not claim physical power-loss calibration.

[R858] PASS Tests — `sw/firmware/ctrl/test/test_aecp.cpp:350`, `aecp_mutants.py:454`, `sw/firmware/ctrl_nvm/test/nvm_mutants.py:373`, `tb/verilator/ctrl_service_budget/save_burst.py`, `selftest_burst.py`, `save_window.py:59`, and the receipts below — Positive, negative, integration and mutation sensitivity checked.

The new AECP test sends acknowledged SET_NAME commands through the real owner, verifies every queued mark and store dirty record, commits using the real store and checks every restored name. The independent runs pass all nine Nvm cases at the default 1x1 fixture and the new all-names case at 8x8. All three focused pending-mark mutants are caught: IDs above 255 dropped, double counting and count retained after delivery.

The original attempt to run every default-fixture Nvm case at 8x8 hit `WholeMapFramingAndEmptySetAreDistinct`: it assumes a nonempty dynamic input map, but this shape's generated input-map capacity is zero. The failed diagnostic is retained in `receipts/aecp-8x8-incompatible-map-fixture.log`; no claim is made that all nine cases pass at 8x8. The shape-independent new name test passes there separately. No repository test or source was modified to obtain these results.

The independent store gate passes 546 tests across five shapes and catches all 152 planted defects, including every capture-join, next-save and busy-step control (`receipts/store.log`, rc 0). All five RV32 compile/size arms also ran; none was skipped. The command used `--self-test --jobs 12`, with disposable outputs under the packet scratch directory.

The harness self-test independently passes with zero failures and 251 mutants caught (`receipts/budget-selftest.log`). Its deliberately exercised `CONTROL ... ESCAPED` printouts are negative grader fixtures, not escaped campaign mutants. The three published executable controls are caught by name: `store-names-past-256-lost` loses the five high names; `store-next-save-waits` takes 112 steps rather than 19; `store-step-only-owed` delays the latest 8x8 name to 8,021.164 ms. Removal of the join harness control in `339d0224` is justified: without joining, that burst still meets 5 seconds, with seven saves instead of six. The store's capture-join mutants test that mechanism directly.

The author sweep at exact `bd252db1` contains 65 distinct passing suites, 2,713,040 checks, zero failures and zero timeouts. Firmware and elaborate receipts at the code-identical `d66b4045`, and docs at `bd252db1`, report zero bad steps. Coverage reports PASS across 39 files; nvm_store is 508/508 lines and 311/320 raw branches, with documented unreachable-branch exclusions yielding the stated 100% obligation. The new exclusions were checked against the count/bit and window invariants. Executed firmware steps and declared NOT RUN contexts are distinguished; the receipts do not establish execution of excluded RTL/Yosys/CDC contexts.

[R858] PASS Docs — `docs/design/SPLIT_CONTROL_MEMORY.md:2730`, `:2803`, `:2821`, `sw/firmware/ctrl_nvm/README.md`, `nvm_store.h`, the issue's scope decisions and the public receipts — Contracts, measured figures, proportional worst cases, merge sizing and evidence provenance checked.

The docs separate the cause from the pacing change, first-dirty delay from chained saves, measured held-load results from starved/datasheet maxima, and pre-merge measurements from merged measurements. The merged memory ledger agrees with the receipts. The two comment-policy instances above remain wording residue only. The historical timing STOP's +0.030 ns hold interpretation is not adopted: the review uses #818's 0 ns hold floor and the public #927 disposition, with no new route run or hardware claim.

Reviewer-owned completion ledger:

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #920 / #665 ruling; REQUIREMENTS.md persistence; aecp_nvm.c:135; nvm_store.c:532; cause and save-group receipts | R858-1 | bd252db1d73511307c0ecb78470f0d15d0c3ea9b |
| RTL | CLEAN | Full 659d7687 diff; nvm_store.c:635,893; ctrl_loop.c; aecp_nvm.h; four merge resolutions; ROM/SRAM ledgers | R858-1 | bd252db1d73511307c0ecb78470f0d15d0c3ea9b |
| Robustness | CLEAN | test_nvm_write.cpp capture_joins, busy_steps, media_failures, step_room, powercut; nvm_store retry/commit/reset; cut_probe.cpp and receipts | R858-1 | bd252db1d73511307c0ecb78470f0d15d0c3ea9b |
| Tests | CLEAN | test_aecp.cpp:350; pending/store mutations; save_burst.py and selftest_burst.py; named controls; local test receipts; exact-head sweep | R858-1 | bd252db1d73511307c0ecb78470f0d15d0c3ea9b |
| Docs | CLEAN | SPLIT_CONTROL_MEMORY.md #920 section and memory ledger; store README/header; ownership/materialization/layout authorities; public issue/PR and gate receipts | R858-1 | bd252db1d73511307c0ecb78470f0d15d0c3ea9b |

Real limits and pending manager duties:

- This is source-head review. There is no manager source bank at this head, and none is inferred. The manager must build and validate the final current-dev merge candidate, including builder/native receipts and #919 composition, then link those receipts. The source base `659d7687` and supplied live dev `6b66f66d89cf25d2717687bcc2c3bf617685a99a` are different validation objects.
- The exact-head hosted snapshot inspected had 14 queued checks and no execution conclusion. It provides no hosted success evidence. Hosted/act acceptance remains the manager's responsibility; no host runner or container was executed by this review.
- The supplied source load receipt and independent rerun establish 1x1/1if at 0.517/0.70. Their larger-shape row is 8x8/2if, not 8x8/1if; it must not be presented as proof of the issue's separate 8x8/1if 0.75 acceptance line. That evidence/disposition belongs in final acceptance with #914's per-shape statements.
- The fixed-image bench acceptance still needs three persistence runs at each requested shape, last-response-to-durable times and the ruling's STOP threshold. Physical calibration was NOT RUN. Field skips and the old-image cause console are not hardware proof of the candidate.
- The #927 timing dependency and #818 grading apply to the final candidate. The known interrupted source runs are not counted as passes; the completed reruns and final sweep receipts are the evidence used here.
- Two independent positive reviews, current-head review integrity, no review in flight, required candidate/hosted gates, explicit merge authorization, post-merge containment and issue completion remain the manager's merge duties. Carry R858-1-F1 to the residue checklist.

`audit_checkout.py` verifies every tracked blob's bytes and executable/symlink mode against HEAD, the index against the tree, and initialized submodules against their gitlinks. `receipts/checkout-audit.json` reports no discrepancy, including the required protocol-processor, gptp-processor, TSN stack, lwSRP and verilog-axis pins. The optional external submodule remains uninitialized as received. No repository source edits, commits, pushes, GitHub writes, hardware actions or full parent/PP/gPTP/Yosys/builder banks were performed. Portable probes and raw receipts are enumerated by MANIFEST.sha256; disposable material under scratch/ is excluded.

R858-1 FINISHED
