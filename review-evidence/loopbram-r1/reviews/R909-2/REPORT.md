[R909] NEGATIVE - exact head dc78aedae34c25a97125ecd6816a1f645db5575f

# R909-2: internal independent delta re-review of PR #987 (issue #979)

- Head `dc78aedae34c25a97125ecd6816a1f645db5575f`, tree `41223b89427673df91715a56a7e8a647d9a339e4`. Branch `pf-loopbram-1` into `dev-soft-core`.
- Delta reviewed: `2e278379c1..dc78aedae3`, six commits (rounds 3 and 4). Implementation base: `3cda030c17`.
- Context was rebuilt from public material only, in this order: AGENTS.md and CONTRIBUTING.md; docs/README.md; the issue #979 body and its option-B ruling; Milan v1.2 5.3.3.8 and 5.4.2.26-28 as cited; the base-to-head and delta diffs; the published `review-evidence/loopbram-r1` packets `author-r3` and `author-r4`.
- I wrote my own findings before reading the earlier R909-1 and R910-1 findings. I did not read any other reviewer report for this round, any private author material or the management tree.
- No source edits, commits, pushes or GitHub writes were made. I did not run Docker/act, any full bank, hardware or sub-agents.

## Verdict summary

The rounds 3+4 delta closes every earlier finding at its cause, and I re-derived each closure myself:

- **R909-1-F2:** the canonical disabled release-top netlists match base and head at both shapes. The only difference is the generated CPU wrapper's module name, which comes from the export inputs, not the RTL.
- **R909-1-F1:** every mutation arm is re-anchored and still armed. The render-queue campaign passes 28/28 at this head.
- **R909-1-F3 / R910-1-F1:** the parent integration controls pass at both sizes. Both parent connection plants fail at runtime, at 8x8 and also at 1x1, which I probed myself.
- **F5 and F6:** the bounds probes pass at both shapes.

The verdict is **NEGATIVE** for one new BLOCKER and two MINORs:

- **N1 (BLOCKER):** the two new Verilator suites are missing from the suite-duration table. As a result `scripts/suite_shards.py --selftest` fails at this head. CONTRIBUTING's mandatory local sweep `scripts/run_all_suites.sh` aborts in preflight, and the hosted shard-ownership step cannot pass. The base passes.
- **N2 (MINOR):** the enabled 8x8 route was last run at `855529fe`. That commit is functionally equivalent to this head but is not this head.
- **N3 (MINOR):** the parent plant campaign is missing from the explicit-campaign registry.

## New findings at this head

### N1 - BLOCKER - Tests, Docs - the two new suites are not in `SUITE_SECONDS`, so the suite planner's self-test and every CI shard selection fail

- **Where:**
  - `scripts/suite_shards.py:78-135`: the `SUITE_SECONDS` table has no `input_loopback` or `input_loopback_dp` entry.
  - Those suites are discovered from `tb/verilator/input_loopback/Makefile` (added in round 2) and `tb/verilator/input_loopback_dp/Makefile` (added in this delta, `c9c6e5ff`). Discovery is `discover_suites()`, `scripts/suite_shards.py:216-222`.
- **Authority:**
  - The `scripts/suite_shards.py` docstring says: "New suites must enter both the discovered inventory and duration table."
  - CONTRIBUTING.md (the two long aggregates) requires `scripts/run_all_suites.sh "$suite_logs"` locally before the PR is marked validated.
  - AGENTS.md section 7 requires the local gates to pass.
- **Evidence (reviewer-run at this head and at the base):**
  - `receipts/suite_shards_selftest_head.txt`: `selftest: 2 FAILURE(S)`. The failures are `input_loopback` and `input_loopback_dp`, each "inventory suite with no recorded duration in SUITE_SECONDS", and the exit code is 1.
  - `receipts/suite_shards_selftest_base.txt`: the base passes, exit code 0.
  - `receipts/ci_pieces_list_head.txt`: `scripts/run_all_suites.sh --ci-pieces --shard 0/19 --list` exits 2 with the same error. The base exits 0 (`receipts/ci_pieces_list_base.txt`).
  - `scripts/run_all_suites.sh:303-307` runs that self-test as a preflight and aborts with exit 2 when it fails. The mandatory local sweep therefore cannot start at this head. I did not run the sweep itself, because the abort predicate is shown directly.
  - `.github/workflows/rtl.yml:256` ("Prove specialized suite ownership", in every `verilator-shards` job) runs the same self-test, so the hosted `verilator-suites` aggregate cannot pass. `rtl.yml:516` (the physical leg) does the same.
  - There are no hosted runs or check runs at this head yet (`check-runs total_count 0`), so no hosted context contradicts or confirms this.
