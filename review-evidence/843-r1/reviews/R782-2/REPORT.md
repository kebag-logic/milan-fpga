[R782] POSITIVE - exact head e079fe66a0cb9006ca718b06f57c23a85fc3582d

# R782-2 external independent review: PR #846 / issue #843

- Head `e079fe66a0cb9006ca718b06f57c23a85fc3582d`, tree `4f9cd735c47deaa5ec70f949e819fc235e506229`, verified in the review clone.
- Delta reviewed: `1105f545` (approved by R781-2 and R782-1) to `e079fe66`. That is the merge `04148cd7` of dev `1eb5289d`, with no rebase, and five first-parent commits after it.
- Live dev and the source base are both `1eb5289db8fc9d139ce90cad2e380b4515793806`, and it is the head's merge base.
- Not re-reviewed: #842, #849 and #847. Dev's first-parent history since round 1's base `cc204c6f` also carries #834 and #841 (`87e9d03a`, `3f6bef88`). I did not re-review those either; they matter here only as part of the dev side.
- Verdict: POSITIVE. No BLOCKER, MAJOR or MINOR is open. Two RESIDUE items and three SUGGESTIONs are listed below.
- The act at this head has not run. It stays open as a manager duty and is not a finding.

## What was checked, and the result

**(1) The eight conflict resolutions keep both sides' intent.** I replayed the merge with `git merge-tree` (`receipts/remerge_tree.txt`, `receipts/replay_merge.log`). Exactly these eight files conflict: `DOCUMENTATION_AUDIT.md`, `PNG_MANIFEST.json`, `submodule_boundaries.drawio`, `submodule_boundaries.png`, `SUBMODULES.md`, `fw_service_budget/oracle.json`, the `milan_dp` Makefile and the `milan_dp` README.

The merge commit differs from git's clean auto-merge in only those eight files and one more, `docs/reference/STRICTER_READINGS.md`. That ninth file is the semantic edit the commit message names. So every file that merged cleanly (the configs, the builder, `test_builder.py`, `rom_digests.tsv`, `sim_gptp.cpp`, `ENDSTATION_BUILDER.md`, CHANGELOG) is exactly git's 3-way result, and no later commit touches any of them.

How each conflict was resolved:
- **`SUBMODULES.md:24-25`:** gptp-processor is `1616fc8f` (from the branch) and protocol-processor is `92100657` (from dev). Both equal the head gitlinks. `check_submodule_docs.py` passes.
- **#843 adoption record in `SUBMODULES.md`:** it now follows #845's record and says "The processor stays at `92100657`". The donor guide links name `1616fc8f`.
- **`milan_dp/Makefile:1020` (`clean`):** it keeps both the branch's `gptp_lat_ucode.hex` and dev's `obj_bootsa`.
- **`milan_dp/README.md:91-93`:** dev's `obj_bootsa` row is kept byte-identical. The `obj_gptp` row is the branch's: dev left the base row unchanged, and the branch's version is the base row plus the #843 clause. The `obj_gptplat` row is also the branch's.
- **Generated files:** the merge took dev's side, then their own tools regenerated them (see item 2).
- **STRICTER_READINGS rows:** I checked them against `gptp-processor/hdl/ucode/gen_gptp_ucode.py:600-610`, which gives `PD_LATE_NS_C` = 15.006181 ms, and against `gptp-processor/tb/verilator/engine/sim_main.cpp:7730-7778`, where the deadline-instant trials age the port and then re-elect. Gate 26c exists at `sw/builder/test_builder.py:26643`.

Semantic check of the auto-merge, by execution at the head:
- `make -C tb/verilator/milan_dp gptp` passes 212/212 with `[CA] ... clockQuality 0xF822436A, expected clockAccuracy 0x22`.
- `gptp-lat` passes 212/212 with `0xF8FE436A, expected 0xFE`.
- Five builder gates pass: `test_all_configs_build`, `test_model_id_hashing`, `test_gptp_dataset_matches_engine_announce`, `test_gptp_clock_accuracy_per_board` and `test_image_identity_is_baked`.
- So dev's prototype identity (#842) and the branch's per-board clockAccuracy coexist in the configs and on the wire (`receipts/milan_dp_gptp*.log`, `receipts/builder_gates.log`).
- In `rom_digests.tsv` the rows are keyed per pin, and both pins' rows are present.

