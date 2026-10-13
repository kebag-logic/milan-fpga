[R558] POSITIVE - exact head 313616d1a18549d41907db389d378f0beb9bc543

# R558-13 - issue #696 / PR #706 - delta review of the merge of dev `e81ce82f`

- **Head:** `313616d1a18549d41907db389d378f0beb9bc543`, tree `8eb5d868bfac1973ba1d82b0665aabae07d9494c`.
- **Parents, in order:** `26e2748f47b0d8fa533f53203264d9f31fc13c48` (the lane head that R558-12 and R559-9 reviewed POSITIVE) and `e81ce82f9aa3e4dcaffa5bcdf7e60f0c7cffd80c` (dev). The merge base is `c6bd08c6f52632c6d33d834ce842ac3cf63f29cc`.
- **Role:** cleared-context internal reviewer. I applied all five lenses to the merge.
- **Verdict:** POSITIVE.
  - The merge commit is exactly git's automatic three-way merge. It had no textual conflict.
  - Only two files changed on both sides, `docs/design/AREA_BUDGET.md` and `docs/design/MARK_II_AREA_PLAN.md`. In each, both sides' edits are carried byte-for-byte.
  - Every other file equals the parent that changed it. The 696 sources and the dev features (M8a, #716, #727, #726) are intact.
  - I found no BLOCKER, MAJOR or MINOR.
  - One new RESIDUE is recorded: stale "unpublished" wording in the PR body (R558-13-R1). Earlier RESIDUE items are retained.

## 1. Scope reconstructed from public state

- **Read in this order:**
  1. AGENTS.md (sections 3, 6 and 7) and CONTRIBUTING.md.
  2. docs/README.md.
  3. Issue #696: the body and acceptance 1-4, assignment 6076750392, the rulings it cites, and the merge-round assignment 6142198285.
  4. The author's REVIEW READY 6147603995 and the live PR body.
  5. The interface and record authorities this merge touches: `docs/design/AREA_BUDGET.md`, `docs/design/MARK_II_AREA_PLAN.md`, `syn/ooc/pp_resource_baseline.json`, `scripts/suite_shards.py`, `docs/testing/CI_WORKFLOWS.md` and `tb/verilator/maap/integration.mk`.
  6. `git diff c6bd08c6..313616d1`, the history, and both parent-relative diffs.
  7. The public packet `696-review-evidence@dd8350f0:review-evidence/696-r1/author-r13`, together with the publisher's `MANIFEST.json`.
- **Prior public review findings:** I read them only after my own pass and my executed checks (section 8).
- **What the round assignment (6142198285) requires:**
  1. A merge commit with no rebase, and a STOP if any conflict touches the MAAP RTL, the `maap` suite or its mutation table.
  2. `suite_shards.py --selftest` passes.
  3. `maap` keeps 1,375 s, on a worker within the 60 % bound.
  4. The `maap` suite, its campaign and the round-7 Annex B checks still pass.
  5. The shipping image is unchanged apart from dev's own changes, with LUT/FF reported against dev.
  6. The merge is recorded in HANDOFF.md and the PR body.
- **Frozen acceptance:** acceptance 1-3 of the issue body are unchanged. Acceptance 4 (bench) belongs to the post-merge bench lane, per item 6 of assignment 6076750392.

## 2. Merge facts

Receipts: `receipts/merge_reconstruct.txt`, `receipts/conflict_file_hunks.txt` and `receipts/merge_check_probe.txt`. The script is `scripts/merge_reconstruct.sh`.

- **The merge is mechanical.** `git merge-tree --write-tree 26e2748f e81ce82f` returns tree `8eb5d868...` with rc 0, and it lists no conflict. That is the recorded tree of `313616d1`. There are no conflict hunks, so no manual resolution exists to judge.
- **Inventory:**
  - The lane side changed 17 files since the base.
  - The dev side changed 57 files since the base.
  - Two files are in both lists.
- **Files the merge resolved, and how:**

| File | Lane hunks (base lines) | Dev hunks (base lines) | Resolution | Lane edits carried | Dev edits carried |
|---|---|---|---|---|---|
| `docs/design/AREA_BUDGET.md` | 13, 107-108, 120-122, 125, 128-131, 140-141, 145-146, 373, 412-413, after 464 | 232, 245-254, 257-261, 266-268, 272, 282, 385 | Automatic: the line ranges are disjoint, so there was no conflict | Yes. The content-line hash of `c6bd08c6..26e2748f` equals that of `e81ce82f..313616d1` (`91742aef...`) | Yes. The hash of `c6bd08c6..e81ce82f` equals that of `26e2748f..313616d1` (`0062af94...`) |
| `docs/design/MARK_II_AREA_PLAN.md` | 56, 110, 118-128, 130-133, 136-138, after 143, 652-653, 692-693, 703, 944, 965, 1091-1092, 1107 | 42, 435, 601, after 774, 795-797, 809-812, 816-822, 825-826, 831-832, 834, 837-838, 840, 859-860, 868-869, 1128 | Automatic: disjoint, no conflict | Yes (`74b5e1c3...` on both sides) | Yes (`621bb02b...` on both sides) |

  The numstats add up exactly. `AREA_BUDGET.md` is +31/-18 on the lane side and +25/-22 on the dev side, and the merge relative to the base is +56/-40. `MARK_II_AREA_PLAN.md` is +34/-30 and +34/-30, and the merge is +68/-60.
- **Every other file:**
  - The 15 remaining lane-side files are byte-equal to `26e2748f`.
  - The 55 remaining dev-side files are byte-equal to `e81ce82f`.
  - No file differs from both parents except the two above.
- **The check can fail.** `scripts/merge_check_probe.sh` plants two defects in a copy of the merged `AREA_BUDGET.md`: one drops a lane line, the other drops a dev line. Each plant makes the hunk-preservation comparison report `NO`, and the real merged file reports `yes`/`yes`.
- **Gitlinks** are identical at `26e2748f`, `e81ce82f` and `313616d1`:
  - `gptp-processor` `7dda9c3b`;
  - `protocol-processor` `2ad2f845`;
  - `third_party/verilog-axis` `48ff7a7e`;
  - `external` `efeb541a`;
  - `third_party/lwSRP` `08ee86e8`.

  The receipt is `receipts/blob_identity.txt`.

## 3. Both sides intact in the merged tree

Receipt: `receipts/blob_identity.txt`.

- **The 696 side:** these files are byte-identical to `26e2748f`:
  - `KL_maap.sv` (`746be52d`) and `milan_datapath.sv` (`e0ad4691`);
  - `MAAP_FABRIC.md`;
  - the MAAP `Makefile`, `integration.mk`, `mutants.py`, `sim_main.cpp` and `sim_integration.cpp`;
  - the differential sources;
  - `pp_resource_baseline.json` and the #234 findings page.

  These blobs equal the author's `merge-provenance.json`.
- **The dev side:** these files are byte-identical to `e81ce82f`:
  - **M8a (#721):** `sw/litex/ctrl_memory.py`, `sw/litex/milan_soc.py`, `syn/ooc/ctrl_memory_ooc.py`, `docs/design/SPLIT_CONTROL_MEMORY.md` and `plat/ctrl_split.ld`;
  - **#716/#724:** `test_ctrl_firmware_shards.py` and `test_ctrl_firmware.py`;
  - **#727/#728:** `scripts/suite_shards.py`, `.github/workflows/rtl-fast.yml` and `docs/testing/CI_WORKFLOWS.md`;
  - **#726/#729:** `KL_avtp_rx_monitor.sv`, `KL_avtp_rx_monitor_ctx.sv`, `tb/verilator/milan_dp/stream_counters.py`, `tb/verilator/milan_dp/Makefile` and `docs/testing/726_STREAM_COUNTERS.md`.
- **Semantic interplay, checked rather than assumed:**
  - **Source derivation.** `integration.mk` takes the datapath source list and flags from `milan_dp`'s `print-srcs`/`print-dp-vflags`, which dev changed in #726. The integration build at this head elaborates the merged datapath, with the #726 monitor RTL and the 696 `KL_maap` wiring (`eff_link_w` and `ptp_now_w[31:0]`, `milan_datapath.sv:7184-7185`). Its result is 5 checks and 0 failures (`receipts/runs/maap_integ.log`).
  - **#727 durations.** No new default suite enters with 696. `maap` already exists, and dev's `SUITE_SECONDS` already holds 696's figure, `"maap": 1375` (`scripts/suite_shards.py:166`). Its comment and `CI_WORKFLOWS.md:238-240` attribute that figure to this PR's run.
    - The self-test passes (`receipts/suite_shards_selftest.txt`).
    - The 5-way split I recomputed is the author's `parallel-selection.json`, set for set (`receipts/suite_shards_split.txt`).
    - The predicted worker seconds are 4,204, 4,205, 4,203, 4,205 and 2,877. `maap` is on worker 1. The bound is 4,320 s, 60 % of the 120-minute `timeout-minutes` (`receipts/shard_predict.txt`).
  - **#726 counter law with the 696 datapath.** `stream_counters.py --shape 1` and `--shape 8` both pass with rc 0 and 0 failures (`receipts/runs/counters.log`).
  - **The M8a ledger against 696's re-record.** The ledger arithmetic (`AREA_BUDGET.md:267`, `MARK_II_AREA_PLAN.md:831`) starts from the recorded 74 RAMB36 / 27 RAMB18 (87.5 tiles). 696's re-record changed no RAMB or DSP figure: the base..lane diff of `pp_resource_baseline.json` has no RAMB or DSP line. The `route-1x1` record still holds RAMB36 74 and RAMB18 27, so the composed arithmetic `87.5 - 6.5 + 6 - 18 + 54 + 2 = 125` stays valid.
  - **Composed reading.** I read the composed ledger pages (`AREA_BUDGET.md:236-300` and the plan's corresponding sections). The 696 record-identity sentences and the M8a 56-tile ruling text do not contradict each other.
  - **PR-body line references.** The body's references to `AREA_BUDGET.md:453` (D7) and `:530` (inherited Mark II movement) resolve to those rules at this head.
- **Register map.** Dev's `REGISTER_MAP.md` hunks (lines 148, 864, 911 and 955) contain no MAAP line, so the issue's no-register-map-change rule is untouched.

## 4. Executed evidence at this head

The simulator is the pinned Verilator 5.050 (`2026-07-01 rev v5.050`), run through a scoped wrapper. Its front-end script sha256 is `fb2cc573...` (the same identity R558-12 recorded) and its binary sha256 is `44898b22...`. GNU make is 4.4.1 and python3 is 3.14.7. The receipt is `receipts/toolchain.txt`.

Campaigns ran concurrently (`scripts/campaigns.sh` and `scripts/differential.sh`). Build and temporary outputs went to unpublished scratch only.

| Command | Result | Receipt |
|---|---|---|
| `make -C tb/verilator/maap` (unit + mutation campaign) | rc 0. `KL_maap: 186 checks, 0 failures`. Campaign `checks: 65 failures: 0`: 63 named rejections (each mutant rc 1 with its named `[FAIL]`) and 2 clean controls (`clean`, `m4_datapath_clean`) | `receipts/runs/maap_suite.log`, `.rc` |
| `make -C tb/verilator/maap integration-build` + run + `coverage` | rc 0. `MAAP integration: 5 checks, 0 failures`. `KL_maap.sv line 100.0% (225/225)`, gate PASS | `receipts/runs/maap_integ.log`, `.rc` |
| `python3 sw/firmware/ctrl/test/maap_differential.py --self-test` | rc 0. Clean: 12 tests, 0 failures. `differential mutants: 17/17 caught` | `receipts/runs/differential_excerpt.log` (bounded; the full-log sha256 is inside), `.rc` |
| `tb/verilator/milan_dp/stream_counters.py --shape 1`, `--shape 8` | rc 0. Both `RESULT: PASS`, failures 0 | `receipts/runs/counters.log`, `.rc` |
| `scripts/suite_shards.py --selftest` and `--shard i/5` for i = 0..4 | selftest PASS, rc 0. The split equals the author's | `receipts/suite_shards_*.txt`, `shard_predict.txt` |
| `scripts/ci_scope.py --selftest` | PASS | `receipts/static/ci_scope_selftest.*` |
| `scripts/docs_check.py` | 0 findings across 206 Markdown files | `receipts/static/docs_check*.{log,rc}` |
| `scripts/gen_toc.py --check` (pinned Markdown environment, `receipts/static/md_env.txt`) | OK, 146 pages | `receipts/static/gen_toc.*` |
| `scripts/check_em_dash.py --base e81ce82f` and `--base 26e2748f` | 0 findings over 347 lines in 7 pages, and 0 over 772 lines in 21 pages | `receipts/static/em_dash*.*` |
| `syn/ooc/pp_resource_gate.py check-baseline` | `baseline PASS: 3 endpoints` | `receipts/static/baseline.*` |
| `scripts/measure_test_evidence.py --check` | PASS, 66 <= 77 | `receipts/static/measure_evidence.*` |
| `scripts/check_py_idiom.py` | rc 0 | `receipts/static/py_idiom.*` |

- **Isolated mode.** The first `check-baseline`, `gen_toc` and `em_dash` attempts ran under isolated mode or without the Markdown renderer, and they refused to run. That was an environment refusal, not a gate result, and the reruns above are the results.
- **Clone integrity** (`receipts/head_integrity.txt`):
  - HEAD, the HEAD tree and the index tree are all `8eb5d868`;
  - porcelain, including ignored files, is empty after cleanup;
  - `diff-index HEAD` is clean;
  - all five gitlinks are as committed;
  - the three initialised submodules are clean, including ignored files;
  - `external` and `third_party/lwSRP` are uninitialised at their gitlinks, as before.

## 5. Author packet `author-r13`, spot-checked

- **Manifests.** The receipt manifest `merge-dev-e81ce82f-receipts/MANIFEST-01.sha256` verifies 530/530.
  - In the top-level `MANIFEST-merge-dev-e81ce82f.sha256`, `HANDOFF.md` differs. The publisher's `MANIFEST.json` records it as `path_redacted: true`, and its `original_sha256` (`896de3a8...`) equals the author's manifest entry.
  - Two comment drafts are listed but not published. They correspond to the posted REVIEW READY comment.
  - Neither point is an integrity defect.
- **Suite tally.** `native/parallel-tally.log` reports `checks: 2187183 in-suite failures: 0`, rc 0.
  - `parallel-results.json` gives five workers, each at head `313616d1`, each rc 0. Worker 1 (`maap`) took 2,768.2 s.
  - The inventory has 62 suites, `complete_disjoint_inventory: true`. Its shard sets equal my recomputation.
  - I did not rerun the full sweep, by the limits of this round.
- **Resource gates.**
  - The candidate route is 49,277 LUT / 53,419 FF / 15,779 slices, 74/27 RAMB, WNS +0.242 and WHS +0.017. It passes against the 50,013 record (`candidate-route-check.log`, rc 0).
  - Dev's route is 49,427 / 53,378, WNS +0.451 (`dev-route-check.log`, rc 0).
  - The delta is -150 LUT / +41 FF (`resource-comparison.json`).
  - The standalone 1x1 and 8x8 endpoints are unchanged, both rc 0.
  - The MAAP ceiling is 446 / 340, which is +7 / +60.
  - Each figure equals the PR body. The `aem_desc.bin` hashes for the candidate and dev 1x1 are equal (`4fc8d615...`), consistent with the body's memory-image claim.
- **Recorded limitations.** Both are acceptable, and both are stated in the PR body under "Known limitations":
  - **Builder gate 11.** This is the legacy `arty_current` estimator calibration, `sw/builder/test_builder.py:19268`, and it skips because the historical mf48 report is absent. Its source blob `eb800f22` is identical at the base, both parents and the head, and it is not claimed as passed.
  - **The earlier 10.56 GB peak.** It exceeded the requested 9 GB, with no OOM event (`final-provenance.json`: `oom 0`). It is an operational resource exception of the validation host. It is not a code or measurement defect, and the later guarded maximum was 8.51 GB.

## 6. Hosted CI at `313616d1` (read only; acceptance is the manager's)

Receipts: `receipts/hosted_runs.json` and `receipts/hosted_jobs_snapshot{1,2}.txt`, the second taken at 14:35Z.

- Runs: `elaborate` 38412310237, `docs` 38412309622, `rtl-fast` 38412310428 and `rtl-full` 38412310060. All four are pull_request runs at the exact head and all four are still in progress.
- **Executed and passed at snapshot:**
  - `changes`, `bdd-conformance`, `firmware-unit`, `verilator-lint` and `yosys-elaboration`;
  - the `firmware-control`, `firmware-aecp` and `firmware-srp` mutants;
  - `wire-accountability` and `docs-check-no-git`;
  - `full-ci-gate` and Yosys shards 0-3/4.
- **In progress:** Verilator shards 0-4/5, `elaborate`, `docs-check` and `publication-census`.
- **Skipped context:** `Physical gPTP (nightly and manual)`. It is a skip, not hardware proof.
- I conclude nothing from jobs still in progress.

## 7. Findings of this round

### R558-13-R1 - RESIDUE - Docs - PR #706 body, `:17-18`, `:98`, `:168` - the body still calls the pushed head unpublished

- **Evidence:** the PR's `headRefOid` is `313616d1...`, and hosted runs are executing at it. The body is byte-identical to the packet's `author-r13/PR-BODY.md`, and it still says:
  - `:17-18`: "Current local head: `313616d1...`. This is an unpublished update for PR #706.";
  - `:98`: "After publication of this head:";
  - `:168`: "New-head independent review, publication, hosted acceptance and the local workflow replica remain pending."
- **Why RESIDUE:** this is PR-body wording only. No figure, check, verdict, gate, clause claim or privacy rule changes.
- **Exact fix:**
  - `:17-18`: "Current head: `313616d1a18549d41907db389d378f0beb9bc543`, pushed as the PR #706 head."
  - `:98`: "At this head:"
  - `:168`: "New-head independent review, hosted acceptance and the local workflow replica remain pending; the head is pushed and hosted checks run at it."
- **Verification:** reread the body.

No BLOCKER, MAJOR, MINOR or SUGGESTION.

## 8. Prior public findings at this head (read after sections 2-7)

| Finding | State at `313616d1` | Evidence |
|---|---|---|
| R558-11-F1 (MINOR) and R558-11-R1 (RESIDUE), M5 wording | **Still resolved** | `MARK_II_AREA_PLAN.md` M5 lines carry the lane's text unchanged (the lane hunks are carried byte-for-byte, section 2). They are now at `:1099-1100` and `:1115` |
| R558-9-F1 (MINOR) and R558-9-R1 (RESIDUE), M2/M6 anchor; R558-5-F1 (MINOR), M0s anchor | **Still resolved** | The lane hunks are carried. The lines are now at `:696-697`, `:707`, `:952`, `:973` and `:656-657` |
| R558-1-F1, R558-3-F1 = R559-3-F1 (BLOCKER), R558-6-F1, R558-7-F1, R559-1-F1/F2/F3, R559-6-F1/F2 | **Still resolved** | Their artifacts are byte-identical to `26e2748f`. Campaign 65/0, integration 5/0, coverage 225/225, differential 12/0 with 17/17 |
| R558-2-R1 / R559-2-R1 (RESIDUE), plan `:66`, `:317`, M0 row | **Retained** | The text is unchanged. It is now at `:66`, `:317` and `:1129` (the "current three-endpoint record" row) |
| R558-5-R1 (RESIDUE), "records ... unchanged" lines | **Retained** | Unchanged, now at `AREA_BUDGET.md:372`, `:389` and plan `:669` |
| R558-10-R1 / R559-7-R1 (RESIDUE, PR body `32582421` / "need the pushed head") | **Superseded** | The rewritten body no longer contains either string. Its successor staleness is R558-13-R1 |
| Earlier SUGGESTIONs (R558-3/4/6/7/8, R559-1/3/4/5/6/7) | **Retained, optional** | No lens effect |

## 9. Lens results (artifact-specific)

```text
[R558] PASS Conformance - hdl/ieee1722/maap/KL_maap.sv (746be52d) and docs/design/MAAP_FABRIC.md byte-identical to 26e2748f (receipts/blob_identity.txt); receipts/runs/maap_suite.log 186/0 and campaign 65/0 with every Annex B M1-M8 named rejection; receipts/runs/differential_excerpt.log 12/0 and 17/17 - the Annex B behaviour reviewed POSITIVE at 26e2748f is carried unchanged by a conflict-free merge and its checks pass at this head
[R558] PASS RTL - merged milan_datapath.sv:7184-7185 (port_operational_i/realtime_ns_i wiring) elaborated with dev's #726 monitor RTL through integration.mk's milan_dp print-srcs derivation; receipts/runs/maap_integ.log 5/0; receipts/runs/counters.log 1x1/8x8 PASS; author candidate-route-check.log rc 0 (49,277 LUT, WNS +0.242) - no RTL hunk was resolved by hand, and the composed datapath builds and passes both lanes' checks
[R558] PASS Robustness - tb/verilator/maap/mutants.py at this head (blob 085989b7); receipts/runs/maap_suite.log - link-loss/return, clock, seed, busy-PROBE and truncation plants through the merged datapath are each rejected by name; dev changes neither eff_link_w nor ptp_now_w drivers (milan_datapath.sv unchanged by dev)
[R558] PASS Tests - scripts/suite_shards.py:166 maap 1375 s, receipts/shard_predict.txt (worker 1 = 4,205 <= 4,320) and suite_shards selftest PASS; receipts/merge_check_probe.txt (planted lane/dev line drops are detected); author-r13 native/parallel-tally.log 2,187,183/0 over the 62-suite disjoint inventory equal to my recomputed split; measure_test_evidence --check PASS - the merge keeps every MAAP check, campaign and duration, and the evidence I relied on can fail
[R558] PASS Docs - docs/design/AREA_BUDGET.md and docs/design/MARK_II_AREA_PLAN.md (receipts/merge_reconstruct.txt and conflict_file_hunks.txt: both sides' hunks byte-preserved; composed ledger AREA_BUDGET.md:236-300 read against the 74/27 record); docs_check 0 findings, gen_toc OK, check_em_dash 0 findings on both bases, check-baseline PASS; PR-body figures equal the author-r13 receipts - only RESIDUE R558-13-R1 (PR-body wording) is new, and earlier RESIDUE items are retained
```

## 10. Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `KL_maap.sv` and `MAAP_FABRIC.md` blob identity; MAAP unit, campaign and differential at this head | R558-13 | `313616d1a18549d41907db389d378f0beb9bc543` |
| RTL | CLEAN | Mechanical merge tree; merged datapath integration build with dev's #726 RTL; stream counters at 1x1 and 8x8; author route receipts | R558-13 | `313616d1a18549d41907db389d378f0beb9bc543` |
| Robustness | CLEAN | Mutation campaign plants through the merged datapath wiring; dev touches no MAAP driver | R558-13 | `313616d1a18549d41907db389d378f0beb9bc543` |
| Tests | CLEAN (earlier SUGGESTIONs retained) | `suite_shards` table, selftest, split and predictions; merge-check plants; author 62-suite tally; test-evidence ratchet | R558-13 | `313616d1a18549d41907db389d378f0beb9bc543` |
| Docs | CLEAN (RESIDUE R558-13-R1, R558-2-R1 / R559-2-R1 and R558-5-R1 retained for the residue checklist) | Both-side doc files hunk by hunk; composed ledger; docs, TOC, em-dash and baseline gates; PR body against receipts | R558-13 | `313616d1a18549d41907db389d378f0beb9bc543` |

## 11. Real limits

- **Not run:**
  - the full parent, PP, gPTP, Yosys and builder banks, and the full `milan_dp` suite;
  - the firmware banks, Vivado, act and the hosted runs;
  - hardware and the bench.
- **Source-head execution evidence** for those banks is the author's published `author-r13` receipts, and I only spot-checked them.
- **No manager source bank** runs at this exact head, and none is claimed or inferred.
- **The accepted `route-1x1` record** still describes `bee1b0d7`. The candidate and dev routes in `author-r13` are the author's measurements. I did not reproduce them.
- **Physical calibration was NOT RUN.** The `Physical gPTP` hosted context is skipped. Field skips are not hardware proof.
- **Hosted runs at this head were in progress** at the 14:35Z snapshot. Nothing is concluded from jobs still running.
- **Redaction:** host home-directory paths in the two MAAP logs are replaced with `<pinned-verilator-root>` / `<home>`. The Markdown environment path is replaced with `<md-venv>`. Nothing else was edited.

## 12. Pending manager duties

- The current-dev merge candidate (source base `c6bd08c6`, live dev `6c810c45`, which now carries B16 #725) and its builder and native banks, at the merge turn. This includes the composition of `docs/findings/README.md` with B16.
- Hosted and act acceptance at the exact head, including the five Verilator shards still running at the snapshot.
- Carrying R558-13-R1 and the retained RESIDUE items to the residue checklist.
- `scripts/suite_shards.py` keeps `maap` at its PR-run figure until a dev run measures it, per its own rule. That re-measurement falls after the merge.
- The external positive review and the maintainer's explicit merge authorization.

R558-13 FINISHED
