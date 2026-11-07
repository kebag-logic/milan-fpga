# [A737b] HANDOFF: milan-fpga #843 round 2, sync with dev 1eb5289d

Status: REVIEW READY at head `e079fe66a0cb9006ca718b06f57c23a85fc3582d` (2026-11-08). dev `1eb5289d` is merged (no rebase); the first route with F1, F2 and F3 fits and meets the floor on its best directive (AltSpreadLogic_high, +0.242 ns, 16 slices free), so no STOP condition holds; the gate's refusal of its LUT and DSP growth is answered by the maintainer decision of 2026-11-06 through a re-record. Every gate is rc 0 at the head, first run. Nothing pushed; the remote branch is still `1105f545`; live dev is still `1eb5289d`.

- Repository: kebag-logic/milan-fpga (origin `https://github.com/kebag-logic/milan-fpga.git`, checked before the merge)
- Branch: `843-adopt-gptp-1616fc8f`; round 1 head `1105f54546b2f19d9577b7fad902c908e34f88ee` (checked before the merge)
- dev: `1eb5289db8fc9d139ce90cad2e380b4515793806` (#842, #849, #847 since round 1's base `cc204c6f`); it is the merge base of the head
- Base: `1eb5289db8fc9d139ce90cad2e380b4515793806`
- Head: `e079fe66a0cb9006ca718b06f57c23a85fc3582d` (6 first-parent commits on round 1's head)
- Issue posts: TAKEN issuecomment-6711665115 (text: `taken.md`); REVIEW READY issuecomment-6714446317 (text: `review-ready.md`)
- Submodules: before every git command inside one, `git -C <dir> rev-parse --show-toplevel` was that directory; origins `https://github.com/Mister-M-alt/FPGA-gPTP.git` (gptp-processor) and `https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan.git` (protocol-processor). The gptp-processor gitlink stays `1616fc8f`. The protocol-processor checkout was moved to the merged gitlink with `git -C protocol-processor checkout 9210065779b0f698fd7bdb22323a1ed5b8482677`.
- Issue #851 (processor `044cb25f`) is not taken: no commit of it is in this branch.

## Commits (first parent, one-line subjects, no body, no trailers)

| Commit | Kind | Subject (abridged) |
|---|---|---|
| `04148cd764` | merge (`git merge --no-ff origin/dev`, parents `1105f545`, `1eb5289d`) | Merge dev 1eb5289d (PR #842, #849, #847) into 843-adopt-gptp-1616fc8f, keeping both pins, both milan_dp additions and both adoption records, stricter-readings gPTP rows at 1616fc8f; generated files take dev's side and are regenerated next |
| `6cae6c1f9a` | regeneration | submodule boundary diagram and PNG manifest entry through `submodule_boundaries.gen.py` |
| `a6d7cdf3e2` | regeneration | time-sync diagram's PNG manifest entry through `timesync_chain.gen.py` |
| `96705759ab` | re-measure / recorder | route-1x1 through `pp_resource_gate.py record --write` (the combined route) |
| `898b58a56f` | re-measure / generator | service-budget traces on both AX7101 shapes and `oracle.json` through `gen_oracle.py` |
| `e079fe66a0` | records of the re-measure | the route against dev, the fourteenth route record and the maintainer decision in the area budget, pin page, changelog and area baseline |

## Conflicts and resolutions

`git merge --no-ff --no-commit origin/dev` reported the 8 expected conflicts (`receipts/merge/conflicts.txt`). 21 files were changed by both sides since `cc204c6f` (`receipts/merge/both-sides-touched.txt`); the 13 that merged cleanly were read for semantic conflicts (below).

| File | Cause | Resolution |
|---|---|---|
| `docs/reference/SUBMODULES.md:24-25` (pin table) | each side moved one gitlink row | gptp-processor `1616fc8f` (branch) and protocol-processor `92100657` (dev); `check_submodule_docs.py` OK, 6 exact gitlinks |
| `tb/verilator/milan_dp/Makefile:1020` (`clean`) | the branch added `gptp_lat_ucode.hex`, dev added `obj_bootsa` | both |
| `tb/verilator/milan_dp/README.md:91-93` (leg table) | dev added the `obj_bootsa` row before `obj_gptp`; the branch extended the `obj_gptp` and `obj_gptplat` rows with #843 | dev's `obj_bootsa` row, then the branch's two rows (each is dev's row plus the #843 clause) |
| `docs/DOCUMENTATION_AUDIT.md` | generated | dev's side in the merge (the #849 generator's format); `docs_inventory.py --check` fresh at the merge, and `--write` at the head rewrites it byte-identical |
| `docs/diagrams/submodule_boundaries.drawio`, `.png`, `PNG_MANIFEST.json` | generated | dev's side in the merge, then `submodule_boundaries.gen.py` (`6cae6c1f`) and `timesync_chain.gen.py` (`a6d7cdf3`) |
| `tb/verilator/fw_service_budget/oracle.json` | generated (binds each AX7101 shape's flash media) | dev's side in the merge, then re-measured and regenerated (`898b58a5`) |

Semantic conflicts resolved in the merge commit:

| File | Cause | Resolution |
|---|---|---|
| `docs/reference/STRICTER_READINGS.md:100-114` | the page arrives from #842 and states the pinned gPTP engine's behaviour at `135afd04`; the merge pins `1616fc8f` (issue item 4) | round 1's prepared text (`843-a737/stricter-readings-gptp.patch`, `git apply`, hunk offset 3): the readings merged in `1616fc8f`, #843 pins it, and the last column states the merged behaviour. Claims checked against `gptp-processor/hdl/ucode/gen_gptp_ucode.py:592-610` (`PD_LATE_NS_C` = 15.006181 ms) and the engine harness trials (`gptp-processor/tb/verilator/engine/sim_main.cpp:7730-7778`) |
| `docs/reference/SUBMODULES.md:635-718` (#843 adoption record) | the record said "The processor stays at `a9e84b66`"; on the merged tree it lands after #845's adoption | the record moves after #845's (records run in adoption order) and reads "The processor stays at `92100657`" (`:637`) |

Merged cleanly and kept as merged: `CHANGELOG.md` (both sections), `docs/design/AREA_BUDGET.md` (#845's thirteenth record and decision, round 1's #843 lines, later rewritten in `e079fe66`), the five configs (dev's prototype MACs and the branch's `clock_accuracy`), `sw/builder/endstation_builder.py`, `sw/builder/test_builder.py`, `docs/ENDSTATION_BUILDER.md`, `tb/verilator/milan_dp/sim_gptp.cpp` (dev's #839/#840 identity lines and the branch's `[CA]` check do not overlap), `syn/yosys/rom_digests.tsv` (both pins' rows), `docs/diagrams/submodule_boundaries.svg` (the generator rewrote it unchanged).

Interaction checked, no change needed: dev's new `bootsa` leg makes its gPTP program with `gen_gptp_ucode.py --clk-hz --cease-ms --mac` and no `--clock-accuracy` (`tb/verilator/milan_dp/gen_boot_fw.py:160-162`). At `1616fc8f` the default is `CLOCK_ACCURACY_C` = 0x22 (`gen_gptp_ucode.py:542-551`, `:2609-2610`), the AX7101 config's `clock_accuracy` (`configs/endstation_ax7101_1x1_tdm8.yaml:98`), so that image announces the config's value. Dev's `ax1x1gptp` rule (`--mac 0x024b4c4b4c01`) is the same case.

## Regeneration and re-measure commands

| Generated file | Command | rc | Result | Commit |
|---|---|---:|---|---|
| boundary diagram, PNG manifest | `python3 docs/diagrams/submodule_boundaries.gen.py`; `--check`; `--selftest` | 0; 0; 0 | drawio and png rewritten, svg unchanged; "OK (6 exact gitlinks, decoded PNG)" | `6cae6c1f` |
| time-sync diagram manifest entry | `python3 docs/diagrams/timesync_chain.gen.py`; `--check`; `--selftest` | 0; 0; 0 | only the manifest entry moved; `scripts/check_diagram_pngs.py` "OK (6 decoded ...)" | `a6d7cdf3` |
| ROM digests | `cd syn/yosys && ./ooc.sh --record-rom-digests` | 0 | "recorded ROM content digests for protocol-processor pin 92100657... and gptp-processor pin 1616fc8f..."; no diff, so no commit | - |
| route-1x1 record | `python3 syn/ooc/pp_resource_gate.py record <shipping> --endpoint route-1x1 --comparison <AltSpreadLogic_high> --comparison <ExtraTimingOpt> --write`; then `scripts/set_measured.py` for the route's `measured` note, the one field `--write` leaves (as #845's lane did); `check-baseline` | 0; 0 | only `route-1x1`'s `record` and `measured` differ from the thirteenth (checked by script); `check-baseline` "baseline PASS: 3 endpoints"; `check` on the set: rc 1 before, rc 0 after | `96705759` |
| service-budget oracle | `svc_driver.sh <clone> <scratch>` (round 1's driver, unchanged steps: both shapes built, populated `all` on both, `uart-paced` on the 1x1, in a network namespace), then in the same clean clone of `a6d7cdf3`: `python3 -B tb/verilator/fw_service_budget/gen_oracle.py --small-build <1x1> --large-build <8x8>`; `make -C tb/verilator/fw_service_budget` | 0 (each run); 0; 0 | 1x1 `all` 14 min, 1x1 `uart-paced` 18 min, 8x8 `all` 88 min; 55 + 14 checks, 0 failures. Run from the lane instead, `gen_oracle.py` refuses before writing ("stale or unbound fixture build": the builds bind the clone), so the clone's output was copied (sha256 `00c9371c...` both); the lane's `make` then passes the same 55 + 14 | `898b58a5` |
| documentation audit | `python3 scripts/docs_inventory.py --write` at `e079fe66` | 0 | "wrote docs/DOCUMENTATION_AUDIT.md", no diff (fresh; #849 removed line counts) | - |

Service-budget verdicts against dev's oracle (`1eb5289d`): 1x1 `all` none and none; 8x8 `all` the same two `over-budget duty: milan_nvm`; 1x1 `uart-paced` none and none. Graded rows move by under 0.04 ms (1x1 boot-to-enabled 361.949 -> 361.910 ms, AEM copy 332.476 -> 332.437 ms; 8x8 unchanged to the microsecond). The media digests move (1x1 `0f9040c5...` -> `3e99d712...`, 8x8 `f0600611...` -> `1f2d5c59...`): the AEM image carries clockAccuracy 0x22 with the prototype identity.

Receipts: `receipts/merge/`, `receipts/regen/`, `receipts/rebaseline/`, `receipts/service-budget/`.

Not gated and not this merge's: `docs/diagrams/egress_queue_map.gen.py` and `nxn_window_map.gen.py` exit 1 ("cannot parse cls_tcq reset value", "cannot confirm SRP_CTX_ROWS_C") on the merged tree, whose `hdl/` and both generators equal dev `1eb5289d`'s. No workflow runs either. (Running them with `--check`, which they do not take, wrote two stray files into the lane; both were deleted at once and are in no commit.)

## Route table: AX7101 TDM8 1x1, the first route with F1, F2 and F3

Recipe: `docs/testing/PP_SHADOW_BASELINE_RECIPE.md` unchanged (`build.sh ax7101 --dry-run`, its `milan_soc.py` argv without `--build`, `pp_baseline.py --single-thread-synthesis`; the shipping route, then AltSpreadLogic_high and ExtraTimingOpt from its synthesis checkpoint, default seed). Vivado 2026.1 under `2026-09-23/vivado-slot.sh`, each run in its own scope (MemoryMax 14G) inside a unit on this lane's CPUs 16-23; one route at a time; no sweep ran beside any route. Head: a clean clone of `a6d7cdf3` (`a6d7cdf3..e079fe66` changes no file under `hdl`, `syn/yosys`, `syn/ooc/*.py`, `sw`, `configs`, `avdecc` or any submodule). Dev: a clean clone of `1eb5289d` (gPTP `135afd04`, processor `92100657`). Figures read from each run's own reports (`scripts/figures.py`, `receipts/route-figures.json`) and by the gate's own parser.

| Directive | Commit | LUT | FF | Slice (of 15,850) | Free | RAMB36 / RAMB18 | DSP | WNS / WHS Slow_0C | Slow_85C | Fast_0C | Fast_85C | Route | Minutes |
|---|---|---:|---:|---:|---:|---|---:|---|---|---|---|---|---:|
| ExtraPostPlacementOpt | dev | 52,845 | 54,596 | 15,841 | 9 | 74 / 27 | 13 | +0.122 / +0.102 | +0.122 / +0.102 | +1.633 / +0.036 | +1.633 / +0.036 | 0 errors | 48.0 |
| AltSpreadLogic_high | dev | 52,968 | 54,596 | 15,817 | 33 | 74 / 27 | 13 | +0.121 / +0.061 | +0.121 / +0.061 | +1.590 / +0.025 | +1.590 / +0.025 | 0 errors | 13.4 |
| **ExtraTimingOpt, dev's best** | dev | 52,973 | 54,595 | 15,817 | 33 | 74 / 27 | 13 | +0.234 / +0.061 | +0.234 / +0.061 | +1.553 / +0.033 | +1.553 / +0.033 | 0 errors | 16.8 |
| ExtraPostPlacementOpt | head | 53,166 | 54,757 | 15,846 | 4 | 74 / 27 | 15 | +0.062 / +0.047 | +0.062 / +0.047 | +1.508 / +0.024 | +1.508 / +0.024 | 0 errors | 49.1 |
| **AltSpreadLogic_high, head's best** | head | 53,221 | 54,754 | 15,834 | 16 | 74 / 27 | 15 | +0.242 / +0.071 | +0.242 / +0.071 | +1.383 / +0.012 | +1.383 / +0.012 | 0 errors | 18.2 |
| ExtraTimingOpt | head | 53,234 | 54,755 | 15,834 | 16 | 74 / 27 | 15 | +0.058 / +0.102 | +0.058 / +0.102 | +1.383 / +0.031 | +1.383 / +0.031 | 0 errors | 15.1 |

Best of three against best of three (the 2026-10-30 rule): +248 LUTs, +159 FFs, +17 slices, +2 DSPs; slow-corner WNS +0.008 ns, fast-corner WNS -0.170 ns; slow WHS +0.010 ns, fast WHS -0.021 ns. Every directive of both commits places, routes with 0 routing errors, and meets the +0.03 ns WNS and 0 ns WHS floors at every corner, so neither STOP condition holds.

Largest contributors (`scripts/hier_diff.py` on the hierarchical utilization, `receipts/hier-diff-*.md`): on each directive the gPTP engine `milan_datapath/g_gptp_plane.u_gptp_shadow/u_engine` grows by +475 (ExtraPostPlacementOpt) or +469 LUTs, +166 FFs, +2 DSPs; within it `u_ucpu` +256 and `u_timer` +110, `u_parser` +57. FPGA-gPTP #100's out-of-context figures predicted +475 LUTs and two DSPs. The rest of the image moves by packing (-154 to -216 LUTs net).

Worst setup path of the selected route: `milansoc_sdram_bankmachine6_row_reg[5]` -> `milansoc_sdram_twtrcon_ready_reg/R`, 16 logic levels, 9.301 ns data path (6.248 ns routing), the SoC's SDRAM controller, outside the gPTP engine and `milan_datapath`. Worst hold: `milansoc_rdat1_reg[2]` -> `storage_43_reg`, +0.012 ns at the fast corners.

Resource gate (`pp_resource_gate.py check <shipping> --endpoint route-1x1 --comparison <ASL> --comparison <ETO>`), against the thirteenth record (#845, ExtraTimingOpt, 52,529 LUT, 13 DSP, +0.373 ns):

| Set | rc | Selected | Refused | Passed |
|---|---:|---|---|---|
| dev `1eb5289d` | 0 | ExtraTimingOpt +0.234 ns | - | LUT +444 (500), FF +13, slice -18, DSP 0, WNS -0.139, WHS +0.021 |
| head, before the re-record | 1 | AltSpreadLogic_high +0.242 ns | LUT +692 (500), DSP +2 (0) | FF +172 (600), slice -1 (80), RAM 0, WNS -0.131 (floor met), WHS 0.000 |
| head, after `record --write` | 0 | AltSpreadLogic_high | - | every figure 0 |

The maintainer decision of 2026-11-06 (issuecomment-6689115541 on #843, the same text as #845's issuecomment-6689114981) accepts the area growth of the mandatory lab fixes, both pins named, with a re-baselined budget; the #845 round 3 ruling (issuecomment-6692097382) sends #846 to sync, route and re-baseline on #847. So `route-1x1` is re-recorded through the gate; no tolerance, floor or ceiling moved. The standalone endpoints (`ooc-1x1`, `ooc-8x8`) are not re-measured: their top is `KL_pp_shadow`, which holds no gPTP logic; `git diff 1eb5289d HEAD` over `hdl`, `syn/ooc`, `sw/litex` and `protocol-processor` is empty; the two exports' generated tops differ only in LiteX's module-tree comment order; and the processor images `ucode.hex` and `ltn_rom.hex` are byte-identical (`49a993be...`, `23cc67ee...`).

Receipts: `receipts/route-head/`, `receipts/route-dev/` (each directive's route status, utilization, IOB pack, DRC, timing design tables, slot log; `large.sha256` for the Vivado logs), `receipts/rebaseline/`, `receipts/route-figures.json`, `receipts/hier-diff-*.md`.

## Changes this round (file:line at the head, clause)

| File:line | Change | Clause |
|---|---|---|
| `gptp-processor`, `protocol-processor` | gitlinks `1616fc8f` (kept) and `92100657` (dev's), through the merge | - |
| `docs/reference/SUBMODULES.md:24-25` | pin table: both pins | - |
| `docs/reference/SUBMODULES.md:635-718` | #843 record after #845's; processor `92100657`; the route against dev `1eb5289d` on three directives, the gate and the decision | - |
| `docs/reference/STRICTER_READINGS.md:100-114` | gPTP readings at the pinned `1616fc8f` (issue item 4) | Milan v1.2 4.2.6.2.3, 4.2.6.2.6; 802.1AS-2011 Figure 10-13 (Cor1), B.2.3, 11.5.3, 8.6.2.3; IEEE 1588-2008 7.6.2.5, Table 6 |
| `tb/verilator/milan_dp/Makefile:1020`, `README.md:91-93` | both sides' clean list and leg rows | - |
| `syn/ooc/pp_resource_baseline.json:5-451` | `route-1x1` record (AltSpreadLogic_high, 53,221 LUT, 15 DSP, +0.242 ns) and its note | - |
| `tb/verilator/fw_service_budget/oracle.json` | three traces re-measured; media digests | - |
| `docs/diagrams/submodule_boundaries.drawio`, `.png`, `PNG_MANIFEST.json` | regenerated | - |
| `CHANGELOG.md:186-194` | the #843 section's route lines | - |
| `docs/design/AREA_BUDGET.md:13`, `:126-131`, `:146-156`, `:192-216`, `:230-231`, `:632-637` | baseline intro, record history, the gate's record table, the #843 route paragraph with the directive table and critical path, the routed hierarchy, the fourteenth record | - |
| `docs/findings/234_PP_SHADOW_AREA_BASELINE.md:14-25`, `:48-142` | intro, contents, the "Re-baseline of 2026-11-07, FPGA-gPTP 1616fc8f" section | - |
| `docs/design/MARK_II_AREA_PLAN.md:59`, `:938-939`; `docs/findings/README.md:25` | the record's WNS and the comparison anchor | - |

No source, RTL, builder or test file changed this round beyond what the merge brought from either side.

## New checks, planted mutants, failing words

This round adds no check. Round 1's eight mutants (`scripts/mutants.py`, round 1's runner with its anchors, checks and phrases unchanged) were re-run on a clean clone of the head `e079fe66`, because the merge brought dev's changes into `test_builder.py`, `sim_gptp.cpp` and the `milan_dp` Makefile. Each planted defect failed its check by name; the clone was clean after (`tree_after` empty). Receipts: `receipts/mutants-e079fe66/`.

| # | Planted mutant (file) | Check run | rc | Failing words |
|---:|---|---|---:|---|
| MB1 | the builder passes `--clock-accuracy 0x22` for every config (`sw/builder/endstation_builder.py`) | gate 26c | 1 | `gate 26c: arty_current passes --clock-accuracy 0x22, its board decided 0xFE` |
| MB1 | same | `make -C tb/verilator/milan_dp gptp-lat` | 2 | `FAIL [CA] every DUT Announce carries the config's clockAccuracy got 0000000000000004 exp 0000000000000000` |
| MB1 | same | gate 1b | 1 | `clockAccuracy: mutation did not reach gptp_ucode.hex` |
| MB2 | the builder passes no `--clock-accuracy` | gate 26c | 1 | `gate 26c: ax7101_1x1_tdm8's generator options ['--mac', '0x024b4c4b4c01', '--p1', '248', '--clk-hz', '50000000'] carry no --clock-accuracy` (the MAC is now dev's prototype identity) |
| MB3 | an omitted key resolves to 0x22 | gate 26b | 1 | `omitted gptp.clock_accuracy resolved to 0x22, 802.1AS-2011 8.6.2.3 b) says 0xFE` |
| MB4 | any octet is accepted | gate 26c | 1 | `gate 26c: gptp.clock_accuracy 0x0 was ACCEPTED` |
| MB5 | the descriptor takes 0x22, not the config | gate 26b | 1 | `arty_4x4: gptp.clock_accuracy 0x22, the board's decided value is 0xFE (#843)` |
| MH1 | gptp_shadow's `OUR_CQ` is the old literal (`tb/verilator/gptp_shadow/Makefile`) | `make -C tb/verilator/gptp_shadow run` | 2 | `FAIL as master: every Announce carries this image's clockQuality got 0000000000000001 exp 0000000000000000` |
| MH2 | gptp_plane's `OUR_CQ` is the old literal (`tb/verilator/gptp_plane/Makefile`) | `make -C tb/verilator/gptp_plane run` | 2 | `FAIL grandmaster Announce carries this image's clockQuality got 00000000f822436a exp 00000000f8fe436a` |
| ML1 | the gptp leg runs the Arty image while expecting 0x22 (`tb/verilator/milan_dp/Makefile`) | `make -C tb/verilator/milan_dp gptp` | 2 | `FAIL [CA] every DUT Announce carries the config's clockAccuracy got 0000000000000004 exp 0000000000000000` |

## Gate table (head `e079fe66a0cb9006ca718b06f57c23a85fc3582d`, each on a clean clone)

Environment: pinned Verilator 5.050, sv2v 0.0.12, GNU Make 4.3, `MAKEFLAGS=-j4 --no-print-directory` in the sweep spec, `TSN_GEN_ROOT` set, the RV32 SDK on PATH for `--require-rv32`, the docs venv with the reference package set. CPU ranges from `cpu_ranges.py pick` (pick8 applied once per shard on the live busy set): shards 96-103, 88-95, 80-83 (shard 2, holding capture_coherence, on 4 CPUs), 72-79; final gates 64-71; mutants 56-63; docs workflow on this lane's 16-23; service-budget re-measure 120-127; early checks 112-119. MemAvailable at the sweep launch 51.6 GB. No Vivado route ran beside the sweep: the routes finished at 21:48Z, the sweep started at 21:54Z.

| Gate | Command | rc | Result | Receipt |
|---|---|---:|---|---|
| Full sweep, 4 shard units | `native-shards.py 843-a737b-e079fe66 <spec> <out> 4 96-103 88-95 80-83 72-79` over `bash scripts/run_all_suites.sh <logs> --wait --shard k/4` | 0, 0, 0, 0 | shard 0: 15/15 suites, 361,192 checks (3,810 s); shard 1: 17/17, 1,525,512 (3,429 s); shard 2: 17/17, 284,230, capture_coherence PASS (5,382 s); shard 3: 16/16, 21,575 (3,239 s). 65 of 65 suites, 2,192,509 checks, 0 failed, 0 timed out, 0 in-suite failures. Preflight (suite cancellation and gptp_shadow mutant lifecycle included) passed first time in all four, so no #833 re-run | `receipts/sweep-e079fe66/` |
| milan_dp gptp / gptp-lat / bootsa (shard 0) | in `make -C tb/verilator/milan_dp` | 0 | `[CA] 4 DUT Announce frame(s); last clockQuality 0xF822436A, expected clockAccuracy 0x22`, 212/212; `... 0xF8FE436A, expected clockAccuracy 0xFE`, 212/212; dev's `bootsa` 67 checks, 0 failures | shard-0 `milan_dp.log` |
| gptp_shadow (shard 1) | `make -C tb/verilator/gptp_shadow` (lifecycle, mutants, run) | 0 | 326/326; mutant lifecycle PASS | shard-1 `gptp_shadow.log` |
| gptp_plane, fw_service_budget (shard 2) | `make -C tb/verilator/gptp_plane`; `make -C tb/verilator/fw_service_budget` | 0; 0 | 31/31, phc_step 62; oracle 55 checks and flash 14 checks, 0 failures | shard-2 logs |
| Firmware self-test | `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` | 0 | saved-state writer gate OK across 5 shapes, every planted defect reddened | `receipts/final-gates-e079fe66/` |
| Coverage | `python3 sw/firmware/gtest/fw_coverage.py --check --jobs 8`; `--selftest` | 0; 0 | PASS (30 files); 29 of 29 planted cases | same |
| Builder | `python3 sw/builder/test_builder.py --require-rv32` | 0 | ALL GATES PASS EXCEPT 2 NOT RUN: gate 1b's `MAKEFLAGS += -e` arm (this make does not re-read MAKEFLAGS mid-parse) and gate 11 (the calibration build tree is not on this machine), the same two as on dev and in round 1 | same |
| behave | `cd tests && behave` | 0 | 14 features, 508 scenarios, 2,330 steps passed (log 442,503 B, kept as tail + sha256) | same |
| docs.yml | every `run:` step of all nine jobs, each job on a fresh clone (the #829 runner and verifier as #845's lane adapted them, this lane's paths, `not_run.json` with its reasons) | 0 | verifier: 72 steps rc 0, 24 not run with their recorded reason, 0 bad; every job's tree clean after | `receipts/docs-yml-e079fe66/` |
| Docs inventory | `python3 scripts/docs_inventory.py --check`; `--selftest` | 0; 0 | fresh (547 lines); 60 controls | `receipts/final-gates-e079fe66/` |
| Whitespace | `git diff --check 1eb5289db8fc9d139ce90cad2e380b4515793806 HEAD` | 0 | no output | same |
| Lint | `python3 scripts/lint_rtl.py --check` | 0 | 89 <= 89 | same |
| Em dash | `scripts/check_em_dash.py --base 1eb5289d...` | 0 | 0 findings over 297 added lines in 16 pages | same |
| Resource gate | `python3 syn/ooc/pp_resource_gate.py check-baseline`; `--selftest` | 0; 0 | baseline PASS: 3 endpoints; selftest PASS | same |
| Vivado front-end | `python3 scripts/xvlog_gate.py --check`, through `vivado-slot.sh` | 0 | 0 findings; pinned at `protocol-processor@92100657; gptp-processor@1616fc8f` | same |
| Route set, head | `pp_resource_gate.py check ... --endpoint route-1x1 --comparison ... --comparison ...` | 1, then 0 | see "Route table" | `receipts/rebaseline/` |
| Route set, dev | the same at `1eb5289d` | 0 | ExtraTimingOpt selected | `receipts/route-dev/gate-check.log` |
| Mutants | `mutants.py` at `e079fe66` | - | 8 of 8 caught by name in 10 check runs | `receipts/mutants-e079fe66/` |

Early checks at `a6d7cdf3` (not the evidence; run to find a merge breakage early): behave rc 0, firmware self-test rc 0, builder rc 0 (ALL GATES PASS EXCEPT 2 NOT RUN).

## Acceptance

| Item | State | Evidence |
|---|---|---|
| Required 1: clockAccuracy per board, builder passes `gptp.clock_accuracy`, comments corrected | met (round 1, unchanged by the merge) | gates 1b, 26b, 26c; mutants MB1-MB5 |
| Required 2: ROM digests re-recorded through the recorder; model-shape pins where clock_accuracy moves them | met: the recorder at the merged tree writes no change; no pinned hash moves (builder rc 0) | `receipts/regen/rom-digests-record.log` |
| Required 3: `OUR_CQ` from the build | met (round 1) | MH1, MH2 |
| Required 4: the stricter-readings page points at the merged gPTP behaviour | met in the merge commit (the page arrived from #842) | `docs/reference/STRICTER_READINGS.md:100-114` |
| Acceptance 1: sweep with the gptp legs, gptp_shadow, gptp_plane, firmware self-test, builder, behave, docs gates green; inventory regenerated | met | gate table; `docs_inventory.py --write` reproduces the page |
| Acceptance 2: a 0xFE config and a 0x22 config each produce that value on the wire in the gPTP leg | met | `[CA]` lines above; gate 26c |
| Acceptance 3: area and timing of the shipping route recorded against dev | met: three directives on head and dev `1eb5289d`, every corner | route table; `docs/reference/SUBMODULES.md:668-718`, `docs/design/AREA_BUDGET.md:192-216` |

## Notes

- `ooc-1x1` and `ooc-8x8` were not re-measured (reason in the route section). The #845 ruling asked this PR to route and re-baseline; the route is the endpoint the gPTP pin moves.
- The service-budget timing rows move by under 0.04 ms against dev's oracle, which binds dev's own media. The media digest moves because the AEM image carries clockAccuracy 0x22.
- Scratch kept outside the output directory for `check` to re-read: the route measurement directories (head and dev) and the service-budget build directories. The four shard clones from `native-shards.py` are reproducible and may be removed.
