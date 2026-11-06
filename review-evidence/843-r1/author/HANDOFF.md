# [A737] HANDOFF: milan-fpga #843, adopt FPGA-gPTP main 1616fc8f, clockAccuracy per board

Status: REVIEW READY at head `1105f54546b2f19d9577b7fad902c908e34f88ee` (2026-11-06 09:45), with two open decisions: the shipping route misses the +0.03 ns build floor and the resource gate refuses it (owner decision), and issue item 4 waits on PR #842. Every gate is rc 0 at the head (the sweep's shard 2 after one uncontended re-run; both runs recorded). Nothing pushed; live remote dev is still `cc204c6f`.

- Repository: kebag-logic/milan-fpga (origin `https://github.com/kebag-logic/milan-fpga.git`, checked)
- Branch: `843-adopt-gptp-1616fc8f`, from dev `cc204c6fd2349b543d73f15c97162a2c4434c86e` (merge base checked; live remote dev was still `cc204c6f` at 01:30)
- Base: `cc204c6fd2349b543d73f15c97162a2c4434c86e`
- Head: `1105f54546b2f19d9577b7fad902c908e34f88ee` (8 commits)
- gptp-processor gitlink: `135afd043309369a87ddbc8d6550aff8ec52a157` -> `1616fc8f062fbf58c35ad31674b5b233207bbdb8` (FPGA-gPTP main, the merge of PR #101; `135afd04` is its ancestor; its tree equals the reviewed PR #101 head `84fd227`). Before every git command in the submodule, `git -C gptp-processor rev-parse --show-toplevel` was that directory and its origin `https://github.com/Mister-M-alt/FPGA-gPTP.git`.
- Issue posts: TAKEN issuecomment-6673278240; REVIEW READY issuecomment-6680794161 (text: `review-ready.md`).

## Commits

| Commit | Subject |
|---|---|
| `070f8181c1` | Move the gptp-processor gitlink to FPGA-gPTP main 1616fc8f and re-record the pin-derived records: ROM digest, boundary and time-sync diagrams, donor links (#843) |
| `c49e85b44f` | Pass each config's gptp.clock_accuracy to the engine generator's --clock-accuracy, 0x22 for the AX7101 and 0xFE for the Arty, and grade each image and descriptor per board (802.1AS-2011 8.6.2.3, #843) |
| `3c28bb1026` | Make the gptp and gptp-lat leg images from the AX7101 and Arty configs through the builder's options and grade clockAccuracy 0x22 and 0xFE in the DUT's own Announce (#843) |
| `8210abaa1f` | Take OUR_CQ from the generator each gPTP harness builds with and grade it in the plane's own grandmaster Announce (#843) |
| `fe991ee120` | State the config's clockAccuracy in the ROM clock contract's independent generator run (#843) |
| `8a68377c85` | Record the gPTP 1616fc8f adoption, clockAccuracy per board and the shipping route against dev: 701 LUTs, 187 FFs and two DSPs more, 4 of 15,850 slices, +0.018 ns slow-corner WNS under the +0.03 ns floor (#843) |
| `4c4c598273` | Regenerate the documentation inventory through docs_inventory.py at the #843 head |
| `1105f54546` | Re-measure the service-budget traces on both AX7101 shapes and regenerate oracle.json through gen_oracle.py, the flash media now carrying clockAccuracy 0x22 (#843) |

## Scope and acceptance, item by item

| Item | State | Evidence |
|---|---|---|
| Gitlink to `1616fc8f` | done | `070f8181c1`; `git submodule status` |
| Required 1: clockAccuracy per board; builder passes `gptp.clock_accuracy` to `--clock-accuracy` and relaxes its pin | done | `endstation_builder.py:3567`, `:3705`, `:3717`, `:4233`, `:5983`; gates 1b, 26b, 26c |
| Required 1: AX7101 `0x22` | done (both AX7101 configs: one board, one oscillator) | `configs/endstation_ax7101_1x1_tdm8.yaml:98`, `configs/endstation_ax7101_8x8.yaml:116` |
| Required 1: Arty `0xFE` | done (stated explicitly in all three) | `configs/endstation_arty_4x4.yaml:200`, `_8ch.yaml:222`, `_current.yaml:242` |
| Required 1: comments at `:3561`, `:4153`, `:4165-4168` | done; neither "consumes only" nor "announces this field from a constant" remains (grep rc 1) | `endstation_builder.py:3561-3567`, `:4197-4205`, `:4211-4217`; docstring `:3655-3664` too |
| Required 2: ROM digests re-recorded through their recorder | done: `syn/yosys/ooc.sh --record-rom-digests`; the new row equals the donor's tracked `syn/ooc/work/gptp_ucode.hex` | `syn/yosys/rom_digests.tsv` (`1616fc8f ... e83709d9...`) |
| Required 2: model-shape pins re-pinned where clock_accuracy moves them | none to move: the Arty configs announced 0xFE before and after, so the pinned arty_current and arty_4x4 hashes stay (`0x001BC5E4438F5B7B`, `0x001BC549808B210C`, gate pins unchanged and green); the AX7101 hash-derived ids move (1x1 `0x001BC5C1935893E1` -> `0x001BC5CD179523AB`, 8x8 `0x001BC5572467AF35` -> `0x001BC5F6CB4A37D1`) and no test pins them | builder bank |
| Required 3: `OUR_CQ` in gptp_shadow and gptp_plane | done: taken from the build (the Makefiles read the generator's `CQ_C`), and each harness now grades it in the plane's own grandmaster Announce | below |
| Required 4: stricter-readings page points at the merged behaviour | **NOT MET here**: the page (`docs/reference/STRICTER_READINGS.md`) is introduced by PR #842 and does not exist on dev `cc204c6f`. Creating it here would collide with #842. The replacement text is prepared: `stricter-readings-gptp.patch` (against #842's `dd764ed7`) and `stricter-readings-gptp-section.md` in this directory | - |
| Acceptance 1: sweep with milan_dp gptp and gptp-lat, gptp_shadow, gptp_plane, firmware self-test, builder, behave, docs gates green; inventory regenerated | see gate table | `4c4c598273` regenerates the inventory |
| Acceptance 2: a builder test with a 0xFE config and one with a 0x22 config each produce that value on the wire in the gPTP leg | done | gate 26c; milan_dp `gptp` (AX7101 config, 0x22) and `gptp-lat` (Arty config, 0xFE) |
| Acceptance 3: area and timing of the shipping route recorded against dev | done, and **the result needs an owner decision** (section "Area and timing") | `SUBMODULES.md:439`, `CHANGELOG.md:102`, `AREA_BUDGET.md:151` |

## Parent-side items from the FPGA-gPTP PR #101 reviews

| Item | Where answered |
|---|---|
| R777-1 S5 / R778-1 P2: every parent build announced 0x22 and none could select 0xFE | the builder passes `gptp.clock_accuracy` per config (`endstation_builder.py:3705-3714`, `:4233`); Arty 0xFE, AX7101 0x22; gate 26c and the two legs |
| R777-1 R2 / R778-1 P4: builder wording "consumes only", "announces this field from a constant", clockQuality a constant | `endstation_builder.py:3561-3567`, `:3655-3664`, `:4197-4205`, `:4211-4217`; the reviews' suggested parenthesis ("is not passed by this builder") no longer applies, since the builder now passes it |
| R778-1 S5: `OUR_CQ` in gptp_shadow and gptp_plane no longer held the engine's clockQuality | taken from the generator in both Makefiles, and graded in each plane's own grandmaster Announce |
| A733 companion patch (configs 0x22, built-in spec 0x22, two Arty hash re-pins) | re-derived for per-board accuracy: only the AX7101 configs move to 0x22; the built-in spec models the Arty and stays 0xFE; no hash pin moves |

## Changes (file:line at the head, clause)

| File:line | Change | Clause |
|---|---|---|
| `gptp-processor` | gitlink `135afd04` -> `1616fc8f` (FPGA-gPTP #98/PR #99, #100/PR #101) | 802.1AS-2011 11.4.1, 10.2.8.2.1 i)-l), 10.2.9, 11.4.4.3, 10.3.9.1, 8.6.2.3; Milan v1.2 4.2.6.2.3, 4.2.6.2.6 |
| `syn/yosys/rom_digests.tsv` | gPTP row for `1616fc8f`, through `ooc.sh --record-rom-digests` | - |
| `docs/diagrams/submodule_boundaries.*`, `timesync_chain.*`, `PNG_MANIFEST.json` | regenerated through their `.gen.py` | - |
| `docs/design/GPTP_PLANE.md`, `TIME_SYNC.md`, `docs/guides/gptp/*.md`, `docs/reference/SUBMODULES.md:24`, `docs/traceability/ieee8021as.md` | donor links and the pin row at `1616fc8f` (`check_gptp_docs.py`, `check_submodule_docs.py`) | - |
| `sw/builder/endstation_builder.py:3561-3567` | `GPTP_ENGINE_CONSUMED = ("priority1", "clock_accuracy")`, comment corrected | 802.1AS-2011 8.6.2.3 |
| `sw/builder/endstation_builder.py:3569-3577` | `GPTP_CLOCK_ACCURACY_UNKNOWN = 0xFE`; `GPTP_CLOCK_ACCURACY_VALUES` = Table 6's 0x20..0x31 and 0xFE | 802.1AS-2011 8.6.2.3 b); IEEE 1588-2008 7.6.2.5, Table 6 |
| `sw/builder/endstation_builder.py:3654-3702` | `gptp_engine_pins()` no longer returns clock_accuracy; docstring corrected | 802.1AS-2011 8.6.2.3 |
| `sw/builder/endstation_builder.py:3705-3714` | `gptp_ucode_args(cfg)`: the generator options (MAC, priority1, clock, `--clock-accuracy`), one list for the build and the legs | 8.6.2.3 |
| `sw/builder/endstation_builder.py:3717-3733` | `_gptp_clock_accuracy_key()`: default 0xFE, refusal outside Table 6 | 8.6.2.3 b); 1588-2008 7.6.2.5 |
| `sw/builder/endstation_builder.py:4197-4217`, `:4233`, `:5978-5984` | comment and refusal message corrected; clock_accuracy resolved from the config; the build passes `gptp_ucode_args()` | - |
| `configs/endstation_ax7101_1x1_tdm8.yaml:82-98`, `configs/endstation_ax7101_8x8.yaml:100-116` | `clock_accuracy: 0x22` with its reason | 8.6.2.3 a); 1588-2008 Table 6 (0x22, 250 ns) |
| `configs/endstation_arty_{4x4,8ch,current}.yaml` (`:200`, `:222`, `:242`) | `clock_accuracy: 0xFE` with its reason; stale "consumes only priority1" comment corrected | 8.6.2.3 b) |
| `avdecc/aem_specs.py:89-92`, `avdecc/aem_descriptors.py:331-338` | comments: the built-in arty spec's 0xFE is the arty config's own; clockAccuracy is passed per image | 1722.1-2021 7.2.8 |
| `docs/ENDSTATION_BUILDER.md:1067-1068` | row 31a `gptp.clock_accuracy`; row 32 no longer lists it | 1722.1-2021 7.2.8; 8.6.2.3 |
| `sw/builder/test_builder.py:361-366` | `GPTP_CLOCK_ACCURACY_BY_BOARD` | 8.6.2.3 |
| `sw/builder/test_builder.py:17970-17978`, `:17996-18004` | gate 1b: a clockAccuracy mutation must reach the image; clock_accuracy left the refused (pinned) set | - |
| `sw/builder/test_builder.py:26480-26505`, `:26508-26601` | gate 26b: per-board clockAccuracy in AVB_INTERFACE bytes 86..96 (helper `_assert_avb_interface_is_the_wire`), consumed set and `--clock-accuracy` in the generator, omitted key -> 0xFE; the parser fixture no longer returns clock_accuracy | 1722.1-2021 7.2.8; 8.6.2.3 b) |
| `sw/builder/test_builder.py:26604-26698`, `:29730` | new gate 26c `test_gptp_clock_accuracy_per_board` | 8.6.2.3; 1588-2008 7.6.2.5 |
| `sw/builder/test_clock_contract.py:141-146` | the independent ROM-clock run states the config's clockAccuracy | - |
| `tb/verilator/milan_dp/gen_gptp_leg_ucode.py` (new) | a leg image from a config through `gptp_ucode_args()`, with the leg's 2 MHz clock, 3000 ms cease and default MAC; refuses a builder option set it does not know | - |
| `tb/verilator/milan_dp/Makefile:445-461`, `:479`, `:527-530`, `:536-543`, `:739`, clean | `GPTP_LEG_CONFIG`/`_ACCURACY` (AX7101, 0x22) and `GPTP_LAT_CONFIG`/`_ACCURACY` (Arty, 0xFE); `gptp-lat` runs `gptp_lat_ucode.hex`; `-DGPTP_CLOCK_ACCURACY_TB` | - |
| `tb/verilator/milan_dp/sim_gptp.cpp:56-65`, `:2060-2086`, `:2126` | `[CA]` check: every DUT Announce's grandmasterClockQuality octet 63 is the leg's clockAccuracy | 802.1AS-2011 10.5.3.2.3, Table 10-7 |
| `tb/verilator/milan_dp/README.md:91-92`, `.gitignore` | leg table rows; ignore `gptp_lat_ucode.hex` | - |
| `tb/verilator/gptp_shadow/Makefile:9-13`, `:22`; `sim_main.cpp:45-52`, `:1445-1473` | `OUR_CQ` from the generator (`-DOUR_CQ_TB`); master phase grades every Announce's clockQuality | 10.5.3.2.3 |
| `tb/verilator/gptp_plane/Makefile:6-11`, `:18`, `:36`; `sim_main.cpp:49-56`, `:506-545` | `OUR_CQ` from the generator; grandmaster phase grades the Announce's clockQuality | 10.5.3.2.3 |
| `CHANGELOG.md:13`, `:102-124`; `docs/reference/SUBMODULES.md:439-494`; `docs/design/AREA_BUDGET.md:151-154` | adoption records and the route figures against dev | - |
| `docs/DOCUMENTATION_AUDIT.md` | regenerated by `scripts/docs_inventory.py --write` | - |

## New checks, planted mutants, failing words

Every mutant ran in a clean clone of `8210abaa` (`mutants.py`, receipts `receipts/mutants-8210abaa/`); each check named below failed with the words shown, and the clone was clean after (`tree_after` empty). `fe991ee1` and later change no file a mutant touched except docs and `test_clock_contract.py`.

| # | Planted mutant (file) | Check run | rc | Failing words |
|---:|---|---|---:|---|
| MB1 | the builder passes `--clock-accuracy 0x22` for every config (`endstation_builder.py`) | gate 26c | 1 | `gate 26c: arty_current passes --clock-accuracy 0x22, its board decided 0xFE` |
| MB1 | same | `make -C tb/verilator/milan_dp gptp-lat` | 2 | `FAIL [CA] every DUT Announce carries the config's clockAccuracy got 0000000000000004 exp 0000000000000000` |
| MB1 | same | gate 1b | 1 | `clockAccuracy: mutation did not reach gptp_ucode.hex` |
| MB2 | the builder passes no `--clock-accuracy` | gate 26c | 1 | `gate 26c: ax7101_1x1_tdm8's generator options [...] carry no --clock-accuracy` |
| MB3 | an omitted key resolves to 0x22 | gate 26b | 1 | `omitted gptp.clock_accuracy resolved to 0x22, 802.1AS-2011 8.6.2.3 b) says 0xFE` |
| MB4 | any octet is accepted | gate 26c | 1 | `gate 26c: gptp.clock_accuracy 0x0 was ACCEPTED` |
| MB5 | the descriptor takes 0x22, not the config | gate 26b | 1 | `arty_4x4: gptp.clock_accuracy 0x22, the board's decided value is 0xFE (#843)` |
| MH1 | gptp_shadow's `OUR_CQ` is the old literal 0xF8FE436A (`Makefile`) | `make -C tb/verilator/gptp_shadow run` | 2 | `FAIL as master: every Announce carries this image's clockQuality got 0000000000000001 exp 0000000000000000` |
| MH2 | gptp_plane's `OUR_CQ` is the old literal | `make -C tb/verilator/gptp_plane run` | 2 | `FAIL grandmaster Announce carries this image's clockQuality got 00000000f822436a exp 00000000f8fe436a` |
| ML1 | the gptp leg runs the Arty image while expecting 0x22 (`milan_dp/Makefile`) | `make -C tb/verilator/milan_dp gptp` | 2 | `FAIL [CA] every DUT Announce carries the config's clockAccuracy got 0000000000000004 exp 0000000000000000` |

The unmutated legs: `gptp` 212 checks (210 at dev plus 2), `[CA] 4 DUT Announce frame(s); last clockQuality 0xF822436A`; `gptp-lat` 212 checks, `last clockQuality 0xF8FE436A`; gptp_shadow 326 (325 + 1); gptp_plane 31 (29 + 2).

## Gate table (head `1105f54546b2f19d9577b7fad902c908e34f88ee`, each on a clean clone)

Environment: pinned Verilator 5.050, sv2v 0.0.12, GNU Make 4.3, `MAKEFLAGS=-j4 --no-print-directory`, `TSN_GEN_ROOT` set (so tsn_fuzz ran its tsn-gen campaigns), the RV32 SDK on PATH for `--require-rv32`. CPU ranges: this lane's own booking 64-79 (`cpu_ranges.py pick` found no free range at launch); MemAvailable at launch 56 GB. No Vivado route ran beside either sweep.

| Gate | Command | rc | Result | Receipt |
|---|---|---:|---|---|
| Full sweep, 4 shard units | `native-shards.py` over `bash scripts/run_all_suites.sh <logs> --wait --shard k/4`; shards on 64-67, 68-71, 72-75 (capture_coherence), 76-79 | 0, 0, **92**, 0 | shard 0: 15/15 suites, 361,125 checks; shard 1: 17/17, 1,525,512; shard 3: 16/16, 21,575; shard 2: 16 passed, 0 failed, **1 timed out: `capture_coherence` at its 2,400 s wall-clock limit** ("result UNKNOWN, not a failure"), killed while running its mutants, with the lane gates, docs.yml and the dev attribution run sharing those CPUs; fw_service_budget and gptp_plane PASS; 0 in-suite failures in every shard; preflight passed first time in all four (no #833 re-run) | `receipts/sweep-1105f545/` |
| Shard 2 re-run alone | the same command, `--shard 2/4`, 72-75, nothing else of this lane running | 0 | 17/17 suites, 284,230 checks, 0 failed, 0 timed out, 0 in-suite failures; capture_coherence 42 PASS; fw_service_budget and gptp_plane PASS; 5,480 s, peak 6.4 GB | `receipts/sweep-1105f545/shard-2-rerun/` |
| milan_dp gptp / gptp-lat (shard 0) | in `make -C tb/verilator/milan_dp` | 0 | `[CA] 4 DUT Announce frame(s); last clockQuality 0xF822436A, expected clockAccuracy 0x22`, 212/212; `... 0xF8FE436A, expected clockAccuracy 0xFE`, 212/212 | shard-0 `milan_dp.log` |
| gptp_shadow (shard 1) | `make -C tb/verilator/gptp_shadow` (lifecycle, mutants, run) | 0 | 326 PASS | shard-1 |
| gptp_plane (shard 2) | `make -C tb/verilator/gptp_plane` | 0 | 31 PASS; phc_step 62; campaign 8 | shard-2 |
| fw_service_budget (shard 2, and alone) | `make -C tb/verilator/fw_service_budget` | 0 | oracle 55 checks, flash 14 checks, 0 failures | shard-2; `receipts/final-gates-1105f545/` |
| Firmware self-test | `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` | 0 | saved-state writer gate OK across 5 shapes | `receipts/final-gates-1105f545/` |
| Coverage | `python3 sw/firmware/gtest/fw_coverage.py --check --jobs 8`; `--selftest` | 0; 0 | PASS (30 files); 29 of 29 | same |
| Builder | `python3 sw/builder/test_builder.py --require-rv32` | 0 | ALL GATES PASS EXCEPT 2 NOT RUN: gate 1b's `MAKEFLAGS += -e` arm (this make does not re-read MAKEFLAGS mid-parse) and gate 11 (the calibration build tree is not on this machine); the same two at dev and in earlier lanes | same |
| behave | `cd tests && behave` | 0 | 14 features, 508 scenarios, 2,330 steps passed | same |
| docs.yml | every `run:` step of all nine jobs, each job on a fresh clone (the #829 runner and verifier, lane paths; `docs-gates-0/ci_step_55` added to the hosted-record reasons) | 0 | verifier: 65 steps rc 0, 31 not run with their recorded reason, 0 bad; every clone clean after | `receipts/docs-yml-1105f545/` |
| Docs inventory | `python3 scripts/docs_inventory.py --check`; `--selftest` | 0; 0 | fresh (540 lines); 50 controls | `receipts/final-gates-1105f545/` |
| Whitespace | `git diff --check cc204c6fd2349b543d73f15c97162a2c4434c86e HEAD` | 0 | no output | same |
| Lint | `python3 scripts/lint_rtl.py --check` | 0 | 89 <= 89 | same |
| Em dash | `scripts/check_em_dash.py --base cc204c6f` | 0 | 0 findings | same |
| Vivado front-end | `python3 scripts/xvlog_gate.py --check`, through `vivado-slot.sh` | 0 | 0 findings; pinned at `gptp-processor@1616fc8f` | same |
| Physical gPTP suite | `make -C tb/verilator/milan_dp_gptp` at `4c4c5982` (`4c4c5982..1105f545` changes only `oracle.json`, which nothing it builds reads) | 0 | physical 151 checks, setup abort 6, no-TX 20, no-Pdelay 14, recentre 14, 0 failures; 5,673 s | `receipts/physical-gptp-4c4c5982/` |
| Shipping route | recipe as above, dev and `8210abaa` | 0, 0 | see "Area and timing" | `receipts/route-dev/`, `receipts/route-head/` |
| Mutants | `mutants.py` at `8210abaa` | - | 8 of 8 caught by name in 10 runs | `receipts/mutants-8210abaa/` |
| Service re-measure | `svc_driver.sh`, `gen_oracle.py` at `4c4c5982` | 0 | see "Service-budget re-measure" | `receipts/service-budget-4c4c5982/` |

### Superseded run at `4c4c598273904f6c994b75c860e74ac742ae49d2`

| Gate | rc | Result | Receipt |
|---|---:|---|---|
| Full sweep, 4 shard units (`native-shards.py`, `MAKEFLAGS=-j4 --no-print-directory`, pinned Verilator 5.050, sv2v 0.0.12, Make 4.3; shards on 48-55, 56-63, 64-67 (capture_coherence), 68-75) | 0, 0, **1**, 0 | shard 0: 15/15 suites, 361,125 checks; shard 1: 17/17, 1,525,512; shard 2: 16/17, **`fw_service_budget` failed**: "oracle image changed; rebuild and regenerate the trace fixture"; shard 3: 16/16, 21,575; 0 timed out, 0 in-suite failures; preflight passed first run in all four (no #833 re-run needed) | `receipts/sweep-4c4c5982/` |
| milan_dp `gptp` / `gptp-lat` (inside shard 0) | 0 | `[CA] 4 DUT Announce frame(s); last clockQuality 0xF822436A` / `0xF8FE436A`; 212 / 212 PASS | shard-0 `milan_dp.log` |
| gptp_shadow (shard 1), gptp_plane (shard 2) | 0, 0 | 326 PASS; 31 PASS, phc_step 8 PASS | shard logs |
| `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` | 0 | saved-state writer gate OK across 5 shapes | `receipts/final-gates-4c4c5982/` |
| `python3 sw/firmware/gtest/fw_coverage.py --check --jobs 8`; `--selftest` | 0; 0 | PASS (30 files); 29 of 29 planted cases | same |
| `python3 sw/builder/test_builder.py --require-rv32` | 0 | ALL GATES PASS EXCEPT 2 NOT RUN (gate 1b's MAKEFLAGS arm on this make; gate 11 needs the absent calibration tree), the same two as on dev | same |
| `cd tests && behave` | 0 | 14 features, 508 scenarios, 2,330 steps passed | same (log 442,503 B kept as tail + sha256) |
| every `run:` step of `.github/workflows/docs.yml` (runner and verifier from the #829 receipts, paths pointed at this lane, the hosted-record step id updated to `ci_step_55`) | 0 | verifier: 65 steps rc 0, 31 not run with their recorded reason, 0 bad; every clone clean after | `receipts/docs-yml-4c4c5982/` |
| `python3 scripts/docs_inventory.py --check`; `--selftest` | 0; 0 | fresh (540 lines); 50 controls | `receipts/final-gates-4c4c5982/` |
| `git diff --check cc204c6f HEAD` | 0 | no output | same |
| `python3 scripts/lint_rtl.py --check` | 0 | 89 <= 89 | same |
| `scripts/check_em_dash.py --base cc204c6f` | 0 | 0 findings over 23 added lines | same |
| `python3 scripts/xvlog_gate.py --check` (Vivado front-end, through `vivado-slot.sh`) | 0 | 0 findings; "pinned at: protocol-processor@a9e84b66; gptp-processor@1616fc8f" | same |

The `fw_service_budget` failure is this adoption's: its oracle binds the sha256 of each AX7101 shape's built flash media, and that media carries the AVB_INTERFACE descriptor, whose clockAccuracy octet is now 0x22. The fix is the suite's own procedure (README "Regenerate the fixture through its generator"): fresh populated `all` runs on both shapes and `uart-paced` on the 1x1, then `gen_oracle.py`. PR #842 regenerates the same file for its identity change; whichever lands second re-measures.

## Area and timing (route-1x1, the shipping AX7101 1x1 export)

Recipe: `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`, unchanged: `build.sh ax7101 --dry-run`, its `milan_soc.py` argv without `--build`, `pp_baseline.py --single-thread-synthesis`, Vivado 2026.1 through `vivado-slot.sh`, the shipping directive `place_design -directive ExtraPostPlacementOpt` only (as assigned), default seed. Each in its own clean clone and its own unit (MemoryMax 12G, CPUs 64-79, this lane's booking), one at a time; no sweep ran beside either. dev `cc204c6f`: Vivado rc 0, 00:38:11Z-01:26:16Z. Head `8210abaa`: Vivado rc 0, 01:26:50Z-02:16:59Z. `8210abaa..4c4c5982` changes `test_clock_contract.py`, three documents and the inventory: no synthesis input. Figures read by the gate's own parser, `pp_resource_gate.py check <dir> --endpoint route-1x1 --shipping-selection`. Receipts: `receipts/route-dev/`, `receipts/route-head/`.

| Figure | dev `cc204c6f` | head (gPTP `1616fc8f`) | change | gate vs the twelfth record |
|---|---:|---:|---:|---|
| LUT | 51,994 | 52,695 | +701 | REGRESSION (+683, tolerance 500) |
| FF | 54,101 | 54,288 | +187 | ok (+581, tolerance 600) |
| Slice (of 15,850) | 15,841 (9 free) | 15,846 (4 free) | +5 | ok (+66, tolerance 80) |
| RAMB36 / RAMB18 | 74 / 27 | 74 / 27 | 0 | ok |
| DSP | 13 | 15 | +2 | REGRESSION (+2, tolerance 0) |
| WNS, Slow 0C / 85C | +0.236 ns | +0.018 ns | -0.218 ns | REGRESSION: below the +0.03 ns floor |
| WNS, Fast corners | +1.633 ns | +1.526 ns | -0.107 ns | - |
| WHS, Slow / Fast | +0.077 / +0.036 ns | +0.065 / +0.015 ns | -0.012 / -0.021 ns | ok |
| Route status | complete, 0 errors | complete, 0 errors | - | - |
| Gate verdict | PASS (rc 0) | MATERIAL REGRESSION (rc 1) | - | - |

Post-synthesis the engine change is +711 LUT as logic, +186 registers and +2 DSPs (the TLV frequency multiply, as FPGA-gPTP #100's OOC figures predicted: +475 LUTs, +159 FFs, +2 DSPs out of context).

Worst setup path at the head (Slow 0C): `milansoc_sdram_bankmachine0_pipe_valid_source_payload_addr_reg[8]` -> `milansoc_sdram_twtrcon_count_reg[0]/R`, 16 logic levels, 9.488 ns data path (6.448 ns routing): the SoC's SDRAM controller, outside the gPTP engine and `milan_datapath`. At dev it is the VexiiRiscv DMA write bridge (+0.236 ns, 18 levels). So the fall is placement pressure at 15,846 of 15,850 slices, not a new engine path.

This is a decision for the owner, not something this lane can settle: the #814/#818 ruling judges WNS on the best of the recipe's three directives, and the other two (AltSpreadLogic_high, ExtraTimingOpt) were not routed because the assignment named one directive. The LUT and DSP rows refuse whatever the directive. Every corner has positive slack and no failing endpoint; only the +0.03 ns build floor is missed.

## Service-budget re-measure (`1105f54546`)

`tb/verilator/fw_service_budget/oracle.json` binds each AX7101 shape's flash media by sha256. The media carries the AEM image, whose AVB_INTERFACE clockAccuracy octet is now 0x22, so the oracle had to be re-measured (the suite's README, "Regenerate the fixture through its generator"). Steps (the #840 lane's driver, unchanged): in a clean clone of `4c4c5982`, each shape built, populated `all` on both and `uart-paced` on the 1x1, in a network namespace with the product environment; then `gen_oracle.py --small-build ... --large-build ...`, which validated builds, logs, images and grading before writing. Runs: 1x1 build 31 s, 1x1 `all` 13.5 min, 1x1 `uart-paced` 16 min, 8x8 `all` 88 min, each rc 0. `make -C tb/verilator/fw_service_budget` then: 55 checks, 0 failures. Receipts: `receipts/service-budget-4c4c5982/`.

| Trace | Verdict, dev oracle | Verdict, re-measured |
|---|---|---|
| 1x1 `all` | budget findings: none | none |
| 8x8 `all` | `over-budget duty: milan_nvm` x2 | the same two |
| 1x1 `uart-paced` | none | none |

Every graded row moved slightly. The first divergence in the raw log is the BIOS SPI-flash "Random" read-speed probe (451.5 KiB/s at the dev oracle, 447.3 KiB/s now), before any firmware runs. The AEM copy, also a flash read, rises by the same ~0.7 % (1x1 330.04 -> 332.46 ms; 8x8 1,218.89 -> 1,227.45 ms), and boot-to-ENTITY-enabled rises 359.41 -> 361.93 ms (1x1) and 1,248.26 -> 1,256.93 ms (8x8). Attribution run (`svc_dev.sh`, dev `cc204c6f` in a clean clone, the same environment and steps, 1x1 build and `all`, rc 0): dev's media digest is unchanged (`f4c978c5...`, the committed oracle's), and its trace now gives exactly the head's figures: AEM copy 332.45978 ms, boot-to-enabled 361.93119 ms, flash random read 447.3 KiB/s. So the timing drift is already on dev, from a change after dev's oracle was recorded; this adoption moves only the media digest. Receipts: `receipts/service-budget-dev-cc204c6f/`.

## Notes

- Item 4 is blocked on PR #842 (the page is not on dev). Text for it: `stricter-readings-gptp.patch` / `-section.md` here. Its last column moves from the pre-#100 state to the merged behaviour; the clockAccuracy row says per board.
- Interpretation recorded in TAKEN: an omitted `gptp.clock_accuracy` resolves to 0xFE (8.6.2.3 b): "not specified or unknown"), the value dev announces today; both AX7101 configs are the AX7101 board, so both state 0x22.
- Reserved and alternate-profile values (0x00-0x1F, 0x32-0xFD, 0xFF) are refused by the builder (1588-2008 7.6.2.5: "shall be taken from the enumeration in Table 6"; 8.6.2.3 names no other profile's range).
- `gptp_ax1x1_ucode.hex` (the physical `ax1x1gptp` leg) still runs the generator with `--mac --p1 --clk-hz` and no `--clock-accuracy`; its default is 0x22, which the AX7101 config now states, so its bytes do not move. It is left alone because PR #842 edits that line.
- `ci/image/command-table.json` is left as it stands: `scripts/ci_tool_inventory.py --check` already refuses on dev `cc204c6f` ("changed declared script 'sw/builder/endstation_builder.py'"), no PR gate runs it, and PR #842 edits that file.
- The docs audit's finding D0-053 (`scripts/docs_inventory.json`) quotes dev's AX7101 model ids as its audit-time measurement of an already-stale page; this adoption moves those ids. Left to #797's owners.
- No STOP condition is written in the issue. Physical calibration of the AX7101 oscillator (the 0x22 claim) is the maintainer's decision; nothing here measures it.
