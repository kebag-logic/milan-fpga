[R781] POSITIVE - exact head e079fe66a0cb9006ca718b06f57c23a85fc3582d

Round R781-3, internal cleared-context review of PR #846 / issue #843. Tree `4f9cd735c47deaa5ec70f949e819fc235e506229`. This is a delta review against `1105f545`, the head that R781-2 and R782-1 approved. Dev base and live dev are both `1eb5289d`.

## Verdict

- All five lenses were applied and all are CLEAN at this head.
- No BLOCKER, MAJOR or MINOR finding is open.
- Five RESIDUE wording items are open, all in the PR body or the hand-off page. Two SUGGESTIONs are open, both carried over from earlier rounds.
- The act run at this head is **not run yet**. It is reported as open, not as a finding (see "Pending manager duties").

## What I checked

### (1) The eight conflict resolutions keep both sides

I ran `git show --remerge-diff 04148cd7` against the automatic merge. Receipt: `receipts/remerge_stat.txt`. It shows the eight conflicts plus one semantic edit, `STRICTER_READINGS.md`.

- **`SUBMODULES.md`**
  - The pin table carries gptp `1616fc8f` and processor `92100657`.
  - The only dev lines that dropped are the `135afd04` pin row and the four `135afd04` donor-guide links, which `1616fc8f` replaces.
  - Dev's #845 record is intact.
  - The #843 record moved after it and now says "The processor stays at `92100657`".
