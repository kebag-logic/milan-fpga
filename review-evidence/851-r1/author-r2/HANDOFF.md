# HANDOFF: milan-fpga issue #851, round 2, [A744b]

Status: **REVIEW READY** at `dafd49c1f9b79d3cc29534a9ab43d98360079d2b`. Every gate below ran on a clean clone of this exact
head and exited 0; the combined route (all four lab fixes) fits and meets the floor on its best directive. Nothing is
pushed. Judgement calls for review are listed below.

- Repository: milan-fpga, origin https://github.com/kebag-logic/milan-fpga.git (checked), branch `851-adopt-pp-044cb25f`.
- Round 1 head: `2d939d2dcb9664c08f7d2dc7b584987a1e0c0f8a` (branched from dev `1eb5289d`).
- Base: origin/dev `0a75aa774b89ac89351700f63dd8cbb89694af6c` (PR #846 merged), the merge base after step 1.
- Head: `dafd49c1f9b79d3cc29534a9ab43d98360079d2b`, four commits on round 1's six, one-line subjects, no body, no trailers.
  Nothing pushed.
- Submodules (top level and origin verified before each git command in them): processor `044cb25f` (unchanged from
  round 1, origin the processor repository); FPGA-gPTP `135afd04` -> `1616fc8f` by the merge (origin FPGA-gPTP).
- TAKEN: issuecomment-6718701725 (`receipts/records/taken.md`). REVIEW READY: issuecomment-6721171788 (`receipts/records/review-ready.md`).

## Commits this round

| Commit | Subject (abridged) |
|---|---|
| `e44a4d20` | merge of origin/dev `0a75aa77` (parents `2d939d2d`, `0a75aa77`), conflicts below |
| `bb9f0a06` | the parent check: `[ONEVEC]` in milan_dp's crflic leg and its planted encoder in `crflic-mutants` |
| `bc80b3d3` | `syn/ooc/pp_resource_baseline.json`: all three endpoints by `pp_resource_gate.py record --write` at `e44a4d20`, then the three `measured` notes |
| `dafd49c1` | the fifteenth record on the pin page, the CHANGELOG and the area pages |

`git diff --name-only e44a4d20 dafd49c1` lists documentation, testbench files and the baseline JSON only, so the route
measured at `e44a4d20` is the head's image.

## Step 1: sync, merge commit `e44a4d20`

`git fetch origin`, `git merge --no-ff origin/dev`. No rebase, no force. The gPTP submodule was checked out at the new
gitlink `1616fc8f` after verifying its top level and origin.

| File | Conflict | Resolution |
|---|---|---|
| `docs/reference/SUBMODULES.md` | pin table rows; the adoption sections | the pin table takes both gitlinks (gPTP `1616fc8f`, processor `044cb25f`), verified by `check_submodule_docs.py`; both adoption sections kept, #843's first, then #851's |
| `docs/design/AREA_BUDGET.md` | 7 hunks | the record list, the headroom narrative and the record history keep both (#843's, then #851's); the single-valued "current record" lines (intro, current table, hierarchy figure) take #851's, matching the baseline taken below; the #845 sentence takes this side's past tense |
| `docs/findings/234_PP_SHADOW_AREA_BASELINE.md` | 4 hunks | both record sections kept, newest first; the contents lists all three 2026-11 records; the intro lines take #851's |
| `docs/design/MARK_II_AREA_PLAN.md` | 2 hunks | the gate-comparison figure takes #851's; the record history keeps both lines |
| `docs/findings/README.md` | 1 hunk | #851's current-record line |
| `syn/ooc/pp_resource_baseline.json` | 23 hunks | taken whole from this side (`git checkout --ours`), the bytes round 1's `pp_resource_gate.py record --write` wrote; all three endpoints then re-recorded at `e44a4d20` by the recorder (`bc80b3d3`) |
| `docs/diagrams/submodule_boundaries.{svg,drawio,png}`, `PNG_MANIFEST.json` | generated | dev's side, then `python3 docs/diagrams/submodule_boundaries.gen.py`; `--check` OK (6 exact gitlinks) |
| `syn/yosys/rom_digests.tsv` | auto-merged | `./syn/yosys/ooc.sh --record-rom-digests` reproduces it (`git diff --exit-code` rc 0) |
| `docs/DOCUMENTATION_AUDIT.md` | auto-merged | `scripts/docs_inventory.py --write` leaves it unchanged; `--check` fresh |
| `CHANGELOG.md` | auto-merged | both sections, contents in section order |

The merge kept both texts as they were; `dafd49c1` then rewrote the #851 prose for the merged tree (renumbered the
record fifteenth, removed the duplicated image history, past tense for #843's record).

The hunk choices were applied by `scripts/resolve_hunks.py`, one recorded choice per hunk.

## Changes at the head (file:line, and the clause each states)

| # | File:line | Change | Clause / source |
|---|---|---|---|
| 1 | `tb/verilator/milan_dp/sim_crf_licence.cpp:72-77`, `:158-175`, `:702`, `:783-877`, `:1457` | `[ONEVEC]`: every MSRP (0x22EA) and MVRP (0x88F5) MRPDU the DUT sends is walked independently of the existing parser; each value is expanded by its type's increment and keyed by application, AttributeType and value; three checks: both applications seen, every MRPDU walks to its EndMark, no value in two VectorAttributes | IEEE 802.1Q-2022 10.7.7, 10.7.5.13 c), 10.8.1.2, 10.8.2.10.1, 35.2.2.6, 35.2.2.7.2 a), 35.2.2.8 a), 35.2.2.9, 11.2.3.1.7, 11.2.3.1.9 |
| 2 | `tb/verilator/milan_dp/crflic_mutants.py:27-34`, `:114-122`, `:125-136`, `:196-224`, `:254-258` | processor-side arm: a copy of the processor's `hdl/` with `KL_srp_encoder.sv`'s `sr_hit_w` tied to 0, built through `crflic-build` with `PP_DIR` | processor #214 |
| 3 | `tb/verilator/milan_dp/Makefile:294-297`; `tb/verilator/milan_dp/README.md:87`, `:532`, `:601`; `docs/testing/TESTING.md:357` | the recipe comment, the leg table, the phase table, the failing-arms table, the campaign row | - |
| 4 | `syn/ooc/pp_resource_baseline.json` | three records by `record --write`, notes by `scripts/set_measured.py` (refuses unless only the notes differ from the recorder's output) | BUILDING.md section 5; recipe Resource gate |
| 5 | `docs/findings/234_PP_SHADOW_AREA_BASELINE.md:14-15`, `:21`, `:27-29`, `:51-177` | the fifteenth record's section, intro, contents | - |
| 6 | `docs/design/AREA_BUDGET.md:13`, `:129-134`, `:149-159`, `:195-237`, `:255-256`, `:663-667` | intro; record list with the stale count fixed (`:133`); current table; headroom narrative; allocation; record history | - |
| 7 | `docs/reference/SUBMODULES.md:727`, `:773-779`, `:781-856` | the #851 section: gPTP base, the parent check, the route, the share, the gate | BUILDING.md section 5 |
| 8 | `CHANGELOG.md:61`, `:79-89`; `docs/design/MARK_II_AREA_PLAN.md:59`, `:939-940`; `docs/findings/README.md:25` | the same figures | - |

Clause texts were read from the standard (802.1Q-2022 PDF), not from an extract: `docs/spec-refs.md` does not exist at
this head.

## New check, planted mutant and failing words (R790-S1)

| Run (scratch clone at `e44a4d20` plus the check) | Result |
|---|---|
| clean leg, encoder at `044cb25f` | `checks: 430   failures: 0`; `[i] 285 MSRP and 184 MVRP MRPDUs, 631 values; 7 MRPDUs carry two vectors of one AttributeType` |
| planted mutant: `assign sr_hit_w    = 1'b0;` (never merges) | `[FAIL] no DUT MRPDU carries one attribute value in two VectorAttributes (802.1Q-2022 10.7.7, 10.7.5.13 c)) got=3 exp=0`; the only failure; the doubled value is MVRP VID 2 (`[ONEVEC] MVRP AttributeType 1 value 0x2 in 2 VectorAttributes, events 1 1`) |
| probe, not committed: the `92100657` encoder in a disposable copy | the same check fails `got=4 exp=0`: MVRP VID 2 three times and the Domain `0x6030002` ({6,3,2}) once, processor #214's two symptoms |
| the campaign's own code path, `crflic_mutants.run_pp_mutant` | `[PASS] mutant caught: the SRP encoder never merges a pending value, every hand-over appends (before processor #214) - breaks "no DUT MRPDU carries one attribute value in two VectorAttributes"` |

Receipts: `receipts/onevec/`. The whole campaign runs again in the gate table at the head.

## Step 2: findings

| Finding | Fix | Evidence |
|---|---|---|
| R789-F1 = R790-F1 | every committed path figure now comes from `report_timing` of the routed checkpoint, per corner, the worst setup and hold path (`-max_paths 1 -nworst 1 -sort_by slack`), each excerpt's slack checked equal to that corner's WNS/WHS in the route's own signoff summary (`scripts/paths.sh`, `scripts/collect_paths.py`, which exits 1 otherwise); the #841 daily-route figure is removed from the pages | `receipts/paths-e44a4d20/{aslh,eppo,eto}/summary.md`, all PASS. Round 1's five routed checkpoints were reported too (`receipts/paths-round1/*/summary.md`, all PASS): round 1's committed path claims were right (ExtraTimingOpt 29 levels, `ctr_pend_r_reg[0]` to `hs_r_reg[1]` CE, 19.439 ns of which 14.237 ns routing; hold `cap_l_r_reg[18]` to `u_tcdc/mem_r_reg_0_7_42_47` +0.036 ns; ExtraPostPlacementOpt 36 levels, AECP to D3), and round 1's `worst-setup-path.txt` was a Fast-corner clock path, not the worst |
| R789-F2 = R790-S2 | the share stated as measured on both bases: on dev `1eb5289d`, ExtraTimingOpt against ExtraTimingOpt, +77 LUT, +134 FF, +14 slices, WNS +0.024 ns, WHS +0.003 ns; at the new base, against #843's record (dev `0a75aa77`'s synthesis inputs), AltSpreadLogic_high against AltSpreadLogic_high, +207 LUT, +83 FF, -5 slices, DSP 0, WNS -0.032 ns, WHS +0.024 ns; the "no route exists" sentences removed | `receipts/f2-routes/dev-1eb5289d/gate-check.log` (copied from the public `843-review-evidence` branch, commit `425a829e`), `receipts/f2-routes/round1-a566d4f9/gate-route-1x1.log`, `receipts/record-e44a4d20/check-dev-route-1x1.log` (the gate's own deltas against dev's record) |
| R789-S1 = R790-RS1 | "All nine measurements" and #843's "All ten measurements" -> one "All these measurements use the same recipe identity and policy." | `docs/design/AREA_BUDGET.md:133` |
| R790-S1 | the parent check above | above |

## Step 3: the combined route (F1, F2, F3, F7) at `e44a4d20`

Recipe form (`docs/testing/PP_SHADOW_BASELINE_RECIPE.md`, Resource gate; the seed selection of BUILDING.md section 5):
`configs/endstation_ax7101_1x1_tdm8.yaml`, synthesis AreaOptimized_high with `synth.maxThreads` 1, opt ExploreArea,
the three placement directives from one synthesis checkpoint, Vivado 2026.1, `general.maxThreads` 32. Each run under
`vivado-slot.sh` in its own scope, one route at a time; `ooc-8x8` synthesized beside the first route (not a route); no
route ran beside a sweep. Nothing was flashed; no bitstream step.

| Directive | LUT | FF | Slice (of 15,850) | Free | RAMB36 / 18 | DSP | Slow WNS / WHS | Fast WNS / WHS | Routing errors |
|---|---:|---:|---:|---:|---|---:|---|---|---:|
| **AltSpreadLogic_high, selected** | 53,428 | 54,837 | 15,829 | 21 | 74 / 27 | 15 | +0.210 / +0.069 | +1.520 / +0.036 | 0 |
| ExtraPostPlacementOpt | 53,383 | 54,837 | 15,848 | 2 | 74 / 27 | 15 | +0.112 / +0.063 | +1.465 / +0.036 | 0 |
| ExtraTimingOpt | 53,402 | 54,838 | 15,829 | 21 | 74 / 27 | 15 | +0.018 / +0.091 | +1.520 / +0.036 | 0 |

The 10-30 gate: the best of the three fits (15,829 <= 15,850) and meets WNS >= +0.03 ns and WHS >= 0 at every corner
(0.180 ns of WNS margin). ExtraTimingOpt misses the WNS floor at its slow corners; ExtraPostPlacementOpt meets it. No
STOP condition. Worst paths (`receipts/paths-e44a4d20/`): AltSpreadLogic_high's setup path is AECP microcode CPU
`uop_e_r_reg[imm][1]` to D3 `deb_cnt_r_reg[10]` R, 37 levels, 20 ns clock, 19.258 ns (6.316 logic, 12.942 route); its
hold path is the gPTP engine's `frame_cid_r_reg[34]` to `evq_pd_ctx_r_reg_0_3_114_119` at +0.036 ns (Fast);
ExtraPostPlacementOpt's setup path is the SoC's write buffer to `storage_17`, 13 levels, 10 ns clock;
ExtraTimingOpt's is AECP `desc_base_r_reg[5]` to D3 `deb_cnt_r_reg[25]` R, 34 levels.

**Resource gate** (`receipts/record-e44a4d20/`):

| Endpoint | `check` vs dev `0a75aa77`'s record (the fourteenth) | `check` vs the record the merge carried (round 1's) | `record --write` | `check` after |
|---|---|---|---|---|
| `route-1x1` | rc 0: +207 LUT, +83 FF, -5 slices, DSP 0, WNS -0.032, WHS +0.024 | rc 1: DSP 15 vs 13 (#843's two gPTP DSPs), LUT +378 | rc 0 | rc 0 |
| `ooc-1x1` | rc 0: +203 / +76 | rc 0: 0 / 0 | rc 0 | rc 0 |
| `ooc-8x8` | rc 0: +184 / +80 | rc 0: 0 / 0 | rc 0 | rc 0 |

`check-baseline` rc 0 (3 endpoints). No tolerance, floor or ceiling moved (field-by-field diff of the JSON). The
standalone figures equal round 1's exactly; their input digests changed because the export's read set holds two
FPGA-gPTP sources, the gPTP microcode and the SoC ROM image, none of which `KL_pp_shadow` instantiates (per-file
comparison of the two read sets through the gate's own `located()`). 18 of 18 recorded memory images rehash to their
digests after measurement. Runs: `receipts/route-e44a4d20/runs.md` (peak 8,527 MB, the shipping route).

## Judgement calls (published, not resolved)

1. **All three endpoints re-recorded although the gate passes all three against dev's record.** The assignment directs
   the re-record; it also makes the record measure one tree (the merged image) instead of #843's route on processor
   `92100657` with #845's standalone records. The maintainer decision is not needed for this record: the gate passed.
2. **The route is the recipe's route set, not three build-dev runs.** BUILDING.md section 5 makes the gate's three
   directives the shipping image's seed selection ("The shipping image is built from that directive"), and #846
   measured its shipping route the same way. No build-dev bitstream was produced this round; the release build takes
   AltSpreadLogic_high.
3. **Shard 2 (capture_coherence) ran on 4 CPUs of this session's own booking (52-55)**: only three 8-CPU ranges were free.

## Gate table (head `dafd49c1`, each group on its own clean clone; every rc read from its log)

| Gate | Command | Result |
|---|---|---|
| Full sweep, 4 shards | `native-shards.py`'s four units, spec `MAKEFLAGS=-j4 --no-print-directory`, pinned tools | rc 0 each: 15 + 17 + 17 + 16 = **65 suites passed, 0 failed, 0 timed out; 2,192,512 checks, 0 in-suite failures**. Preflight `suite cancellation: PASS` in every shard; the #833 case did not occur. `capture_coherence` in shard 2 on 4 CPUs (52-55): PASS in about 2,342 s of its 2,400 s (log timestamps 10:45:00 to 11:24:02 CET). `milan_dp` (shard 0) carries `[ONEVEC]`: 285 MSRP and 184 MVRP MRPDUs, 0 doubled, leg 430 of 430 |
| Firmware self-test | `test_ctrl_firmware.py --require-rv32 --self-test --jobs 8 --shard k/4`, k = 0..3, four units | rc 0 each: `test_ctrl_firmware: PASS`; control campaign `mutants: 523 of 523 caught` (shard 1); shard 3 holds both SRP campaigns |
| Firmware unit job's other steps | `tally_selftest.py`; `ci_rv32_sdk_selftest.py` and `ci_rv32_sdk.py --verify-only`; `fw_rv32_selftest.py --require-rv32`; `test_ctrl_nvm.py --require-rv32 --jobs 8` | rc 0: 18 of 18; 25 tests OK and SDK verified (archive `d42680e9...`); 17 checks PASS; OK across 5 shapes, 435 tests |
| `fw_coverage.py --check` | `python3 sw/firmware/gtest/fw_coverage.py --check --jobs 8` (and `--selftest`) | rc 0: "firmware coverage: PASS (30 files)"; self-test 29 of 29 |
| Firmware boundary / verilator | `ctrl_boundary.py --require-rv32 --selftest --without verilator` (LiteX-pinned venv) / `--only verilator` | rc 0, `ctrl_boundary: PASS` each (first run rc 2: see Process notes) |
| Builder | `python3 sw/builder/test_builder.py --require-rv32` | rc 0: "ALL GATES PASS EXCEPT 17 NOT RUN" (no LiteX interpreter in that leg) |
| Builder, LiteX chain | the same with `MILAN_LITEX_PYTHON` set | rc 0: "ALL GATES PASS EXCEPT 2 NOT RUN" (as round 1: gate 1b and gate 11) |
| behave | `cd tests && behave --no-capture -f plain` | rc 0: 14 features, 508 scenarios, 2,330 steps passed |
| docs.yml, every `run:` step | `run_docs_yml.py` per job on a fresh clone, `verify_docs_yml.py` | verifier rc 0: **65 steps ran rc 0, 31 not run with a stated reason, 0 bad**; every job's tree clean after; the act runner contract gate (docs-gates-2 `gate_42`) `selftest: PASS` |
| docs inventory | `python3 scripts/docs_inventory.py --check` | rc 0: fresh, 547 lines |
| `git diff --check` | `git diff --check 0a75aa77 HEAD` (the merge base) | rc 0, no output |
| rtl-fast scope | `ci_scope.py --selftest`; classify | rc 0; RTL/tooling relevant: `true` |
| rtl-fast verilator-lint | `lint_rtl.py --check --self-test --jobs 8`; `pp_srcs.py --check --selftest` | rc 0: 89 <= ratchet 89; 46 sources derived |
| rtl-fast yosys-elaboration | `syn/yosys/run.sh --mode elaborate --no-structural` (3 tops); `ooc_selftest`, `guard_selftest`, `cache_selftest`; the OOC read-set and gate self-tests with `check-baseline` | rc 0 each: RESULT PASS; 75 arms; 36 controls; cache OK; baseline PASS, 3 endpoints |
| rtl-fast publication-census | `publication_census.py --check --selftest --jobs 8` | rc 0: 0 of 31 rules no arm proves |
| act runner | `python3 scripts/act_ci.py --selftest` | rc 0: selftest PASS |
| `check_cpp_idiom.py` | plain, `--list`, `--selftest` | rc 0: every rule 0 <= 0; 75 of 75 |
| `check_py_idiom.py` | plain | rc 0: every rule within its ratchet |
| xvlog gate | `XVLOG=<vivado>/bin/xvlog python3 scripts/xvlog_gate.py --check` | rc 0: PASS, 0 findings |
| ROM ledger | `./syn/yosys/ooc.sh --record-rom-digests && git diff --exit-code -- syn/yosys/rom_digests.tsv` | rc 0: the recorder reproduces the committed rows |
| Submodule docs | `check_submodule_docs.py`; `submodule_boundaries.gen.py --check` | rc 0: 6 exact gitlinks; diagram OK |
| SRP-reading campaigns | `make -C tb/verilator/milan_dp crflic-mutants`, `gsi-mutants`, `unb-mutants` | rc 0: **11 of 11** (the new encoder arm caught); 15 of 15 (clean leg 499; arms 7, 7, 7, 7, 24, 50, 16, 2, 3, 3, 3, 3, 1, 1); 6 of 6 (clean leg 499; arms 4, 2, 2, 2, 2): every count as the milan_dp README records, so nothing re-recorded |
| Resource gate | `pp_resource_gate.py check` on the three endpoints against the new record; `check-baseline` | rc 0 each |
| Push privacy check | `push-privacy-check.py <lane> 0a75aa77` | rc 0: 0 private lines |

Receipts: `receipts/sweep-dafd49c1/`, `receipts/gates-dafd49c1/`, `receipts/docsyml-dafd49c1/`, indexed by
`receipts/INDEX.md`.

## Process notes

- **CPUs.** This session's unit holds 48-55. Sweep shards: 80-87, 72-79 and 16-23 (the only three free 8-CPU ranges,
  `cpu_ranges.py show`), shard 2 on 52-55 of this session's own range. Other gate units each on a range
  `cpu_ranges.py pick` returned when it was launched (`receipts/records/cpu-booking.txt`). The Vivado runs inherited 48-55.
- **Memory.** This session's unit peaked at 5.3 GB. The largest Vivado peak was 8,527 MB (the shipping route).
- **Vivado overlap.** One route at a time; `ooc-8x8` synthesis and the read-only `report_timing` runs beside a route,
  never a route beside the sweep.
- **The shared RV32 SDK vanished mid-run.** The firmware groups first used another lane's SDK through a symlink in the gate
  HOME (as round 1 did). Between 10:32 and 10:38 CET that whole scratch tree was deleted by something outside this lane.
  `fw_rv32.compiler()` then fell back to the host's own RISC-V toolchain on PATH; the boundary gate caught it
  (`fw_rv32_selftest.py`'s "hosted headers restored" arm, rc 2, twice). A verified pinned SDK was then installed in this
  lane's gate HOME through `scripts/ci_rv32_sdk.py`, and **every** firmware group was re-run on fresh clones; the table
  holds only the re-runs. The first runs are in `receipts/superseded/sdk-deleted/`.
- **Two closing records written after the fact.** The rtl and camp groups ran in one stream whose bash read
  `lane_gates.sh` after I edited it (adding the firmware subgroups), so after each group bash stopped on a syntax error
  before writing `tree-after.txt` and `DONE` (`receipts/gates-dafd49c1/stream2-journal.txt`). No other command ran.
  Every gate's own log and rc are intact; both clones are at the head with no tracked change
  (`tree-after-recorded.txt`). That stream was stopped before its builder group, which ran as its own unit (`builderp`).
- **Corrected before use:** the first worst-path Tcl had a quoting error, so its run was discarded and repeated; a
  collector briefly walked superseded clone directories into the output directory, and that copy was deleted.
- Tools: Verilator 5.050, Yosys 0.66, sv2v 0.0.12, GNU Make 4.3, GoogleTest 1.14.0, the pinned RV32 SDK (GCC 14.3.0),
  CPython 3.12.3 venvs of `ci/constraints-ci.txt`, Vivado 2026.1.
- Scripts are in `scripts/`; receipts in `receipts/`. Logs over 200 KB are a masked tail plus size and SHA-256 in that
  directory's `RAW-RECORDS.txt`.

## Not done (by the assignment's rules)

No push, no PR creation or edit, no merge other than step 1's, no rebase, no comment edits, no other issue posts, no
hardware or bench access, no flashing, no sub-agents.
