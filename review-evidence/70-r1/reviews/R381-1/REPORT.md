[R381] NEGATIVE - exact head 6029890c8ba6fd35fac3d3210b8f3a7b30bb1769

# R381-1: external review of PR #610 (issue #70 lane 0, D3 contract adoption)

- Head under review: `6029890c8ba6fd35fac3d3210b8f3a7b30bb1769`, tree `071521406d21866951d6f424f87bea90b405a17e` (verified in the clone, `receipts/integrity.txt`).
- Base: `c07232228c12b72805dd20e6852bf93f25794da0`. Two one-line docs commits (`0309a9ee`, `6029890c`). Four files change: `docs/README.md`, `docs/design/SAVED_STATE_FASTCONNECT.md`, `docs/design/SAVED_STATE_MATERIALIZATION.md` (D3) and `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md`. No RTL, firmware, processor or builder source changes.
- Processor pin at head: `16be6768f710e79450aace277abacd6c2c3336e5`. PR #109 (`008edbbf`) and PR #110 (`939c1433`) are ancestors of it.
- Authorities, in the order read: AGENTS.md, CONTRIBUTING.md section 6, docs/README.md, and the issue #70 body. Then the #70 status audit (5862191328), the assignment (5862193501), the manager rulings (5862405632), the TAKEN comment and both REVIEW READY comments. Then REQUIREMENTS.md sections 1 and 8, and processor docs at the pin. Then the diff and history, then the public evidence tree `review-evidence/70-r1` at `6cf46c2a`.

The contract's main work is correct. D3 is marked Accepted, and all 26 FASTCONNECT acceptance lines map one-to-one to D3 section 17 with their checkbox states unchanged. All ten register rows read RULED, and each one reproduces the manager's selected option byte-for-byte. DR3a and DR4 are carried into the acceptance text and every child contract. The lane 1-5 contracts state acceptance, negative controls and physical results. Nothing claims new implementation or proof. REQ-VER-06 is carried without weakening.

The verdict is still NEGATIVE, because of two open MINOR findings (F1 and F2). F1: the processor F07.9 edit table (item 3 of the assignment) leaves out processor documents at the pin whose statements the adopted contract supersedes. F2: FASTCONNECT section 1 still gives a stale processor pin as current, which contradicts D3's reconciliation baseline and a sentence this change added.

## Findings

### F1: MINOR: Conformance, RTL, Docs: `docs/design/SAVED_STATE_MATERIALIZATION.md:2250-2269` (section 15.2): the processor F07.9 edit table is incomplete against the pin

- **Authority and evidence.**
  - Item 3 of the assignment asks for "the processor F07.9 edit list the adopted contract implies: file, section and change". Section 18.1 makes that table lane 1's documentation acceptance ("Apply the processor documentation table in section 15.2").
  - At processor `16be6768`, these statements contradict the adopted contract and fall outside every row of the table (reproduced by `scripts/finding_evidence.sh`; output in `receipts/finding_evidence.txt`):
    - `docs/architecture/02_interfaces.md:532-536`, the section 8 boot paragraph. It says the sequencer "falls back to vendor defaults on failure, **then** releases `entity_enable`". The table's 02 row covers only 8.1/8.2, lines 538-572. D3 section 8.8 has a CLOSED terminal ("never enabled; no AECP program runs") and requires image proof first.
    - `docs/guides/integrator.md:334`, which says "OR it with `aecp_dyn_dirty_o` for a 'saved state pending' bit". D3 section 5.2 (`:555`) says `aecp_dyn_dirty_o` "leaves `pend_i`", and section 5.1 (`:540`) adds `d3_unflushed_o`.
    - `docs/guides/integrator.md:336`, which says "Nothing in the processor writes a record for 6 or 7". D3 section 3 rule 1 puts the processor-side writer in charge of maps and names.
    - `docs/guides/operator.md:202-206`: "`restore_fail_o` means the whole boot restore was abandoned ... Every sink then starts unbound". D3 section 5.1 (`:540`) makes `restore_fail_o` cover both walks, and section 15.2 itself requires "Preserve completed bindings on D3 rollback". So after a D3-only failure the sinks are not unbound.
    - `docs/architecture/01_overview.md:170` (F01.5 parameter table). D3 section 5.1 (`:541`) adds `DEB_TICKS_P`, `RETRY_MAX_P` and `RS_TMO_CYC_P` for the writer. The 08_timing row covers the T- constants, but no row covers the P- parameter table.
- **Accuracy of the rows that are listed.** These were checked and are correct at the pin:
  - `07_memory_maps.md`: F07.9 runtime at 447-458 and boot at 459-475; the failure table at 476-511; sections 5.1/5.2/5.4.
  - `02_interfaces.md` 8.1/8.2 at 538-572; `05_acmp_engine.md` 5.1; `08_timing.md:42-43`; `09_verification.md` sections 3 and 8.
  - `tb/pp_top`, `tb/nvm_port`, `tb/acmp_nvm` and `tb/desc_mem_guard` all exist.