- **Makefile `clean`**: the union of both sides (`gptp_lat_ucode.hex` and `obj_bootsa`).
- **milan_dp README**: dev's `obj_bootsa` row is there, and so are this branch's #843 clauses on `obj_gptp` and `obj_gptplat`.
- **Dev's `bootsa` leg**: `gen_boot_fw.py:160` builds its gPTP program without `--clock-accuracy`. The generator default is `0x22` (`gptp-processor/hdl/ucode/gen_gptp_ucode.py:25,545`), which is what the AX7101 config states. No change is needed.
- **Generated files**: `DOCUMENTATION_AUDIT.md`, the diagram `.drawio`/`.png`, `PNG_MANIFEST.json` and `oracle.json` took dev's side in the merge and were then regenerated (see (2)).
- **`STRICTER_READINGS.md`** (from #842):
  - The gPTP rows now state the pinned behaviour.
  - `PD_LATE_NS_C` is at `gen_gptp_ucode.py:606`, and 15006181 is asserted at `gptp-processor/tb/verilator/engine/sim_main.cpp:734`.
  - Builder gate 26c is at `test_builder.py:26613,26643`.
  - This meets issue item 4.
- **Configs**: all five auto-merged configs carry dev's #840 MAC and this branch's `clock_accuracy`: AX7101 `0x22`, Arty `0xFE`.

### (2) Every generated file is exactly what its generator gives

I ran each generator in this clone at the head. Receipts: `receipts/gen/`.

- `docs_inventory.py --check` and `--write`, `submodule_boundaries.gen.py --check` and regenerate, `timesync_chain.gen.py --check` and regenerate, `check_diagram_pngs.py` and `check_submodule_docs.py` all exit 0.
- After the regenerations `git status --porcelain` is empty, so every output is byte-identical, PNGs included.
- **ROM ledger**: the `1616fc8f gptp_ucode.hex` row equals the sha256 of the donor's tracked `tb/verilator/ucpu/gptp_ucode.hex`. Both processor rows are present.
- **Service-budget oracle**:
  - All three `oracle.json` rows match the published fixture receipts field by field: raw_log, log_sha256 (recomputed), media, rows, budget_findings, heartbeat and liveness. Receipt: `receipts/oracle_vs_receipts.log`.
  - `run.py --self-test` passes at the head: 55 oracle checks and 14 flash checks, 0 failures. Receipt: `receipts/fw_service_budget_selftest.log`.

### (3) Route table, comparison rule, floors and re-record

- **Figures**: `rederive_routes.py` re-derives all six routes from the raw Vivado receipts. It parses the per-corner timing tables, the utilization report and the route status without using `route-figures.json`. Receipt: `receipts/rederive_routes.log`.
  - Every figure in the `AREA_BUDGET.md:203-209`, `SUBMODULES.md` (#843 record), `234_PP_SHADOW_AREA_BASELINE.md` (new section), CHANGELOG and PR tables matches.
  - Every route has 0 routing errors and rc 0.
- **Floors**: every corner of all six routes meets +0.030 ns WNS and 0 ns WHS. The worst is head ExtraTimingOpt at +0.058 / +0.031 ns.
- **Comparison rule**: the best of three was compared against dev's best (the 2026-10-30 rule, A10 comment 6681870221).
  - Head AltSpreadLogic_high is +0.242 ns; dev ExtraTimingOpt is +0.234 ns.
  - The deltas follow: +248 LUT, +159 FF, +17 slices, +2 DSP, +0.008 / +0.010 ns slow and -0.170 / -0.021 ns fast.
  - The hierarchy diffs give `u_engine` +469 / +475 / +469 LUTs, +166 FF and +2 DSP on each directive.
  - The run-log hashes and minutes in the findings page match `route-head/large.sha256` and the rc seconds.
- **Gate**:
  - `check-before` rc 1: +692 LUT against 500 and +2 DSP against 0.
  - `record-write` rc 0.
  - `check-after` rc 0.
  - `check-baseline` rc 0.
  - The dev route against the thirteenth record: rc 0.
- **Re-record**: `baseline_delta.py` compares dev's `pp_resource_baseline.json` with the head's (`receipts/baseline_delta.log`).
  - Only `/endpoints/route-1x1/{record,measured}` leaves differ.
  - `tolerance`, `floor` and `ceiling` are untouched, as are `ooc-1x1` and `ooc-8x8`.
  - The note's deltas are correct: +172 FF, -1 slice, WNS -0.131 ns, WHS 0.000 ns.
- **Provenance**: the route ran at `a6d7cdf3`. Since then only docs, `pp_resource_baseline.json` and `oracle.json` changed (`receipts/after_route_commit_files.txt`), so no synthesis input moved.
- **Standalone records**: keeping #845's standalone records holds up. Branch against dev changes no HDL and no processor gitlink (`receipts/branch_vs_dev_files.txt`).
- **Dev PRs after the thirteenth record**: dev merged #841 and #842 after it (first-parent history of `87e9d03a..1eb5289d`), as the docs say.

### (4) Changes outside what dev brought

- `git diff 1105f545..e079fe66` outside dev's own content is:
  - the eight resolutions and the stricter-readings edit in the merge commit;
  - five post-merge commits that touch only CHANGELOG, `AREA_BUDGET.md`, `MARK_II_AREA_PLAN.md`, the diagram and its manifest, the findings page and index, `SUBMODULES.md`, `pp_resource_baseline.json` and `oracle.json` (`receipts/postmerge_stat.txt`).
- These are all records of this round.
- No code or test changed outside the merge.
- **Comment rule**: the delta adds no source comment with a lane label, lane name, review round or reviewer ID. The issue-comment links that were added are in docs, not source.

### Author's head evidence (spot-checked, not re-run)

- **Sweep**: four shards at `e079fe66`, each exit 0, 65 of 65 suites. The checks total 2,192,509, which equals the PR's figure.
- **Final gates**: every rc is 0, with the tree clean after the run.
- **Mutants**: all eight caught by name at `e079fe66`.
- **Docs workflow**: run on every step.

## Findings

### S1 - SUGGESTION - Docs - worst-path detail has no public receipt (retains R782-1 S2 at this head)

- **Where**: `docs/design/AREA_BUDGET.md:211-212`, `docs/findings/234_PP_SHADOW_AREA_BASELINE.md:119-122`, and the PR body, line 112 of the body.
- **Evidence**: this delta adds new path figures:
  - setup `milansoc_sdram_bankmachine6_row_reg[5]` to `twtrcon_ready_reg`, 16 levels, 9.301 = 3.053 + 6.248 ns;
  - hold `milansoc_rdat1_reg[2]` to `storage_43_reg`.
  
  No published receipt contains them. The timing tables are summaries, and the only binding is the hash of the unpublished `aslh-baseline.log` in `route-head/large.sha256`.
- **Impact**: a cold reviewer cannot disagree with these figures. They feed no gate or verdict.
- **Optional outcome**: publish the selected route's worst setup and hold `report_timing` excerpt on the evidence branch. No head change is needed.

### S2 - SUGGESTION - Robustness, Conformance - `sw/builder/endstation_builder.py:3725` (retains R781-1 S1 / R782-1 S1)

`int()` coercion of `gptp.clock_accuracy`. The line is unchanged by this delta: the builder's diff from `1105f545` is dev's identity warnings, and none of it touches `clock_accuracy`.

### W1 - RESIDUE - Docs - PR #846 body, line 62: incomplete list of what dev brought

- **Problem**: the body says dev brought #842, #849 and #847. The merge also brought #834 (`87e9d03a`) and #841 (`3f6bef88`), and #841's transmitter hold is a synthesis input in the route difference.
- **Exact fix**: "(dev: #834 owned-process cleanup, #841 transmitter hold, #842 prototype identity and 1000BASE-T only, #849 audit without line counts, #847 processor `92100657`)".

### W2 - RESIDUE - Docs - PR body lines 27, 92 and 168: "F1, F2 and F3" is never defined

- **Problem**: the body uses "F1, F2 and F3" without saying what they are.
- **Exact fix**: on first use, name each lab fix with its PR or pin, for example "F1 (#847, processor `92100657`), F2 (...), F3 (FPGA-gPTP `1616fc8f`)", or write "both lab-fix pins".

### W3 - RESIDUE - Docs - PR body route section (lines 94-112): the measured commit is not named

- **Problem**: the "this PR" columns do not say which commit was measured. This is the same pattern as R781-2 W1. The tree docs do bind it.
- **Exact fix**: in line 94, after "one route at a time", add "measured at `a6d7cdf3`, the dev merge; later commits change no synthesis input".

### W4 - RESIDUE - Docs - PR body lines 37-38: reviewers still "to be named" (R781-2 W2, retained)

- **Exact fix**: name the internal and external reviewer identities.

### W5 - RESIDUE - Docs - hand-off page does not explain a failed oracle attempt

- **Where**: evidence branch `review-evidence/843-r1/author-r2/HANDOFF.md`, row 57.
- **Problem**: the published receipt `receipts/service-budget/gen_oracle-lane.log` records rc 1 ("stale or unbound fixture build"), and the hand-off does not account for it.
- **Exact fix**: add one sentence saying that the lane-tree attempt failed its build binding and was superseded by the clean-clone run (`gen_oracle.log`), whose output is the committed `oracle.json`.

## Prior public findings at this head

- **R781-1 F1 (MINOR, Docs)**: stays resolved. The Status line names `e079fe66` and merge base `1eb5289d`.
- **R781-2 W1 (RESIDUE)**: superseded. Mutants were re-run at `e079fe66`. The route-binding half recurs as W3.
- **R781-2 W2 (RESIDUE)**: retained as W4.
- **R781-1 S1 / R782-1 S1 (SUGGESTION)**: retained as S2.
- **R782-1 S2 (SUGGESTION)**: retained and extended as S1.

## Lens results

- [R781] PASS Conformance - `configs/endstation_*.yaml` `clock_accuracy`, `docs/reference/STRICTER_READINGS.md` gPTP rows against `gen_gptp_ucode.py:25,545,606` and `engine/sim_main.cpp:734`, `gen_boot_fw.py:160` default, maintainer decision 6689115541 and issue #843 Acceptance against the route receipts - per-board clockAccuracy kept through the merge, issue item 4 met, area recorded against dev under the decision.
- [R781] PASS RTL - `receipts/branch_vs_dev_files.txt`, the remerge diff and `receipts/rederive_routes.log` - the delta changes no HDL or processor gitlink. Six routes have 0 routing errors and meet the floors at every corner, and the growth is localised to `u_engine` by the hierarchy diffs.
- [R781] PASS Robustness - Makefile `clean` and `bootsa`/`gptp`/`gptp-lat` image wiring at the head, the `gen_boot_fw.py` gPTP options, the merged configs - no auto-merge interaction leaves a leg on the wrong image or value. S2 is a SUGGESTION.
- [R781] PASS Tests - `receipts/oracle_vs_receipts.log`, `receipts/fw_service_budget_selftest.log`, the author's `sweep-e079fe66/shard-*/complete.json` and `mutants-e079fe66/mutants.json` - the oracle was re-measured rather than hand-edited, and the self-test passes. 65/65 suites ran at the head, and all eight mutants are caught at the head.
- [R781] PASS Docs - `receipts/gen/*` (byte-exact regeneration, porcelain empty), `receipts/baseline_delta.log`, `AREA_BUDGET.md:126-213`, the `SUBMODULES.md` #843 record, the `234_*` new section, CHANGELOG and `MARK_II_AREA_PLAN.md:59,939` against the route receipts - figures match. Only RESIDUE W1-W5 and SUGGESTION S1 remain.

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | configs, STRICTER_READINGS gPTP rows, gPTP generator defaults, maintainer decision, issue Acceptance | R781-3 | `e079fe66a0cb9006ca718b06f57c23a85fc3582d` |
| RTL | CLEAN | branch-vs-dev file list (no HDL), six route receipts re-derived, hierarchy diffs | R781-3 | `e079fe66a0cb9006ca718b06f57c23a85fc3582d` |
| Robustness | CLEAN (S2 SUGGESTION) | milan_dp Makefile/README resolution, bootsa gPTP options, merged configs | R781-3 | `e079fe66a0cb9006ca718b06f57c23a85fc3582d` |
| Tests | CLEAN | oracle against receipts, fw_service_budget self-test, author sweep and mutants at head | R781-3 | `e079fe66a0cb9006ca718b06f57c23a85fc3582d` |
| Docs | CLEAN (W1-W5 RESIDUE, S1 SUGGESTION) | generators byte-exact, baseline delta, AREA_BUDGET, SUBMODULES, 234 page, CHANGELOG, MARK_II, PR body | R781-3 | `e079fe66a0cb9006ca718b06f57c23a85fc3582d` |

## Real limits

- I did not re-run the sweep, the builder bank, mutants, Vivado, Yosys or the service-budget re-measure. For those I relied on the author's published receipts, which I spot-checked.
- I did not re-run the ROM digest recorder. I checked the ledger rows by hash instead.
- The worst-path figures (S1) cannot be verified from public evidence.
- Physical calibration was not run, and field skips are not hardware proof.
- I ran no manager source bank and claim none.

## Pending manager duties

- The act run at this exact head (not yet run).
- Hosted contexts at this head. Several were still queued or in progress when I looked; "Physical gPTP" was skipped.
- The current-dev merge candidate's builder and native banks, at the merge turn.
- Carrying W1-W5 to the residue checklist.

R781-3 FINISHED
