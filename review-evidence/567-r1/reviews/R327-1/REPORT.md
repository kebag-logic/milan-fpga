[R327] NEGATIVE - exact head 54b4c3bbbc8cdea5ced0be29c9226fdf82233b74

# R327-1 external independent review: issue #567 / PR #569

Round: R327-1. Head: `54b4c3bbbc8cdea5ced0be29c9226fdf82233b74`. Tree: `36338cae0ebdd410a366e38a67d80af7c3efb4a7`.
Base and live `dev`: `7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a`, which is the merge base; both values were read publicly (`receipts/history_and_scope.txt`).
Processor pin: `990f96526bb89356c963a260ebbdcf2a77e6623a` -> `0922e43408f891fc0b84a84691df86b4fd0f1c0d`.

I reconstructed the task from public sources only, in this order: AGENTS.md and CONTRIBUTING.md (sections 2.2 and 3); docs/README.md; the issue #567 body and acceptance; the A10 comments (the ready assignment, the Round 2 ledger decision 5845149786 and the Round 3 text assignment); the A325, A330 and A332 TAKEN and REVIEW READY comments; the PR #569 body; `docs/reference/SUBMODULES.md`, `syn/yosys/ooc.sh` and `rom_digests.tsv`; the processor range 990f9652..0922e434; the parent diff and history; the manager's public evidence manifest at `d7d077b0`; and the exact-head hosted check runs.

The verdict is NEGATIVE because one MINOR finding remains open (F1). The pin move itself is correct and verified: the processor HDL is identical across the range, the ledger rows reproduce byte for byte, the OOC path accepts the pin, the diagram reproduces byte for byte, and every parent gate that reads processor files passes. However, one parent document still tells the reader to restore the previous pin as the pin of record.

## Findings

### F1: MINOR (Docs, Conformance): a README procedure still restores `990f9652` as the pin of record

- **Location:** `tb/verilator/milan_dp/README.md:468`, in the row "the pre-#112 processor `7a47f578`". The row reads: "Local control only: temporarily repin the existing submodule, build the same leg in a fresh directory, run once, then restore `990f9652` ... The same fixture passes at the restored pin."
- **Authority:** issue #567 acceptance 1 requires the pin text to be updated. The review focus item 3 requires that nothing still describes `990f9652` as current. The same lane rewrote line 520 of this README ("The adopted pin `0922e434` includes processor PR 115"), so current-pin statements in this file are in the lane's scope. The row two lines below, at line 470, already uses the pin-neutral wording "then restore the pin". Evidence: `receipts/grep_990f9652.txt` lists every remaining `990f965` reference. The others are dated measurements (`:442`), pinned-content permalinks whose target sections are unchanged in the range (`:552`), historical changelog and adoption records, or the retained ledger rows. Only `:468` gives an instruction that names the old pin as the restore target.
- **Impact:** someone reproducing this failing arm at the adopted head ends with the processor checked out at `990f9652` and believes it is the pin of record. `receipts/offpin_probe.txt` shows the consequences. The OOC path refuses that state (rc 2: the checkout disagrees with the superproject pin). `lint_rtl.py --check` still passes (rc 0), and the `milan_dp` Makefile derives sources from the checked-out tree without a pin check. So a later local run silently measures the previous processor. That is harmless for RTL only while the two pins' `hdl/` trees are identical, which is true at this head. The document is also internally inconsistent with the adopted pin that it states 50 lines later.
- **Required outcome:** the procedure names the pin of record, or uses the wording "restore the pin", instead of `990f9652`. If the dated evidence should keep its provenance, state the measurement pin as history, for example "measured at `990f9652`". No other change is required.
- **Verification:** `git grep -n '990f965'` shows no instruction or current-state statement naming `990f9652`. Docs gates (`docs_check.py` in both modes, `check_em_dash.py --base 7eb3b0d4...`, `gen_toc.py --check/--verify-anchors`, `check_doc_paths.py`) return 0.

### S1: SUGGESTION (Docs): "OOC synthesis requires rows for every pin" is imprecise

- **Location:** `docs/reference/SUBMODULES.md:57`.
- **Evidence:** `syn/yosys/ooc.sh:378-396` and `:463-470` read the superproject gitlinks and require rows keyed by the exact protocol-processor and gPTP pins of record. It does not require rows for every pin. `receipts/rom_ledger_probe.txt` probe 4 shows the refusal.
- **Suggested wording:** "OOC synthesis requires ledger rows for the exact pin of record."