**(2) Every generated file at the head is exactly what its generator gives.**
- I ran `docs_inventory.py --write`, `submodule_boundaries.gen.py` and `timesync_chain.gen.py` in the clone. They wrote, and `git status --porcelain` stayed empty, so the head bytes are the generators' output (`receipts/regen_write_inplace.log`).
- The `--check` modes and `check_diagram_pngs.py` also pass (`receipts/gen_*.log`).
- `oracle.json` is byte-identical to `json.dumps(..., indent=2)+'\n'`, which is `gen_oracle.py`'s writer. Each of its three entries equals the published re-measured trace receipt (`service-budget/fw-*.json`) in every field `gen_oracle.convert` copies, and each raw log hashes to its `log_sha256` (`receipts/oracle_vs_receipts.log`).
- `make -C tb/verilator/fw_service_budget` at the head gives 55 checks and 0 failures; the flash checks pass too (`receipts/fwsb_head.log`).
- Probe: I put dev's oracle in place and re-ran. It is refused with `oracle image changed; rebuild and regenerate the trace fixture`, rc 2 (`receipts/fwsb_probe_devoracle.log`). So the oracle is bound to this tree's media.
- Against dev's oracle, graded rows move by at most 0.0391 ms on the 1x1 traces and by 0 on the 8x8 trace. The 8x8 trace's two `over-budget duty: milan_nvm` findings are dev's own.

**(3) Route table, best-of-three rule, floors and the re-record.**
- `scripts/check_evidence.py` parses every one of the six published route runs (head and dev, three directives each). It reads LUT, FF, slice, RAMB36/18 and DSP from `*-utilization_place.rpt`, the WNS/WHS of each signoff corner from `*-timing-design-tables.txt`, and routing errors from `*-route_status.rpt`.
- Every figure equals `route-figures.json` and the tables in `SUBMODULES.md`, `AREA_BUDGET.md`, `234_PP_SHADOW_AREA_BASELINE.md` and CHANGELOG (`receipts/check_evidence.log`).
- Under the rule (`docs/testing/PP_SHADOW_BASELINE_RECIPE.md:583`: best worst-corner WNS) the head's best is AltSpreadLogic_high at +0.242 ns and dev's best is ExtraTimingOpt at +0.234 ns.
- Best against best: +248 LUT, +159 FF, +17 slices and +2 DSP. Slow-corner WNS/WHS change by +0.008/+0.010 ns and fast-corner WNS/WHS by -0.170/-0.021 ns. All of these are recomputed from the raw reports.
- All 24 run-corners meet WNS >= +0.030 ns and WHS >= 0 ns. The worst are a WNS of +0.058 ns (head, ExtraTimingOpt) and a WHS of +0.012 ns (head, AltSpreadLogic_high, fast corners). There are 0 routing errors.
- Structured diff of `syn/ooc/pp_resource_baseline.json` from `1eb5289d` to the head (`receipts/baseline_diff.log`): only `route-1x1/measured` and `route-1x1/record` change (figures, flow directive, inputs digest and scopes). No tolerance, floor, ceiling or policy key changed, and `ooc-1x1` and `ooc-8x8` are untouched.
- Spot checks: the record's CARRY4 is 3726, matching the utilization report. Scope `u_pp` is 24222/19091 and `milan_datapath` is 44,631, matching the hierarchy report.
- The gate logs `rebaseline/check-before.log` (rc 1, LUT +692 and DSP +2 refused) and `check-after.log` (rc 0) match the docs.
- At the head, `check-baseline` passes and `--selftest` passes.
- The maintainer decision (issuecomment-6689115541) accepts the area growth of the mandatory lab fixes and names the gPTP pin. It requires the decision to be recorded in `AREA_BUDGET.md` and on the pin page, and a re-baseline through the gate if it refuses. All three were done.

**(4) The delta outside what dev brought is limited to this round's records.** `receipts/delta_1105_head_classes.txt` lists every file changed from `1105f545` to the head.
- 51 files equal dev's blob.
- The rest are either clean auto-merges of both sides or one of the following:
  - the 8 conflict resolutions and the STRICTER_READINGS edit;
  - the two diagram regenerations;
  - the `route-1x1` re-record;
  - the oracle re-measure;
  - the records commit `e079fe66`, which touches CHANGELOG, `AREA_BUDGET.md`, `MARK_II_AREA_PLAN.md`, the 234 page, the findings README and `SUBMODULES.md`.
