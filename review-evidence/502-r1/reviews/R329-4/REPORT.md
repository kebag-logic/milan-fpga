[R329] NEGATIVE - exact head 92c6154a17d1f1192f20a3a642e6a01b616afb67

Round R329-4, external independent review of PR #579 for issue #502.
Head `92c6154a17d1f1192f20a3a642e6a01b616afb67`, tree `05cd6071fb1249af03873ad7ab0d349ee7e630a0`.
Delta judged: `867a2e38a4e3231545a0a24b97d1e5612a6659fe..92c6154a` (one commit).
Source base for the full change: `831f94f4146cc45ec476f8c8dcf5afac7cd8eacf`.

Verdict in one line: every executable claim of the round holds. The three SystemVerilog edits are comment-only. Both test targets pass. R329-3 F1 and S1 are closed, and so is R328-3 S1. The mandated whole-tree sweep missed one current-state statement of the old pending source, in the ownership contract's section 13. That is one open MINOR under Docs and Conformance, so the verdict is NEGATIVE.

## Finding

### F1 - MINOR - Docs, Conformance - `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1354-1355` - section 13 still gives the pre-#502 `pend_i` as the current parent use

- **Authority and evidence.**
  - The round-4 assignment (issue 502 comment 5854288100, item 2) says: "Correct each current-state statement" that names the command mark as the pending trigger. Dated history may stay only "if it is labelled as history".
  - At head, :1354-1355 reads, in the present tense: "Parent use: KL_pp_shadow drives the backend's `pend_i = aecp_dyn_dirty_o | (|nvm_unflushed_o) | <the D2 sticky bit>`".
  - The same page defines the D2 bit at :1378-1383 as "a class-6/7 mark set sticky pending". It labels that "Original parent use" and says "Issue #502 replaces that trigger with accepted live writes".
  - The shipped glue is different: `hdl/milan/KL_pp_shadow.sv:945-957` is `aecp_dyn_dirty_o | (|nvm_unflushed_w) | aecp_live_wr_w | aecp_live_pend_r`, with `aecp_live_wr_w = aecp_name_wr_w | amap_live_wr_i`. That adds a live-write pulse term the formula lacks, and replaces the mark bit with the live-write history.
  - The page's own section 6.1 (:957-975) is correct, so the contract now contradicts itself.
  - `docs/design/SAVED_STATE_MATERIALIZATION.md:2057-2059`, edited this round, says that section 13 "records D2's original mark-based pending as history". :1355 does not.
- **Why the sweep missed it.** I reproduced all seven of the author's published patterns at `867a2e38`: 335 hits, 264 distinct lines, and every one has a row in the HANDOFF table. None of them reaches :1351-1352 at the starting head. The line names the source by its scope ("D2") and not by the word "mark" (receipts/author_sweep_repro.txt). The table is complete for its patterns, but the patterns do not meet the assignment's criterion.
- **Impact.** A reader of the authoritative ownership contract's donor section learns a pending equation that no longer exists. It names the mark-set bit as a live `pend_i` term and omits the accepting-edge pulse. That pulse is the property #502 delivers. This is the same class of stale-document defect as R329-3 F1, in the page the issue's scope item 3 names.
- **Required outcome.**
  - :1354-1355 either states the current composition, matching section 6.1 and `KL_pp_shadow.sv:956-957`, or is explicitly labelled as the parent use at D2's landing and points to section 6.1.
  - The sweep record must cover statements of the `pend_i` composition and references to the D2 bit by scope name, not only lexical "mark" matches.
- **Verification.**
  - `git grep -n -E "pend_i *=|D2 sticky" <head>` returns no present-tense line naming the D2 or mark bit as a current term.
  - The docs gates and `git diff --check` return rc 0.
  - The change must be comment- or doc-only.

## Suggestions (non-blocking, do not affect coverage)

- **S1 - SUGGESTION - Tests - `tb/verilator/pp_shadow/sim_main.cpp:1430`.** The `K12 GET_AUDIO_MAP exact record` label is still untagged. It runs only for a non-zero count, so no refusal control reaches it and R328-3 S1 is met. Tagging it too would make every map diagnostic name its case.
- **S2 - SUGGESTION - Docs - `hdl/common/csr/milan_csr.sv:197`.** The new three-line insert leaves "No CSR" alone on a line before "address, width, access...". Rewrapping it is cosmetic.

## Round-3 finding and suggestion, and R328-3 S1