### S2: SUGGESTION (Conformance, RTL): three shape parameters agree with the entity model only by default, outside this lane's scope

- **Location:** `hdl/milan/KL_pp_shadow.sv:1057-1072`, with `sw/builder/endstation_builder.py:5085-5090`.
- **Evidence:** the adopted inventory (`protocol-processor/docs/guides/integrator.md` section 2 at `0922e434`) documents `N_AUDIO_UNIT_P`, `N_CLK_DOMAIN_P` and `N_CONTROL_P` as values that must "match the entity model". The parent leaves all three unbound, so they take the processor default of 1. The builder emits exactly one AUDIO_UNIT, one CLOCK_DOMAIN and one CONTROL descriptor, so the values agree today (`receipts/param_agreement.txt`: AGREEMENT OK). `KL_pp_shadow` already receives `N_AUDIO_UNIT_P`/`N_CLK_DOM_P` from the generated header but forwards them only to its saved-state allocation. This predates the pin move, because the processor HDL is unchanged.
- **Suggestion:** file a separate Issue to bind these parameters from the generated header, or to make the builder refuse counts other than 1. Do not change it in this pin-only lane.

### S3: SUGGESTION (Docs): the PR body carries two stale status lines

- **Location:** the PR #569 body, "Status" and "How to validate" sections.
- **Evidence:** the body says "The branch remains unpublished; hosted checks and review are pending" and "Round 3 documentation evidence is posted on the issue for the candidate head". At review time the head is published as the PR head, exact-head hosted contexts are running or complete (`receipts/hosted_checks_54b4c3bb.txt`), and the A332 REVIEW READY comment on the issue carries the Round 3 evidence.
- **Suggestion:** refresh the status paragraph at the next head so a cold reader is not misled.

## Per-lens results

- `[R327] PASS RTL — protocol-processor gitlink 990f9652..0922e434; hdl/milan/KL_pp_shadow.sv:1057-1072; syn/yosys/run.sh; syn/yosys/ooc.sh — processor hdl tree d8879608 identical at both pins, diffstat empty; parent hdl/ and VERSION unchanged; 14 parent bindings name real top parameters; three-top elaboration, KL_pp_shadow OOC synthesis, xvlog (Vivado ran, 4 == ratchet) and lint pass`
- `[R327] PASS Robustness — syn/yosys/ooc.sh:378-470 with syn/yosys/rom_digests.tsv — ledger without the 0922e434 rows refuses rc 2; a wrong 0922e434 digest refuses rc 2; an off-pin processor checkout at 990f9652 refuses rc 2 despite the retained 990f9652 rows; the record mode reproduces the committed ledger byte for byte and retains all other pins`
- `[R327] PASS Tests — tb/verilator/pp_shadow; tb/verilator/milan_dp notify and crflic legs; protocol-processor/tb/pp_top; protocol-processor/scripts/check-integrator-params.py — pp_shadow 402/0 in each of three builds; notify 381/0 including all [GSI] phases; crflic 415/0; the processor's native pp_top 7666/0 (7646 default + 20 fixture) under Verilator 5.050; the inventory checker fails on a dropped guide row and an extra top parameter, and passes when restored; the lane adds no parent test and weakens none`
- `[R327] UNCLEAN Conformance — issue #567 acceptance 1-4 against the head — acceptances 2, 3 and 4 are met, and so is the Round 2 ledger decision. In acceptance 1, the gitlink, SUBMODULES.md, the regenerated diagram and CHANGELOG are met, but the pin text is not complete because of F1`
- `[R327] UNCLEAN Docs — CHANGELOG.md:11,34-47; docs/reference/SUBMODULES.md:25,29,42-65,153-158; docs/diagrams/submodule_boundaries.{drawio,svg,png}; docs/diagrams/PNG_MANIFEST.json; tb/verilator/milan_dp/README.md:442,468,520,552 — the diagram regenerates byte for byte, all docs gates pass in both modes, and the removed F01.5 conflict row is resolved by processor PR 118 (F01.5 now marks P-EN-MVU-SUID/MCR reserved, n/a); F1 remains open`

## Acceptance evidence, item by item