- **Impact:**
  - The required local and hosted Verilator gates are red at this head. Both new suites also run in neither sweep.
  - The PR body's "All requested regression and portability gates pass" omits that the mandatory sweep cannot start.
  - Earlier rounds missed this because the evidence ran suites one at a time (`make -C ...`) and never ran the sweep.
- **Required outcome:**
  - Register both suites in `SUITE_SECONDS`, following the docstring's new-suite steps: a provisional `suite_timeout` figure, and a worker check against the 60-percent bound.
  - Re-run `python3 scripts/suite_shards.py --selftest` and the complete local sweep (`scripts/run_all_suites.sh`) at the new head, and publish those receipts.
  - Correct the PR body's gate claim.
- **Verification:**
  - The self-test exits 0.
  - `--ci-pieces --shard i/19 --list` exits 0 for every i, and each new suite is owned exactly once.
  - The sweep's tally includes both suites.

### N2 - MINOR - Conformance, RTL - the enabled 8x8 route is not exact-head evidence

- **Where:**
  - Issue #979 acceptance: "Routing: both shapes routed at #818's timing floor."
  - `author-r4/REVIEW-READY.md`: "The enabled 8x8 route is not repeated in this round."
- **Evidence:**
  - The last enabled 8x8 route is at `855529fe` (`author-r3`, AltSpreadLogic_high: +0.295 ns setup, +0.036 ns hold). Its four signoff reports are published (`author-r3/receipts/route--endstation_ax7101_8x8--gateware--AltSpreadLogic_high--*`).
  - From `855529fe` to this head, the RTL delta (`68d17a98`) packs the enabled ports into existing buses. It also moves invalidation into the enabled generate branch.
  - I checked the new invalidation predicates against the old writers. `edit_change_w` (`hdl/milan/milan_datapath.sv:5176-5178`) equals the enclosing `!pp_amap_edit_req_w / amap_edit_beat_w / phase 5 / context && in_change` nest of the store write (`:5285-5299`). The direct-write and restore predicates equal their old writers, the register timing is the same and the reset value is still 1. So the enabled logic is intended to be equivalent.
  - However, the enabled 1x1 route with the same directive (ExtraTimingOpt) moved from +0.228 ns (`855529fe`) to +0.124 ns (this head). An equivalent-intent repackaging therefore shifted slack by 0.10 ns.
  - The 8x8 margin above the floor was 0.265 ns. The 8x8 route is likely still closed, but that is not demonstrated.
- **Impact:** a frozen acceptance criterion has no evidence at the merge head for one of its two shapes. I judge that a route is owed. The S14 control-memory debt does not remove that duty, because the earlier rounds already routed through the measurement export.
- **Required outcome:** either one of these:
  - route enabled 8x8 at an `hdl/`-identical successor of this head, using the measurement export (the allocator refusal stays as recorded S14 debt), and publish the four-corner signoff; or
  - publish an explicit owner ruling that the `855529fe` route stands for this head.
- **Verification:** WNS >= +0.030 ns and WHS >= 0 at every corner, with zero failing endpoints and zero routing errors, on a head whose `hdl/` matches the merge candidate.

### N3 - MINOR - Tests, Docs - the parent plant campaign is not in the explicit-campaign registry

- **Where:** `docs/testing/TESTING.md:353` registers `make -C tb/verilator/input_loopback` and the leaf `mutants.py` only.
- **What is missing:** the parent controls (`make -C tb/verilator/input_loopback_dp`) and the parent plant campaign (`python3 tb/verilator/input_loopback_dp/mutants.py --output ...`) are named nowhere in the testing authority. These are the checks that close R909-1-F3 / R910-1-F1.
- **Authority:** `docs/testing/TESTING.md:344-348`: "A long mutation campaign is an explicit target ... this page keeps the list of such targets."
- **Impact:**
  - A later change to the parent map writers or the invalidation predicates in `milan_datapath.sv` has no documented duty to run the only plants that detect a broken parent connection.
  - Once N1 is fixed, the suite runs the controls only, not the plants.
- **Required outcome:** a TESTING.md row naming the parent plant campaign and who runs it. That includes changes to the `milan_datapath.sv` map writers, `g_input_invalidation`, or the queue/capture packed fields.
- **Verification:** documentation diff, with the docs gates green.

