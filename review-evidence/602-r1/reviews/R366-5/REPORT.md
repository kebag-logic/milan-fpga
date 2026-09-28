[R366] POSITIVE - exact head d09c72ea2b0be1a2df3e18e77774f14f6df3242c

# R366-5: internal independent delta review of PR #603 (issue #602), F1 answer round

- **Head:** `d09c72ea2b0be1a2df3e18e77774f14f6df3242c`, tree `59af42f36951fab42be918452ee3fa3e1c7f63ea`. Source base `6d5ebd7357c1e468e446f18a61527c5be6118a04`.
- **Delta under review:** `6c5ca18f..d09c72ea`. This is one commit by the executor, "Clarify pre-602 measurements and post-602 acceptance contract". It answers R366-4 F1 under the fourth disposition (issue 602 comment 5868627247).
- **Reconstructed from the public record, in this order:**
  - AGENTS.md and CONTRIBUTING.md.
  - The #602 ruling 5859297355 and the fourth disposition 5868627247, together with the earlier scope record I used in R366-4. That record is the round-2 acceptance 5860151273 and disposition 5866668156.
  - [A414] REVIEW READY 5868773906 and issue #387's acceptance list (items 2 and 4).
  - `docs/design/GM_LOSS_RECOVERY.md#media-re-base-on-a-phc-step` and `docs/design/TIME_SYNC.md#step-policy`.
  - The diff and history, then the executable evidence below.
- **Read-only inputs:** my own R366-4 packet. From it I copied `stale_scan.py` byte for byte, plus three helper scripts. R367-3 stands as the POSITIVE at the pre-merge ancestor, and I did not re-litigate it.
- **Independence:** the verdict and ledger below come from my own pass.
  - I read the public PR comments after all checks had run and my verdict was settled. My first attempt to write the draft verdict into this file failed on a tool precondition, so the draft was not saved before that read.
  - The only review content published since my R366-4 round is R366-4 itself. That round was already my read-only input. No other reviewer's report was read.

## Verdict

**POSITIVE.** The one-commit delta resolves R366-4 F1 exactly as the fourth disposition prescribes and changes nothing else. No `BLOCKER`, `MAJOR` or `MINOR` finding is open at this head. All five lenses were applied and are clean.

| Focus item | Result |
|---|---|
| (1) Lines 165-173 now mark the counted `mr`/MEDIA_RESET text as the contract of the measured pre-#602 image and link the #602 ruling. Line 349 states the pending #387 acceptance-4 measurement in post-#602 terms. | **MET** |
| (2) The page's measurement tables are byte-identical | **MET** |
| (3) At the new head, no current statement outside `docs/history/**` presents a PHC-only step as toggling `mr` or counting MEDIA_RESET, whatever the wording | **MET** |
| (4) Nothing else changed, and the Markdown gates pass | **MET** |

### (1) The page's text: MET

`delta_check.py` found 0 failed assertions (`receipts/delta-check.log`). Every changed line lies inside the two disposed regions. At the new head these are lines 165-177 and 353-355; old line 349 moved down by four inserted lines.

- **Old line 165, now 165-169.** The old "#387 item 2 records the [media re-base contract](GM_LOSS_RECOVERY...)" becomes three lines:
  - "#387 item 2 defined the measured pre-#602 image's media re-base contract."
  - "The [#602 ruling](…issuecomment-5859297355) supersedes that contract's PHC-step `mr` and MEDIA_RESET obligation."
  - "The [current contract](../design/GM_LOSS_RECOVERY.md#media-re-base-on-a-phc-step) retains the render re-base and `tu`."
- **Old line 169, now 173.** It reads "That pre-#602 contract required one counted event per step."
- **Old line 171, now 175.** It reads "Licensed streams kept running." Only the tense changed.
- **Old line 173, now 177.** It reads "Under that pre-#602 contract, one `mr` toggle and one MEDIA_RESET recorded the event."
- **Old line 349, now 353-355.** It reads "Under the [#602 ruling](…), that measurement must observe the step's counted render re-base and `tu`." and "A PHC-only step must leave `mr` and MEDIA_RESET unchanged."

I checked the new text against its authorities:

