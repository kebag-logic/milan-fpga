[R312] POSITIVE - exact head efcabc379b1e0be1366bfc05bdcc05a759b55616

# R312-4: internal independent delta review of issue #501 / PR #557

- Reviewer: [R312], the internal reviewer, working from a cleared context.
- Round: R312-4, a delta review of round 4 by executor [A292].
- Head: `efcabc379b1e0be1366bfc05bdcc05a759b55616`, tree `fc2e430a4a3635cfb2f62819ff5beb53a209b7c6`. It equals the PR head (PR open, not draft, base `dev`).
- Previous head: `afdd28b701e7f5849317e27ce845c31d1c87f2a6` (R312-3).
- Source base: `573f0052a0e4412e81f0845438fcec2086ce5d55`.
- Assignment: issue #501 comment 5824399821. Executor evidence: issue #501 comment 5824473127.

## Reconstruction

I read, in this order:

1. AGENTS.md and CONTRIBUTING.md (unchanged since round 3).
2. The round-4 assignment and decision (5824399821). Decision: stage-3 release does not depend on the capture-hold measurement; the 8x8 hold margin is a liveness question owned by #559. Scope: delete the sentence at `SAVED_STATE_MATERIALIZATION.md:1648-1649`; no page may assign the capture-hold measurement or its resolution to processor #61/#83; leave the capacity-adoption lines alone (`:1639, :1705, :2048, :2149`, `FASTCONNECT:457`, numbered at the round-3 head).
3. The executor's REVIEW READY (5824473127) and the PR body at review time (`receipts/pr557_body_at_review.md`).
4. `git diff afdd28b7..efcabc37` and the commit record (`receipts/delta_audit.log`).

The delta changes no RTL, firmware, script, test or gitlink. My round-3 ledger stands for everything the delta did not touch, and each lens was re-applied below to the one changed artifact.

## Delta audit

`receipts/delta_audit.log`:

- One commit, `efcabc37`, parent `afdd28b7`. Subject "docs: remove donor capture-hold measurement condition": one line, no body, no trailers.
- One blob changed: `docs/design/SAVED_STATE_MATERIALIZATION.md`, `8cb7e0551…` to `421a72959…`, mode 100644 unchanged.
- The patch is `-2 +0`. It removes exactly:
  > Processor #61/#83 must also satisfy the
  > [capture-hold measurement obligation](SAVED_STATE_SNAPSHOT_OWNERSHIP.md#20-unresolved).
- It adds no line. The bullet that remains ends "Release still requires donor adoption, #502, and silicon persistence proof." and reads correctly.
- The four gitlinks are identical at both heads.

## Findings

No open BLOCKER, MAJOR or MINOR.

### R312-3 F1: CLOSED at `efcabc37`

- **Was:** MINOR (Conformance, Docs). `SAVED_STATE_MATERIALIZATION.md:1648-1649` made processor #61/#83 responsible for the capture-hold measurement. The corrected decision had withdrawn that obligation.
- **Now:** the sentence is gone (`receipts/delta_audit.log`).
- **My unchanged `r3_text_check.py`** (sha256 `94393f71…3101`, byte-identical to round 3) was re-run at head (`receipts/r3_text_check.log`):
  - 23 required checks and 14 forbidden-text checks: all PASS, rc 0.
  - The `SAVED_STATE_MATERIALIZATION.md:1649` RESIDUE line is gone. Diffed against the round-3 receipt, that line and the head stamp are the only differences.
  - The only RESIDUE left is `SAVED_STATE_FASTCONNECT.md:457`: "The later output-capacity adoption is a separate donor obligation." That line is about map capacity, not the hold. The assignment keeps it on purpose.
- **Its inputs, re-run at this head:** my unchanged `capture_copy_probe.py` and `hold_margin.py` match round 3 exactly (`receipts/capture_copy_probe.log`, `receipts/hold_margin.log`). Only the head stamp differs.
- **Repository-wide residual search:** `scripts/residual_search.sh` → `receipts/residual_search.log`, rc 0.
  - My earlier packets held no script of this name, so I wrote this one this round. It searches all tracked files, not only `docs/`.
  - Section 1 lists every capture-hold mention. None names an owner except SNAPSHOT_OWNERSHIP `:1607` and `:1710`, which name #559.
  - Section 2 finds no line that pairs processor #61/#83 or the donor with the capture hold or #559 and an ownership word.
  - Section 3 finds no link to the withdrawn obligation and none of the removed wording.
  - Only SNAPSHOT_OWNERSHIP `:1607` and `:1710` cite #559. Both read "Issue #559 owns measurement and resolution of this firmware copy."
- **Fault sensitivity:** run on the round-3 head `afdd28b7` from a scratch clone:
  - `residual_search.sh` reports the F1 lines and exits 1 (`receipts/residual_search_sensitivity_r3head.log`).
  - `r3_text_check.py` prints the MATERIALIZATION RESIDUE line (`receipts/r3_text_check_sensitivity_r3head.log`).
  - Both detect the defect, so a clean result at head is meaningful.
- **Kept lines:** each capacity-adoption line the assignment keeps is still there and is about capacity only (`receipts/donor_lines.log`). After the two-line shift they are MATERIALIZATION `:1639, :1703, :2046, :2147` and FASTCONNECT `:457`. None mentions the hold or #559.
- **Stage 3:** the release list (`:1631-1647`) and the stage-3 row (`:1659`) no longer carry any capture-hold condition. This matches the decision.

### R312-4 S1: SUGGESTION. Lens: Docs

- **Where:** PR #557 body, "Status" (`receipts/pr557_body_at_review.md`, line 6).
- **What:** it says "Round 4 correction is committed locally on `501-outmap-record`". The commit is now the published PR head.
- **Status:** optional. Refresh the status wording when the body is next edited for the evidence checklist.

### R312-2 S1: retained, SUGGESTION. Lens: Docs

- The historical row in `SAVED_STATE_SNAPSHOT_OWNERSHIP.md` ("about 22 ms and 44 ms at 8x8…") is untouched and remains optional.

## Per-lens results

```text
[R312] PASS Conformance — issue 501 comment 5824399821; docs/design/SAVED_STATE_MATERIALIZATION.md:1631-1659 at efcabc37; receipts/delta_audit.log, receipts/residual_search.log, receipts/donor_lines.log — the round-4 scope is met exactly: the sentence at the round-3 :1648-1649 is deleted and nothing else changes; no tracked page assigns the capture-hold measurement or its resolution to processor #61/#83 or the donor; the capacity-adoption lines are unchanged; stage-3 release carries no capture-hold condition, per the decision
[R312] PASS RTL — receipts/delta_audit.log (one .md blob; no hdl/, sw/, tb/ or gitlink change); receipts/residual_search.log section 1 (KL_nvm_backend.sv:145 T_HOLD_MS_P=50, :297-299 refusal, unchanged) — no RTL or firmware in the delta; the R312-3 RTL result at afdd28b7 covers the unchanged source, which this delta does not touch
[R312] PASS Robustness — SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1607,1710 (unchanged); SAVED_STATE_MATERIALIZATION.md:1631-1647 — removing the donor condition moves no failure path; the 8x8 lapse (void, release and retry, safe) and its liveness exposure keep their one recorded owner, #559; 1x1 margins unchanged (receipts/capture_copy_probe.log, receipts/hold_margin.log)
[R312] PASS Tests — scripts/r3_text_check.py (unchanged), scripts/capture_copy_probe.py, scripts/hold_margin.py (unchanged), scripts/residual_search.sh with receipts; receipts/gate_check_nvm_record_space*.log — the text check passes 37/37 at head; both residual tools detect the F1 defect at afdd28b7 and are clean at head; both probes reproduce round 3; the record-space gate and --self-test are rc 0; the delta adds or changes no test
[R312] PASS Docs — SAVED_STATE_MATERIALIZATION.md at efcabc37; receipts/gate_*.log — docs_check, check_doc_style, check_doc_paths, gen_module_matrix --check, git diff --check (base..head and delta), and, under the pinned renderer in a disposable environment, gen_toc --check and check_em_dash --base 573f0052a all rc 0; F1 closed; R312-4 S1 and R312-2 S1 are optional
```

## Reviewer-owned lens ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | round-4 decision and scope (5824399821); MATERIALIZATION stage-3 text `:1631-1659`; repository-wide residual search; kept capacity lines; earlier acceptance as in R312-1..3 | R312-4 | efcabc379b1e0be1366bfc05bdcc05a759b55616 |
| RTL | CLEAN | delta audit (no HDL, firmware or gitlink change); hold parameter and refusal unchanged. R312-3/R312-2 RTL results cover the untouched source. | R312-4 (delta); R312-3 for the untouched source | efcabc379b1e0be1366bfc05bdcc05a759b55616; afdd28b701e7f5849317e27ce845c31d1c87f2a6 (parent; no RTL-scope artifact touched since) |
| Robustness | CLEAN | lapse and void path and 8x8 liveness ownership (#559) at SNAPSHOT_OWNERSHIP `:1607,1710`; probe re-runs | R312-4 | efcabc379b1e0be1366bfc05bdcc05a759b55616 |
| Tests | CLEAN (suggestions only) | text check, residual search with fault sensitivity, both probes, record-space gate and `--self-test`. R312-2 covers the untouched test artifacts. | R312-4 (delta); R312-2 for untouched test artifacts | efcabc379b1e0be1366bfc05bdcc05a759b55616; dd6a68e9063c3f7aa81536197254d187e9cb65ba (ancestor; no test artifact touched since) |
| Docs | CLEAN (suggestions only) | MATERIALIZATION at head; docs gates; PR body | R312-4 | efcabc379b1e0be1366bfc05bdcc05a759b55616 |

## Prior public findings at this head

I wrote the verdict, findings and ledger above before reading any other reviewer's round-3 report. My own earlier findings come from my own reports.

| Finding | Status at `efcabc37` |
|---|---|
| R312-3 F1 MINOR (Conformance, Docs) | **Closed.** See above. |
| R312-2 F1 MAJOR | Closed at `afdd28b7` in both sections; its residual was R312-3 F1, now closed. |
| R312-2 S1 SUGGESTION | Not taken; stays optional. |
| R312-1 F1, F2 figures, F3 | Closed at `dd6a68e9`; untouched. |
| R312-1 S1, S2, S3 | As recorded at R312-2 and R312-3; untouched and optional. |
| R313-2-F1, R313-1 F1-F4, S1, S2 | Closed or taken as recorded at R312-3; untouched by the delta. |
| R313-3 F1 | See the addendum below. |

### Addendum: the other reviewer's round-3 findings

I read PR #557 comment 5824395155 (R313-3) only after the verdict, findings and ledger above were written.

- **R313-3-F1, MINOR (Conformance, Docs).** This is the same line as my R312-3 F1 (`SAVED_STATE_MATERIALIZATION.md:1648-1649`).
  - **Closed at `efcabc37`.** The line is deleted, and the decision owner authorized the change (5824399821). That is the authorization the finding asked for.
  - The decision says stage-3 release does not depend on the measurement, so no replacement condition naming #559 is needed.
  - Its verification also passes. My own residual search is repository-wide and wider than its `docs/`/`README.md`/`REQUIREMENTS.md` scope. It finds no sentence that assigns the capture-hold measurement or its resolution to processor #61/#83. `docs_check.py`, `check_doc_paths.py` and `git diff --check` are rc 0.
  - I did not run that reviewer's script; I did not open it.
- **R313-3-S1, SUGGESTION (Docs).** "This head" appears at `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1606` and `:1709`.
  - Still present at `efcabc37`. The round-4 scope excluded it.
  - I agree it is optional: the wording loses its referent after merge. It does not affect coverage.
- **The stale "committed locally" status in the PR body,** which that report noted as not a finding, is my R312-4 S1.
- Nothing in that report changes my verdict or ledger.

## Real limits

**Hosted runs at the exact head, when sampled** (`receipts/hosted_check_runs.tsv`, about 00:21Z):
- 6 were completed `success`: `full-ci-gate`, `verilator-lint`, `changes`, `bdd-conformance`, `docs-check-no-git` and `wire-accountability`.
- 9 were in progress and 3 queued: `docs-check`, `elaborate`, `yosys-elaboration`, the four Yosys shards and the five Verilator shards.
- `Physical gPTP (nightly and manual)` was skipped. It is not evidence.
- Hosted and act acceptance belong to the manager.

**Renderer gates:** `gen_toc --check` and `check_em_dash` ran under the pinned renderer in a disposable virtualenv under scratch, installed with `--require-hashes` from `tools/markdown/requirements.txt` (`receipts/renderer_venv_freeze.txt`). Nothing was installed on the host.

**Model, not measurement:** the copy times are the page's cost model applied to bytes the host bench counts. Physical calibration: NOT RUN.

**Scope of this round:**
- No Verilator build ran; the delta has no HDL or test artifact. The pinned Verilator was not used.
- Not run, per the round's rules: the full parent, processor, gPTP, Yosys and builder banks; act or Docker; hardware.

**The 8x8 exposure:**
- The modelled pessimistic 8x8 margin is 0.78x at this head. Safety holds through void and retry.
- By decision 5824399821 it is a liveness question owned by #559, which is open.
- Under AGENTS section 7 it is not an open finding of mine. The maintainer should still explicitly accept that it merges with #559 open.

**Probe placement and restore:**
- Probes and the sensitivity run used scratch copies only.
- The gates and the capture probe left interpreter caches in the clone: 21 ignored `.pyc` files in the superproject and one in `protocol-processor`. I removed them.
- `receipts/restore_verification.log` records the state afterwards:
  - the index tree equals the HEAD tree `fc2e430a…`;
  - all 883 tracked non-gitlink files re-hash to their index blobs with no mode drift;
  - the four gitlinks equal HEAD (`external` is uninitialized, as it was at start);
  - there are no untracked or ignored files in the superproject or the three initialized submodules.

## Pending manager duties

- A second independent positive at this head, and acceptance of the reviewer-owned ledgers.
- Explicit maintainer acceptance of the modelled 8x8 hold exposure merging with #559 open.
- Hosted and act acceptance at the exact head, including the runs still in progress.
- The candidate merge build at live `dev` `ffcbd33de70278ae34b533dcbadde0b36c8cba13` (source base `573f0052a`). Source validation at this head is not that candidate.
- Maintainer merge authorization, post-merge containment, and copying the round 2-4 evidence into the PR (its Definition of Done still lists this as open).
- Publication of this packet.
- Optional: R312-4 S1, R312-2 S1, and my round-1 S2 and S3.
R312-4 FINISHED