1. **Gitlink and pin documentation.** The gitlink is at `0922e434`. This is the upstream `main` head and the merge commit of processor PR 119; it is 9 commits ahead of `990f9652` and 0 behind (`receipts/pp_upstream_reachability.txt`). SUBMODULES.md, CHANGELOG and the diagram are updated. The repository generator's write mode reproduces the committed `.drawio`, `.svg`, `.png` and `PNG_MANIFEST.json` byte for byte (`receipts/diagram_regen.txt`). The `--check` and `--selftest` modes pass, as do `check_submodule_docs.py` and `check_diagram_pngs.py`. Open item: F1.
2. **ROM ledger.** The processor ROM generators live under `hdl/` (`ooc.sh:434-436`), and `hdl/` is identical across the range, so the ROM sources did not change. Under the A10 Round 2 decision the rows are keyed by exact pin, so re-recording is required anyway. `./ooc.sh --record-rom-digests` reproduced the committed ledger byte for byte. The two new rows equal the `990f9652` rows (ltn `23cc67ee...`, ucode `23605682...`). The committed ledger diff against the base is exactly those two added lines. `./ooc.sh KL_pp_shadow` passes at the pin (rc 0; 66991 LUT_TOT, 30187 FF). Receipts: `receipts/rom_ledger_probe.txt`, `receipts/ooc_KL_pp_shadow.txt`.
3. **Gates that read processor files, and the inventory.** `check-integrator-params.py`, run from the parent pin, reports top 24, guide 24 and diagram 24, OK. Its inventory names no parent parameter. Every parent binding names a processor top parameter, and the stated contracts of the unbound parameters hold for the generated model (see S2 for the latent coupling). The following all return 0: `pp_srcs --check/--selftest`, `check_rtl_source_lists`, `xvlog_gate --check`, `lint_rtl --check`, the sv/cpp/py/sh idiom checks, `check_port_contracts`, `measure_naming --check`, `measure_test_evidence --check` (which reads the changed processor `hdl.yml`), `check_todo_ownership` (which reads the changed processor `Makefile`), `check_hygiene`, `check_soc_sources`, `gen_module_matrix --check`, `ci_events --check`, the docs gates in both modes, and `git diff --check` over the range (`receipts/gates/SUMMARY.txt`). The first attempt at the em-dash and TOC gates stopped with rc 2 because the locked renderer was missing. After the hash-locked `tools/markdown/requirements.txt` set was installed in a disposable environment, both returned 0. The simulation legs are listed under Tests above.
4. **No parent RTL change.** `git diff 7eb3b0d4..HEAD -- hdl VERSION` is empty. The PR changes nine files: the gitlink, the ledger, and documentation and diagram artifacts.

Pin-only scope: every changed file follows from the pin move. The deleted SUBMODULES.md conflict row about F01.5 `P-EN-MVU-SUID/MCR` at 1/1 is justified by the adopted processor `docs/architecture/01_overview.md`, which now marks those names reserved and n/a. The parent MVU documents and BDD tables (`FR_NFR.md` FR-MVU-02, `MILAN_COMPLIANCE_MATRIX.md:136-137`, `aecp_response_contract.feature:136-139`) already match the adopted waiver and its cdl 28/20/92/20. All three commits have one-line messages with no body or trailers.

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | issue #567 acceptance 1-4, A10 Round 2/3 decisions, gitlink, processor range and PRs 118/119, ledger, parameter agreement | R327-1 | 54b4c3bbbc8cdea5ced0be29c9226fdf82233b74 |
| RTL | CLEAN | processor `hdl/` tree ids, parent `hdl/` diff, `KL_pp_shadow.sv:1057-1072`, three-top elaboration, KL_pp_shadow OOC, xvlog, lint | R327-1 | 54b4c3bbbc8cdea5ced0be29c9226fdf82233b74 |
| Robustness | CLEAN | `ooc.sh` ledger/pin refusals (missing rows, wrong digest, off-pin checkout), record-mode retention | R327-1 | 54b4c3bbbc8cdea5ced0be29c9226fdf82233b74 |
| Tests | CLEAN | pp_shadow (3 builds), milan_dp notify and crflic, processor pp_top, inventory-checker fault probes | R327-1 | 54b4c3bbbc8cdea5ced0be29c9226fdf82233b74 |
| Docs | UNCLEAN (F1) | CHANGELOG, SUBMODULES.md, diagram set and manifest, milan_dp README, PR body, docs gates both modes | R327-1 | 54b4c3bbbc8cdea5ced0be29c9226fdf82233b74 |

