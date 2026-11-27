[R958] NEGATIVE - exact head 095995243bc354b8a41755f3fdfae343511cc668

All five lenses were applied. One MAJOR defect and one MINOR documentation defect remain open; no lens is banked CLEAN. There is also wording residue and an additional dependency merge conflict.

Reviewed tree: `843b1ede3d27b14048269ce9c3b2f9cde65bfdff`. Public base: `dev-soft-core`, `4df125b8c11f0e1706b3c1e489f3e66a5d856b18`; that merge is incorporated by `163e467f`. The local clone lacked the branch name, so the diff used its verified commit ID. This is a source review, not acceptance of the eventual current-dev merge candidate.

The independent source findings and reviewer-owned ledger were written before the PR discussion/review queries. Reconstruction used AGENTS.md, CONTRIBUTING.md, docs/README.md, [issue #977](https://github.com/kebag-logic/milan-fpga/issues/977) and its public scope rulings, REQUIREMENTS.md, FR_NFR.md 3.4.1, the mailbox and memory/interface authorities, the complete 70-file parent diff and history, then the [published author evidence](https://github.com/kebag-logic/milan-fpga/tree/f7a322f9e65e5ceb7fa520b3d1df6037b362db90/review-evidence/977-r1). The donor integration and pin were examined; this does not replace the separate donor PR #41 review.

**R958-1-F1 — MAJOR — Conformance, RTL, Robustness, Tests, Docs**

Artifact: `sw/firmware/ctrl/srp/srp_mbx.c:1041`, with the same population assumption in the fallback at `:1025`; `tb/verilator/ctrl_service_budget/poll_grade.py:336`; `sw/firmware/ctrl/test/srp_mbx.cpp:518`; `sw/firmware/ctrl/test/srp_drain_mutants.py:27`.

The record charge undercounts a legal vector containing bound and kept Talkers. It caps every vector at `CTRL_SRP_SINKS`, but `interested_msrp` accepts both matching bound streams and `keep_talker`'s additional unbound population (`srp_mbx.c:614` onward). `SRP_KEPT_TALKERS == CTRL_SRP_SINKS` (`srp_mbx.h:157`). These populations can coexist. The comment at `srp_mbx.c:1003` incorrectly says the filter accepts only bound StreamIDs.

Authority: [#977's November 23 ruling, item 4](https://github.com/kebag-logic/milan-fpga/issues/977#issuecomment-7091882145) requires the count read before parsing never to undercount values that can register. THE DRAIN uses this charge to admit work into the remaining slice; FR_NFR 3.4.1 and THE SHARE retain their bounds.

Verification on unchanged firmware, through its real receive filter and lwSRP, with an Ethernet-minimum-sized MSRP JoinIn frame:

| Shape | Values in vector | Registrar IN values after receive | Charge returned | Charge required by the firmware's own unit and per-value statement |
|---|---:|---:|---:|---:|
| 1x1/1if | 4 | 4 | 505 us = 285 + 2 × 110 | 725 us = 285 + 4 × 110 |
| 8x8/1if | 18 | 18 | 1500 us = 375 + 9 × 125 | 2625 us = 375 + 18 × 125 |

At each shape the bound-only positive control passed; the mixed-population case failed the independent count assertion. The probe counts actual Registrar IN attributes, rather than duplicating the charge parser. See `charge-1x1.log`, `charge-8x8.log`, `probe_charge.cpp`, `probe_charge.py`.

Impact: admission and the claimed upper bound are unsound for this valid input. The 8x8 conservative charge already exceeds THE SHARE, so fixing the count alone must also be checked against the allowed first-record exception and the actual processing bound. These host results prove the count defect; they do **not** measure a physical or simulated-CPU pass exceeding 2 ms. The 110/125 us drain costs above are distinct from the 120/135 us all-in registration terms used by the load model.

The existing test explicitly expects the sink cap for a vector with more values, and the `charge-vector-uncapped` mutant enforces that assumption. The grader copies it. Separate all-bound and all-kept scenarios do not cover their simultaneous population. The ordinary SRP suite still passes 114/114 tests at each shape.

Required outcome: the pre-parse bound, including its bounded-scan fallback, must cover every accepted registration population. Preserve ordering and progress without exceeding the applicable work bounds. Correct the grader, the cap-dependent expectations and the filter/count documentation; add mixed bound/kept, boundary and fallback cases whose oracle observes receiver behavior.

Verification of a fix: both supplied mixed probes must pass alongside their bound-only controls; exercise the boundary with both Talker kinds and the fallback scan. Measure the corrected mixed cases on the built images and re-establish slice/THE SHARE and load evidence as applicable. Do not weaken the frozen owner bounds.

**R958-1-F2 — MINOR — Docs**

Artifact: `tb/verilator/ctrl_service_budget/README.md:401` and `:402`.

These changed lines describe the current size-fixture ledger as 61.0 RAMB36 for 8x8/2if and 57.0 for 8x8/1if. The executable `sw/litex/ctrl_memory.py:269` and `:288` entries are 58.5 and 62.5 respectively, agreeing with `docs/design/SPLIT_CONTROL_MEMORY.md:137`. The local memory checks pass with those executable entries.

Impact: a reviewer following the harness's current-build instructions is given the wrong resource acceptance limits. This changes a numerical claim and therefore is MINOR, not wording residue.

Required outcome: state current limits **62.5** (8x8/2if) and **58.5** (8x8/1if), and identify the old 61.0/57.0 measurements as historical if retained. Verification: compare both README entries to `ctrl_memory.LEDGERED`, the authoritative memory table and the platform/fixture receipts.

**R958-1-F3 — RESIDUE — Docs**

Artifacts: `sw/firmware/ctrl/aecp/aecp_mbx.h:78`, `sw/firmware/ctrl/loop/ctrl_loop.h:383`, `tb/verilator/ctrl_service_budget/flip_grade.py:64`, `load_grade.py:233` and `:336`, `poll_grade.py:108` and `:148`, `register_window.py:4`, `whole_grade.py:11`.

New comments carry review-round labels, a comment ID, or the default arm's letter label. The owner's comment rule requires behavior/reason with issue and requirement IDs instead. This finding concerns wording only: retain every measurement, statement, commit identity and clause reference. It does not clear or dirty a lens.

Required exact wording changes are in `residue-fixes.json` (23 literal replacements, verified against the source in `residue-check.log`). Examples: replace “round 2's walk of 80 us” with “the 80 us walk”; retain #977 and the decision date but remove `issuecomment-7160202807`; identify the default test arm as `none`. No source change was applied. Verification: check the proposed replacements and scan the added comments again under the owner rule. Existing untouched wording remains outside this delta.

**Reviewer-owned coverage ledger**

All artifact names below refer to the exact head in the last column. UNCLEAN means the lens was applied and has an open finding, not that it was omitted.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN — F1 | #977 frozen rulings; FR_NFR 3.4.1; IEEE 802.1Q-2018 10.7.11/35.2.6; Milan v1.2 4.2.7 and 5.6.3; register_window.py, load_grade.py, scenario.py, ctrl_loop.h, srp_mbx.c | R958-1 | 095995243bc354b8a41755f3fdfae343511cc668 |
| RTL | UNCLEAN — F1 | Complete firmware scheduling/index/peek changes in ctrl_loop.c/.h, ctrl_app_srp.c, mbx.c/.h, srp_mbx.c/.h; shape generation and all changed callers; linker/hot lists; memory plans; pinned interfaces. The diff contains no HDL/CDC implementation change. | R958-1 | 095995243bc354b8a41755f3fdfae343511cc668 |
| Robustness | UNCLEAN — F1 | Mixed-vector receive probes; source and tests for malformed/end-mark vectors, event-ring wrap, tick ordering, deferred completion, retained frames, declaration splits, reset/rebind, hash collisions and the two-interface/default-option paths | R958-1 | 095995243bc354b8a41755f3fdfae343511cc668 |
| Tests | UNCLEAN — F1 | All changed firmware tests/mutation definitions; register_window and changed grading/disposition paths; native SRP/loop/ADP runs; focused grader/memory checks; published 16-arm and four-shard receipts | R958-1 | 095995243bc354b8a41755f3fdfae343511cc668 |
| Docs | UNCLEAN — F1, F2 | Changed interface/firmware READMEs, MAILBOX_SPLIT, SPLIT_CONTROL_MEMORY, FR_NFR, SUBMODULES, diagram source/SVG/PNG and manifest, harness README, issue/PR scope and evidence provenance | R958-1 | 095995243bc354b8a41755f3fdfae343511cc668 |

**Specific conformance and evidence checks**

- The standards themselves support the rate construction: 802.1Q-2018 10.7.11 permits at most three point-to-point transmit opportunities in 1.5 JoinTime; Milan Table 4.3 gives 180 ms minimum JoinTime. Thus the chosen three-record burst window is 270 ms. Alternating Talker kinds is consistent with 35.2.6 replacement behavior and Milan 4.2.7.2.2's immediate leave. The implementation does not substitute LeaveAll frequency for registration rate. The primary documents read are identified by hashes in `standards-identity.log`; full copyrighted texts are not published.
- Milan v1.2 5.6.3.5.2 uses 0–2 s for startup with link up; 5.6.3.5.3 and Table 5.50 use 0–4 s after DOWN/LINK_UP. `scenario.advertised` raises the link after enable, so its 4200 ms observation window is appropriate. The five affected group time limits grow with it. The published `adp-link-up-window-control.txt` retains the 2200 ms refusal at both 1x1 fixture arms and the approximately 3.48 s draw; this is a harness-window correction, not relaxation of a response deadline.
- `ADP_MBX_LAT_LINK` is 12, matching #1015's line. The local ADP suite passes 77/77, including the latency model. The `mbx_tick_pending` change checks posted ticks before arming a new join timer without consuming events; the local mailbox/loop suite passes 53/53, including ring wrap, and the SRP suite includes `PostedTickPrecedesANewJoinTimerEvenWithGrandmasterEvents`. The earlier ten-runout negative control is a public scope/evidence claim, not an independently replayed run here.
- Local load and flip checks reproduce 1x1/1if load **0.518 ≤ 0.70**, 8x8/1if **0.757 ≤ 0.76**, last notice **132.95 ms** (statement 135, owner limit 140), ACMP **29.40 ≤ 30 ms**, txL **47.98 ≤ 49 ms**, and 8x8/1if transmit **76.86 ≤ 77 ms**. These are the published ruling figures, not newly raised limits. The registration all-in terms are **120/135 us**; the published maxima 11,172/12,806 cycles yield those figures by the stated margin/rounding rule. F1 prevents extending these results to all accepted vector populations.
- The 16 published arm summaries consistently show zero refusals and zero work passes over THE SHARE. At each point, default/answering-ports have 103/104 groups and seven ledgered backlog-owed misses; the other six arms have 16/8/5/2/8/3 groups and zero misses. The author's REVIEW READY records all 16 exits as zero. These are **author execution receipts**, not reviewer reruns or a manager source bank.
- The exact-head kept receipts pass with nothing owed; the 8x8/1if egress receipt covers all seven rows with 0.11–0.21 ms margin. Local kept and egress self-tests pass, 33 checks and 18 controls respectively.
- The four published firmware shards at `ea52ec11` each finish PASS/rc 0; shard 1 records **851/851** planted defects caught. Coverage records 40 files passing. A local diff verifies that `ea52ec11..09599524` changes only `scenario.py`, allowing the firmware-only evidence to carry forward; the four affected fixture arms were regraded at the reviewed head. Published ELF identity receipts cover the earlier execution images. This review did not rebuild or independently compare those 16 ELFs.
- The published route summary reports worst-corner WNS/WHS **+0.234/+0.036 ns** at 1x1/1if and **+0.098/+0.036 ns** at 8x8/1if, with zero routing errors. Those reported values satisfy [#818](https://github.com/kebag-logic/milan-fpga/issues/818)'s **+0.030 ns setup / 0 ns hold** floor. Raw routed corner reports are not present in the inspected packet; this is a consistency check of the published route claim, not independent route signoff.
- `scenario.py` is exactly **1000 lines**. The hot-list check passes with **279 entries**. Diagram pins match the gitlinks, and its source/raster manifest verifies. Local memory verification passes using the existing dependency environment; an initial run without that environment failed to import its dependency and is not a product defect.

**Independent execution and reproducibility**

`run_focused.py`, `focused_native.py` and `probe_charge.py` are portable entry points accepting `--root` and `--packet`; native builders receive `--jobs 4`. Native builds were run concurrently within the allowed job cap. The mixed probe is a separate translation unit including the existing suite, linked against unchanged firmware; production source was not patched.

Receipts with matching `.rc` files include: both mixed probes (exit 1, expected defect detection, with passing bound-only controls); both original SRP suites (114/114 each); mailbox/loop (53/53); ADP (77/77); load; both flip points; shape; hot list; kept/egress self-tests; and memory verification. `evidence-audit.log` checks the published summaries and source identities.

The optional complete budget-grader mutation self-test was started, then stopped to avoid extending this focused review into a lengthy redundant campaign. Its receipt ends with interruption, rc 130; **no completed local pass is claimed**. The complete published exact-head harness self-test remains author evidence. No full parent, PP, gPTP, synthesis or builder bank was run.

`public-identity.log` verifies 47 downloaded public files against their published Git blob IDs at `f7a322f9...`. The public packet contains summaries, hashes and gate receipts; it does not supply the original per-group simulation logs needed for an independent regrade of all timing rows.

**Prior public findings and integration**

After the independent verdict and ledger were written, the PR conversation, formal reviews and review threads were queried. The returned public state contains the two review-start comments, **no prior review submissions and no inline review threads**. There are therefore no earlier public PR findings in the available state to resolve or retain. The snapshot is `public/pr993-discussion.json`; no other reviewer's report was used.

Read-only merge-tree trials found:

| Dependency head | Conflicting files | Disposition |
|---|---|---|
| #1015 `35d29eb71d2cc76717a4550787ef53ff2b72181f` | SUBMODULES.md, submodule_boundaries.drawio/.svg/.png, PNG_MANIFEST.json | Matches the reported pin/documentation conflict. Regenerate for the final pin after ordering the merges. |
| #1017 `079c4fa1514be460949ddc28ae3277ea1873cb48` | **docs/design/SPLIT_CONTROL_MEMORY.md** | Additional conflict: #977's memory-growth/limit history overlaps #1009's binding-save memory paragraph and old half-tile refusal line, around line 166. Preserve both histories and the final candidate's correct limits. |

Receipts: `trial-1015.log`, `trial-1017.log`. These are individual dependency trials, not a validated combined current-dev candidate. The #1015 trial also reports missing older submodule objects during ancestry traversal; its final result fast-forwards the stack pin. Do not treat this trial as complete donor-history or merge acceptance.

**Limits and pending manager duties**

The tracked checkout was preserved. `checkout-audit.log` verifies all **1987 root blobs**, their bytes/modes and index, plus all tracked bytes/modes/indexes of the five populated required submodules. The required pins are tsn-c-stack `5d03517f2ab42416654a8f2be2f71cfc51d82440`, lwSRP `73007b4807977517045e8aa485c61ebb8f5ee843`, and the recorded gPTP/protocol/AXI pins. The unused external import remains uninitialized. There were no source fixes, commits, pushes, GitHub writes, author contact, sub-agents or hardware operations.

The exact-head hosted query returned no check runs, and the combined commit status had zero statuses. It supplies no executed-job proof; an absent or skipped context is not execution evidence. Hosted/local-replica acceptance belongs to the manager.

The manager still owns: fixing and obtaining independent re-review of F1/F2; carrying F3 to the residue checklist; landing #1017 and #1015 first and resolving the additional conflict; advancing the stack pin to the reviewed donor merge commit and regenerating its documentation/diagram; rebuilding and validating the resulting candidate against live dev `e275d7950ef3385753e6a15d2e191ba855b171ed` (or its then-current tip), with builder/native banks and receipts, required hosted acceptance, and post-merge containment. **No manager source bank at this head is asserted or inferred.**

Physical calibration: **NOT RUN**. Simulation, author route summaries and field skips do not constitute hardware proof. This NEGATIVE verdict authorizes no merge.

R958-1 FINISHED