- **The ruling.** Its supersession scope is "only the PHC-step-to-`mr` obligation of the #387 decisions … and the step-only MEDIA_RESET that follows from it". It "does not change … the render re-base". Line 167 names exactly that obligation, and lines 169 and 353 keep exactly the render re-base and `tu`.
- **The linked current contract.** `GM_LOSS_RECOVERY.md:142-156` says "Each step … is one counted event". It also says a PHC-only re-base "signals `tu`, without changing `mr` or MEDIA_RESET". Lines 169, 353 and 355 agree with this. `delta_check.py` confirms that both link anchors exist, and `check_doc_paths` and `docs_check` pass.
- **The measured image.** The page's image identity is `9e9954e9…`, measured on 2026-09-27, before the ruling. The #602 RTL change exists only on this lane. So calling the measured image's contract "pre-#602" is accurate.
- **Line 179,** "It specifies no step-to-relocked-media time bound", is unchanged. It now refers to that pre-#602 contract, and it stays true: #387 item 2 recorded no bound, and the current contract adds none.
- **#387 acceptance 4** grades step-to-relocked-media time through MEDIA_LOCKED/UNLOCKED, `CLKV_STAT` `tu` and `A_MCSRV_STAT`. Lines 351-355 keep the unexercised condition as it was: a GM change while locked CRF keeps running. They re-express only the event that the measurement must observe, exactly as the disposition's line-349 bullet dictates.

### (2) Tables: MET

- **Identical to the prior head.** All 91 table rows on the page are byte-identical to `6c5ca18f`, 8,286 bytes including newlines (`receipts/delta-check.log`). This matches the executor's stated byte count.
- **Identical to dev.** The rows are also identical to dev `0eff6d2e`.
- **The only lane edit.** The page at `6c5ca18f` equals dev's copy, so this commit is the lane's only edit to the page.

### (3) Stale scan at the new head: MET

- **Unchanged `stale_scan.py`** (`receipts/stale-scan.log`, byte-identical to the R366-4 copy). The scan found 2 strict hits and 71 broad hits.
  - The two strict hits are `394_387_E1_SWITCH_CYCLES.md:177`, now explicitly "Under that pre-#602 contract", and `TESTING.md:273`, the mutation-control inventory row. Neither presents a PHC-only step as an `mr` or MEDIA_RESET cause.
  - The broad inventory equals R366-4's 69 hits line for line, except for two new hits on the page, `:167` and `:355`. Both state the #602 rule. I had already classified every carried-over hit as consistent in R366-4, and no file outside this page changed.
- **Multi-line companion, `window_scan.py`, new this round.** The F1 statement spanned lines, so this scan lists every 7-line region, in every tracked text file outside `docs/history/**`, where a PHC-step term and an `mr`/MEDIA_RESET term co-occur (`receipts/window-scan.log`).
  - At this head it finds 75 regions: 44 carry a #602-consistent marker, and 31 do not.
  - **I read all 31 unmarked regions in context.** They cover:
    - the gmstep control list at `GM_LOSS_RECOVERY.md:216-228` and its test table;
    - the `TIME_SYNC.md` notification table;
    - the page's outage-measurement table header;
    - FR_NFR and REGISTER_MAP counter rows;
    - packetizer, CRF-transmit and render-setpoint port comments;
    - builder census mutants, whose message is that the restart pulse reads "only selected CRF disruption and received mr propagation";
    - soak self-tests, tkdiag, sim_nxn and pcmlpf harness lines;
    - counters-contract steps.
  - None presents a PHC-only step as toggling `mr` or counting MEDIA_RESET.
  - **Sensitivity check.** At `6c5ca18f`, the same scan reports the two F1 regions of the page (`:167-179` and `:343-355`) as unmarked. At this head, both carry the #602 marker (`receipts/window-scan-prior.log`). So the scan distinguishes the defect from its fix.

### (4) Nothing else changed, and the gates pass: MET

- **Scope of the delta.**
  - The commit's only parent is `6c5ca18f`.
  - Its message is one line with no trailers.
  - `git diff --name-status` lists exactly one path, `M docs/findings/394_387_E1_SWITCH_CYCLES.md`.
  - All four gitlinks are unchanged: `protocol-processor 16be6768`, `gptp-processor 5dce647a`, `third_party/verilog-axis 48ff7a7e`, and `external efeb541a` (uninitialised).
  - No path under `hdl`, `tb`, `sw`, `tests`, `scripts`, `syn`, `configs`, `REQUIREMENTS.md`, `docs/design` or `docs/testing` differs from `6c5ca18f`.
- **Markdown gates,** run with the pinned Markdown environment. Every one returned rc 0:
  - `docs_check`: 0 findings across 172 md files.
  - `check_em_dash --base 6d5ebd73`: 0 findings over 1,638 added lines.
  - `check_em_dash --base 6c5ca18f`: 0 findings over 11 added lines.
  - `check_doc_style`: 22 current documents.
  - `check_gptp_docs --with-submodule`.
  - `gen_toc --check`.
  - `check_doc_paths`: 854 cited paths resolve.
  - `git diff --check` against both `6d5ebd73` and `6c5ca18f`.

## Findings