### R1 - RESIDUE - Docs - `tb/verilator/input_loopback/README.md:17`

- **Text:** "bind flush" is listed among the covered scenarios.
- **Why it is residue:** the same file says, at lines 52-55, that the bind-only flush term is one of the five untested guards. This is wording only; no test, figure or verdict changes.
- **Exact fix:** replace "bind flush" with "bind flush together with map invalidation (the bind-only term is untested; see below)".

### S1 - SUGGESTION - Tests - `tb/verilator/input_loopback_dp/mutants.py:24-31`

- The two parent connection plants run at 8x8 only, and the two queue retention plants at 1x1 only.
- My probe (`scripts/parent_plant_probe.py`) shows that both connection plants are also detected at 1x1:
  - `disconnected_map`: 3391 PARENT_SAMPLE failures, `receipts/runs/parent_1x1_disconnected_map.json`;
  - `missing_edit_invalidation`: 124 failures, `receipts/runs/parent_1x1_missing_edit_invalidation.json`.
- Adding the 1x1 arms (about one minute each) makes "both sizes" part of the campaign itself.

### S2 - SUGGESTION - Docs, Tests - canonical-hash reproducibility (`author-r4/receipts/canonical.py.txt`)

- LiteX names the CPU wrapper `VexiiRiscvLitex_<md5 of generation inputs>`. My base and head exports used different directories and produced different names.
- As a result, my raw canonical hashes do not reproduce the published ones:
  - 1x1: mine base `25db0f2f...`, head `4b690ebe...`, published `18af89e6...`;
  - 8x8: mine base `c810c476...`, head `457ef479...`, published `fe344bba...`.
- They differ only in that identifier, at 12 lines per shape. After normalizing it, base equals head, and the author's published 1x1 chunks equal my head (`receipts/f2_compare.json`).
- Suggested fix: normalize that one name in the recipe, or state that hash equality requires identical export inputs.

### S3 - SUGGESTION - Tests - `tb/verilator/input_loopback_dp/run.py:34-38`

- The parent harness elaborates `milan_datapath` at its default `MILAN_CLK_FREQ_HZ` of 100 MHz. Both release shapes export with `--milan-clk-freq 50e6`.
- So `FULL_WALK_DEADLINE` (`sim_main.cpp:478`, `< 2083`) tests the 100 MHz budget. At the release clock the budget is 1041 cycles.
- The real margin is still positive: an 899-cycle walk at the generated 8x8 geometry, and 873 measured. The leaf bounds run at 49.152 MHz covers the stamp window.
- An extra parent run at the release clock would bind both bounds at the product frequency.

### S4 - SUGGESTION - RTL - `hdl/ieee1722/aaf/KL_render_queue.sv:821`

- On the `copy_done_w` cycle (`cursor_r == INPUT_CH_P`), `entry_w` indexes key `INPUT_FIRST_P + INPUT_CH_P`. That is key 64 of a 64-key map, or 16 of 16, which is one past the map.
- `copy_stream_w` then drives `ra_w` and `fl_rd_w` for that one cycle. The read result is unused, because `return_r` is low on the next cycle, so the behaviour is harmless.
- Clamping the index would remove the out-of-range select.

## Earlier findings: disposition at this head (read after my own pass)

