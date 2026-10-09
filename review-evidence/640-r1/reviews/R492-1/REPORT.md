[R492] NEGATIVE - exact head c4b8b7d373c9233bc9e71c6ed32eae9ad2b3f970

# R492-1: internal independent review of PR #698 (relates to #640), Mark II area plan

- Head: `c4b8b7d373c9233bc9e71c6ed32eae9ad2b3f970`, tree `a95adb1ad43e09865509188697ec4a96f42d7a83`.
- Source base and live dev at assignment: `5603c353137e90c1fa95429f6d00ef7a2298d9ee`.
- Diff `5603c353..c4b8b7d3`: `docs/design/MARK_II_AREA_PLAN.md` (+861, new) and `docs/design/AREA_BUDGET.md` (+89/-8). No RTL, script, record or policy change. Verified with `git diff --stat`.
- History: `8d3be734`, `06f5e7e5` (round 1), merge `a959b787` (parents `06f5e7e5`, `5603c353`; it adds only the plan file to dev), then four round-1b commits. All messages are one line with no trailers.
- Reviewer role: cleared-context internal reviewer. Five lenses applied independently. No source edit, commit, push or GitHub write.

## Verdict basis

Three MINOR findings remain open. Each is attributed to every lens it touches, so all five lenses are unclean at this head. Four RESIDUE items and two SUGGESTIONs do not affect the verdict.

The plan is otherwise strong:

- Every recorded figure and ledger sum I recomputed matches (174 of 174 checks).
- Every decision named in the assignment is folded in without contradiction.
- The 48 documentation and resource-policy gates pass at the head.

## Findings

### R492-1-F1 MINOR - split-aware measurement is a prerequisite of the flip and of the week-4 checkpoint, but is scheduled for no lane

