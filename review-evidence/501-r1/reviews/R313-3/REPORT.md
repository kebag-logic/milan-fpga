[R313] NEGATIVE - exact head afdd28b701e7f5849317e27ce845c31d1c87f2a6

# R313-3: external independent delta review of issue #501 / PR #557

- Head: `afdd28b701e7f5849317e27ce845c31d1c87f2a6`, tree `505f3cb63cae98c463c00dc0ac1437241ac1ff0f`.
- Previous reviewed head: `dd6a68e9063c3f7aa81536197254d187e9cb65ba` (R313-2). Source base: `573f0052a0e4412e81f0845438fcec2086ce5d55`.
- Delta: one commit, `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md` only, +25/-15. It changes section 18 (Timing) and UNRESOLVED 6. No RTL, firmware, script, test, donor source or pin changed.
- Role: external independent reviewer, cleared context, isolated detached clone. The review started publicly at PR #557 comment 5824323797.
- Authorities read:
  - AGENTS.md and CONTRIBUTING.md, as in rounds 1 and 2.
  - The corrected capture-hold decision (issue #501 comment 5824117439).
  - The round-3 assignment (5824209814).
  - Issue #559 (body, open).
  - The donor withdrawal (processor #61 comment 5824117647) and the withdrawn obligation (5823590638).
  - The executor's REVIEW READY (5824296477) and the PR body at this head.
  - The delta, a search of the full head for owner and trigger wording, and the RTL and firmware lines the new text cites.
- Verdict: **NEGATIVE**.
  - Section 18 and UNRESOLVED 6 now state what the implementation does, and they match my unchanged probes exactly. For those two sections, R313-2-F1 is closed.
  - One MINOR is open under Conformance and Docs. It is a residual of the same defect, in the sibling page. A line this PR added in round 2 still makes the donor responsible for the capture-hold measurement, as a stage-3 release condition. That obligation has been withdrawn publicly, and UNRESOLVED 6, which the line links to, now gives the owner as #559.
  - RTL, Robustness and Tests are covered clean at this head.

## Findings

### R313-3-F1: MINOR. Lenses: Conformance, Docs

- **Where:** `docs/design/SAVED_STATE_MATERIALIZATION.md:1648-1649`, in the stage-release conditions ("Work that may proceed while those are open"):
  > Processor #61/#83 must also satisfy the
  > [capture-hold measurement obligation](SAVED_STATE_SNAPSHOT_OWNERSHIP.md#20-unresolved).

  `git blame` shows it was added by this PR's round-2 commit `dd6a68e9`, on the premise that has since been corrected.
- **Title:** a donor-adoption trigger for the capture-hold measurement survives in the sibling page and contradicts the corrected owner.
- **Authority and evidence:**
  - **The corrected decision** (issue #501 comment 5824117439): "The copy belongs to this repository, not to the donor writer". The Owner is "new parent issue #559". The pages "must point to #559, not to the donor". Also: "The donor obligation I posted on processor #61 is withdrawn there."
  - **The withdrawal** (processor #61 comment 5824117647): "Withdrawn ... The parent owns it: kebag-logic/milan-fpga#559."
  - **Round-3 assignment item 2** (5824209814): "The owner of the measurement and the resolution is #559, not the donor writer. Remove the donor-adoption trigger wording".
  - **The head's own target** of the link, `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1710`: "Issue #559 owns measurement and resolution of this firmware copy." So the line points to a section that names a different owner from the one the line names.
  - **My R313-2-F1 required outcome:** "The measurement obligation, and its trigger, cover the exposure that exists now." A release condition that makes the donor satisfy it does not. My round-2 pass read this line at `dd6a68e9` without flagging it separately. At that head it matched the decision then in force, which F1 disputed.
  - A search of `docs/`, `README.md` and `REQUIREMENTS.md` for capture-hold, #559 and donor-obligation wording finds this line as the only residual (`receipts/residual_search.log`, from `scripts/residual_search.sh`).
  - Other donor-adoption lines are about the output-map capacity itself, and they remain correct under the decision: `SAVED_STATE_MATERIALIZATION.md:1639`, `:1705`, `:2048`, `:2149` and `SAVED_STATE_FASTCONNECT.md:457`.
- **Impact:**
  - An authoritative release condition assigns a withdrawn obligation to a party that no longer carries it, and it conflicts with the page it cites.
  - A reader gating stage-3 release would take the obligation to be met, or pending, on processor #61/#83, the wrong lane.
  - The processor issue no longer tracks it. From that page, the parent obligation (#559) is invisible.
  - Nothing reaches flash unattested and no behaviour changes, which is why this is MINOR.
  - The assignment's item 3, "Change nothing else", explains why the executor left the line. It does not make the line true. AGENTS section 2 requires the conflict to be published, not resolved privately.
- **Required outcome:**
  - The sibling page names no donor obligation for the capture-hold measurement.
  - If stage-3 release is to depend on the measurement, the condition names #559, the parent owner, or UNRESOLVED 6 as it now reads.
  - Whether release depends on it at all is the decision owner's call.
  - Because the assignment scoped the edit to two sections, the decision owner authorizes the one-line change, or states why it stays.
- **Verification:**
  - A reviewer re-runs `scripts/residual_search.sh` at the corrected head. No sentence may assign the capture-hold measurement or its resolution to processor #61/#83.
  - `docs_check.py`, `check_doc_paths.py` and `git diff --check` return rc 0.

### R313-3-S1: SUGGESTION. Lens: Docs

- **Where:** `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1606` ("exists at this head") and `:1709` ("applies at this head").
- **What:** after merge, "this head" has no referent in a durable page. "At the current source", or "since #501", would read the same after merge.
- This is optional and does not affect coverage.

## R313-2-F1: status at this head

**CLOSED for section 18 and UNRESOLVED 6. The residual is carried forward as R313-3-F1.**

Each point was checked against the head text:

- **Every CLOSED record is copied, whatever is materialized:**
  - The page says so at `:1600-1601` and `:1704-1705`.
  - The firmware does exactly that: `milan_baremetal.c:1003-1017`, where the copy predicate is only the open bit (`copy = !((own[...] >> ...) & 1u)`).
- **An accepted RELOAD closes every allocated record:**
  - The page says so at `:1602` and `:1706`.
  - The RTL matches: `hdl/milan/KL_nvm_backend.sv:1121-1129`. With `reload_ok_w`, `open_n_w` drops to 0 for each allocated record unless a same-cycle grant hits it.
- **Counted bytes:** the page gives 12,634 bytes over 156 records, 4,672 of them output maps (`:1603-1605`, `:1699`, `:1707-1708`). My unchanged `capture_copy_probe.py` at this head gives `copied_bytes=12634 records=156 maps_out_bytes=4672 area_raw=12634` for 8x8 (`receipts/capture_copy_probe.log`).
- **Model margins:** the page gives 31.9/63.8 ms and 1.57x/0.78x, with the table at `:1578-1585`. My unchanged `hold_margin.py` gives exactly these (`receipts/hold_margin.log`).
- **Safety and 1x1:**
  - Safety holds through void and retry (`:1594`, `:1702`). The liveness risk under sustained activity is stated (`:1595`, `:1702`).
  - 1x1 is unchanged at 3,218 B over 53 records, 8.3/16.5 ms, 6.06x/3.03x (`:1596`, `:1703`). The probe gives `copied_bytes=3218 records=53` for 1x1.
- **Owner cited:** #559 at `:1607` and `:1710`. The issue is open, and its acceptance (measure, then size, cheapen or prove, and record in section 18 / UNRESOLVED 6) matches the page's `:1608-1611` and `:1711-1714`.
- **No donor trigger in either section:**
  - The processor #61 link and the "Donor writer adoption ... must measure" wording are removed from both.
  - The decision link now points to the corrected decision, 5824117439.
  - The only residual is in the sibling page (R313-3-F1).
- **Hold parameter:** unchanged at 50 ms. Nothing in `hdl/` changed in the delta, and the page's claims about the hold staying below the heartbeat and commit deadline (`:1613-1616`) are untouched.

## What was checked, per lens (this round)

### Conformance: UNCLEAN (R313-3-F1)

- Round-3 assignment item 1 is met in the two named sections, as shown above.
- Item 3 is met: the delta is the one file, and my probes match the page.
- Item 2, to remove the donor-adoption trigger wording, is met in the named sections. It is not met across the PR: `SAVED_STATE_MATERIALIZATION.md:1648-1649` still makes the donor responsible, which contradicts the corrected decision.
- Everything else under this lens stands from R313-2 at `dd6a68e9`, an ancestor of this head. The delta touches nothing in that scope. That covers the figures comparison, the D3 replay and scope items 1-6.
- Two checks were re-run here:
  - `receipts/figures_head_vs_r313-2.log`: my unchanged `tree_figures.py` at this head gives JSON identical to round 2's once the tree path is normalised.
  - `receipts/gate_default.log`: rc 0, 8x8 at 156 records, top id 0xE2, 12,680 B, commit at most 3.26 s.

### RTL: CLEAN

- The delta changes no RTL, firmware or pin: `git diff --stat dd6a68e9..afdd28b7` shows the one doc file.
- The doc's RTL and firmware claims were checked against `KL_nvm_backend.sv:1117-1137` (open-vector priority and accepted-RELOAD closure) and `milan_baremetal.c:1003-1017` (the copy predicate and span). They are now accurate. This is what R313-2-F1 attributed to this lens.
- The executed RTL evidence from R313-2 at `dd6a68e9` carries to this head, because nothing in its scope changed:
  - nvm_backend 525/525 and 208/208;
  - the RTL mutants killed;
  - nvm_cosim 8x8 150/150.
- The capture probe was re-run at this head on a disposable clone with every initialised submodule at its pin (`receipts/capture_copy_probe.log`, rc 0).

### Robustness: CLEAN

- The hold-lapse path and its consequences are stated as the implementation behaves:
  - void and retry keep safety (`:1594`, `:1702`);
  - the 8x8 liveness risk is present from this head (`:1595`, `:1606`, `:1709`);
  - 1x1 is unaffected.
- R313-2-F1's liveness-scope point is resolved.
- The over-capacity mutants and static-port results stand from R313-2 at `dd6a68e9`. Nothing in scope changed.

### Tests: CLEAN

- The delta touches no test, gate or script.
- Re-run at this head:
  - `check_nvm_record_space.py`: rc 0 (`receipts/gate_default.log`).
  - `--self-test`: rc 0, with all 18 named-finding controls OK (`receipts/gate_selftest.log`).
- Everything else stands from R313-2 at `dd6a68e9`, with nothing in scope changed: the crash probe, the six-arm matrix, the source mutants, the firmware host test and the builder fixture test.

### Docs: UNCLEAN (R313-3-F1)

- The delta was read in full, as were section 18 (`:1505-1616`) and section 20 (`:1673-1780`) at the head.
- Owner and trigger wording was searched across `docs/`, `README.md` and `REQUIREMENTS.md` (`receipts/residual_search.log`).
- The cited probe link (`blob/247a9151.../review-evidence/501-r1/reviews/R312-2/scripts/capture_copy_probe.py`) resolves: blob `8af2f24e...`, 3,246 B (`receipts/cited_link_exists.log`). I did not read its contents. The page's figures are independently confirmed by my own probe.
- Local gates:
  - `docs_check.py` rc 0: 165 md files, scrub 23/23, routing 4/4.
  - `docs_check.py --selftest` rc 0.
  - `check_doc_style.py` rc 0.
  - `check_doc_paths.py` rc 0, 843 paths.
  - `git diff --check`, on the delta and the full diff: rc 0.
- Checked manually (`receipts/delta_hygiene.log`): the delta and the full diff add no U+2014, and the delta changes no heading, so the TOC cannot move.
- Not run locally, as in rounds 1 and 2: `check_em_dash.py` and `gen_toc.py --check` exit 2, because the pinned Markdown renderer is absent and shared installs are not allowed (`receipts/em_dash.log`, `receipts/gen_toc_check.log`).
- The PR body is current in its Round 3 section.
  - Its "Status" says the corrections are "committed locally". The PR head is `afdd28b7`, so they are pushed. That is stale wording, not a finding.
  - Its Description line "The saved-state documents record the allocation and donor adoption requirement" is about capacity adoption, which is correct.

## Reviewer-owned completion ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R313-3-F1 MINOR) | decision 5824117439; assignment 5824209814 items 1-3; #559; processor #61 withdrawal 5824117647; `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1578-1616,1697-1717`; `SAVED_STATE_MATERIALIZATION.md:1639-1649`; `figures_head_vs_r313-2.log`; `gate_default.log` | R313-3 | `afdd28b701e7f5849317e27ce845c31d1c87f2a6` |
| RTL | CLEAN | `KL_nvm_backend.sv:1117-1137`; `milan_baremetal.c:1003-1017`; `capture_copy_probe.log` at head; the delta is doc-only, and R313-2's nvm_backend, mutant and nvm_cosim receipts apply with nothing in scope changed | R313-3 (executed RTL suites: R313-2) | `afdd28b701e7f5849317e27ce845c31d1c87f2a6` (suites at ancestor `dd6a68e9063c3f7aa81536197254d187e9cb65ba`, scope untouched since) |
| Robustness | CLEAN | `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1593-1611,1697-1714`; `hold_margin.log`; `capture_copy_probe.log`; R313-2 over-capacity mutants (scope untouched) | R313-3 | `afdd28b701e7f5849317e27ce845c31d1c87f2a6` |
| Tests | CLEAN | `gate_default.log`, `gate_selftest.log` (18/18) at head; R313-2 crash probe, matrix, source mutants, fw host test and builder fixture (scope untouched) | R313-3 (re-run gate); R313-2 (rest) | `afdd28b701e7f5849317e27ce845c31d1c87f2a6`; `dd6a68e9063c3f7aa81536197254d187e9cb65ba` ancestor, scope untouched |
| Docs | UNCLEAN (R313-3-F1 MINOR) | the delta; sections 18 and 20 in full; `residual_search.log`; `cited_link_exists.log`; doc gates; `delta_hygiene.log`; PR body at head | R313-3 | `afdd28b701e7f5849317e27ce845c31d1c87f2a6` |

Every lens was applied at this head. RTL, Robustness and Tests are banked clean. Conformance and Docs are not.

## Prior public review findings on this PR

This section was written after the verdict and ledger above. It covers every public review of this PR up to the review start. R312-3 had not been published when this section was written, and I did not read it.

- **R312-2** (PR #557 comment 5824109822; internal; I first read it after my R313-2 verdict):
  - **F1 (MAJOR; Conformance, RTL, Robustness, Docs): CLOSED for section 18 and UNRESOLVED 6. RETAINED for Conformance and Docs as R313-3-F1.**
    - The first bullet of its required outcome is met at this head. The same holds for the re-recorded disposition (5824117439, owner #559) and the corrected donor comment (5824117647).
    - Its third bullet, "The measurement obligation's trigger and owner match the copy that exists today", is not met across the PR. Its own item-3 text notes that the obligation "is linked from UNRESOLVED 6 and from MATERIALIZATION `:1647-1649`". That MATERIALIZATION link still names processor #61/#83 (R313-3-F1).
    - Its RTL and Robustness parts are resolved: the page now states the firmware copy and the RTL closure truthfully, and no HDL or firmware changed.
    - The severity differs as before: MAJOR there, MINOR here. The residual is ownership routing only, so I keep MINOR. The decision owner may settle it.
  - **S1 (SUGGESTION; Docs): not taken, and it stays optional.** The historical row, now at `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1841` after the delta shifted it, still reads "1.1 to 2.3". The round-3 assignment limited the change set.
- **R313-2** (5824206585, mine): F1 is CLOSED for the two sections, and its residual is RETAINED as R313-3-F1 (Conformance, Docs). Its RTL and Robustness attributions are cleared, as the ledger shows.
- **R312-1** (5823344017) and **R313-1** (5823585783): every finding and suggestion was resolved at R313-2 on `dd6a68e9`, and the one-file delta does not touch those passages.
  - The R312-1 F2 exposure part is the R312-2 F1 / R313-2 F1 chain above.
  - R312-1 S3 stays optional and not taken.

None of the above changes the verdict word or the ledger.

## Real limits

- No hardware ran. Physical calibration was NOT RUN, and the hosted "Physical gPTP" context was skipped. Neither is hardware proof.
- The copy times on the page and here are the page's model, not a measurement. Issue #559 owns the measurement.
- The host bench has no producer. With one, records open during a write are skipped, so the real copy can only be shorter than the full area.
- This is a delta review. For the scope the delta does not touch, the executed RTL suites, mutants, cosim, D3 replay, firmware host test and builder fixture are R313-2 receipts at the ancestor `dd6a68e9`. They were not re-run.
- Not run, by instruction: the full parent, PP, gPTP, Yosys and builder banks, act, and host `act_ci` and its selftest.
- `check_em_dash.py` and `gen_toc.py --check` could not run locally (renderer absent). They were replaced by the manual checks above.
- `hold_margin.py` takes the base figures as input. I reused my R313-2 `figures_base.json` for base `573f0052`, which is unchanged, and it is copied here as `receipts/figures_base_from_r313-2.json`. The head figures were regenerated at this head.
- Hosted contexts at this head were listed read-only at 2026-09-25T00:06:02Z (`receipts/hosted_checks.txt`): 10 success, 1 skipped (Physical gPTP), and 8 still in progress at listing time (docs-check, elaborate, Verilator shards 0-4, yosys-elaboration). The manager owns hosted and act acceptance.
- Where the receipts ran:
  - Gates, figures and doc checks ran from the review clone with bytecode writing disabled.
  - The capture probe ran on a disposable clone at the head under `scratch/`. Its submodules were initialised from the review clone's own module stores at the recorded pins, with no network fetch.
- Clone restoration: `receipts/verify_clone.log` shows the following, and nothing was fetched into or written to the review clone.
  - HEAD and tree are exact, and the index matches.
  - All 883 tracked files have exact bytes and modes.
  - The three initialised gitlinks are at their pins and clean, and `external` is uninitialised, as at start.
  - Nothing untracked or ignored remains.
- The five reused scripts are byte-identical to my R313-2 copies (`receipts/scripts_identity.txt`).

## Pending manager duties

- Publish this report and the manifest.
- Route R313-3-F1 to the decision owner, who confirms or authorizes the one-line change outside the assignment's two sections. Then route it to the executor, and re-review the corrected head.
- Candidate-merge validation against live `dev` `ffcbd33de70278ae34b533dcbadde0b36c8cba13` (source base `573f0052a0e4412e81f0845438fcec2086ce5d55`).
- Hosted and act acceptance at the final head, including the 8 contexts still in progress at listing time.
- Merge authorization and post-merge containment.

R313-3 FINISHED
