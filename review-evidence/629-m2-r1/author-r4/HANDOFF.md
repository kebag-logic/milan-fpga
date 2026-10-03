# HANDOFF: lane M2 round 4 ([A512]), issue #629, PR #634

Status: REVIEW READY at `c12886486c1e4acf2003bfaba25db2a307446428` (one merge commit on `0b066b6e`; local, not pushed). One open finding for a ruling: F-A512-1 (a `gmstep-mutants --all` control this lane's round 1 disarmed; predates the merge; proven one-line fix not applied).

- Start head: `0b066b6e66df2a3ba3167805a6a591f8b96fa449` on `629-media-clock-impl`; commits added, none amended; local, not pushed.
- Merge source: live `dev` `1269cdafb4bb964c757baae0f0c5a932d43f540b` (PR #636, #635: processor pin `631eeb34`).
- Assignment: https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5964785948
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5964796154
- REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5966345440
- Reviews at the start head: R432-3 POSITIVE (PR #634 comment 5957678325), R433-3 POSITIVE (PR #634 comment 5957949217).

## Items

| # | Item | Commit | State |
|---|---|---|---|
| 1 | Merge dev `1269cdaf` (`--no-ff`), conflicts kept both sides, ratchets re-recorded through their generators, auto-merged files checked | `c12886486` | done |
| 2 | Shipping image rebuilt at the merge commit: WNS, WHS, LUT and slices against round 2, #607 check | (no tree change) | done: WNS +0.193 ns, WHS +0.024 ns, slices 99.89 %, #607 clean; no STOP |
| 3 | Re-measure: every CI shard and the docs gates under GNU make 4.3; capture gate; `milan_dp`, `milan_dp_mclk`, `aaf_clock_meter` with campaigns | (no tree change) | done: every hosted job green under make 4.3 (59/59 suites, 2,149,266 checks; 55/55 Yosys tops; docs-check 46/46 run steps); capture not owed (census and firmware unchanged); meter 36/36, root 31/31, `milan_dp` sweep campaigns 6/6 and 6/6, `crflic-mutants` 7/7, `gsi-mutants` 9/9; `gmstep-mutants --all` 21/22 (F-A512-1) |

## Item 1: the merge

Merge commit `c12886486c1e4acf2003bfaba25db2a307446428`, parents `0b066b6e` (lane) and `1269cdaf` (live dev), made with `git merge --no-ff --no-commit 1269cdaf`, resolved, then committed with a one-line subject. No rebase. Submodules: `protocol-processor` checked out at the merged gitlink `631eeb342ca1e3fa80e734077a56a943aee76ff1` (`git submodule update --init protocol-processor`, toplevel verified first); `gptp-processor` `5dce647a` and `third_party/verilog-axis` `48ff7a7e` unchanged; `external` not checked out, as before.

Against the lane parent the merge adds dev's 13 paths (+97 / -17): the gitlink, `hdl/milan/KL_pp_shadow.sv` (C6 tie-offs), the boundary diagram and its PNG manifest, `SUBMODULES.md`, `REGISTER_MAP.md:1020` (`ADP_IDX0`), `measure_test_evidence.py` (two dispositions), `rom_digests.tsv`, and the three resolved files below.

Conflicts, each kept on both sides:
- `CHANGELOG.md`: both sections, this lane's first (it lands on dev after #635): Contents rows `:11-12`, "Unreleased - AAF or CRF media-clock following" at `:40`, "Unreleased - processor pin 631eeb34" at `:88`, each section's text byte-identical to its parent's.
- `docs/design/MEDIA_CLOCK_FOLLOWING.md:7-13` (the only conflicting hunk): this lane's "Implemented by lane M2" status with #635's "then-pinned submodule commit `b2db3a97`", and one added sentence beside the implementation status: "Its processor part **landed at `631eeb34`** ([Protocol-processor changes](#protocol-processor-changes))." #635's "Status: landed at `631eeb34`" bullet auto-merged unchanged into "Protocol-processor changes" (`:1284-1292`).
- `scripts/naming.budget`: re-recorded by `python3 scripts/measure_naming.py --write-budget` at the merge (rc 0, "95 candidate(s)"). The generator's output is byte-identical to the lane parent's file: count line `95 candidate(s): gptp-processor 1, protocol-processor 22, superproject 72`. Dev's 96 / superproject 73 still counted the servo's `crf_rate_i`, which this lane removed.

Auto-merged files checked against both parents (the changed lines of each side's own delta equal the merge's delta against the other parent, compared as sorted +/- line sets): `docs/reference/REGISTER_MAP.md` (lane: the AAF meter rows and the A2-a slip-counter wording; dev: `ADP_IDX0[15:0]` at `:1020`) and `scripts/measure_test_evidence.py` (lane: the `aaf_clock_meter` and `milan_dp_mclk` dispositions; dev: `acmp_mutants.py` and `notify_mutants.py`). Both: equal on both sides.

Every pin-derived record re-run through its generator at the merge, before commit:

| Record | Generator | Result at the merge |
|---|---|---|
| `scripts/naming.budget` | `measure_naming.py --write-budget` | conflict resolved by it: equal to the lane parent's file |
| `scripts/port_docs.budget` | `check_port_contracts.py --write-budget` | **moved by the merge**: `:21` `ports per tree: hdl 1916` becomes `hdl 1940` (dev counted 1916 without this lane's 24 new ports; the lane parent's comment line was stale at `1902/124/1550`). Every ratchet number unchanged. Committed in the merge |
| `syn/yosys/rom_digests.tsv` | `(cd syn/yosys && ./ooc.sh --record-rom-digests)` | byte-identical (dev's `631eeb34` rows) |
| boundary diagram (`.svg`, `.drawio`, `.png`) | `docs/diagrams/submodule_boundaries.gen.py` | byte-identical |
| `scripts/py_idiom.budget`, `cpp_idiom.budget`, `sh_idiom.budget` | `check_{py,cpp,sh}_idiom.py --write-budget` | byte-identical |
| `scripts/lint.budget` | `lint_rtl.py` (write mode) | unchanged, "90 <= 90" |
| `scripts/test_evidence.budget`, `fail_fast.budget`, `hygiene.budget`, `sv_idiom.budget` | no generator | `--check` rc 0: test evidence 72 <= 77 (dev's figure; the #635 ruling keeps 77), fail fast 81 <= 84, hygiene PASS, sv idiom OK |
| saved-state capture receipt | `scripts/check_nvm_capture.py` | PASS: census and product firmware digest equal the receipt, so no re-measure (item 3) |

## Item 2: shipping image

Rebuilt at the merge commit `c12886486c1e4acf2003bfaba25db2a307446428` through the repository build path, alone (nothing else heavy ran during synthesis; the light replay jobs and `docs-check` ran during place and route): `TAG=a512m2c1288648 sw/litex/build.sh ax7101`, Vivado v2026.1, the recipe of round 2 (`synth_design -directive AreaOptimized_high`, `opt_design -directive ExploreArea`, `place_design -directive ExtraPostPlacementOpt`, `phys_opt_design -directive AggressiveExplore`, `route_design -directive AggressiveExplore`, post-route `phys_opt_design -directive AggressiveExplore`); design argv from `sw/builder/out/endstation_ax7101_1x1_tdm8/soc_params.json`, regenerated by `build.sh` from `configs/endstation_ax7101_1x1_tdm8.yaml`; pre-build entity-shape check PASS. Session 04:53:39 to 05:32:34. The tree was clean before and after.

| Figure | Merge `c1288648` (round 4) | Round 2 `d81198c2` | Delta |
|---|---|---|---|
| WNS / TNS | **+0.193 ns** / 0.000 (0 of 181,419 endpoints failing) | +0.065 ns / 0.000 (0 of 180,759) | +0.128 ns |
| WHS / THS | **+0.024 ns** / 0.000 (0 of 181,338) | +0.036 ns / 0.000 (0 of 180,678) | -0.012 ns |
| WPWS | +0.264 ns (0 of 64,207) | +0.264 ns | 0 |
| "All user specified timing constraints are met." | yes | yes | |
| Sign-off corners Slow 0C, Slow 85C, Fast 0C, Fast 85C | "No timing paths found" for negative slack at all four | the same | |
| Routing | 106,622 of 106,622 routable nets fully routed, 0 with routing errors | 106,333 of 106,333, 0 | |
| CRITICAL WARNING lines in `gateware/vivado.log` | 0 (the one text hit is the IOB-pack Tcl source echo, a `##` line) | 0 (the same echo) | |
| #607 constraint refusal | `[constraints] .../vivado.log: no 12-4739, 20-1307 or 12-5201 diagnostics`; the #607 pattern counts 0 lines; bitstream written, not quarantined | clean | |
| Slice LUTs | **50,767 (80.07 %)**: 48,535 logic, 2,232 memory | 51,051 (80.52 %): 48,858 logic, 2,193 memory | -284 (-0.45 pp) |
| Slice Registers | 59,634 (47.03 %) | 59,519 (46.94 %) | +115 |
| Slices | **15,832 of 15,850 (99.89 %)** | 15,834 (99.90 %) | -2 (-0.01 pp) |
| F7 / F8 muxes | 1,334 / 46 | 1,349 / - | |
| Block RAM tiles | 92.5 of 135 (68.52 %): 79 RAMB36, 27 RAMB18 | 92.5 (68.52 %) | 0 |
| DSPs | 14 of 240 (5.83 %) | 14 (5.83 %) | 0 |
| Bonded IOB | 109 of 285 (38.25 %) | 109 | 0 |
| Placed `protocol_processor_top` (`pp_shadow/u_pp`) | 23,335 LUT, 23,435 FF | 23,552 LUT, 23,310 FF | -217 LUT, +125 FF (the new pin) |
| Placed `KL_aaf_clock_meter` | 483 LUT (32 LUTRAM), 630 FF | 483, 630 | 0 |
| Placed `KL_mmcm_drp_servo` | 899 LUT, 814 FF | 897, 814 | +2 LUT |

No STOP condition: timing is met, placement and routing completed, and no resource exceeds 100 % (the fullest is slices at 99.89 %, 18 slices free).

Artifacts (not copied here; sizes and sha256): `alinx_ax7101.bit` 3,825,992 B `d2742a8652a114c65e1a352338efef570ad57bd708acd0788b0448b8204fc2ec`; `alinx_ax7101_timing.rpt` 1,319,622 B `757dd3bd8c8a3dccdcc9ed3ea92a55bee96562b2e78e5779eafe653518d7e7ef`; `vivado.log` 820,708 B `66e8d37605e383920aab1181cfcfbf1dca760d1fcb95b1f6ebf64da915d1f215`; `alinx_ax7101_utilization_place.rpt` 13,329 B `5918d8eead27000e17c669800f04251ad139af9f6f1154a72f71d65572a83e28`. Copies of the route status, placed utilization, hierarchical utilization, the four sign-off negative-slack reports and the timing summary excerpt are in `receipts/`.

## Item 3: re-measured inputs

### Saved-state capture: not re-measured (neither input moved)

`scripts/check_nvm_capture.py` at the merge: rc 0, all seven controls detected, "PASS: capture census, clocks, both timing arms and receipt agree". The inputs it compares, printed from its own `current_inputs()` at `c1288648`:
- census: 8x8 13,210 bytes / 164 records, 1x1 TDM8 3,290 bytes / 54 records, CPU 50 MHz configured and measured, sys 100 MHz: equal to `measurements.json` `measured_for`;
- product firmware `sw/firmware/milan_baremetal/milan_baremetal.c` sha256 `a73ecc25c77bfb7c4e1c2c711d72f0b560dd7e8d18cde92f40e67efcc84f0eb3`: equal to `product_firmware_sha256`.

The merge changes nothing under `sw/firmware/`, `tb/verilator/nvm_capture_cpu/`, `configs/`, `sw/builder/` or `avdecc/` against the lane parent. So the assignment's rule (re-measure only if the census or the firmware digest moved) does not trigger. The receipt's `processor_pins` (`b2db3a97`) is provenance. Stated for the reviewers: the capture SoC is the product SoC (`ProductSimulation(milan_soc.MilanSoC)`, `tb/verilator/nvm_capture_cpu/soc.py:63`), which elaborates `milan_datapath` with the processor, so the processor RTL in that simulation moved with the pin (10 processor `hdl/` files, +1,391 / -179); the processor's NVM path `hdl/packet_engine/` is byte-identical between `b2db3a97` and `631eeb34` (`git diff` empty). Round 2's measurement stands: 8x8 maximum 13.86484 ms against 24.5 ms.

### Hosted jobs replayed under GNU make 4.3

Method as round 3 (the driver, substitutes and sequences are in `scripts/`; adapted paths only): each job's steps are read from its workflow file and run verbatim with `bash -e`, the workflow, job and step env and the pull_request event's expressions resolved (base ref `dev`, recorded base oid `cdf49d1a`, frozen at PR open; the em-dash step derives its base from `origin/dev`, `1269cdaf`). A `make` shim first on PATH logs every invocation and execs GNU make 4.3, built here from the GNU tarball (sha256 `e05fdde47c5f7ca45cb697e973894ff4f5d79e13b750ed57d7b66d8defc78e19`). A fresh Python 3.12.13 venv stands in for the runner's `python3`; a scratch HOME per job family. Sequences: `light.sh` (05:06-05:07, during Vivado place and route), `docs.sh` (05:08-05:34), `shards.sh` (05:40-07:59, after the image), `yosys.sh` (05:34-05:57), `elaborate.sh` (05:37-05:57), then the `rtl-fast` aggregate.

| Job | Steps: verbatim (of them path-mapped) / substituted; actions; skipped by `if:` | make calls, all GNU make 4.3 | Result |
|---|---|---|---|
| docs.yml `docs-check` (docs-check) | 50: 43 (0) / 3; 4; 0 | 2,947 (19: 1, 25: 1,031, 26: 1,538, 31: 14, 50: 363) | rc 0, head `c1288648` |
| docs.yml `wire-accountability` (wire-accountability) | 3: 2 (0) / 0; 1; 0 | 0 | rc 0, head `c1288648` |
| docs.yml `docs-check-no-git` (docs-check-no-git) | 2: 0 (0) / 1; 1; 0 | 0 | rc 0, head `c1288648` |
| rtl.yml `full-ci-gate` (full-ci-gate) | 5: 4 (0) / 0; 1; 0 | 0 | rc 0, head `c1288648` |
| rtl.yml `verilator-shards` (vshard0) | 14: 5 (1) / 0; 3; 6 | 41 (13: 41) | rc 0, head `c1288648` |
| rtl.yml `verilator-shards` (vshard1) | 14: 6 (1) / 0; 3; 5 | 276 (12: 2, 13: 274) | rc 0, head `c1288648` |
| rtl.yml `verilator-shards` (vshard2) | 14: 5 (1) / 0; 3; 6 | 173 (13: 173) | rc 0, head `c1288648` |
| rtl.yml `verilator-shards` (vshard3) | 14: 5 (1) / 2; 4; 3 | 55 (13: 55) | rc 0, head `c1288648` |
| rtl.yml `verilator-shards` (vshard4) | 14: 5 (1) / 0; 3; 6 | 34 (13: 34) | rc 0, head `c1288648` |
| rtl.yml `verilator-suites` (verilator-suites) | 5: 3 (0) / 0; 2; 0 | 0 | rc 0, head `c1288648` |
| rtl-fast.yml `yosys-elaboration` (rf-yosys-elab) | 10: 5 (0) / 2; 2; 1 | 0 | rc 0, head `c1288648` |
| rtl.yml `yosys-shards` (yshard0) | 10: 3 (0) / 2; 4; 1 | 0 | rc 0, head `c1288648` |
| rtl.yml `yosys-shards` (yshard1) | 10: 3 (0) / 2; 4; 1 | 0 | rc 0, head `c1288648` |
| rtl.yml `yosys-shards` (yshard2) | 10: 3 (0) / 2; 4; 1 | 0 | rc 0, head `c1288648` |
| rtl.yml `yosys-shards` (yshard3) | 10: 3 (0) / 2; 4; 1 | 0 | rc 0, head `c1288648` |
| rtl.yml `yosys-portability` (yosys-portability) | 5: 3 (0) / 0; 2; 0 | 0 | rc 0, head `c1288648` |
| rtl-fast.yml `changes` (rf-changes) | 2: 1 (0) / 0; 1; 0 | 0 | rc 0, head `c1288648` |
| rtl-fast.yml `verilator-lint` (rf-lint) | 6: 3 (1) / 0; 2; 1 | 0 | rc 0, head `c1288648` |
| rtl-fast.yml `bdd-conformance` (rf-bdd) | 4: 3 (0) / 0; 1; 0 | 0 | rc 0, head `c1288648` |
| rtl-fast.yml `rtl-fast` (rf-aggregate) | 1: 1 (0) / 0; 0; 0 | 0 | rc 0, head `c1288648` |
| elaborate.yml `elaborate` (elaborate) | 20: 11 (1) / 1; 7; 1 | 1,540 (15: 1,538, 19: 2) | rc 0, head `c1288648` |

Tallies: Verilator shards 11/11 (401,934 checks), 23/23 (197,119), 12/12 (1,523,725), 12/12 (14,649), 1/1 (11,839); `verilator-suites` 59 suites, 2,149,266 checks, 0 failures, target SHA 5 of 5, equal to round 3's tally at `0b066b6e`. Yosys tops 1 + 1 + 27 + 26 = 55 of 55, structural gates and tied-input gate PASS, target SHA 4 of 4. `docs-check`: step 50 `check_entity_shape.py --self-test` 222/0 (363 make calls); step 26 builder gates `ALL GATES PASS EXCEPT 14 NOT RUN` (the LiteX arms; the hosted docs-check has no LiteX either); step 9 em-dash 0 findings over 538 added lines `[1269cdaf..HEAD]`; step 43 NOT RUN (AGENTS.md section 5), `scripts/act_ci.py` byte-identical to live dev `1269cdaf`. `elaborate`: step 15 `ALL GATES PASS EXCEPT 2 NOT RUN` (gate 1b's `MAKEFLAGS += -e` arm under make 4.3; gate 11 needs the Arty build tree), LiteX simulations 4/4. `bdd-conformance`: 404 scenarios, 1,968 steps. Lint 90 <= 90.

Disclosed deviations (each in its receipt):
- **PyYAML in the stand-in runner python.** The first `bdd-conformance` attempt (in `light.sh`) stopped at "endstation_builder: PyYAML required": the hosted image's `python3` ships PyYAML, my fresh venv did not. PyYAML 6.0.3 was installed into the venv as runner provisioning and the job re-run: rc 0 (`receipts/replay/light_sequence.first-bdd-attempt-rc1.log`).
- **Clean build state.** The first shard launch (05:34:56) was stopped at 05:40, during shard 0 (one suite done), because the sweep would have reused ignored `obj_*` products built at the previous pin. `git clean -fdX -- tb/verilator` removed only ignored build products (141 paths, listed first with `-n`), and the sequence was relaunched; every reported shard is from the relaunch (`receipts/replay/shards_sequence.cancelled-first-launch.log`).
- **CPU count.** 32 CPUs here against the runner's 4; `capture_coherence`'s campaign sizes its build pool by CPU affinity and ran 29 builds on 32 workers, peaking at the 12 GB memory cap with no OOM kill (`memory.events` `oom_kill 0` throughout).
- **`tsn_fuzz`** (shard 1, field campaigns run: tsn-gen built, no declared skip) rewrote the timestamp line of `hdl/ieee1722/avtp/doc/TEST_RESULTS.md` and `hdl/ieee8021as/gptp_plane/doc/TEST_RESULTS.md`; counts unchanged (164 and 677 pass). Both restored to HEAD (`receipts/replay/vshard1.tsn_fuzz_test_results_timestamp.diff`).
- Substitutes as round 3: diagram dependencies (presence check plus the workflow's pip line), sv2v (pinned zip and digest, into the replay's bin), Yosys (host 0.66 package, external ABC), `docs-check-no-git` in a `git archive` export, and `act_ci.py --selftest` NOT RUN. `physical-gptp` is skipped on a pull request, as hosted.


## Test rows and failing mutants

Round 4 adds and changes no test. Every campaign of the three named suites was re-run at the merge, inside the replayed shard under GNU make 4.3 from a clean build (copies: `receipts/replay/vshard2.aaf_clock_meter.log`, `vshard2.milan_dp_mclk.log`, `vshard4.milan_dp.log`).

`aaf_clock_meter` (shard 2): cases 465/0, servo 6/0, `mutants.py` **36/36 as required**: the clean control passes, and each of the 35 named mutants fails its named check:

| Mutant | Named check it fails |
|---|---|
| `decimation_by_1` | [M1 +0.00 ppm] rate_valid rises within 4.2 s and holds |
| `rate_over_512ms_E1` | [M2 rsign] every rate within 360 ns of the planted rate |
| `bound_2048_B1` | [M2 indep] no history restart |
| `first_pdu_pick_P1` | [M2 indep] every rate within 256 ns of the planted rate |
| `spacing_bound_16384_B3` | [M3 rsign1800] the error restarts the history |
| `within_group_void_removed` | [M3 indep2100] the error restarts the history |
| `stream_data_length_unchecked` | [M4 12-sample] does not lock |
| `continuity_without_wrap` | [M5] zero restarts across the sequence wraps |
| `timeout_disabled` | [M6] unlocks 100 ms after the last PDU |
| `no_restart_on_tu_edge` | [M7 tu edge] rate_valid falls at the event |
| `restart_on_any_loss` | [M8 indep 1 s] rate_valid from 4.1 s on and never falls |
| `snapshot_next_pick_less_2ms` | [M9] every rate equals the no-loss run within 1 LSB |
| `voided_snapshot_restarts` | [M9] no history restart |
| `multi_group_gap_accepted` | [M10 two losses in adjacent groups] restarts once |
| `gap_bound_4096` | [M11 a] +3,900 ns at +300 ppm, 5,100 ns from 4 ms: no restart |
| `gap_bound_scaled_with_k` | [M11 b] half sample at -300 ppm against +/-J, 6,365 ns off: one restart |
| `no_check_across_a_gap` | [M12 PDU 0 lost, step +20833 @1] restarts the history once |
| `listener_compare_ignored` | [M13 another listener] not measured |
| `no_reseed_at_era_start` | [M14 listener change to the opposite mr level] mr_toggle_p pulses |
| `era_lock_clear_on_disrupt` | [M14 listener change to the opposite mr level] disrupt_p pulses |
| `disrupt_tied_low` | [M14 100 ms of silence] disrupt_p pulses |
| `enable_tied_high` | [M14 enable low, talker 0 toggling its mr] mr_toggle_p pulses |
| `servo_with_meter_E1` | [S2 worst] every window's \|e\| under 1,024 ns after the first LOCKED |
| `servo_with_meter_restart_on_any_loss` | [S2 loss] the trim followed the 4 ppm step within 0.5 ppm |
| `held_lock_cleared_on_a_gap` | [S2] LOCKED never left after the first LOCKED |
| `deviation_verdict_deferred_to_pdu15` | [M12 PDU 15 lost, step +20833 @1] the deviation check restarts it at the step's PDU, before the gap |
| `listener_change_keeps_lock` | [M7 listener change] the held lock clears at the event |
| `gap_does_not_break_settle` | [M6 gap before lock] not locked at the gap PDU and 7 clean PDUs after it |
| `bind_edge_clears_lock` | [M7 bind edge] the held lock is kept through the event |
| `cpf_zero_accepted` | [M4 0 channels] does not lock |
| `max_dev_not_tracked` | [M1 +10.64 ppm] the largest deviation is the offset over 15 spacings |
| `max_dev_not_cleared_at_era_start` | [M1 max_dev, listener change] the new era's largest deviation reads 0 |
| `max_dev_no_saturation` | [M1 max_dev, step +65536 @5] reads min(\|step\|, 65,535) after it |
| `max_dev_includes_gap_pdus` | [M1 max_dev, a lost PDU] the PDU after the gap is no deviation |
| `switch_through_idle_W1` | [U16] the integrator is kept through the switch (trim unchanged) |

`milan_dp_mclk` (shard 2): legs 55/0, 32/0 and 50/0; `mclk_mutants.py` **31 checks: 31 PASS, 0 FAIL**: the schemata at id 0 pass every leg (15 controls), and each of the 16 named mutants is caught:

| Mutant | Leg | Named check it breaks |
|---|---|---|
| 1 the decode kept as the CRF-only compare | `--select` | AAF0: the servo leaves IDLE once the meter locks |
| 2 the reference mux stuck on KL_crf_rx | `--refmux` | AAF0: the trim holds until the meter's rate validates |
| 3 the aligner left disengaged at INTERNAL (no A2-a) | `--internal` | INTERNAL: the packet grid holds the physical grid's rate |
| 4 the one-cycle unlocked presentation removed (W2) | `--w2` | W2: the switch onto a locked CRF passes HOLDOVER |
| 5 no re-seed on a change of the followed listener | `--switch` | switch: no request pulse at any switch |
| 6 the meter's raw lock-fall edge wired as the disruption | `--switch` | switch: no request pulse at any switch |
| 7 the meter's enable tied high | `--dwell` | (iii) INTERNAL dwell: AAF0's mr toggle raises no request |
| 8 disrupt_p not ORed into the request | `--aafloss` | AAF loss: one request at the meter's timeout |
| 9 the echo ungated (the meter's listener compare ignored) | `--echo` | echo: the unfollowed AAF1's toggle raises no request |
| 10 C0's level (~tu only) | `--select` | C1: UNLOCKED moves at the switch onto AAF0 |
| 11 C2's level (the reference lock) | `--select` | C1: LOCKED holds until the servo reads LOCKED |
| 12 the meter's held lock cleared on a sequence gap | `--loss` | loss leg: the servo stays LOCKED through single lost PDUs |
| 13 the read-window terms missing | `--csr` | CSR: AAFM_STAT reads the meter's status word |
| 14 the decode table one source short (the previous shape's) | `--switch` | switch: AAF1 decodes as listener 1 and the meter follows it |
| 15 tu taken from the tv net (the CRF wiring) | `--tu` | tu: the followed talker's tu edge restarts the meter's history |
| 16 a change of the followed listener keeping a held lock | `--silent` | switch (iv): the meter's lock clears at the switch |

`milan_dp` (shard 4, alone): PASS, 11,839 checks, 0 failures, round 3's tally (legs include gmstep 104, notify 383, crflic 416, nxn 1,961, nxndv 1,961, nxn8 3,746, nxn4c 1,961, prune 33, media_aclk 193). [CLKSRC-WALK] and [CLKSRC-RANGE] all `ok` at the new pin: every listed index answers SUCCESS, reads back, decodes, drives the servo select and the meter's status word; index `clock_sources_count` and 0xFFFF answer BAD_ARGUMENTS carrying the current index (`receipts/replay/vshard4.milan_dp.excerpt.log`). The sweep's campaigns: `render_mutants.py` **6 checks: 6 PASS** (four render-law mutants caught, two clean controls); `gmstep_mutants.py` (default inventory) **6 checks: 6 PASS** (five controls caught, clean leg).

`milan_dp`'s three explicit campaigns, outside the sweep's deadline, run after shard 4 under GNU make 4.3 with the pinned 5.050 (`scripts/milan_dp_campaigns.sh`; `receipts/milan_dp_campaigns/`):

| Campaign | Result |
|---|---|
| `make -C tb/verilator/milan_dp crflic-mutants` | rc 0, **7 checks: 7 PASS**: the clean `obj_crflic` leg (416/0) and six licence mutants, each breaking its named check |
| `make -C tb/verilator/milan_dp gsi-mutants` | rc 0, **9 checks: 9 PASS**: the clean `obj_notify` leg (383/0) and eight [GSI] mutants planted in copies of the processor's `hdl/` at `631eeb34` and of the datapath, each breaking its named check |
| `make -C tb/verilator/milan_dp gmstep-mutants` (`--all`) | **rc 2, 22 checks: 21 PASS, 1 FAIL**: both clean legs pass and 19 controls are caught; the control "a PHC step suppresses a coincident CRF restart" SURVIVES. Finding F-A512-1 below |

### Finding F-A512-1 (Tests): a `gmstep_mutants.py --all` control no longer plants its defect

- **What.** The control appends ` & ~media_rebase_p_w` to `RESTART_TRIGGER`, the restart request's last line (`tb/verilator/milan_dp/gmstep_mutants.py:228-231`). At dev `cdf49d1a` that line closed a pure AND chain (`mcr_restart_p_w = crf_clk_selected_r & ((tkd_crflk_q_r & ~crf_locked_w) | crf_mr_toggle_p_w);`), so the AND suppressed the whole CRF restart. This lane's `94e718913` (round 1) made the request `(crf_clk_selected_r & (...)) | aafm_disrupt_p_w | aafm_mr_toggle_p_w;` (`hdl/milan/milan_datapath.sv:3229-3232`) and moved `RESTART_TRIGGER` to its last line (`gmstep_mutants.py:61-64`; `CRF_RESTART_TERMS` is `:66`). There `&` binds tighter than `|`, so the planted AND gates only `aafm_mr_toggle_p_w`; the CRF terms are untouched, the mutant is the clean design for this leg, and it survives.
- **Not the merge.** The merge changes neither `gmstep_mutants.py`, `milan_datapath.sv` nor `KL_media_clock_restart.sv` (`git diff --stat 0b066b6e c1288648` over them is empty). It is the lane's own since round 1. No hosted job runs it: the sweep runs `gmstep_mutants.py` without `--all` (six controls, all caught), and the control is `--all` only. So no earlier round's evidence covered it.
- **Impact.** The `--all` inventory reports a survivor and exits 1; the named check "coincident: a PHC step does not suppress the CRF restart" is still sound, but this PR leaves dev's control for it disarmed.
- **Proven fix (not applied: not a round 4 item).** Plant the same AND inside the selected-CRF term group: anchor `CRF_RESTART_TERMS`, replacement `CRF_RESTART_TERMS[:-1] + " & ~media_rebase_p_w)"`, giving `& ((tkd_crflk_q_r & ~crf_locked_w) | crf_mr_toggle_p_w) & ~media_rebase_p_w)`. `scripts/coincident_probe.py` runs the campaign's own `run_control` on both forms at `c1288648`, outside the tree: the published form SURVIVES; the fixed form is CAUGHT, breaking exactly "coincident: a PHC step does not suppress the CRF restart" (`receipts/milan_dp_campaigns/coincident_probe.log`). The tree was clean after.
- **Asked of the manager:** a ruling on taking the fix in this PR (recommended: it restores a dev control this PR disarmed; a one-line test change) or on its own Issue.

## Area against the design estimate

The merge changes no RTL of this lane's (`git diff 0b066b6e c1288648 -- hdl` touches only `hdl/milan/KL_pp_shadow.sv`, dev's C6 tie-offs). Re-measured at the merge anyway, `(cd syn/yosys && ./ooc.sh KL_aaf_clock_meter KL_mmcm_drp_servo)` (Yosys 0.66, `synth_xilinx -family xc7 -flatten`), rc 0 (`receipts/ooc_merge.log`):

| Block | LUT (LUTRAM) | FF | RAMB18 | DSP | CARRY4 | Design estimate | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| `KL_aaf_clock_meter` | 574 (16) | 636 | 0 | 0 | 102 | 380 to 580 LUT, 270 to 420 FF, 0 RAMB18 | unchanged since round 2: LUT inside, FF over (accepted, #629 STOP ruling item 8) |
| `KL_mmcm_drp_servo` | 865 | 792 | 0 | 1 | 150 | 871 LUT, 792 FF at the design base | unchanged |

Placed in the shipping image at the merge: meter 483 LUT (32 LUTRAM) / 630 FF, servo 899 LUT / 814 FF (item 2).

## Gates

All at the merge head `c12886486c1e4acf2003bfaba25db2a307446428`, from the physical `/data` worktree path, never piped, each to its own log (copies in `receipts/gates/` and `receipts/replay/`, home prefix written `$HOME`). The worktree was clean (`git status --porcelain` empty, submodules at their gitlinks) before and after every run, except the two `TEST_RESULTS.md` timestamp lines `tsn_fuzz` rewrites in shard 1 (restored to HEAD; counts unchanged; diff kept). Simulator: the pinned Verilator 5.050 (the replay maps `/opt/verilator` to a local 5.050 install).

| Gate | Command | Make | Result |
|---|---|---|---|
| Markdown gates (pinned md venv) | `docs_check.py`; `check_doc_style.py`; `gen_toc.py --check`; `gen_toc.py --verify-anchors`; `check_em_dash.py --base` `1269cdaf`, `cdf49d1a` and `0b066b6e`; `check_doc_paths.py` | none invoked | rc 0 each: 0 findings over 186 md files; 22 documents; 128 pages; 300 anchors; em-dash 0 findings over 538 / 606 / 73 added lines; 891 cited paths |
| `git diff --check` | worktree; `0b066b6e HEAD`; `1269cdaf HEAD`; `cdf49d1a HEAD` | none | rc 0 each |
| Ratchets and records | `lint_rtl.py --check`; `check_sv_idiom.py`; `check_hygiene.py --check`; `check_{py,cpp,sh}_idiom.py`; `measure_test_evidence.py --check`; `measure_naming.py --check`; `check_port_contracts.py`; `measure_fail_fast.py --check`; `check_rtl_source_lists.py`; `pp_srcs.py --check --selftest`; `check_baremetal_only.py --check`; `check_submodule_docs.py`; `submodule_boundaries.gen.py --check`; `check_entity_shape.py`; `check_feature_status.py --self-test`; `ci_scope.py --selftest` | none, or `make -pqrR` reads (host make) | rc 0 each: lint 90 <= 90; naming 95 recorded; test evidence 72 <= 77; fail fast 81 <= 84; port contracts 59 without a rationale, all recorded; 108 closure files, 4 of 4 lists; entity shape PASS |
| Capture gate | `check_nvm_capture.py` | none | rc 0: census and firmware equal the receipt, seven controls detected |
| OOC area | `syn/yosys/ooc.sh KL_aaf_clock_meter KL_mmcm_drp_servo` | none | rc 0: 574 / 636 and 865 / 792, unchanged |
| Shipping image | `TAG=a512m2c1288648 sw/litex/build.sh ax7101` | (Vivado) | WNS +0.193 ns, WHS +0.024 ns, 0 critical warnings, #607 clean, bitstream published |
| Hosted jobs, replayed | `scripts/run_job.sh <workflow> <job> <name>` per job (sequences `light.sh`, `docs.sh`, `shards.sh`, `yosys.sh`, `elaborate.sh`) | 4.3 (shim) | see "Hosted jobs replayed under GNU make 4.3" |

## Parent-visible changes

Round 4 writes no RTL, port, parameter, register, CSR, AEM, builder, configuration or generated-file change of its own. Its only own edits are the merge resolutions: the design page's header (`MEDIA_CLOCK_FOLLOWING.md:7-13`), the changelog's two sections side by side, and the port-contract ratchet's comment line re-recorded by its generator (`scripts/port_docs.budget:21`, `hdl 1940`).

What the merge brings from dev (PR #636, already reviewed there) and is now part of this PR's merge result:
- `protocol-processor` gitlink `b2db3a97` -> `631eeb34`. `protocol_processor_top` gains input `identify_button_i` and parameter `EN_IDENTIFY_NOTIF_P` (default 0); `hdl/milan/KL_pp_shadow.sv` ties both to 0 with their `//!` rationales. No other processor top port or parameter changes.
- The processor behaviours #636 lists (C2 to C6, P141): the AECP deadline answer, hazard-class serialization, the locked-refusal values, GET_AUDIO_MAP 63 to 71 records, READ_DESCRIPTOR current values, the ADPDU configuration index after SET_CONFIGURATION, the 84-byte unsolicited SET_STREAM_INFO; P141's SET/GET_CLOCK_SOURCE tests over ten sources for #629.
- Records: ROM digest ledger rows for `631eeb34`; the boundary diagram; `SUBMODULES.md`; `REGISTER_MAP.md:1020` (`ADP_IDX0`); two test-evidence dispositions.

No processor-boundary port change by this lane, no top-level port change, no protocol-processor edit. VERSION stays `0x0002_0060`.

## Observations outside the round 4 items (for the manager)

- **F-A512-1** (above, in "Test rows and failing mutants"): the one open item; a ruling on taking its proven fix in this PR is asked.
- **Open RESIDUE R432-3-R1 = R433-3-R1** (not a round 4 item): `docs/design/MEDIA_CLOCK_FOLLOWING.md:1000-1001` at the merge, "The last two are the bench's measurement of a talker's timestamp regularity." Both reviews give the exact replacement ("The history-restart count and the largest deviation are the bench's measurement of a talker's timestamp regularity.") and carry it to the residue checklist. Not taken here.
- **Wording drift in this lane's own record**: `scripts/measure_test_evidence.py:681` says the `milan_dp_mclk` campaign plants "the #629 design's fourteen named root defects"; since round 2 it plants sixteen (15 and 16 added). Wording only; the ratchet keys the entry by path.
- **R432-3-S1 = R433-3-S1** (the entity shape gate's database read counts a parse stopped by `$(error)` as readable): unchanged, the manager's to file, as both reviews say.
- **Replay host vs runner**: 32 CPUs here, 4 on the runner. `capture_coherence`'s campaign sizes its pool by CPU affinity and ran 29 builds on 32 workers, which touched this service's 12 GB cap (no OOM kill). A local replay on a capped unit may want a narrower affinity for that suite.

## Receipts and scripts in this directory

- `receipts/`: the image's route status, placed and hierarchical utilization, the four sign-off negative-slack reports, the timing summary excerpt and the launch tail (`[constraints]` line); `ooc_merge.log`; `capture_inputs_merge.txt`; the merge-time generator runs (`merge_*`).
- `receipts/gates/`: every gate log at the merge (`head_*`, the Markdown gates `md_head_*`, the pre-commit ratchet runs `pre_*` and generator writes `write_*`), and `head_entity_shape_selftest_host.log` (222/0 under GNU Make 4.4.1).
- `receipts/replay/`: every replayed job's driver log, `summary.json` and make calls per step; the key step logs (docs-check steps 9, 25, 26, 43, 50; elaborate 15 and 19; the shard steps; the aggregates); the meter and root suite logs from shard 2; the `milan_dp` excerpt from shard 4 (the full log's size and sha256 head it); the `tsn_fuzz` timestamp diff; the first light sequence (bdd rc 1 before PyYAML) and the cancelled first shard launch.
- `receipts/milan_dp_campaigns/`: `crflic-mutants`, `gsi-mutants`, `gmstep-mutants` and the F-A512-1 probe.
- `scripts/`: `replay_workflow.py` (round 3's driver, the make 4.3 path changed), `replay_subst.json` (unchanged), `run_job.sh`, the sequences `light.sh`, `docs.sh`, `shards.sh`, `yosys.sh`, `elaborate.sh`, `milan_dp_campaigns.sh`, `collect_receipts.sh`, `tabulate_replay.py` and `coincident_probe.py`. They run from the scratch directory `$VALIDATION_STORAGE/629-a512/` (make 4.3 build, venvs, scratch HOMEs, full logs), which is outside the tree and this directory.
- Every file here is under 200 KB; the home-directory prefix in receipts is written `$HOME`.