| Item | Status at 92c6154a | Evidence |
|---|---|---|
| R329-3 F1 (MINOR, Docs) `SAVED_STATE_MATERIALIZATION.md:2081-2083` listed #502 as open | **CLOSED** | Now :2083-2089, "RESOLVED by #502". It says the name source is `aecp_name_wr_o`, the map source is `amap_edit_live_wr_p`, unchanged maps raise nothing, the mark stays the command-completion trigger, and pending is sticky until reset. It also says there is no materialization. Each claim matches `KL_pp_shadow.sv:945-957`, `milan_datapath.sv:4250-4271` and processor `gen_ucode.py:1786-1790` (FINISH bit 0 skips `NVM_MARK` when unchanged). |
| R329-3 S1 (SUGGESTION) :1717 present-tense mark trigger | **CLOSED** | Now :1719: "as the pre-#502 glue did ... Historical ... corrected by #502". |
| R329-3 S1 (SUGGESTION) :2070-2071 | **CLOSED** | Now :2072-2073: "the pre-#502 mark trigger falsely read durable ... (historical EXECUTED evidence, section 2)". |
| R328-3 S1 (SUGGESTION) case tags on refusal status and map-count checks | **CLOSED** | `sim_main.cpp:1356-1372` and `:1420-1428` take a tag. It is passed at :1462-1465, :1476-1479 and :1527-1528. In the log at head, input and output legs print the case name on both the response-status and the GET_AUDIO_MAP-count checks (receipts/tag_labels.txt). Check counts are unchanged at 591/591/591/295. |

## What was verified

1. **The three .sv edits are comment-only.**
   - `scripts/sv_comment_only.py` strips `//` and `/* */` comments, respecting strings. It then compares the code token streams of `milan_csr.sv`, `KL_nvm_backend.sv` and `cosim_top.sv` at 867a2e38 and 92c6154a. All three have different raw bytes and identical code: `COMMENT-ONLY`, rc 0.
   - Negative control: the same script on `KL_pp_shadow.sv` across 831f94f4..head reports `CODE-CHANGED`, rc 1.
   - `KL_pp_shadow.sv` (blob 2098892e) and `milan_datapath.sv` (blob 16a36b90) are byte-identical across the delta.
   - No other HDL file changed. No gitlink changed.
   - Receipt: `receipts/sv_comment_only.txt`.
2. **The whole-tree sweep, rerun independently.**
   - `scripts/sweep.sh` ran 12 pattern groups at head and at 867a2e38 (receipts/sweep_*.txt). By hand I also searched for `pend_i` composition, `sticky`, `D2`, `_nc_w`, and `mark` in READMEs, testing docs and scripts.
   - Zero hits remain for `aecp_mark_pend_r`, "every commit beat" and "conservative duplicate".
   - Every late-mark, program-tail, class-6/7, `#502` and "reads durable over" hit is either corrected current-state text or labelled history. The exceptions are the deliberate historical mutant's names, which are accurate. The one residual current-state statement is F1.
   - The author's HANDOFF table is complete for its own seven patterns: 335/264 reproduced exactly, with no missing or extra rows.
   - Receipts: `receipts/sweep_disposition.md` and `receipts/author_sweep_repro.txt`. The published HANDOFF copy (`receipts/author-r5-HANDOFF.md`) comes from branch `502-review-evidence` at `06f57d47`.
3. **pp_shadow default and pending-mutant.** Both ran with Verilator 5.050, identity verified in `receipts/tool_identity.txt`. The `verilator_bin` sha256 is 44898b22..., which matches the recorded identity; every Verilation report in the logs names 5.050.
   - `make -C tb/verilator/pp_shadow`: rc 0 in 68 s, four legs at 591, 591, 591 and 295 checks, 0 failures.
   - `make -C tb/verilator/pp_shadow pending-mutant`: rc 0 in 26 s. The clean control passes 295/0. The mark-trigger mutant fails 12 checks, all of them named: K10 and K10 repeat; K12 input, output, remove input and remove output; each on both `no_durable_claim_over_unsaved` and `pending_from_accepting_edge`.
   - Receipts: `receipts/pp_shadow_default.log` and `receipts/pending_mutant.log`.
4. **Docs gates, rc 0 with the pinned Markdown environment** (cmarkgfm 2025.10.22, html5lib 1.1 and the rest of `tools/markdown/requirements.txt`):
   - `docs_check.py` in Git mode and with `GIT_DIR=/dev/null`;
   - `check_em_dash.py --base 831f94f4...`, `check_doc_style.py`;
   - `gen_toc.py --check` and `--verify-anchors`, `check_doc_paths.py`;
   - `git diff --check` over both the delta and the base.

   Also rc 0: `measure_test_evidence.py --check`, `check_port_contracts.py` (the `pend_i` `//!` contract text changed) and `lint_rtl.py --check`.

   On the system interpreter, three gates refused with rc 2 because the renderer was missing. That is an environment refusal, recorded in `receipts/docs_gates.txt`, and I do not count it as a pass or a fail. The passing runs are in `receipts/docs_gates_mdenv.txt`.