None. There is no BLOCKER, MAJOR, MINOR or SUGGESTION at this head.

**Observation, not a finding.** `scripts/check_doc_style.py:15-38` does not list `docs/findings/**`, so its 10-word sentence limit does not gate this page. The new lines 167 and 353 exceed that limit, as many pre-existing lines on the page already do. The page is outside the gate by the repository's own scope, so this is not a defect of this delta.

## Prior public findings on this PR, resolved or retained at this head

The table below was written after my independent pass. No lane-only file other than the page changed since `6c5ca18f`, so every item R366-4 found intact remains intact.

| Prior finding | Status at `d09c72ea` | Evidence |
|---|---|---|
| **R366-4 F1** (MINOR, Conformance and Docs): the current finding page stated the superseded PHC-step `mr`/MEDIA_RESET contract | **RESOLVED** | Items (1)-(3) above; `receipts/delta-check.log`, `stale-scan.log`, `window-scan.log` and `window-scan-prior.log` |
| R366-4 observation: the page is missing from the `docs/findings/README.md` index | Routed to the #495 checklist by disposition 5868627247; not in this PR's scope | Unchanged |
| R366-1 F1 = R367-1 F1: current documents stated the superseded rule | **RESOLVED**, including the merge-head outcome that R366-4 F1 had re-opened | Stale and window scans |
| R366-1 F2 = R367-1 F2; R366-1 F3; R366-2 F1; R367-2 F1 | **RESOLVED**, still intact | No lane file other than the page changed. Controls 3, 14 and 15 caught; gmstep 103/0 |
| R366-1 F4 = R367-1 F3; R366-2 F2, F3 = R367-2 F2, F3 | **TAKEN**, still intact | Unchanged files |
| R367-1 F4 (rename control) | Closed by assignment 5860151273 | Unchanged |
| R366-3 S1, S2 and R367-3 S1 (SUGGESTIONS) | Retained as optional; not taken | `sim_main.cpp` and `sim_gmstep.cpp` are unchanged |

## Reviewer-owned lens ledger (R366-5)

| Lens | Status | Examined artifacts (at the head) | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `docs/findings/394_387_E1_SWITCH_CYCLES.md:165-179,349-355`, against: ruling 5859297355 and its supersession scope; disposition 5868627247; `GM_LOSS_RECOVERY.md:142-156`; #387 items 2 and 4; and the page's image identity. Stale scan (2 strict and 71 broad hits read) and window scan (31 unmarked regions read). | R366-5 | `d09c72ea2b0be1a2df3e18e77774f14f6df3242c` |
| RTL | CLEAN | `hdl/**` is identical to `6c5ca18f` (`delta_check.py`; path diff empty). `milan_datapath.sv:3132-3134`: `mcr_restart_p_w` carries no re-base term, and `media_rebase_p_w` still feeds the render path. `lint_rtl.py --check --jobs 8` PASS, 90 <= 90. tkdiag 96/0 with 4/4 restart-engine mutants caught. | R366-5 | `d09c72ea2b0be1a2df3e18e77774f14f6df3242c` |
| Robustness | CLEAN | The gmstep leg's coincident, pending and holdover checks (103/0, `receipts/gmstep-clean.log`), including "coincident: a PHC step does not suppress the CRF restart". Option-off settime and adjtime controls 14 and 15 caught (`receipts/gmstep-control-14-15.log`). Soak NOT RUN and resolution boundaries (self-test, 78 OK). The page's new text in its failure-path sense: the acceptance-4 condition stays NOT MET, and the page now names the observable that must be absent. | R366-5 | `d09c72ea2b0be1a2df3e18e77774f14f6df3242c` |
| Tests | CLEAN | `tb/**` and `tests/**` are identical to `6c5ca18f`. At this head: `make gmstep` 103/0; control 3, the restored re-base term, is caught on exactly the two PHC-only checks; controls 14 and 15 are caught; `torture_release_mutants.py` 132 killed; behave `torture_campaign_plan.feature` 87/0; self-test 78 OK. The scans' sensitivity is shown on `6c5ca18f`. | R366-5 | `d09c72ea2b0be1a2df3e18e77774f14f6df3242c` |
| Docs | CLEAN | `394_387_E1_SWITCH_CYCLES.md` (full diff, 91 table rows identical, both anchors present). Stale and window scans over every current document. The nine Markdown and diff gates, all rc 0 (`receipts/docs-*.log`, `diff-check*.log`). PR and issue evidence: [A414] REVIEW READY 5868773906. | R366-5 | `d09c72ea2b0be1a2df3e18e77774f14f6df3242c` |

## Commands and receipts (all run in the foreground, sequentially)