| Finding | Disposition | Evidence at this head |
|---|---|---|
| R909-1-F1 BLOCKER (disarmed arms) | **RESOLVED** at cause | My anchor probe (`scripts/anchor_probe.py`, `receipts/anchor_probe.json`) covers all 25 mutation drivers that target the changed RTL: no anchor lost (`ANCHOR-DRIVERS-WITH-FEWER-ANCHORS 0`). Each changed arm is re-anchored one-for-one, with count 1 at head; the base literal has count 1 at base. Re-anchored arms: `render_queue/mutants.py` "a bind wipe ignored" (`flush_w`) and "lead_o kept" (`&& !copy_active_w`); `capture_coherence` TBASE and `tdm_walk_ns_o[31:0]`; `tdm8_render_mutants` `rq_tdata_w[63:0]`. Each still plants the same defect, and in the disabled harnesses `flush_w == flush_i`. `milan_dp/render_mutants.py` ("a PHC step resets the stage") is byte-identical to base and its anchor counts 1 at head. `make -C tb/verilator/render_queue all` at head: run 39/0, odd 38/0, `28 checks: 28 PASS, 0 FAIL`, including "a bind wipe ignored" caught (`receipts/runs/render_queue_all.log`). I did not run the `milan_dp` suite (not allowed); its arm is armed by count. |
| R909-1-F2 MAJOR (disabled growth) | **RESOLVED**, re-derived | `scripts/f2_prepare.py` and `scripts/f2_elaborate.py` re-ran the stated recipe at base and head: builder → platform firmware link → SoC export → `synth_design -rtl` → `write_verilog` → canonicalize. After normalizing the CPU wrapper name, base equals head at both shapes: 1x1 `bbfe2ac8...`, 8x8 `368cd18e...`, 0 other differing lines (`receipts/f2_compare.json`). The CPU wrapper netlists are byte-identical modulo name. Builder outputs (12 files per shape), `ctrl_app.elf`, ROM/mem init files, xdc, `csr.json` and the descriptor image are byte-identical, and the export argv is identical modulo tree path (`receipts/f2_inputs.txt`). The disabled LUT/FF/BRAM/DSP equality is the author's (`author-r4/receipts/disabled-summary.json.txt`); it follows from netlist identity. The generate split is checked by reading: all optional state, the 8-page RAM, invalidation and the capture read FSM sit in the `g_input_*` enabled branches, and the disabled branches assign constants only (`KL_render_queue.sv:782-939`, `KL_chan_map_capture.sv:1376-1426`, `milan_datapath.sv:5174-5196`). |
| R909-1-F3 MAJOR / R910-1-F1 MAJOR (no parent integration) | **RESOLVED** | I re-ran `tb/verilator/input_loopback_dp/mutants.py` at head with pinned Verilator 5.050. control1 passes: 4248 words, 88 packets, max walk 89, first_eligible 5. control8 passes: 34004 words, 704 packets, max walk 873, first_eligible 5. All four plants are built and fail `PARENT_SAMPLE` (`receipts/runs/parent_plants_results.json`). Scenarios covered: production AECP core with ADD, REMOVE, replacement (REMOVE then ADD) and an idempotent ADD (no invalidation); rejected BAD_ARGUMENTS with no commit (`sim_main.cpp:520`); GET_AUDIO_MAP on both pages of 8x8 port 0 (`:551`); boot clipping writer; an edit aligned inside the copy (`:704`); all destinations concurrent (`:710`); every transmitted packet graded per stream. "Both sizes" for the connection plants is shown by my 1x1 probes (S1). |
| R909-1-F4 MINOR (five guards) | **RESOLVED** by its permitted second outcome | F4 allowed "record these guards as untested defence in depth in the README and the design document". Both do so: `tb/verilator/input_loopback/README.md:52-55`, `docs/design/INPUT_MAPPED_LOOPBACK.md:426-429`, and `hdl/ieee1722/aaf/README-parameters.md:101`, where the earlier replay claim is replaced. The wording left at README:17 is R1 (RESIDUE). This is not an open MINOR. |
| R909-1-F5 MINOR (lead > 2) | **RESOLVED** | `KL_render_queue.sv:782` refuses `KMIN_C > 2`, and there are now 8 sample pages (`:797`) with the full claimed page address. My `bounds.py` run: lead3 refuses at elaboration at both shapes (`receipts/runs/bounds_results.json`). The parent `overwritten_capture_page` and `truncated_claim_page` plants fail. |
| R909-1-F6 MINOR (stamp window) | **RESOLVED** | The window is derived at `KL_render_queue.sv:817-819`, with the derivation documented at `:847-850` and in both READMEs: four clock cycles, 1000 ppm across `KMIN_C+1` periods, and 1 ns. My `bounds.py` run at both shapes: control pass, inside (84 ns jitter plus 1000 ppm) pass, outside (87 ns) fails `COPY_SAMPLE`. |
| R909-1-F7 MINOR (stale banners) | **RESOLVED** | Updated banners: `KL_chan_map_capture.sv:338-346` (walk budget with `2 * INPUT_LOOPBACK_P`, 930/899); `KL_render_queue.sv:66-74` (copy before scrub), `:130-133` (enabled clock-loss flush) and `:138-139` (FLUSH). The packed fields are in `hdl/ieee1722/aaf/README-parameters.md:81-88`. |
| R909-1-R1 / R2 / R3, R910-1-R1 (RESIDUE) | **RESOLVED** | Author label removed (`INPUT_MAPPED_LOOPBACK.md:7`); off-tree pointers now link PR #987; builder row 16g follows 16e (`docs/ENDSTATION_BUILDER.md:1116-1117`); the stale sentence is replaced (`INPUT_MAPPED_LOOPBACK.md:107`). |
| R909-1-S1 (SUGGESTION) | **RESOLVED** | The PR body and `sw/builder/README-parameters.md:129-132` disclose the layout-3 NAME capacity for split builds. |

