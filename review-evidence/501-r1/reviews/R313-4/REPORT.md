[R313] POSITIVE - exact head efcabc379b1e0be1366bfc05bdcc05a759b55616

# R313-4: external independent delta review of issue #501 / PR #557

- Head: `efcabc379b1e0be1366bfc05bdcc05a759b55616`, tree `fc2e430a4a3635cfb2f62819ff5beb53a209b7c6`. The PR head on GitHub matches it (read-only query).
- Previous reviewed head: `afdd28b701e7f5849317e27ce845c31d1c87f2a6` (R313-3). Source base: `573f0052a0e4412e81f0845438fcec2086ce5d55`.
- Delta: one commit, `efcabc37` "docs: remove donor capture-hold measurement condition".
  - It deletes two lines, `docs/design/SAVED_STATE_MATERIALIZATION.md:1648-1649`, and adds none.
  - `git diff-tree -r afdd28b7 efcabc37` has exactly one entry: blob `8cb7e0551` becomes `421a72959`, mode 100644 in both.
  - No RTL, firmware, script, test, donor source or gitlink changed. All four gitlinks are identical at both heads (`receipts/delta_hygiene.log`).
- Role: external independent reviewer, cleared context, isolated detached clone. The review started publicly at PR #557 comment 5824494625.
- Authorities read:
  - AGENTS.md, which is unchanged.
  - The round-4 assignment and decision (issue #501 comment 5824399821). It says: "stage-3 release does not depend on the capture-hold measurement. The 8x8 hold margin is a liveness question owned by #559, independent of the donor writer's adoption."
  - The executor's REVIEW READY (5824473127).
  - My own R313-3 report and its unchanged scripts.
  - The delta, the full head for owner and trigger wording, and the hosted check list at this head.
- Verdict: **POSITIVE**.
  - R313-3-F1 is closed. No page assigns the capture-hold measurement or its resolution to processor #61/#83, and the stage-3 release condition now matches the decision.
  - Nothing else changed.
  - All five lenses are covered clean at this head.

## Findings

No new findings.

## R313-3-F1: CLOSED at this head

- **The line is gone.** `SAVED_STATE_MATERIALIZATION.md:1639-1647` now reads, in order:
  1. "Processor #61/#83 must adopt the capacity when implementing maps.", which concerns capacity only.
  2. "The #501 allocation decision permits stage-3 implementation."
  3. "Release still requires donor adoption, #502, and silicon persistence proof."

  The next bullet is the release-notes item. The measurement condition and its link to `SAVED_STATE_SNAPSHOT_OWNERSHIP.md#20-unresolved` are removed. The bullet list is still well formed.
- **It matches the decision.** Per 5824399821, stage-3 release does not depend on the measurement. The remaining release condition lists donor adoption of the capacity, #502 and silicon proof, and does not list the measurement.
- **My unchanged `scripts/residual_search.sh` finds no residual.** Its bytes are identical to R313-3's (`receipts/scripts_identity.txt`), and its output is in `receipts/residual_search.log`, rc 0.
  - Capture-hold and #559 references remain only at `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1607` and `:1710`, each "Issue #559 owns measurement and resolution of this firmware copy".
  - `SAVED_STATE_FASTCONNECT.md:457` matches the obligation wording, but it reads "The later output-capacity adoption is a separate donor obligation." That is capacity, not measurement. It is unchanged and kept by the assignment.
  - Withdrawn-premise wording: none.
  - Every remaining `#61/#83` line is a capacity-adoption line: `SAVED_STATE_MATERIALIZATION.md:1639`, `:1703`, `:2046` and `:2147`. The last three are R313-3's `:1705`, `:2048` and `:2149` shifted by the two deleted lines. The R313-3 match at `:1648`/`:1649` is the only line that disappeared.
- **A supplementary wider search (new, `scripts/residual_search_wide.sh`) is also clean** (`receipts/residual_search_wide.log`).
  - Nothing in `*.md` or `*.txt` joins processor, donor or #61/#83 to measure, capture-hold or hold margin in one sentence. The only matches are unrelated area-measurement history pages, the Milan traceability table and one code-quality path.
  - No page links into `SAVED_STATE_SNAPSHOT_OWNERSHIP.md#20` or `#18` any more.
  - The only "Release still requires" line is `SAVED_STATE_MATERIALIZATION.md:1647`, quoted above.
- **About `r3_text_check.py`.** The round-4 assignment asks for "both reviewers' `r3_text_check.py` and `residual_search.sh`". `r3_text_check.py` is not one of my scripts: none of my R313 packets contains it, and the R313-3 manifest lists only `residual_search.sh` among text probes. I re-ran my own script unchanged. I did not run the other reviewer's script, because I had not read it before my verdict. The author's archived run of it is in the public evidence tree (`review-evidence/501-r1/author-r4/receipts/r3-text-check.log`), and I did not use it as evidence.

## What was checked, per lens (this round)

### Conformance: CLEAN

- Round-4 assignment scope is met:
  - The sentence was deleted.
  - No page assigns the capture-hold measurement or its resolution to #61/#83 (both searches).
  - Every other donor-adoption line is untouched: the capacity lines at `:1639`, `:1703`, `:2046` and `:2147`, which were `:1705`, `:2048` and `:2149` before the deletion, and `SAVED_STATE_FASTCONNECT.md:457`.
- The decision "stage-3 release does not depend on the capture-hold measurement" is reflected at `SAVED_STATE_MATERIALIZATION.md:1646-1647`.
- The owner (#559) is stated at `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1607` and `:1710`. Neither line was touched.
- Everything else stands from R313-3 at `afdd28b7` and R313-2 at `dd6a68e9`, because the delta touches nothing else in scope. Two re-runs at this head confirm this:
  - `tree_figures.py` gives JSON identical to R313-3 after tree-path normalisation (`receipts/figures_vs_r313-3.log`).
  - `check_nvm_record_space.py` returns rc 0: 8x8 at 156 records, top id 0xE2, 12,680 B, commit at most 3.26 s (`receipts/gate_default.log`).

### RTL: CLEAN

- The delta contains no RTL, firmware or pin (`receipts/delta_hygiene.log`: one doc blob, all gitlinks identical).
- R313-3's RTL coverage at `afdd28b7`, an ancestor, carries to this head with nothing in scope touched since. It rests on `KL_nvm_backend.sv:1117-1137` and `milan_baremetal.c:1003-1017` against the doc, the capture probe, and R313-2's executed nvm_backend, mutant and nvm_cosim receipts.
- `hold_margin.py`, unchanged, gives output identical to R313-3 (`receipts/hold_margin.log`, `receipts/figures_vs_r313-3.log`). At 8x8 that is 31.9/63.8 ms and 1.57x/0.78x. It matches `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1584-1585` and `:1699-1701`.

### Robustness: CLEAN

- The deletion removes a gate and adds no behaviour.
- The liveness exposure is still stated where its owner is named: `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1606-1611` and `:1702`, `:1709-1714`, which cover void and retry safety, the sustained-activity liveness risk, 1x1 unaffected, and #559 owning it.
- Removing the release gate therefore leaves the risk documented and owned, not hidden. That matches the decision, which classes the margin as a liveness question.
- Over-capacity and restore robustness stands from R313-2 and R313-3, with scope untouched.

### Tests: CLEAN

- The delta touches no test, gate or script.
- Re-run at this head:
  - `check_nvm_record_space.py`: rc 0.
  - `--self-test`: rc 0 (`receipts/gate_selftest.log`).
- The executed test evidence of R313-2 and R313-3 applies with nothing in scope changed: the crash probe, the six-arm matrix, the source mutants, the firmware host test, the builder fixture and the RTL suites.

### Docs: CLEAN

- The delta was read in full, with its context at `SAVED_STATE_MATERIALIZATION.md:1620-1665`. Sections 18 and 20 of `SAVED_STATE_SNAPSHOT_OWNERSHIP.md` were re-read at `:1598-1616` and `:1695-1716`, along with `SAVED_STATE_FASTCONNECT.md:450-460`.
- Local gates at this head:
  - `docs_check.py` rc 0: 165 md files, scrub 23/23, routing 4/4.
  - `docs_check.py --selftest` rc 0.
  - `check_doc_style.py` rc 0.
  - `check_doc_paths.py` rc 0, 843 paths.
  - `git diff --check` rc 0 on the delta and on the full diff from the source base.
- Checked manually (`receipts/delta_hygiene.log`): the delta adds 0 lines and touches 0 headings, so the TOC cannot move. The full diff adds no U+2014.
- The deletion removed the only cross-page link into section 20. `check_doc_paths.py` still passes.
- Not run locally, as in rounds 1 to 3: `check_em_dash.py` and `gen_toc.py --check` exit 2, because the pinned Markdown renderer is absent and shared installs are not allowed (`receipts/em_dash.log`, `receipts/gen_toc_check.log`). The manual checks above replace them for a deletion-only delta.
- R313-3-S1 ("at this head" in a durable page, `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1606` and `:1709`) stays an optional SUGGESTION that was not taken. It does not affect coverage.

## Reviewer-owned completion ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | decision/assignment 5824399821; `SAVED_STATE_MATERIALIZATION.md:1620-1665`; `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1598-1616,1695-1716`; `SAVED_STATE_FASTCONNECT.md:450-460`; `residual_search.log`; `residual_search_wide.log`; `figures_vs_r313-3.log`; `gate_default.log` | R313-4 | `efcabc379b1e0be1366bfc05bdcc05a759b55616` |
| RTL | CLEAN | `delta_hygiene.log` (one doc blob, gitlinks identical); `hold_margin.log`; R313-3 RTL/firmware line checks and capture probe, and R313-2 nvm_backend/mutant/nvm_cosim receipts, whose scope is untouched since | R313-4 (executed RTL suites: R313-2; capture probe: R313-3) | `efcabc379b1e0be1366bfc05bdcc05a759b55616` (suites at ancestor `dd6a68e9063c3f7aa81536197254d187e9cb65ba`, probe at ancestor `afdd28b701e7f5849317e27ce845c31d1c87f2a6`, scope untouched since) |
| Robustness | CLEAN | `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1593-1611,1697-1714`; `SAVED_STATE_MATERIALIZATION.md:1639-1647`; `hold_margin.log`; R313-2 over-capacity mutants (scope untouched) | R313-4 | `efcabc379b1e0be1366bfc05bdcc05a759b55616` |
| Tests | CLEAN | `gate_default.log`, `gate_selftest.log` at head; R313-2 crash probe, matrix, source mutants, firmware host test, builder fixture (scope untouched) | R313-4 (re-run gate); R313-2 (rest) | `efcabc379b1e0be1366bfc05bdcc05a759b55616`; ancestor `dd6a68e9063c3f7aa81536197254d187e9cb65ba`, scope untouched |
| Docs | CLEAN | the delta; the context sections above; doc gates (`docs_check*.log`, `doc_style.log`, `doc_paths.log`, `diff_check_*.log`); `delta_hygiene.log`; `residual_search*.log` | R313-4 | `efcabc379b1e0be1366bfc05bdcc05a759b55616` |

Every lens was applied at this head, and all five are covered clean. No finding is open under any lens.

## Prior public review findings on this PR

This section was written after the verdict and ledger above. It covers every public review of this PR up to the review start: R312-1, R313-1, R312-2, R313-2, R312-3 and R313-3. I read R312-3 (5824394329) for the first time after my verdict. R312-4 had not been published when this section was written, and I did not read it.

- **R313-3-F1** (mine; MINOR; Conformance, Docs): **CLOSED**, with the evidence above.
- **R312-3 F1** (MINOR; Conformance, Docs): **CLOSED.** It names the same line, `SAVED_STATE_MATERIALIZATION.md:1648-1649`.
  - Its required outcome is met. No tracked page makes the donor responsible for the measurement, and the stage-3 release text drops the sentence.
  - The manager amended the scope (5824399821), which is its third bullet.
  - Its grep verification returns no match for `capture-hold measurement obligation` (`receipts/r312_3_f1_grep.log`, rc 1). The only "measurement obligation" hit is an unrelated area-budget row in `docs/ENDSTATION_BUILDER.md:992`.
  - I did not run its `r3_text_check.py` RESIDUE check (see the F1 section). My own searches cover the same line.
- **R312-2 F1 / R313-2-F1**: closed in section 18 and UNRESOLVED 6 at `afdd28b7`, as both round-3 reports record. The residual carried into R312-3 F1 and R313-3-F1 is now closed too. Those sections are unchanged in this delta.
- **R312-2 S1 / R312-3 retained S1** (SUGGESTION; Docs; the historical row now at `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1841`): not taken, and it stays optional.
- **R313-3-S1** (SUGGESTION): not taken, and it stays optional.
- **R312-1 and R313-1 findings**: closed or taken at `dd6a68e9`, as the round-2 and round-3 reports record. Neither round-3 nor round-4 delta touches them.
- **Carried from R312-3's pending duties, as a note and not a finding:** R312-3 asks for explicit maintainer acceptance that the modelled 8x8 hold exposure (0.78x under doubled costs) merges with #559 open.
  - The round-4 decision (5824399821) classes it as a liveness question owned by #559. It also makes stage-3 release independent of the measurement.
  - It is a manager decision, not a stated maintainer merge acceptance, so I list it under pending manager duties. It does not change my verdict: the page states the exposure truthfully and names its owner.

None of the above changes the verdict word or the ledger.

## Real limits

- No hardware ran. Physical calibration was NOT RUN, and the hosted "Physical gPTP (nightly and manual)" context was skipped. Neither is hardware proof.
- The copy times are the page's cost model, not a measurement. Issue #559 owns the measurement.
- This is a delta review of a two-line deletion. For all scope the delta does not touch, the evidence is from earlier rounds and was not re-run here:
  - R313-3 at `afdd28b7`: the capture probe and the RTL and firmware line checks.
  - R313-2 at `dd6a68e9`: the executed RTL suites, mutants, cosim, D3 replay, firmware host test and builder fixture.

  Nothing in their scope changed (`receipts/delta_hygiene.log`). No Verilator build ran, so the pinned Verilator's identity was not checked.
- Not run, by instruction: the full parent, PP, gPTP, Yosys and builder banks, Docker, act, and host `act_ci` and its selftest.
- Not run by me:
  - The other reviewer's `r3_text_check.py`, which is not my script.
  - `check_em_dash.py` and `gen_toc.py --check`, because the renderer is absent on the host and shared installs are not allowed. For a deletion-only delta the manual checks replace them.
- The manager's source static, builder and native banks at this head: I found no public comment on #501 or #557 that names this head for those banks. I have not verified them, and I did not rely on them.
- Hosted contexts at this head were listed read-only at 2026-09-25T00:22:00Z (`receipts/hosted_checks.txt`):
  - 10 completed success;
  - 1 skipped (Physical gPTP);
  - 8 in progress: docs-check, elaborate, Verilator shards 0-4 and yosys-elaboration.

  The manager owns hosted and act acceptance.
- `hold_margin.py` takes base figures as input. I reused my R313-2 `figures_base.json` for base `573f0052`, which is unchanged, copied here as `receipts/figures_base_from_r313-2.json`. The head figures were regenerated at this head.
- Clone restoration and where things ran:
  - All commands ran from the review clone with bytecode writing disabled. No probe edited the clone.
  - `receipts/verify_clone.log` reports `CLONE EXACT`. HEAD and tree are exact, the index matches, and all 883 tracked files have exact bytes and modes.
  - The three initialised gitlinks are at their pins and clean, and `external` is uninitialised, as at start. Nothing untracked or ignored remains.
  - The scratch directory holds only two normalised JSON copies used for the figures comparison. It is not published.
- The six reused scripts are byte-identical to my R313-3 copies (`receipts/scripts_identity.txt`). `residual_search_wide.sh` is new this round.

## Pending manager duties

- Publish this report and the manifest.
- Obtain explicit maintainer acceptance that the modelled 8x8 hold exposure merges with #559 open, if the manager's round-4 decision is not taken as that acceptance (carried from R312-3).
- Candidate-merge validation against live `dev` `ffcbd33de70278ae34b533dcbadde0b36c8cba13` (source base `573f0052a0e4412e81f0845438fcec2086ce5d55`).
- Hosted and act acceptance at the exact head, including the 8 contexts still in progress at listing time.
- The second independent positive review (R312-4).
- Merge authorization and post-merge containment.
- Optional: R313-3-S1 and R312-2 S1.

R313-4 FINISHED