- **Receipts.** `run_receipt.py NAME TIMEOUT CWD -- CMD` records the head, command, environment overrides, rc, elapsed time, and the log's size and SHA-256.
  - The gmstep and tkdiag logs had the host path of the pinned simulator root replaced by `<pinned-verilator-root>`.
  - Their receipts keep the raw log's hash and size (`log_sha256_raw`, `log_bytes_raw`) next to the published log's hash and size.
- **Scope and text:** `python3 -B delta_check.py <clone>`.
- **Scans:**
  - `python3 -B stale_scan.py <clone> d09c72ea…`.
  - `python3 -B window_scan.py <clone> d09c72ea…`, and the same at `6c5ca18f…`.
- **Simulator identity** (`receipts/tools_identity.txt`):
  - The assigned path `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` is **absent** on this host.
  - I used a copy of `$VALIDATION_STORAGE/602-manager-r4/pinned-tool-bin/verilator` instead. Its wrapper sha256 is `905795b9…`, and it reports `Verilator 5.050 2026-07-01 rev v5.050`, the project pin at `rtl-fast.yml:18`. The `verilator_bin` sha256 is `44898b22…`. This is the same identity as in R366-4.
- **Simulation:**
  - `make gmstep`, and `make` in `tb/verilator/tkdiag`, with `VERILATOR_JOBS=8`.
  - `python3 -B gmstep_chunk.py <clone> 3 3` and `14 15`. These plant the clone's own unmodified controls through its `run_control`.
- **Soak and lint:**
  - `torture_campaign.py --self-test`;
  - `torture_release_mutants.py`;
  - `python3 -B -m behave tests/features/torture_campaign_plan.feature -f plain`;
  - `lint_rtl.py --check --jobs 8`.
- **Markdown gates:** as listed in item (4).
- **Hosted checks at the head** (read-only, at 11:20Z; `receipts/hosted_check_runs_at_head.txt`). The PR is ready, not draft, at this head.
  - Success: bdd-conformance, changes, docs-check-no-git, full-ci-gate, verilator-lint, wire-accountability, Yosys shards 0-3.
  - In progress: docs-check, elaborate, yosys-elaboration, Verilator shards 0-4.
  - Skipped by design: Physical gPTP.
  - Not yet emitted when read: the `rtl-fast`, `verilator-suites` and `yosys-portability` aggregates.
  - These are a snapshot. The manager owns hosted and act acceptance.
- **Clone restoration** (`audit_clone.py`, `receipts/clone-audit.log`, AUDIT CLEAN):
  - I removed only the ignored build products and `__pycache__` directories that my runs created, in the superproject and in `protocol-processor`.
  - HEAD, the tree and the index-written tree equal the reviewed ids.
  - All 942 tracked blobs and modes match.
  - All four gitlinks are at their recorded commits, with no untracked, ignored or modified entry. `external` is uninitialised, as before.

## Real limits

- **Not run, by assignment:**
  - the full `milan_dp` run, the full `gmstep_mutants.py --all` inventory, and the builder banks;
  - the full parent, PP, gPTP and Yosys banks; OOC;
  - act, and the hosted aggregates.
- **Mutation coverage at this head is partial.** Only controls 3, 14 and 15 were planted. R366-4 ran the full 22/22 inventory at `6c5ca18f`, and no file in `tb/**`, `hdl/**` or `tests/**` has changed since then.
- **The source banks were not re-executed.** I relied on the assignment's statement that the manager's full source static/builder and native banks passed at this head. The only public executor evidence at this head that I found is [A414] REVIEW READY 5868773906.
- **The scans are heuristic prefilters.** Their completeness rests on my reading of every hit and every unmarked region. A statement with no PHC-step term and no `mr`/MEDIA_RESET term within seven lines would not be listed.
- **Nothing here is physical proof.** There was no physical calibration, bench, lwSRP reservation or placed-area measurement. The gmstep leg runs in compressed time.
- **Simulator path.** The assigned simulator path was absent. The substitute's identity is recorded above.

## Pending manager duties

- Build and gate the final current-dev candidate at the merge turn. The source base is `6d5ebd73` and the live dev is `7a7582f0`. This includes any further dev overlap with the page, `GM_LOSS_RECOVERY.md`, `TESTING.md` or `REQUIREMENTS.md`, and a re-run of the stale scan on the candidate.
- Accept the exact-head hosted `rtl-fast`, `verilator-suites` and `yosys-portability` aggregates once they are emitted, and run the act replica.
- Obtain the external review for the merge bar. Confirm the completion ledger against the merge candidate. Run post-merge containment.
- Track the `docs/findings/README.md` index entry under #495, as disposed.

R366-5 FINISHED