5. **PR body.** The live body (receipts/pr579_body_live.md) is the author's round-4 `PR-BODY.md` byte for byte, apart from one trailing newline.
   - It carries no stale lines. Its behaviour, reproduction, refusal-control description (status 7, empty map, both pending bits clear, case-named diagnostics), check counts and mutant description all match what I reproduced at head.
   - Prior-head evidence is labelled as prior-head.
   - Its sentence "Every search pattern and hit has a disposition in the handoff" is true for the published patterns. F1 shows the patterns were not sufficient.
   - Nothing in the body needs changing for this round, beyond a later round's own update.
6. **Label-only harness edits.**
   - `sim_nxn.cpp:2324` changes only the VERSION check's label. The expected value `0x00020060` is unchanged.
   - No script greps for the old label, and none greps for the old pp_shadow labels.
   - Payloads, expected values and check counts are unchanged.

## Reviewer-owned lens ledger

| Lens | Result | Examined artifacts (at head) | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | Round-4 assignment items 1-3 (issue 502 comment 5854288100). `SAVED_STATE_MATERIALIZATION.md:209-248, 1651-1700, 1716-1719, 2026-2127`. `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:24-35, 955-975, 1255-1275, 1336-1390, 1735-1750`. Issue #502 decision comments 5844866872, 5846418959 and 5848417938 against `KL_pp_shadow.sv:925-957`, `milan_datapath.sv:4245-4271` and processor `gen_ucode.py:1765-1795` | R329-4 | 92c6154a17d1f1192f20a3a642e6a01b616afb67 |
| RTL | CLEAN | `receipts/sv_comment_only.txt`, a token-level proof that `milan_csr.sv`, `KL_nvm_backend.sv` and `cosim_top.sv` changed in comments only, with a negative control. `KL_pp_shadow.sv` and `milan_datapath.sv` are blob-identical to 867a2e38. I checked the pending glue `KL_pp_shadow.sv:925-957` (single `clk_i`/`rst_n`, no CDC, sticky until reset) and the qualified write `milan_datapath.sv:4250-4271` against ownership section 6.1 | R329-4 | 92c6154a17d1f1192f20a3a642e6a01b616afb67 |
| Robustness | CLEAN | `tb/verilator/pp_shadow/sim_main.cpp:1448-1530`: zero-record, out-of-range record (status 7), two-record partial refusal (status 7) in both directions, static-output refusal (status 11), and reset between cases through `pending_boot`. All pass at head in `receipts/pp_shadow_default.log`, with pending clear and storage unchanged. The delta changes no behaviour (RTL row) | R329-4 | 92c6154a17d1f1192f20a3a642e6a01b616afb67 |
| Tests | CLEAN | The delta in `sim_main.cpp:1353-1372, 1417-1428, 1457-1479, 1524-1528` is label-only. Check counts are unchanged (591/591/591/295). `receipts/tag_labels.txt` shows the case names in both legs. `receipts/pending_mutant.log` shows the mark-trigger mutant killed by 12 named K10/K12 checks and the clean control passing. `receipts/p4_probe.txt` shows P4 killed by the case-tagged partial-refusal checks. `sim_nxn.cpp:2324` changes a label only, and no tool depends on the old label | R329-4 | 92c6154a17d1f1192f20a3a642e6a01b616afb67 |
| Docs | UNCLEAN (F1) | The delta in `CHANGELOG.md:254-260`, `SAVED_STATE_FASTCONNECT.md:123, 1371-1397`, `SAVED_STATE_MATERIALIZATION.md` (all hunks), `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:29-34`, and `tb/verilator/pp_shadow/README.md:95`. The whole-tree sweep (`receipts/sweep_disposition.md`). The docs gates (`receipts/docs_gates_mdenv.txt`). The live PR body (`receipts/pr579_body_live.md`) | R329-4 | 92c6154a17d1f1192f20a3a642e6a01b616afb67 |

The Conformance and Docs lenses stay unclean while F1 is open. RTL, Robustness and Tests are covered clean at this exact head.

## Prior public review findings on this PR

I read the prior findings only after my own pass over the delta and after the verdict and ledger above were written. None of them had raised F1. The R329-3 Docs row examined `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1374-1384`, not :1351-1352, so I missed this line at round 3.