- Lenses: Conformance, RTL, Robustness, Tests, Docs.
- Where: `docs/design/MARK_II_AREA_PLAN.md:676`, `:708`, `:716`, `:724-740`; `docs/design/AREA_BUDGET.md:212-215`.
- Authority and evidence:
  - The stage-1 assignment (#640 comment 5988586965, item 4) and round 1b (6080904058, item 4) ask for each lane's dependency and order.
  - D7 (5990755268) requires that "the resource gate still judges each lane against the last record, so growth stays visible".
  - The integrated recipe refuses an image without exactly one wrapper: `syn/ooc/pp_baseline.py:35` and `:50` ("Expected exactly one protocol wrapper"); `syn/ooc/pp_resource_gate.py:176`. The plan states the same at `:736`.
  - The flip is order 1 of the ledger (`:676`, weeks 1-6 at `:708`). On the plan's own central figures it alone reaches 36,267, already under 38,040. The default-flip PR must run "the full local and hosted implementation gates on that head" (`docs/ARCHITECTURE_HW_SW_SPLIT.md`, section 7, step 7).
  - The week-4 checkpoint now depends on "the first integrated split route" (`:724-727`).
  - Yet the split-aware capability appears only as an M9 need (`:737`; AREA_BUDGET `:214`) and as "a future tooling obligation" (`:740`). No lane, owner or week carries it. Neither the F0-F5 row (`:708`) nor the M9 row (`:716`) lists it as a dependency.
- Impact: once the default flips, no resource gate comparison can run until the tooling exists. That affects M2-M8 lanes measured after the flip and any other merge that moves the shipping image, so the D7 visibility is lost. The week-4 checkpoint can only report "missing". The order and dependency table therefore schedules a step that cannot be measured.
- Required outcome: the plan and AREA_BUDGET name the split-aware measurement capability as a scheduled dependency, with its owner lane and week. It must come before the first measured split route (week 4) and before the default flip. Alternatively, the plan states that the flip lands inside M9 and that no split route is measured earlier, and the week-4 and ledger text agree with that. Either way, the D7 comparison must stay possible for every lane after the flip.
- Verification: re-read the lane table and the "Lane sequence" text at the fix head. The capability's lane must precede the flip and the week-4 checkpoint, and AREA_BUDGET must state the same order.

### R492-1-F2 MINOR - M8a's saving basis cites #649 LUT cells as LUTs, against the source's own warning

- Lenses: Conformance, RTL, Docs.
- Where: `docs/design/MARK_II_AREA_PLAN.md:545` ("The historical #649 controller/PHY census contains 823 + 873 LUTs"); the M8a basis at `:650`; AREA_BUDGET `:189`.
- Authority and evidence:
  - Round 1b item 3 requires each figure to have its basis stated.
  - `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:262-273` says the report cannot split the SoC top's LUTs. The 823 and 873 are "LUT cells", counted "before Vivado combines two into one LUT site, so they are not comparable to the LUT column". 3,231 of the top's LUT cells are anonymous and carry no owner.
- Impact: the 1,600-LUT central (1,200-2,000) for M8a rests on a misread measurement. Pre-packing cells overstate packed LUTs by an unknown factor. Unowned cells add uncertainty in either direction. The ledger's conservative image still clears the bar with M8a at its low end, so the plan's conclusion does not move. The stated basis is still wrong.
- Required outcome: describe the basis as pre-packing LUT cells with the unowned remainder. Then either justify the 1,600 central and its range against that, or reprice it. Mirror the change in AREA_BUDGET.
- Verification: compare the corrected sentence with `649_RESOURCE_MAP_AND_SENSITIVITY.md:262-273`. Re-run the ledger arithmetic (`scripts/recompute_ledger.py`) if any figure changes.

### R492-1-F3 MINOR - the no-split figure omits the plan's own retained-fabric lanes, and no partial-flip outcome is priced

- Lenses: Conformance, RTL, Robustness, Docs.
- Where: `docs/design/MARK_II_AREA_PLAN.md:690`, `:691-692`, `:729-730`; AREA_BUDGET `:182-206`.
- Authority and evidence:
  - The owner decision 5993114362 says each function ships in the split only after its suites and bench re-run. "Any other function ships all-fabric." A partial flip is therefore an anticipated outcome.
  - Focus item 4 asks whether the plan reaches 38,040 with the stated margin.
  - `:690` states "Without the split, these retained-fabric levers reach only 45,067 centrally". That is 50,267 minus M2 to M8b only. The plan prices M3 (2,600) and M10 (1,200) at `:654-665` precisely for images where fabric AECP remains. With them, the no-split central is 41,267 (NOTE lines in `receipts/recompute_ledger.txt`).
  - No scenario prices the most likely partial outcome: F5 (AECP and notification) left in fabric, with M3 and M10 active. The plan says only that a partial flip "must subtract only its measured disjoint contribution" (`:691`) and that a missed bound "blocks the default ledger" (`:729`).
  - Reviewer arithmetic, illustrative only, from the plan's own rows:
    - Assumptions: AECP, notification, the originator and the fabric NVM path stay in fabric. The mailbox and allowances are debited. M2-M8b, M3 and M10 apply.
    - Result: about 37,357 centrally, just inside the 37,659 margin bar, and about 42,757 conservatively, over the limit.
    - The answer depends on assumptions the plan should own.
- Impact: the plan's only fallback figure misstates the all-fabric case by 3,800 LUTs. The manager has no priced view of whether a partial qualification still meets NFR-RES-01, or what more would then be needed. That is exactly the week-4 decision D8 assigns.
- Required outcome:
  - Correct or qualify the no-split figure so that it includes M3 and M10, or explicitly excludes them with the inclusive figure beside it.
  - Add at least one priced partial-flip scenario (F5 unqualified), with its assumptions. State whether it meets 38,040 and 37,659, and what extra lever or ruling would be needed if not.
  - Keep AREA_BUDGET consistent.
- Verification: recompute the new scenario rows from the record and the plan's own lane figures.

### RESIDUE (wording only; carried to the residue checklist)

- R492-1-R1, sentence length (`docs/README.md:140`, "Keep current sentences under eleven words"):
  - Measured with the repository's own analyser (`receipts/style_probe.txt`): 132 sentences over ten words in the plan and 130 in AREA_BUDGET.
  - That includes 73 in the plan's current sections (`:378-816`), for example the 37-word basis sentence at `:655-658`. On AREA_BUDGET it includes added lines `:32`, `:168`, `:202`, `:209`, `:266` and `:272`.
  - The style gate does not list these pages, so it passes.
  - Exact fix: split each current-section sentence to ten words or fewer. Alternatively, move the long historical prose (`:142-376`, `:817-861`) under an explicit history note.
- R492-1-R2, references that are not links:
  - Bare issue numbers do not render as links in a repository file: #640, #645, #647, #686, #661, #664, #665, #396, #70, #75, #117, #232, #230, #639, #649, #233, #653, #652, #682.
  - Code paths named in backticks are also unlinked: `milan_soc.py` (`:414`), `milan_datapath.sv` (`:415`), `check_nvm_capture.py` (`:561`), `sw/firmware/ctrl/` and `sw/firmware/ctrl_nvm/` (`:708`), `hdl/common/csr/milan_csr.sv` (`:710`), `syn/resmap/resmap_map.py` (`:827`).
  - Exact fix: make each a Markdown link to its issue or file.
- R492-1-R3, present tense in labelled history:
  - These lines read as current, although the record now describes `a5ca6e51`: `:150` ("The resource gate's record describes dev `54643724`"), `:169` ("22 slices are free ... until this plan lands") and `:827-828`.
  - Exact fix: past tense, or an "at `e6172750`" qualifier.
- R492-1-R4, `docs/design/AREA_BUDGET.md:280-281`: two consecutive blank lines added. Exact fix: delete one.

### SUGGESTION

- R492-1-S1: the L11b core pricing (3,066 / 843 / 1,051 LUT, `:553-557`) rests on logs kept outside the repository, cited by 16-hex digest prefixes (`:853-855`). Publishing the Tcl and utilisation reports, or the exact reproduction command, would let a cold reviewer check the second-largest M-lever.
- R492-1-S2: M2's scope "outside other lanes" (`:445`, `:645`) would be checkable if it named the SoC FIFOs that survive D4. Several generated FIFOs serve the DDR3 path that M8a removes.

## Prior public findings

At the start of this round, PR #698 carried no review, no review comment and no finding. Its only comments are the two review-start notices. Issue #640 carries no reviewer finding on the plan. Nothing is to be resolved or retained.

## What each lens examined

### Conformance

- Target (`:46-59`), checked against the issue #640 body (frozen acceptance) and the stage-1 assignment 5988586965:
  - 38,040 is 60 % of 63,400.
  - The timing gate is +0.030 / 0 ns (`docs/integration/BUILDING.md` section 5).
  - Function stays unchanged.
  - The re-record happens in the reaching lane (M9 under D7).
- Decisions, each checked against its comment text:
  - D1 (`:784`) and D3 (`:786`, `:763-766`), including stream restart under 1 s, fast connect and the capture bound.
  - D6 (`:789`): deferred, then planned by 5991591637, then given zero default credit after the split.
  - D7 (`:756-762`, `:790`; AREA_BUDGET `:271-278`). The rule and the 2026-10-05 schedule correction (AREA_BUDGET `:148-153`) are both present.
  - D8 (`:51`, `:791`), D2 (`:480-489`), D4 (`:542-547`) and D9 (`:792`).
  - D5 (`:549-563`). The 24.5 ms bound is half of 49 ms in `scripts/check_nvm_capture.py:108-115`.
  - Milestone 13 decisions 5991605450, 5991626132, 5991695093 and 5991737927 (`:796-799`).
  - The default split 5991745829 and the before-release landing 5993114362 (`:800-807`).
  - The #664 flip rule (`:813`; `docs/reference/FR_NFR.md` NFR-SCOUT-02). The approval link 6015500032 resolves.
- Nothing contradicts a decision. F1 and F3 are completeness defects of item 4. F2 is a basis defect of item 3.
- All 14 added comment links resolve to the issue they name (`receipts/comment_links.txt`).

### RTL

- No RTL is in the diff. Architecture claims checked in source at the head:
  - `KL_pp_shadow` is instantiated unconditionally at `hdl/milan/milan_datapath.sv:8003`.
  - `--ctrl-mailbox` defaults off, and its datapath side is held idle (`sw/litex/milan_soc.py:2480-2510`, `:2548-2550`).
  - F0-F4 firmware is present (`sw/firmware/ctrl/{adp,acmp,maap,srp,mbx}`, `sw/firmware/ctrl_nvm/`). There is no AECP firmware.
  - The mailbox's last RTL change (`a00c2681`) is the measured round 3.
  - Retained fabric ownership matches NFR-SCOUT-02/03.
- The record's inputs `a5ca6e51` are an ancestor of dev. Between them no `hdl/`, `sw/litex`, submodule or `syn/` input changed except the records file. So the record describes dev's design.
- Findings:
  - F1: the flip's resource and timing effects cannot be measured on the plan's schedule.
  - F2: the resource basis is misread.
  - F3: the partial-flip resource effect is unpriced.

### Robustness

- Failure and alternate paths of the plan:
  - The D5 revert (`:563`) and a missed deadline or service bound (`:729-731`).
  - BRAM ceiling and primitive-growth handling (`:634-638`, `:759-762`; AREA_BUDGET `:276-278`). The record's tolerance for RAMB and DSP is 0.
  - Memory capacity for F5 (`:427-431`, `:567-568`) and the second-port seam (`:753-755`).
- Findings:
  - F1: measurement depends on the configuration after the flip.
  - F3: the partial-qualification outcome is unpriced.

### Tests

- Every named verification suite exists as `tb/verilator/<name>`: pp_shadow, nvm_cosim, milan_dp, tcam_csr, avtp_rxmon, tkdiag, chmap_capture, render_setpoint, gptp_plane, gptp_shadow, gptp_txts, milan_dp_gptp, nvm_capture_cpu, csr, mbx.
- The documented commands exist:
  - `pp_resource_gate.py record --baseline --write`.
  - `resmap_map.py map --baseline --endpoint --out`.
  - `syn/resmap/route_map.tcl`.
- Gates rerun independently at the head: 48 of 48 rc 0 (`receipts/gates/summary.txt`), with the same command list as the author's receipts. The resource self-test, mutant driver and `check-baseline` are included.
- My ledger checker passes 174 of 174. A planted two-figure mutant makes it fail with rc 1, naming both figures (`receipts/recompute_ledger_mutant.txt`).
- Finding F1: the week-4 and post-flip measurements cannot run with the current recipe.

### Docs

- Recomputed against `syn/ooc/pp_resource_baseline.json`:
  - The three endpoint rows, nine figures each, and the three input digests.
  - All 22 current-inventory rows at three endpoints.
  - 71 free slices, 47.5 free BRAM tiles, a 34-tile ceiling allowance and the +0.049 ns WNS bar.
- Recomputed ledger arithmetic:
  - Split basis: 17,678; gross 18,107; residual 5,501; 6.5 tiles; split 14,005 / 11,505 / 16,005.
  - All 24 cumulative cells.
  - Headroom: 6,973 (18.33 %) central and 2,973 (7.82 %) conservative; 36,367 without M8b.
  - M3 basis: AECP own logic 1,302, dispatch queue 421, about 3,380 displaced.
- AREA_BUDGET's ledger and endpoint tables agree with the plan.
- Cross-checked against their sources:
  - The #234 receipt: route log SHA-256 and size.
  - The mailbox figure (`docs/design/MAILBOX_SPLIT.md`, "Measured area"): 3,102 LUT, 2,946 FF, 1 RAMB36 + 10 RAMB18, +0.402 ns at 10 ns.
  - The #649 per-stream figures: 2,893 / 210.6 / 208.5 / 316.9 / 205.1.
- Findings: F1, F2 and F3, plus residue R1 to R4.

## Reviewer-owned completion ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2, F3) | #640 body; comments 5988586965, 5990755268, 5991591637, 5991605450, 5991626132, 5991695093, 5991737927, 5991745829, 5993114362, 6080904058; plan `:46-59`, `:401-441`, `:577-816`; AREA_BUDGET `:120-215`, `:263-278`; FR_NFR NFR-RES-01, NFR-SCOUT-01/02/03 | R492-1 | c4b8b7d373c9233bc9e71c6ed32eae9ad2b3f970 |
| RTL | UNCLEAN (F1, F2, F3) | `milan_datapath.sv:8003`; `milan_soc.py:2480-2610`; `pp_baseline.py:35,50`; `pp_resource_gate.py:176`; `MAILBOX_SPLIT.md` measured area; mailbox RTL history; record inputs ancestry | R492-1 | c4b8b7d373c9233bc9e71c6ed32eae9ad2b3f970 |
| Robustness | UNCLEAN (F1, F3) | plan `:426-441`, `:549-568`, `:634-639`, `:686-693`, `:724-740`, `:742-775`; AREA_BUDGET `:271-278`; record tolerances | R492-1 | c4b8b7d373c9233bc9e71c6ed32eae9ad2b3f970 |
| Tests | UNCLEAN (F1) | 48 gate receipts; `recompute_ledger.py` with its mutant control; suite directories; CLI help of the documented commands | R492-1 | c4b8b7d373c9233bc9e71c6ed32eae9ad2b3f970 |
| Docs | UNCLEAN (F1, F2, F3) | both changed pages in full; `pp_resource_baseline.json`; `234_PP_SHADOW_AREA_BASELINE.md:30-100`; `649_RESOURCE_MAP_AND_SENSITIVITY.md:262-273, 640-655`; `ARCHITECTURE_HW_SW_SPLIT.md` section 7; comment-link check; style probe | R492-1 | c4b8b7d373c9233bc9e71c6ed32eae9ad2b3f970 |

## Real limits

- Docs-only review. I ran no synthesis, route or simulation, and verified no figure by a new measurement. Every LUT figure in the plan is either a committed record or an estimate the plan labels as one.
- The historical 2026-10-05 measurements (route at `e6172750`, core pricing) cannot be reproduced from public state. Their logs are outside the repository (S1).
- From the published author evidence (`review-evidence/640-r1` at `994453e9`), I checked only the manifest digests and the gate receipt list (`receipts/public_evidence_sha256.txt`). My gate results are my own reruns.
- I ran the gates with the pinned Markdown environment (cmark-gfm 2025.10.22, html5lib 1.1). The `gptp-processor` and `protocol-processor` submodules were initialised. `external` and `third_party/lwSRP` were not, and no gate needed them.
- Hosted contexts at the exact head are a snapshot from about 13:00 UTC (`receipts/hosted_checks.tsv`). Several were still in progress. One physical context was skipped and proves nothing. I make no hosted claim.
- Physical calibration NOT RUN. No hardware evidence is claimed or implied.
- After the probes, the clone matches the exact head (`receipts/restore_check.txt`):
  - HEAD is `c4b8b7d3`. The tree and the index tree are both `a95adb1a`.
  - The status is empty, and the submodule gitlinks are unchanged.

## Pending manager duties

- Carry R492-1-R1 to R4 to the residue checklist.
- Route F1 to F3 to the executor for a corrected head, then re-review all five lenses at that head.
- Hosted and act acceptance at the exact head.
- The current-dev merge candidate (builder and native banks) at the merge turn. No manager source bank is claimed for this head.
- The second independent review (external) and merge authorization are still outstanding.

## Receipts

Listed with digests in `MANIFEST.sha256`:

- `scripts/run_gates.sh`: the gate runner.
- `scripts/recompute_ledger.py`: the ledger checker.
- `scripts/style_probe.py`: the sentence-length probe.
- `scripts/check_comment_links.sh`: the link resolver.
- `scripts/dump_records.py`: the record dump.
- `receipts/`: all outputs. Local paths in two gate receipts are redacted as `<clone>` and `<pinned-md-python>`.

R492-1 FINISHED