- No source, RTL, builder or test file changes beyond what the merge brought. `git diff 1eb5289d HEAD -- hdl syn/ooc/pp_baseline.py syn/ooc/pp_resource_gate.py sw/litex protocol-processor` is empty. That backs the claim that the standalone `KL_pp_shadow` endpoints keep #845's records.

**Published evidence.** The publisher's `review-evidence/843-r1/MANIFEST.json` lists 472 author-r2 files.
- All 472 published sha256 values match the extracted bytes, and 20 of them are path-redacted (`receipts/publisher_manifest_check.log`).
- The route logs' digests in `route-head/large.sha256` equal those in the 234 page's run table.

**Comment rule.** The merge adds no source comment of its own; the only new comment lines in the delta's sources come from the round-1 side. No new lane label, review round or reviewer ID appears in a source comment.

## Findings

### N1 - RESIDUE - Docs - `docs/reference/SUBMODULES.md:670` ("It was measured at lane commit `a6d7cdf3`, the dev merge."); the same apposition is at `docs/design/AREA_BUDGET.md:13`, `:126`, `:193` and `:633`, and in `docs/findings/234_PP_SHADOW_AREA_BASELINE.md:51`
- Evidence: the merge commit is `04148cd7`. `a6d7cdf3` comes two commits later and adds only the two diagram regenerations (`git diff --stat 04148cd764 a6d7cdf3e2`: drawio, png, manifest). The measured synthesis inputs are the same, and the commit is named correctly by full SHA, so nothing measured or claimed changes.
- Required outcome (wording only): change "the dev merge" / "its merge of dev `1eb5289d`" to "on the merge of dev `1eb5289d`", or to "the merged tree after its diagram regenerations". The free-text `measured` note in `pp_resource_baseline.json` reads the same way. Changing that note is optional and needs no re-record.
- Verification: reading the changed text.

### N2 - RESIDUE - Docs - PR #846 body, "Sync with dev 1eb5289d" (line 63), and the HANDOFF list of what dev brought
- Evidence: the merge also brought #834 (`87e9d03a`) and #841 (`3f6bef88`); neither is an ancestor of `1105f545`. The body names only #842, #849 and #847. The tree docs are right, saying "Dev merged PRs #841 and #842 after the thirteenth".
- Required outcome (wording only): name #834 and #841 among the PRs dev brought. The merge commit's subject cannot change and is left as it is.
- This concurs with R781-3 W1, which is the same defect.

### S1 - SUGGESTION - Robustness, Conformance - `sw/builder/endstation_builder.py:3725` (`int(gp_raw.get("clock_accuracy", ...))`)
- R781-1 S1 and R782-1 S1, retained. The line is unchanged at this head.

### S2 - SUGGESTION - Docs - worst setup and hold paths in `docs/design/AREA_BUDGET.md:212-213`, `docs/findings/234_PP_SHADOW_AREA_BASELINE.md:120-122` and `docs/reference/SUBMODULES.md`
- R782-1 S2, retained. The path endpoints, 16 levels and 9.301/6.248 ns appear in no published receipt; the author-r2 receipts carry only summary timing tables. The full Vivado logs are bound by hash only.
- Optional: publish `report_timing` for the selected route's worst setup and hold paths.

### S3 - SUGGESTION - Docs (evidence packaging) - `review-evidence/843-r1/author-r2/receipts/INDEX.md`
- Three INDEX rows (`PR-BODY.md`, `review-ready.md`, `taken.md`) are not published as files. Their texts are the PR body and issue comments 6711665115 and 6714446317.
- Ten `scripts/*` rows disagree with the publisher manifest's `original_sha256` (`receipts/check_evidence.log`, `receipts/publisher_manifest_check.log`). So the index was written before those scripts' final edit.
- No figure depends on this: every route figure was re-derived from the raw reports.
- Optional: regenerate INDEX.md as the last step before publishing.

