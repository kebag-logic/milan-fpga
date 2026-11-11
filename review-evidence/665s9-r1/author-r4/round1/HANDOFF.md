# [A760] #870 (S9 of #665): handoff

Lane: `665-s9-split-image`, from `dev-soft-core` `1d6bf555`. PR target: `dev-soft-core`. Nothing pushed.
TAKEN: #870 issuecomment-6759671811 (2026-11-10).

## Status: STOP, acceptance 1 (timing) not met; every other item done

Final head `ad2ed0e3ab3daa9697bdf42ae504b4504bfd04aa` (8 commits on `1d6bf555`, 16 files, +1,287 / -282).
Resumed 2026-11-10 09:44 after the planned host power-off at 07:49, which killed the first integrated split
route in synthesis (started 07:26 at `5d6d2835`) and `nvm_cosim`; both were re-run from the same inputs.
Resumed again 2026-11-10 18:04 after the host reset at 17:00 (memory fault), which killed the final gate pass at
`ad2ed0e3` mid-way: no commit was lost, the tree was clean, and no new commit was needed. Gates that had finished
with rc 0 at `ad2ed0e3` on clean clones are kept (the tree is unchanged); the five CI job instances in flight at
17:00 (elaborate-gates-1, firmware-boundary, firmware-control-mutants, firmware-verilator, verilator-shards 0) were
moved aside as killed attempts and re-run; the sweep (one shard launched at 16:08) was re-run from scratch; S2's
harness at 1x1 and 8x8 was re-run (killed mid-run). Only TAKEN had been posted on #870.

| # | Acceptance item (#870) | Result |
|---|---|---|
| 1 | Route: WNS >= +0.030 ns and WHS >= 0 at every endpoint, #818 best of 3 | **NOT MET**: best `ExtraTimingOpt` +0.002 ns slow-corner WNS (0.028 under the floor); WHS met at every corner. Every path under +0.030 ns is in `KL_mbx` at 100 MHz |
| 2 | All-fabric endpoint unchanged: tracked outputs and manifest byte-identical | Met: 21/21 export files at 1x1 and 8x8 equal the base's (normalised paths/timestamps/comment tree); 50/50 builder outputs of the 5 configs byte-identical; no all-fabric manifest is written; its route at this head passes the gate (rc 0) |
| 3 | Ledger rows (text, rodata, data, BSS, stack, pools; RAMB36/RAMB18 as mapped; 5 largest BSS; usable bytes) | Met: `MARK_II_AREA_PLAN.md`, M8a-2 section, four points |
| 4 | Whole image LUT, FF, tiles vs 121.5 tiles and 38,040 LUT | Met: 29,277 LUT, 39,060 FF, 12,767 slices, 56/32 = 72 tiles (8,763 LUT below the bar; 49.5 tiles below 121.5) |
| 5 | Bound-talker term at 1 and 2 interfaces and in the route, D7 close-out row | Met: OOC 285/87 (1 if), 682/159 (2 if); in the route its storage is as OOC (64 SRL + 22 LUTRAM, 87 FF), logic not separable; D7 (a) row in the ledger |
| 6 | Planted negative control for each identity mismatch, split+DDR3, all-fabric+mailbox | Met: gate 23p, 12 planted images, each failing by its kind |

STOP condition check: the route is 8,763 LUT **below** the M9 bar, not within 300 LUT of it, so D7 (b) is not
triggered. No all-fabric change was needed to remove DDR3. No contract, VERSION, channel or ring-depth decision
was needed. The STOP is acceptance 1: closing the floor needs a `KL_mbx` change, which this lane may not make.

## Commits (added only, one-line subjects)