## Lens results (artifact-specific)

```text
[R909] BLOCKER Tests, Docs — scripts/suite_shards.py:78-135; tb/verilator/input_loopback{,_dp}/Makefile — N1
[R909] MINOR Conformance, RTL — issue #979 Routing acceptance; author-r4/REVIEW-READY.md; author-r3 8x8 signoff reports — N2
[R909] MINOR Tests, Docs — docs/testing/TESTING.md:353 — N3
[R909] PASS Robustness — hdl/ieee1722/aaf/KL_render_queue.sv:776-939 at this head; receipts/runs/{bounds_results,leaf_plants_results,parent_plants_results}.json — lead refusal; derived stamp bound inside/outside; clock-loss flush plant; ignored invalidation; retained word; wrong bank/latency; invalidation during copy (sim_main.cpp:704); a mixed-map copy is never published (the invalidate_w clear at :925-930 overrides the copy_done publication at :922, and the claim gate requires !invalidate_w); an idempotent ADD does not invalidate. The five unisolated guards are recorded as untested, F4's permitted outcome.
```

- **Conformance** applied:
  - Milan 5.3.3.8 mono clusters and the option-B topology. The factory image at `milan_datapath.sv:5005-5014` maps `INPUT_LOOP_FIRST_C + 8p + c` to `{p,c}`. The bucket-6 templates at `aem_specs.py:183-187` use `{idxh, idx, half}`, which matches the capture address `{ent[6:4], ent[1:0], ent[11]}` at `KL_chan_map_capture.sv:1393` and the copy cursor index at `KL_render_queue.sv:821`.
  - Milan 5.4.2.26-28 command behaviour is exercised through the production core (parent controls).
  - The disabled-image acceptance is re-derived (F2).
  - Open: N2.
- **RTL** applied: the delta and the enabled branches.
  - Copy timing: issue, then a one-cycle bank return, then a write at `{cons_w[2:0], addr}`.
  - Bank parity `ch[0] ^ cons[0]` matches the even/odd lane mux at `:674-675`.
  - Capture, queue and invalidation all run on the single clock `axis_clk`, so there is no CDC.
  - The asynchronous-reset invalidation register resets to 1.
  - The disabled branches are constant-only (netlist identity).
  - The walk budget term matches `TLK_WALK_CYC_C` (`milan_datapath.sv`, `+ 2 * 4 * N_STREAMS`).
  - Open: N2. Note: S4.
- **Tests** applied: re-anchoring, campaign arming, the parent and leaf controls, plants and bounds runs, and the suite registration check. Open: N1, N3.
- **Docs** applied: the design document, both READMEs, both `README-parameters.md` files, ENDSTATION_BUILDER row 16g, TESTING.md and the PR body.
  - I scanned every added line in `3cda030c..dc78aeda` for the comment rule: no lane labels, review rounds, reviewer IDs, issue-comment IDs, tool or model names, or private paths in source comments. There is no new residue instance.
  - Open: N1 (the PR claim), N3. Residue: R1.

## Reviewer-owned completion ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (N2) | Issue #979 acceptance and option-B ruling; `milan_datapath.sv:5005-5014, 5174-5196, 8469-8497`; `aem_specs.py:183-187`; `aecp_shape.py:95-113`; parent harness command scenarios; F2 re-derivation receipts | R909-2 | dc78aedae34c25a97125ecd6816a1f645db5575f |
| RTL | UNCLEAN (N2) | `KL_render_queue.sv` (delta and `:776-939`); `KL_chan_map_capture.sv:330-350, 1376-1426, 1481-1497`; `milan_datapath.sv` delta; elaborated netlists | R909-2 | dc78aedae34c25a97125ecd6816a1f645db5575f |
| Robustness | CLEAN | Enabled queue branch `:776-939`; `bounds.py`, leaf and parent plant results; guard documentation | R909-2 | dc78aedae34c25a97125ecd6816a1f645db5575f |
| Tests | UNCLEAN (N1, N3) | All 25 mutation drivers on the changed RTL (anchor probe); `render_queue all`; the `input_loopback` and `input_loopback_dp` campaigns; `scripts/suite_shards.py`; `scripts/run_all_suites.sh`; `rtl.yml:256` | R909-2 | dc78aedae34c25a97125ecd6816a1f645db5575f |
| Docs | UNCLEAN (N1, N3) | `docs/design/INPUT_MAPPED_LOOPBACK.md`; both READMEs; both `README-parameters.md` files; `docs/ENDSTATION_BUILDER.md:1116-1117`; `docs/testing/TESTING.md:353`; PR body; comment-rule scan | R909-2 | dc78aedae34c25a97125ecd6816a1f645db5575f |