- **Impact.** A lane 1 that applies section 15.2 exactly still leaves processor interface and integration documents describing the superseded contract: marks and `aecp_dyn_dirty_o` as the pending source, an unconditional defaults-then-enable boot, and a `restore_fail_o` that always means "unbound". Integrators read those documents. The contract's own "synchronized processor documentation edits" (`:543-545`) would then be unsynchronized.
- **Lenses.** Conformance: assignment item 3 is not fully met. RTL: the processor's documented interface contracts would stay inconsistent with the accepted D3 interfaces. Docs: an authoritative edit list is incomplete.
- **Required outcome.** Section 15.2 lists every processor document location at the pin whose statement D3 supersedes, at minimum the five above, with the required change for each. Alternatively, it states an explicit scope rule under which lane 1 must find and reconcile every such statement, with a named check.
- **Verification.** Re-run `scripts/finding_evidence.sh`. Every location it prints under F1 appears in a section 15.2 row, or falls under the stated rule.

### F2: MINOR: Docs: `docs/design/SAVED_STATE_FASTCONNECT.md:119,131-133` against `:83` and `SAVED_STATE_MATERIALIZATION.md:72`: stale processor pin and wiring lines presented as current

- **Authority and evidence.**
  - D3 now states "The reconciliation baseline is parent `c0723222` ... Its processor pin is `16be6768`" (`:71-72`).
  - FASTCONNECT section 1 still says, in the present tense, "**Which donor commit.** The processor pin is `2faa5af8...`". `2faa5af8` is an ancestor 97 commits behind the actual pin.
  - The same section says "The shadow is the ONLY manager wired to the port today (`protocol_processor_top.sv` lines 2261 and 2278)". At the pin, those lines are SRP wiring. The port now sits behind `KL_pp_nvm_mgr_arb` (`:2523`), with manager 1 tied idle (`:2542`).
  - This change replaced the old "Every row below is marked with what proves it" with "Implementation and historical evidence remain explicitly distinguished below" (`:83`). That is a new claim the section 1 pin statement does not meet.
- **Impact.** A cold reader gets two different "current" processor pins from the two pages this lane was told to reconcile, and line citations that point at unrelated RTL. Lane 1 starts from this page's section 1.
- **Required outcome.** Update section 1's pin and line claims to the pin D3 names. Alternatively, mark them explicitly as historical, with the commit they were true at. Or withdraw the new "explicitly distinguished" sentence.
- **Verification.** Re-run the F2 part of `scripts/finding_evidence.sh`. No present-tense pin or line claim on FASTCONNECT contradicts `16be6768`.

### S1: SUGGESTION: Tests, Docs: `SAVED_STATE_FASTCONNECT.md:1548-1552` (Status 10)

The old line "loses exactly the marked changes, and `nvm_dirty` said so beforehand" became "unsaved changes may be lost". The obligation is kept through the cross-reference to D3 section 7.1 (`no_durable_claim_over_unsaved`, K18 `pending_at_the_cut` and `power_cut_loses_only_unsaved`), and DR2a rules it this way, so this is not a weakening. It would still help to state the test oracle inline: every change lost at a cut was reported by producer pending or `nvm_dirty` at the cut.

### S2: SUGGESTION: Docs: `SAVED_STATE_MATERIALIZATION.md:579-583` (section 5.3 change 1)

This paragraph cites `milan_baremetal.c` "lines 1448 and 1219" and says "The code follows the first". At the reconciliation baseline, the quoted comments are at 1450 and 1220-1221. Section 15.1 on the same page cites `:1254` and `:1438` correctly. Aligning the two citations would help.

## What was verified clean (per review focus item)

1. **D3 Accepted; one normative home per rule; no contradiction.**
   - D3 status (`:11`) reads "ACCEPTED contract; materializer not implemented".
   - Section 3.1 (`:400-435`) lists the nine live-write groups. Each has its trigger and replay control, independent input and output formats and maps, user names covering every ordinal, and IDENTIFY (selector 7) excluded, with its checks.
   - The selectors and record IDs agree with `KL_aecp_dyn_state.sv:131-147` at the pin (0 to 5, and 7 = IDENTIFY) and with FASTCONNECT section 4.2 (`:264-277`).
   - The name inventory in section 15.1 equals `scripts/nvm_contract.py` `NAME_SLOTS`.
   - Section 17 (`:2341-2386`) maps all 26 lines. `scripts/check_acceptance_map.py` (in `receipts/acceptance_map.txt`) gives: 5/4/11/3/2/1 per group, 26 rows, and a checked-state sequence identical at base and head.
   - Dirty retirement is owned by D3 section 7 and cross-referenced from FASTCONNECT 9.3 and 16. The boot transaction (AEM first, store-local rollback, combined enable, CLOSED) is owned by D3 sections 8.1, 8.6 and 8.8 and cross-referenced from FASTCONNECT 9.3, 10 and 16. The snapshot page's sections 11, 13 and UNRESOLVED 1, 6 and 10 are consistent with these.
   - The DR3b firmware citations `milan_baremetal.c:1254` (early return before the restore strobe) and `:1438-1455` (`nvm_boot` before `load_aem_image`) are accurate.