## Prior public findings on this PR, at this head
- **R781-1 F1 (MINOR, Docs; PR body Status and reproduction head): stays RESOLVED.** The live PR body's Status names `e079fe66` and merge base `1eb5289d`, and its checkout command is `git checkout --detach e079fe66...`.
- **R781-1 S1 / R782-1 S1 (SUGGESTION):** RETAINED as S1.
- **R782-1 S2 (SUGGESTION):** RETAINED as S2, now for the new worst path.
- **R781-2 W1 (RESIDUE, route and mutant figures bound to an older commit): SUPERSEDED.** The route is re-measured at `a6d7cdf3`, the docs name that commit, and the mutants were re-run at `e079fe66` (`mutants-e079fe66/`).
- **R781-2 W2 (RESIDUE, reviewers "to be named" in the PR body, lines 38-39): RETAINED.**
- I read the other findings published at this head (R781-3 W2, W3 and W5) after writing my draft (`DRAFT_VERDICT.txt`). I add nothing to them.

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN (S1 SUGGESTION) | Issue #843 items 1-4 and Acceptance; `STRICTER_READINGS.md:97-114` against `gen_gptp_ucode.py:600-610` and engine `sim_main.cpp:7730-7778`; on the wire, 0x22 and 0xFE in `[CA]` (`milan_dp_gptp*.log`); gate 26b/26c; decision comment 6689115541 against `AREA_BUDGET.md` and `SUBMODULES.md` | R782-2 | `e079fe66a0cb9006ca718b06f57c23a85fc3582d` |
| RTL | CLEAN | No RTL file in the delta (`git diff 1eb5289d HEAD -- hdl` empty; gitlinks `1616fc8f` and `92100657`). Route reports for all six runs: slices, DSP, corners, routing errors, floors (`check_evidence.log`); hierarchy attribution `hier-diff-*.md` | R782-2 | `e079fe66a0cb9006ca718b06f57c23a85fc3582d` |
| Robustness | CLEAN (S1 SUGGESTION) | Makefile `clean` union and the per-leg image wiring (`gptp_ucode.hex` from the AX7101 config, `gptp_lat_ucode.hex` from the Arty config); stale-oracle refusal probe (`fwsb_probe_devoracle.log`); baseline policy keys unchanged (`baseline_diff.log`) | R782-2 | `e079fe66a0cb9006ca718b06f57c23a85fc3582d` |
| Tests | CLEAN | Executed at the head: `milan_dp` gptp and gptp-lat (212/212 each), five builder gates, `fw_service_budget` (55/0 and flash), `pp_resource_gate.py check-baseline` and `--selftest`; oracle-to-receipt identity; author sweep and mutant receipts accepted as source-head evidence | R782-2 | `e079fe66a0cb9006ca718b06f57c23a85fc3582d` |
| Docs | CLEAN (N1, N2 RESIDUE; S2, S3 SUGGESTION) | Generators byte-exact (`regen_write_inplace.log`, `gen_*.log`); the `SUBMODULES.md` pin table and #843 record; `AREA_BUDGET.md`; 234 page; CHANGELOG; `MARK_II_AREA_PLAN.md:59,938-939`; `findings/README.md:25`; `milan_dp/README.md` rows; PR body | R782-2 | `e079fe66a0cb9006ca718b06f57c23a85fc3582d` |

## Limits
- I ran no full sweep and no full builder, PP, gPTP or Yosys bank. The sweep, behave, docs.yml, coverage and mutant results are the author's published source-head receipts, which I did not re-execute.
- I re-derived the route figures from the published Vivado reports. I ran no Vivado route. The full Vivado logs are bound by hash only.
- I did not re-run the service-budget re-measure, which takes 14 to 88 minutes per trace. The oracle is bound by receipt identity and by the media-binding self-test at the head.
- The builder run covered 5 of 109 gates.
- No manager source bank runs at this head, and I claim none.
- Physical calibration was NOT RUN. Field skips are not hardware proof.
- I did not judge hosted CI contexts.

## Pending manager duties
- The act local replica at this exact head (open).
- The current-dev merge candidate's builder and native banks at the merge turn.
- Hosted exact-head `rtl-fast`, `verilator-suites` and `yosys-portability` acceptance.
- Carrying N1, N2, R781-2 W2 and R781-3's residue items to the residue checklist.
- The release-build routing of the integrated image with every lab fix, which the maintainer decision requires before release (this route has not got #851's processor pin).

## Restore
- `receipts/restore_verify.txt`: the clone is back at `e079fe66` with tree `4f9cd735` and the index tree equal to it. `git status --porcelain --ignored` is empty.
- Gitlinks are `1616fc8f` (gptp-processor) and `92100657` (protocol-processor), both checked out clean.
- All build artifacts I created were removed.

R782-2 FINISHED