## Commands and receipts (in this packet, listed in MANIFEST.sha256)

- **Scratch trees.** `scripts/mk_submodules.sh` makes shared local clones of base `3cda030c` and head `dc78aeda`, with submodules at their gitlinks. They were needed because the firmware link proves the stage-0 gitlink pins.
- **Export.** `scripts/f2_prepare.py <tree> <work>`, run with the LiteX venv Python on both sides: builder, platform firmware link, then SoC export with the measurement hook.
- **Elaboration.** `scripts/f2_elaborate.py <vivado 2026.1> <work> <json> head=... base=...`: four sequential `synth_design -rtl` runs of 53-76 s each (`receipts/f2_elaboration_hashes.json`, `receipts/f2_elaboration.log`).
- **Comparison.** `scripts/f2_compare.py` (`receipts/f2_compare.json`) and `receipts/f2_inputs.txt`.
- **Anchors.** `scripts/anchor_probe.py <base> <head> <25 drivers>` (`receipts/anchor_probe.json`).
- **Focused campaigns at head (Verilator 5.050; identity in `receipts/clone_integrity.txt`):**
  - `input_loopback_dp/mutants.py`;
  - `input_loopback/mutants.py`: control and seven plants pass (`receipts/runs/leaf_plants_*`);
  - `make -C tb/verilator/input_loopback one`: 76017 checks, 447 packets, 0 failures (`receipts/runs/leaf_one_tail.txt`);
  - `input_loopback/bounds.py`;
  - `make -C tb/verilator/render_queue all`;
  - `scripts/parent_plant_probe.py`: the 1x1 connection plants.
- **Planner.** `python3 scripts/suite_shards.py --selftest` and `scripts/run_all_suites.sh --ci-pieces --shard 0/19 --list`, at head and at base (`receipts/suite_shards_*`, `receipts/ci_pieces_list_*`).
- **Evidence integrity.** I checked 146 downloaded author receipts against `review-evidence/loopbram-r1/MANIFEST.json` at `e2c78ae9`: 146 verified, 0 mismatches. The concatenated 115 published 1x1 canonical chunks hash to the recorded `18af89e6...` (`receipts/evidence_manifest_check.txt`).
- **Clone restoration.** The review clone was never written. HEAD and tree are as stated, worktree and index are clean, there are 0 untracked/ignored entries, the index (mode/blob/path) equals the HEAD tree, and all six gitlinks are unchanged (`receipts/clone_integrity.txt`).

## Real limits

- **Sweep not run.** I did not run the complete local sweep or the `milan_dp`, capture-coherence, Yosys or builder banks. For N1 the abort predicate is shown directly.
- **Utilization not re-measured.** Disabled utilization equality comes from the author's synthesis. I re-derived netlist identity, not post-synthesis utilization.
- **No route run.** I ran no route. The 1x1 route evidence is the author's, at this head. For 8x8, see N2.
- **No hosted evidence.** There are no hosted runs at this head. I make no hosted, act or manager source-bank claim.
- **Not hardware proof.** Physical calibration was NOT RUN, the one builder calibration row is NOT RUN, and skipped field contexts are not hardware proof.
- **CPU name source not isolated.** I did not pin down which generation input changes the CPU wrapper md5 between my two exports. Both wrapper netlists are byte-identical apart from the name.

## Pending manager duties

- Hosted `rtl-fast`, `verilator-suites` and `yosys-portability` at the final head; `verilator-suites` cannot pass until N1 is fixed.
- The act replica.
- Current-dev candidate-merge validation (source base `3cda030c17`, live dev `e275d7950e`), builder and native banks at the merge turn.
- Carrying R1 to the residue checklist.
- An exact-head enabled 8x8 route, or an owner ruling, for N2.
- S14 debt (enabled 8x8 control memory 70.5 tiles) remains open under the owner rule.

R909-2 FINISHED