2. **Register reproduces the ruling.**
   - `scripts/compare_rulings.py` (in `receipts/compare_rulings.txt`, rc 0): 10/10 rows are RULED, and the selected-option cells are byte-identical to comment 5862405632.
   - The adopted-default cells differ from the round-0 proposals only by the ruling's own qualifications (`receipts/defaults_r0_vs_head.txt`).
   - DR3a (lane 1 measures; the manager ratifies or revises both numbers before lane 2 implements) appears in D3 section 8.8, section 15 item 8, sections 17 and 18.1-18.5, FASTCONNECT 14, 15 and 16, and snapshot UNRESOLVED 1.
   - DR4 (1x1 TDM8 shipping area acceptance; the 8x8 keeps synthesis diagnostics and its post-place obligation stays open and blocked, not waived; non-shipping until it fits, #584/#229) appears in D3 section 10, section 15.1, sections 17 and 18.1-18.5, and FASTCONNECT 8.3 and 16.
3. **F07.9 edit table.** The rows that are listed are accurate. The table is incomplete; see F1.
4. **Child contracts.** Sections 18.1-18.5 each carry acceptance, validation, negative controls and dependencies, and a physical result. Lane 1 explicitly owns none and assigns the physical proof to lane 2. Lanes 2-4 each owe a targeted cold cycle. Lane 5's physical result matches REQ-VER-06 (`REQUIREMENTS.md:250-330`): seven days, 200 cuts (160 idle, 40 during commits), T0 plus 20 s for the first ENTITY_AVAILABLE, the provisional 30 s restoration ceiling, and reconnect under 1 s.
5. **No new implementation or proof claimed; nothing silently weakened.**
   - The status lines disclaim implementation. The PR body says "Relates to #70", not a closing keyword.
   - The FASTCONNECT lede's binding-survival claim links the dated silicon comment 5753091599.
   - The area narrowing is the manager's DR4 ruling, and the 8x8 obligation is retained open.
   - The mark-deletion lines are replaced by nine trigger deletions and nine replay deletions. The IDENTIFY control is kept, and it now also checks flash activity.
   - The cleared-first vacuity rule and REQ-VER-06 are unchanged.
   - Milan item coverage matches the issue body's eight items plus binding, and processor `07_memory_maps.md` section 5.1.
   - Referenced dispositions match public state (`receipts/refs_state.txt`): parent #500, #501 and #502 closed; PRs #557 and #579 merged; processor #92, #93 and #94 closed; #109 and #110 merged into the pin; #15, #20, #61, #83 and #18/#19/#21 open; PRs #129, #130, #603 and #609 open.

## Executed checks (this round, exact head, foreground)

| Check | Result | Receipt |
|---|---|---|
| `docs_check.py`, `check_doc_paths.py`, `check_doc_style.py`, `gen_toc.py --check`, `check_em_dash.py --base c0723222`, `check_baremetal_only.py --check`, `ci_scope.py --selftest`, `check_feature_status.py` (hash-locked Markdown dependencies and PyYAML 6.0.3 in a disposable environment) | all exit 0 | `receipts/gates.txt` |
| `git diff --check c0723222 HEAD` | exit 0 | `receipts/gates.txt` |
| New relative links and anchors (39) resolve | PASS | `scripts/check_new_anchors.py`, `receipts/new_anchors.txt` |
| Register versus ruling, byte-exact | PASS | `scripts/compare_rulings.py`, `receipts/compare_rulings.txt` |
| Acceptance line mapping and checkbox states | PASS | `scripts/check_acceptance_map.py`, `receipts/acceptance_map.txt` |
| Finding evidence F1/F2 | reproduced | `scripts/finding_evidence.sh`, `receipts/finding_evidence.txt` |
| Clone integrity after all checks | HEAD, tree, index (mode/blob/path hash equal to HEAD), 0 porcelain entries, 4 gitlinks unchanged, submodules clean | `receipts/integrity.txt` |

No probe or mutation edited the clone. No Verilator run was needed, because the change is documentation only.

## Reviewer-owned lens ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | assignment items 1-4 against D3 sections 3.1, 15.1, 15.2, 17 and 18; ruling 5862405632; REQUIREMENTS.md sections 1 and 8 (REQ-VER-06); issue #70 item list; processor `07_memory_maps.md` section 5.1; `KL_aecp_dyn_state.sv:131-147` | R381-1 | `6029890c8ba6fd35fac3d3210b8f3a7b30bb1769` |
| RTL | UNCLEAN (F1) | D3 5.1 interface table (`:523-541`) against processor `02_interfaces.md` section 8, `protocol_processor_top.sv:2448-2546` (arbiter, manager 1 tied idle), `KL_aecp_dyn_state` selectors; D3 6.2/6.3 terminal and `own` rules against 8.8 and FASTCONNECT 9.3; DR3b coupled-reset premise; no RTL, clock or CDC change in the diff | R381-1 | `6029890c8ba6fd35fac3d3210b8f3a7b30bb1769` |
| Robustness | CLEAN | D3 6.2 (every abort to DEFAULTS or CLOSED), 8.8 (per-wait deadline, quarantine, no timed port reuse), DR2b/DR2c (identical writes, bounded attempts, sticky alarm), DR3b (shape-mismatch, bad-AEM and CPU-restart paths), 18.1-18.5 negative controls (zero, boundary, corrupt, refused, indefinitely delayed, over-capacity, malformed, cuts at erase/program/verify/capture/ACK/restore), single-legal-value rows and the 1x1/8x8 configuration dependence in 15.1 | R381-1 | `6029890c8ba6fd35fac3d3210b8f3a7b30bb1769` |
| Tests | CLEAN | FASTCONNECT section 16 at base and head (`receipts/acceptance_map.txt`); D3 3.1 trigger/replay/IDENTIFY controls and 8.2 cleared-first rule, each stated so that it can fail; child-lane negative controls, each bound to a named assertion; no test or criterion weakened except the manager-ruled DR4 scope, with the 8x8 retained; lane gates rerun at head (`receipts/gates.txt`). S1 is a SUGGESTION only. | R381-1 | `6029890c8ba6fd35fac3d3210b8f3a7b30bb1769` |
| Docs | UNCLEAN (F1, F2) | all four changed pages at head; `docs/README.md:72-73`; snapshot status line; anchors (`receipts/new_anchors.txt`); REGISTER_MAP control rows `:2238-2245`; processor docs and guides at `16be6768` (`receipts/finding_evidence.txt`); other parent references to D3 (`tb/verilator/nvm_cosim/README.md:176`, CHANGELOG) | R381-1 | `6029890c8ba6fd35fac3d3210b8f3a7b30bb1769` |

## Prior public review findings

At the time of this review, PR #610 had no reviews, no review comments, and two issue comments, both review-start notices. Issue #70 had no reviewer findings against `0309a9ee` or `6029890c`. This is the first review round of the PR, so there are no prior findings to resolve or retain.

## Real limits

- The Milan v1.2 and IEEE texts were not available to this review. Clause citations (5.3.4.1/.2, 5.3.5.1, 5.3.7.1/.6, 5.3.8.x, 5.3.9.1, 5.3.10.1, 5.3.11.1, 5.3.12, 5.3.13, 5.6.2) were checked against the repository's own quotations (the issue #70 body, processor `07_memory_maps.md` section 5.1, REQUIREMENTS.md), not against the specification.
- The historical EXECUTED claims in D3 sections 2-14 are text unchanged by this PR. The out-of-tree evidence branch they cite was not re-run.
- The public evidence tree `review-evidence/70-r1` at `6cf46c2a` contains the author's docs-gate logs only. This review did not locate the manager's full static/builder/native bank receipts in it, and did not re-run those banks, which is outside this review's allowance.
- Hosted checks at the exact head, at fetch time (`receipts/hosted_checks.txt`): `rtl-fast`, `full-ci-gate`, `elaborate`, `bdd-conformance`, `wire-accountability`, `changes` and `docs-check-no-git` succeeded. `docs-check` was still in progress. The Verilator/Yosys long gates and the physical gPTP context were skipped, not executed. These are not evidence here.
- There is no physical evidence. Physical calibration was NOT RUN, and field skips are not hardware proof.

## Pending manager duties

- Publish this report. Obtain the internal review's verdict.
- Have the executor address F1 and F2 (S1 and S2 are optional), then re-review at the new head. Because both fixes are documentation, the Docs, Conformance and RTL lenses must be covered again at a head that includes the change.
- Confirm hosted `docs-check` completes successfully at the exact head, and own hosted/act acceptance.
- Build and validate the final current-dev candidate at the merge turn. The source base and live dev were both `c07232228c12b72805dd20e6852bf93f25794da0` when this review started.
- After merge: DR3a ratification or revision following lane 1's measurements, before lane 2 implements. #70 stays open; this lane does not close it.

R381-1 FINISHED