## Limits

- The Verilator 5.050 path named in the assignment (`.../372-manager-candidate1/pinned-tool-bin/verilator`) does not exist on this host. I used a private wrapper around the same container-image Verilator binary that other lanes' pinned wrappers use. It reports `Verilator 5.050 2026-07-01 rev v5.050`; the binary's sha256 is in `receipts/tool_identity.txt`. The host sv2v is v0.0.13, not the v0.0.12 the author recorded. `ooc.sh` accepted it and the netlists were not compared.
- This review did not run the full parent, processor, gPTP, Yosys or builder banks, the other milan_dp legs, the builder, NVM or BDD suites, act, or any hardware. The xvlog gate did run, with Vivado present.
- The M4/M4L MVU checks in the processor's pp_top print no per-check lines. Their presence is inferred from the default-build total of 7646, which equals the 7,640 measured before M4L (processor `tb/pp_top/README.md`) plus 6. No processor-side mutation was repeated.
- Hosted contexts at the exact head were read only. Several Verilator shards were still `in_progress`, "Physical gPTP" was `skipped` (a skip is not a pass), and the combined commit status was `pending`.
- Physical calibration was NOT RUN; field skips are not hardware proof.

## Pending manager duties

- Hosted and act acceptance at the exact head, including the Verilator shards that were still running.
- Candidate-merge validation against live `dev` and post-merge containment.
- Coordinating the F1 fix. The fix un-covers Docs and Conformance at the new head, and only those lenses need re-review if nothing else changes.
- Deciding whether S2 becomes a separate Issue.

## Prior public review findings

(I wrote this section after the verdict and ledger above.) At that point the only prior review on PR #569 was the internal round [R326] POSITIVE at this same head (PR comment 5845456786). It has no BLOCKER, MAJOR or MINOR findings and four SUGGESTIONs. Issue #567 carries no reviewer findings, and there are no PR reviews or line comments. No commit has landed since R326-1, so every item below is RETAINED at this head. None changes this round's ledger.

| prior item | status at 54b4c3bb | this round's assessment |
|---|---|---|
| R326 S1 (Docs, Conformance): `MILAN_COMPLIANCE_MATRIX.md:136-137` and `FR_NFR.md:194` lag the adopted processor | RETAINED, SUGGESTION | Confirmed. Row 137's "(no per-command PP arm yet)" was true at `990f9652` but is false at `0922e434`, where processor `tb/pp_top` M4 grades 0x0001-0x0005 and M4L grades the waived SETs under lock. My pp_top run passes 7646 default checks. This follows from the pin move, but it is under-reporting, the files are outside #567's frozen file list, and no behavior claim is wrong. I agree with the follow-up Issue route. |
| R326 S2 (Docs): `tb/verilator/milan_dp/README.md:552` permalinks at `990f9652` | RETAINED, SUGGESTION | Agreed: the F06.13 and F05.5 target sections are unchanged in the range. **I disagree with the R326 note in this item that `:468` is "correct as history".** Line 442 is a dated measurement, but line 468 is an instruction that names `990f9652` as the pin to restore. That is F1 in this report (MINOR, Docs and Conformance), and it keeps this round NEGATIVE. |
| R326 S3 (Docs): `SUBMODULES.md:57` "every pin", and `CHANGELOG.md:42` "the repository generator refreshes the submodule diagram and pin text" | RETAINED, SUGGESTION | Agreed. The first half is S1 in this report. The second half is also accurate: the generator's write mode wrote only `.svg`, `.drawio` and `.png` (`receipts/diagram_regen.txt`). The SUBMODULES.md pin table is hand-maintained and checked by `check_submodule_docs.py`. |
| R326 S4 (RTL, Robustness): AEM unit, domain and control counts are not forwarded to `protocol_processor_top` | RETAINED, SUGGESTION | Agreed. This is S2 in this report. It predates the lane, is not a consequence of the pin, and belongs in a separate Issue. |

The two reviews differ in one place: whether `tb/verilator/milan_dp/README.md:468` is history or a current instruction. This round treats it as an instruction and holds F1 open. The fix is a few words: "restore the pin", optionally keeping "measured at `990f9652`" as provenance.

R327-1 FINISHED