- `2d57d365ab` Build a shipped config at the split placement through one builder recipe that keeps its shape and writes no tracked file (#665)
- `c075c3856f` Name the split placement in the SoC ident, record it in a split image manifest, and refuse a disagreeing image with an identity gate and eleven planted images (#665)
- `9f3ef61229` Build no DDR3, main RAM or processor memory bridge in the split image, and refuse a split image that carries DDR3 (#665)
- `e16c134305` Keep the DDR3 plant's anchor of the identity gate within the Python line limit (#665)
- `5d6d28356a` Read the split control firmware's rom banks as banks, the last ending with the image, in the M0s recipe's full-split inventory (#665)
- `9f6d58365d` Say an all-fabric image in the identity gate's pass line (#665)
- `0f3c475685` Map a ledgered point's firmware memory out of context through --ledgered, refused on any other image, with three planted defects (#665)
- `ad2ed0e3ab` Record the integrated split route, its timing against the floor, the firmware ledger at four points and D7's close-out of the bound-talker term (#665)

## Changes (file:line at the final head, reason)

Builder recipe (acceptance: scope "a builder recipe for split images"):
- `sw/builder/endstation_builder.py:4450` `with_placement()`: a loaded config at a placement, every other key
  unchanged, so the split image is built from the shipped file as it stands (#665 S9, D2).
- `sw/builder/endstation_builder.py:5915` `_derive_artifacts(..., placement)` and `:6082` `build(placement=)`:
  the recipe derives in memory, writes beside the config's own outputs, and refuses `--write-rtl` /
  `--write-fragment` ("the split recipe writes no tracked file"), so no sweep builds the split by accident.
- `sw/builder/endstation_builder.py:6173` `--placement {all-fabric,split}` CLI flag.

Identity (D2), manifest, identity gate:
- `sw/litex/milan_soc.py:2998` the SoC ident ends in ` split` for a split image; the all-fabric ident is unchanged.
- `sw/litex/milan_soc.py:3006` `write_image_manifest()`: placement, ident, VERSION, mailbox contract (major,
  minor from `KL_mbx_pkg.sv`), control firmware ELF sha256, and after a Vivado build the bitstream payload
  sha256 and part; the build runs the identity gate on what it wrote and fails on a finding
  (`:4966`). An all-fabric build writes no manifest, so its outputs are unchanged.
- `sw/litex/check_image_identity.py:64` the six kinds (manifest, ident, firmware, bitstream, placement, ddr3);
  `:130` `facts()` reads an image's outputs; `:228` `findings()`; `:253` the CLI (0 agree, 1 a finding,
  2 unreadable). The pass line wording is fixed in `9f6d5836`.
- `scripts/ci_builder_legs.py:49` the builder leg requires `test_image_identity_gate`.

M8a-2, DDR3 removal (D4):
- `sw/litex/milan_soc.py:3450` `--ctrl-mailbox` builds no DDR3 and no integrated main RAM; `:4600` the CLI
  refuses `--ctrl-mailbox --with-dram` with D4's words; `:4718` `--full` builds MAC and flash but no DDR3
  under `--ctrl-mailbox`. The three processor memory bridges and their `ppmem` observer are not built in the
  split (no processor master remains: S6 removed `KL_pp_shadow` from the split datapath). The all-fabric
  build is unchanged (no all-fabric change was needed, so no STOP on that line).

Route recipe:
- `syn/ooc/pp_baseline.py:179` under `full-split` the image inventory reads the split firmware's `rom_bank<k>`
  memories as banks (each never empty, never past its depth, at its width; the last ends with the image), so the
  M0s recipe can prepare the integrated split route; `syn/ooc/pp_baseline_mutants.py:44` two mutants.

Ledger measurement tool:
- `syn/ooc/ctrl_memory_ooc.py:98` `--ledgered TAG=POINT`, `:123` passed to `ctrl_memory.plan()`: maps the
  target platform's 59.0-tile ledgered point out of context (refused past 56 without it, as every SoC build is);
  refused on any other image and on a tag naming no image.
- `sw/litex/ctrl_memory_ledger.py:134` `MAPPER_MUTANTS`, `:160` `mapper_facts()`, `:177` `mapper_arms()`;
  `sw/litex/test_ctrl_memory.py:983` runs them as its eighth arm (kept in the ledger module because the test
  module is at the 1,000-line idiom limit).

Documentation:
- `docs/design/MARK_II_AREA_PLAN.md`: new section "M8a-2: the integrated split route" (route table, timing by
  directive, gate verdict, block RAM by owner, the firmware ledger at four points, the five largest BSS consumers
  with reduction options, reconciliation against 121.5 owner by owner, the bound-talker term and D7's
  close-out row, the all-fabric endpoint); Summary and Contents lines updated.
- `docs/design/MAILBOX_SPLIT.md`: the split image's identity (recipe, ident, manifest, the gate and its 12
  plants); Measured area: the term at one and two interfaces closed by D7 (a), and its read-back on the route's
  critical path; the Open-items entry for the term removed (closed).
- `docs/design/SPLIT_CONTROL_MEMORY.md`: no DDR3, main RAM or processor memory bridge in the split (D4); the
  regions list; the mapper's `--ledgered` in Reproduce.
- `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`: the full-split rom-bank inventory.
- `docs/testing/TESTING.md`: the memory test's mapper arm and its three mutants; the mutant count corrected to
  forty-seven (the base text said forty-four while the base table held 47).
- `docs/ENDSTATION_BUILDER.md` row 34a: the `--placement` recipe.

## New checks (planted mutant -> failing words)

Gate 23o (`sw/builder/test_builder.py:23862`, `test_placement_recipe`), 5 configs:
- a recipe that also changes the UART baud rate -> "the recipe's config differs from the file stating the key";
- a recipe that leaves the placement all-fabric -> the same words;
- `--write-rtl` / `--write-fragment` with `--placement split` -> "the split recipe writes no tracked file";
- an unknown placement `both` -> "placement recipe 'both' is not one of all-fabric, split".

Gate 23p (`sw/builder/test_builder.py:23707`, `test_image_identity_gate`): both good images pass, and
`--ctrl-mailbox --with-dram` is refused by "--ctrl-mailbox builds no DDR3". Twelve planted images, each failing
the gate by its kind:
- the split ident names no placement -> `FINDING ident: the ident '...' does not name the split placement`;
- the manifest records another VERSION -> `FINDING manifest: the manifest's VERSION 0x00030060 is not the image's milan_csr.sv 0x00020060`;
- the manifest records another mailbox minor -> `FINDING manifest: the manifest's mailbox contract {'major': 2, 'minor': 5} is not the image's KL_mbx_pkg.sv (2, 4)`;
- the split datapath built without `CTRL_SPLIT_P` -> `FINDING placement: a split image whose datapath has CTRL_SPLIT_P = 0`;
- a split image with DDR3 left in -> `FINDING ddr3: a split image carries DDR3: ddram pads, ddrphy, main_ram, sdram (decision D4 builds none)`;
- an all-fabric image with the mailbox -> `FINDING placement: an all-fabric image carries a mailbox ...`;
- the firmware relinked after the build -> `FINDING firmware: the control firmware ... has sha256 ..., the manifest records ...`;
- the manifest forged to the relinked firmware -> `FINDING firmware: the rom banks hold 3017 words that are not the 3017 rom words of ...`;
- the manifest removed from a split image -> `FINDING placement: an all-fabric image carries a mailbox ...`;
- a bitstream the manifest does not bind -> `FINDING bitstream: the manifest binds no bitstream, the image has [...]`;
- a bitstream other than the bound one -> `FINDING bitstream: ... binds {...}, the manifest records {...}`;
- the manifest's placement renamed -> `FINDING manifest: the manifest is schema 1 at placement 'all-fabric'; only a split image has a manifest, schema 1`.
The first six are planted in `milan_soc.py` and must also fail the build ("identity gate refuses it").

`test_ctrl_memory.py` mapper arm (`ctrl_memory_ledger.py:160`): facts and their mutants:
- facts: the platform's ledgered image refused without `--ledgered` (exit 2); mapped at 59.0 beside an image at
  exactly 56.0 planned with no override (exit 0); the override refused on another image and on a tag naming none
  (exit 2 each);
- mutant "the mapper's override ignored" -> "`--ledgered p=platform-8x8-two-interfaces` maps that image at 59.0
  RAMB36 ... (exit 2, {})";
- mutant "the mapper's override on every image" -> the same fact (exit 2, {});
- mutant "the mapper's stray override accepted" -> "the mapper refuses the platform-8x8-two-interfaces override
  whose tag names no image (exit 0)".

`pp_baseline_mutants.py`: "split rom banks read as complete images" and "every placement's rom banks read as
banks", each killed by `pp_baseline.py --selftest`'s bank arm.

## Measurements

Integrated split route (shipping 1x1 via the split recipe, exported at `5d6d2835`, M0s recipe `full-split`,
census: mailbox 1, gPTP 1, wrapper and the five engines 0; 66,578/66,578 nets routed):

| Directive | Slow WNS / WHS ns | Fast WNS / WHS ns | Setup endpoints < 0 | LUT | FF | Slice |
|---|---|---|---:|---:|---:|---:|
| ExtraPostPlacementOpt (recipe) | -0.078 / +0.065 | +1.687 / +0.030 | 11 | 29,277 | 39,060 | 12,767 |
| ExtraTimingOpt | +0.002 / +0.102 | +1.636 / +0.036 | 0 | 29,314 | 39,059 | 13,634 |
| AltSpreadLogic_high | -0.061 / +0.102 | +1.636 / +0.036 | 8 | 29,297 | 39,063 | 13,638 |

- Block RAM 56 RAMB36 / 32 RAMB18 = 72 tiles: firmware rom 25/1 and sram 12/0 (as the OOC mapping), mailbox 1/10,
  datapath 10/10, CPU 3/5, LiteX FIFOs 5/5, identifier 0/1. DSP 5, CARRY4 2,290, LUTRAM 1,035.
- Critical paths: LiteX AXI-Lite-to-Wishbone bridge state -> `KL_mbx/reg_rdata_r` through the bound-talker
  read-back (`rb_a_w`, `g_cmp[0].sr_r`, `bnd_eid_vld_w`), and `KL_mbx/u_rx/head_r` -> `u_{maap,aecp,srp}_rx` ring
  RAM. The 50 MHz datapath clock: +1.359 to +1.377 ns.
- Resource gate, split judged alone (`--placement full-split --shipping-selection`): rc 1, WNS below the floor and
  RAMB18 +5; a route set is refused for a selected split ("judged alone").
- All-fabric endpoint route at this head: 52,272 LUT, 54,108 FF, 15,843 slices, 74/27, 13 DSP, WNS +0.245 / WHS
  +0.027; gate rc 0 against `route-1x1`.
- Reconciliation (split vs the all-fabric route, tiles): BIOS -18, wrapper storage -17.5, mailbox +6, ctrl_split
  +1.5, CPU +1, DDR3 buffers -17, processor memory bridges' crossings -9, firmware +37.5 -> 72.
- Firmware ledger (planned / as mapped tiles): 1x1-1if 39.0 / 37.5; 1x1-2if 42.0 / 41.0; 8x8-1if 52.0 / 51.0;
  8x8-2if 59.0 / 57.5 (ledgered, owed to S14).
- Bound-talker term OOC (mailbox RTL = base): 1 if 285 LUT / 87 FF (WNS +0.151 / +0.231 tied); 2 if 682 / 159
  (WNS -4.715 / -2.667 tied, the 2-if mailbox misses 10 ns either way).
- M8a-2 runs: split boot to ready at 1x1 (84.4 ms) and 8x8, 0 findings; `check_nvm_capture.py` PASS;
  `nvm_split_target --point 8x8` all cases pass with its controls caught; `nvm_cosim` 465/465;
  `nvm_capture_cpu` 8x8 at 50 MHz, 16 captures each, traffic on 13.85-13.86 ms and off 13.62-13.68 ms, 0 mismatches.

## Gate table (final head, clean clones)

Every row at `ad2ed0e3ab3daa9697bdf42ae504b4504bfd04aa`, each on its own clean clone, rc as its log shows. Receipts:
`receipts/gates/`, `receipts/ci/`, `receipts/sweep/` (index `receipts/INDEX.md`).

| Gate | Command | Result |
|---|---|---|
| CI replay, every `run:` step of every job a ready pull_request to dev-soft-core triggers | `ci_replay.py` over docs.yml (9 jobs), elaborate.yml (6), rtl-fast.yml (17, the firmware jobs incl. firmware-boundary and firmware-verilator), rtl.yml (37) | 69/69 instances success; 497 run steps rc 0, 0 failed or missing; 110 not run, each with its reason in `receipts/ci/not_run.json` (APT resolution 41, tool builds into /opt 27, the 19 hosted sweep workers' suite step 19 and the 9 steps reconciling their uploads, both covered by the sweep below, GitHub API 13, physical-gptp's schedule-only job 1) |
| docs.yml, the 829 verifier | `verify_docs_yml.py ad2ed0e3 <root>` on the replay's docs.yml results (`tools/docsyml/`) | rc 0: 88 steps ran rc 0, 7 not run with a reason, 0 bad |
| Full sweep, 4 native shards | `scripts/run_all_suites.sh <logs> --wait --shard k/4`, MAKEFLAGS `-j4 --no-print-directory`, one clone and unit each (MemoryMax 10G) | shard 0 (64-71): 15/15 suites, 360,992 checks, rc 0; shard 1 (40-47): 17/17, 1,526,104 checks, rc 0; shard 2 (56-59, 4 CPUs, holds capture_coherence): 17/17 suites (capture_coherence among them), 284,228 checks, rc 0; in all 65/65 suites, 2,192,899 checks, 0 in-suite failures; shard 3 (40-47): 16/16, 21,575 checks, rc 0. No preflight failure (#833 did not arise) |
| Firmware self-test | `test_ctrl_firmware.py --require-rv32 --self-test`, as rtl-fast's four shards 0/4 to 3/4 (firmware-unit, -control-mutants, -aecp-mutants, -srp-mutants) | each `test_ctrl_firmware: PASS`, rc 0; control shard `mutants: 570 of 570 caught` |
| Firmware mutant drivers | the four shards above (every driver runs in its shard) | rc 0 each |
| fw_coverage | `fw_coverage.py --selftest`; `fw_coverage.py --check` (firmware-unit) | rc 0; `firmware coverage: PASS (35 files)` |
| Boundary | `ctrl_boundary.py --require-rv32 --selftest --without verilator` / `--only verilator`, LiteX venv | rc 0 each, `ctrl_boundary: PASS` |
| S2's harness | `ctrl_service_budget/run.py --self-test`; `--point 1x1` (1 if) and `--point 8x8` (2 if) `--record-budget-findings` | rc 0 each; 1x1: 18 groups graded, 0 refusals, 34 T_svc misses (34/141 probes, 13/81 paths); 8x8: 17 groups, 0 refusals, 63 misses (63/182, 31/129). Both tallies equal the base `1d6bf555`'s (another lane's receipt at that base) |
| test_builder | `test_builder.py --require-rv32` (standalone), and the builder legs 0 and 1 in docs.yml and elaborate.yml | rc 0 each |
| behave | `cd tests && behave --no-capture -f plain` (bdd-conformance) | rc 0; 14 features, 508 scenarios, 2,330 steps passed |
| git diff --check | `git diff --check 1d6bf555 ad2ed0e3` | rc 0 |
| Lane gates | `test_ctrl_memory.py`; `ctrl_split_boot/run.py` at 1x1 and 8x8 | rc 0 each |
| All-fabric endpoint | the 1x1 and 8x8 exports against the base's (`tools/endpoint_compare.py`) | 21/21 files identical at each shape, rc 0 |

Attempts, as their logs show (every attempt kept under `receipts/ci/attempts/`):
- `elaborate-gates-1`: five attempts. 1 (15:13 to 16:06) and 3 (18:13 to 19:24): 17 of the 18 run steps rc 0, and `gate_19` rc 92, where
  `run_litex_sims.sh` timed `test_soc_timing_cuts` out at its 900 s wall clock ("result UNKNOWN, not a failure"; the
  other seven simulations passed), on the session pool at load 100 to 185. 2: killed by the 17:00 reset. 4 (in its
  own unit): `ci_step_14` rc 1, github.com unreachable from the host for 135 s during the VexiiRiscv submodule fetch.
  5 (its own unit, 64-71): success, `gate_19` 8/8 simulations passed. The elaborate aggregator failed while
  gates-1 had (`ci_step_6`, "Require every gate exactly once"), then passed after attempt 5.
- `test_soc_timing_cuts.py` alone, to tell host load from a regression: at the head 16:17-16:49 rc 0 in 1,911 s;
  then base `1d6bf555` and head together on clean clones under the same load: base rc 0 in 1,702 s, head rc 0 in
  1,774 s. The test file is unchanged and builds no split image.
- `firmware-boundary`, `firmware-control-mutants`, `firmware-verilator`, `verilator-shards 0`: killed by the reset,
  re-run, success.
- The four `ci-cancel-tail` jobs were re-run once the replay's override was narrowed to the GitHub-API cancel step
  (step2), so their "Set CPU-derived job budgets" step runs (rc 0) rather than being listed as not run.
- The first 8x8 endpoint compare (14:55) exported with the 1x1's place directive and differed in its flow file; it
  was re-run with each shape's own flow flags (`sw/litex/build.sh:380` and `:391`, as the base exports used): rc 0.
- The sweep: native-shards.py takes all four CPU ranges at once, and the host had none free after the reset, so each
  shard was launched exactly as native-shards.py launches one (`tools/sweep-shard.py`) on the range
  `cpu_ranges.py pick` gave as ranges freed (`tools/sweep-watch.py`), MemAvailable above 30 GB throughout.

## Open items / STOP lines

- **STOP, decision needed (acceptance 1).** Options: (a) a mailbox timing change in a lane that owns `KL_mbx*`
  (register the host read data, or the bound-talker read-back, and the receive block's ring write address), then
  re-route S9; (b) a register stage on the mailbox's bus window in `milan_soc.py` (one more cycle per mailbox
  access, which the firmware's service budget would need to re-measure); (c) an owner exception to the +0.030 ns
  floor at +0.002 ns. D7 (a) was ruled on area; the term's read-back is on this critical path, which (a) and (b)
  would address.
- Found, not fixed: the ledger's conditional total (115.5) never credited the 26 tiles of DDR3 and bridge
  buffers; the new section reconciles it but leaves the old table as recorded.
- `nvm_split_target` 8x8 and `check_nvm_capture` ran at `e16c1343`, the split boots at `e16c1343` too: the later
  commits change none of their inputs (`git diff --stat e16c1343 ad2ed0e3` lists only pp_baseline, the identity
  gate's message, the OOC mapper and its test, and docs); the boots re-ran at the final head in the gate pass.
- Scratch removed after the gate pass (no receipt cites their contents; every log a receipt names was copied first):
  the four sweep clones, the standalone gates' clones and the boot and budget build trees. Kept: the route, OOC,
  ledger, M8a-2 and replay logs.
- Posted on #870: TAKEN (05:17Z, issuecomment-6759671811) and STOP with this head (issuecomment-6779583701); nothing else, nothing edited.