| Finding | Severity, lenses | State at 92c6154a | Evidence at this head |
|---|---|---|---|
| R328-1 F1 = R329-1 F2: no refused-at-validation map control | MINOR, Tests/Robustness | CLOSED | `K12 refused record input/output` pass: status 7, count 0, pending clear (`receipts/tag_labels.txt`, `receipts/pp_shadow_default.log`) |
| R328-1 F2: materialization section 1 and 5.2 text stale | MINOR, Docs | CLOSED | `SAVED_STATE_MATERIALIZATION.md:125-134` and :145-146 name `aecp_name_wr_o` and `amap_edit_live_wr_p`. :485 names `aecp_live_pend_r`, which exists at `KL_pp_shadow.sv:938` (`receipts/prior_findings_check.txt`) |
| R328-1 F3: pending-mutant missing from the explicit-campaign table | MINOR, Docs | CLOSED | `docs/testing/TESTING.md:268` |
| R328-1 S1 = R329-1 F3: an unchanged duplicate set pending | MINOR, Conformance/Tests/Docs | CLOSED | `milan_datapath.sv:4269-4271` requires a change. The `K12 duplicate input/output` controls pass with pending clear. "Conservative duplicate" has zero hits tree-wide |
| R328-1 S2: observer anchored on the glue's own triggers | SUGGESTION, Tests | CLOSED | `sim_main.cpp:263-265`. `live_state_changed` is graded from storage. The delta is label-only |
| R329-1 F1: REMOVE never observed from a durable baseline | MINOR, Tests/Robustness | CLOSED | The `K12 remove input/output` checks pass. The mark-trigger mutant fails both `K12 remove` pairs (`receipts/pending_mutant.log`) |
| R329-2 F1 = R328-2 F1: CHANGELOG:39 and SUBMODULES:61 trigger text | MINOR, Docs | CLOSED | `CHANGELOG.md:39-40`, `docs/reference/SUBMODULES.md:61` |
| R329-2 S1 = R328-2 S2 (PR body): "prepared locally" sentence | SUGGESTION, Docs | CLOSED | Zero matches in the live body |
| R328-2 S2 (ownership :1263 "first accepted write") | SUGGESTION, Docs | CLOSED | Now :1266, "from the first actual write" |
| R328-2 S1: P4 (phase-5 term dropped) survived | SUGGESTION, Tests/Robustness | CLOSED | Rerun at this head (`scripts/p4_probe.py`, `receipts/p4_probe.txt`): the mutant fails 4 checks, all named `K12 partial refusal input/output sticky_pending_PP_STAT/_PP_NVM_STAT`. The case tag survives the relabelling |
| R329-3 F1, R329-3 S1, R328-3 S1 | MINOR / SUGGESTION | CLOSED | See the round-3 table above |

The open set at this head is F1 (MINOR). S1 and S2 are optional.

## Real limits

- Physical calibration was NOT RUN. The field/freshness skips are not hardware evidence. This round adds no hardware or flash-persistence claim, and I did not test any.
- I ran only focused targets: pp_shadow default and pending-mutant, the docs gates, and three light repository gates. I did not run the full parent, processor, gPTP, Yosys or builder banks, the `milan_dp` suite (whose `sim_nxn.cpp` label changed), `nvm_cosim` (whose `cosim_top.sv` comment changed) or `nvm_backend`. The comment-only proof covers the two `.sv` files, and the label-only diff covers `sim_nxn.cpp`.
- The simulator path in the assignment (`$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator`) does not exist on this host. I used the round-4 manager wrapper `$VALIDATION_STORAGE/502-manager-r4/pinned-tool-bin/verilator` after verifying version 5.050 and the `verilator_bin` digest against its identity record. The system Verilator 5.052 was not used.
- I did not judge the hosted contexts. A read-only snapshot at 09:10Z (`receipts/hosted_checks_snapshot.txt`) showed 14 completed-success, 5 in progress (Verilator shards 1, 2 and 4 of 5, `elaborate`, `docs-check`) and 1 skipped (Physical gPTP, nightly/manual). A skipped context is not an executed job. Acceptance remains the manager's duty.
- Host paths in this report and its receipts are abbreviated as `$CLONE` (the review clone), `$PACKET` (this packet), `$VALIDATION_STORAGE`, `$PINNED_TOOL_ROOT` (the 5.050 package root) and `$MD_VENV` (the Markdown environment). The scripts take their paths as arguments.
- I made no GitHub writes, source edits, commits or pushes, and did not use Docker or act. After the probes the clone was restored: HEAD, index listing, gitlinks and tree `05cd6071` are identical, and the worktree has no untracked or ignored residue (`receipts/integrity_before.txt`, `receipts/integrity_after.txt`).

## Pending manager duties

- Route F1 to the executor, and re-review the corrected head for Docs and Conformance. The RTL, Robustness and Tests coverage above stays banked only if the fix touches no artifact in their scope.
- Accept the hosted and act evidence at the final head.
- Build and validate the candidate merge on live dev `e0920d77162284d8da52ffaf13a973e451e44f90` (source base 831f94f4). Run post-merge containment.
- Get maintainer merge authorization.

R329-4 FINISHED
