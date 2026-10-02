[R433] NEGATIVE - exact head d81198c2001756fd84c353d93c312c133c5af66b

# [R433] Round R433-2: external re-review of PR #634 (issue #629, lane M2)

- Exact head: `d81198c2001756fd84c353d93c312c133c5af66b`, tree `4f0217ae46ef99d71a63bba26cee3da8fe827ebd`. That is eight commits on the round-1 head `57f4b742`, on dev `cdf49d1a28527562888f0a903de51b6b15b1244f`. Live dev was still `cdf49d1a` at 12:19Z.
- Reviewer role: cleared-context external independent reviewer. Round start: https://github.com/kebag-logic/milan-fpga/pull/634#issuecomment-5951642809.
- Verdict: **NEGATIVE**, on one MINOR finding (R433-2-F1, under Tests and Docs). The hosted `docs-check` is red at this exact head. Its step "Entity shape gate" (`scripts/check_entity_shape.py --self-test`) fails under GNU make 4.3 on the root suite's builder-written shape header. Everything else the delta touches was re-run or reproduced and is clean, including the capture re-measure: both 8x8 contract arms were reproduced bit-exactly.
- Every round-1 finding of mine (F1 to F4, R1 to R3) is closed at this head under its original severity. Every R432-1 finding is closed too. The retained suggestions keep their reasons, which are accepted. One new SUGGESTION is recorded.
- The verdict and ledger were written after an independent pass over the delta. The prior public findings (R433-1, R432-1) were read only after that pass, and they were then re-checked at this head. No round-2 report of any other reviewer was read.

## Contents

- [Scope reconstructed](#scope-reconstructed)
- [Findings](#findings)
- [Suggestions](#suggestions)
- [Delta items judged](#delta-items-judged)
- [Per-lens results](#per-lens-results)
- [Ledger](#ledger)
- [Prior public review findings](#prior-public-review-findings)
- [Real limits](#real-limits)
- [Pending manager duties](#pending-manager-duties)
- [Clone integrity](#clone-integrity)
- [Receipts](#receipts)

## Scope reconstructed

Sources, read in this order:

- AGENTS.md, then the issue #629 body;
- the lane M2 assignment (5942692103), the STOP (5946475441) and its ruling (5946491571), which accepts the eight deviations;
- the round-2 assignment (5946975634), the author's TAKEN (5946993512) and REVIEW READY (5951606845);
- the PR #634 body, including its Round 2 section;
- `docs/design/MEDIA_CLOCK_FOLLOWING.md` at the head;
- `git diff 57f4b742..d81198c2` (26 files) and `git diff cdf49d1a..d81198c2` for context;
- the public evidence: the author round-2 packet `review-evidence/629-m2-r1/author-r2` at archive `9423a7b1` (scripts, HANDOFF, receipts);
- the exact-head hosted check runs.

The eight ruled deviations are taken as ruled. Protocol-processor #141 landing first, then the parent pin bump, is the manager's merge-turn duty. It is not judged here.

## Findings

### R433-2-F1 - MINOR - Tests, Docs - the hosted `docs-check` "Entity shape gate" fails at the exact head under GNU make 4.3: the root suite's builder-written shape header is classified only by its unexpanded text

- **Where:**
  - `scripts/shape_consumer_inventory.py:80-83`, the `CLASSIFIED_CONSUMERS` entry `("tb/verilator/milan_dp_mclk/Makefile", "$(MCLK_GEN)/gen/adp_shape_defaults.svh")` added by `57f4b742`;
  - `tb/verilator/milan_dp_mclk/Makefile`, where `mclk-build` depends on `$(MCLK_HDR)`;
  - `scripts/shape_consumer_inventory.py:181-209` (`shape_prereqs_from_database`) and `:271-298` (`_frozen_prereq_findings`). The second path checks the database token against `CLASSIFIED_CONSUMERS` in its expanded form, `obj_mclk_aem/endstation_mclk/gen/adp_shape_defaults.svh`, so the classification above does not match it.
- **Evidence.**
  - **Hosted run.** Run 37002531093, job 110823266548 (`docs-check`), on head `d81198c2`, failed at step 51 "Entity shape gate": `[FAIL] I every shape-header consumer resolves: got ['tb/verilator/milan_dp_mclk/Makefile: obj_mclk_aem/endstation_mclk/gen/adp_shape_defaults.svh -> ... is outside the tracked tree and is not classified']`, `checks: 219 failures: 1` (`receipts/hosted_docs_check_entity_shape_failure_excerpt.txt`, `receipts/hosted_docs_check_steps_d81198c2.txt`, `receipts/hosted_checks_d81198c2.txt`).
  - **Local reproduction under a real GNU make 4.3**, built from the GNU tarball with sha256 `e05fdde4...e19`, in a pristine copy of the head: the same `[FAIL]`, rc 1. Under the host's make 4.4.1 the same gate passes, 219/0. The cause is the make version: under 4.4.1, `make -pqrR` lists no frozen shape prerequisite for this Makefile, and under 4.3 it lists the expanded token (`receipts/check_entity_shape_head_make43.log`, `receipts/check_entity_shape_head.log`, `receipts/make43_checks_script_run.log`).
  - **Introduced by this PR.** At a clean checkout of the base `cdf49d1a` the gate passes under make 4.3 (219/0). At the round-1 head `57f4b742` it fails the same way. At round 1 the hosted `docs-check` stopped at the earlier capture step, so this step never ran. The round-2 fix of that step exposed it.
  - **Achievable.** A disposable probe that also classifies the expanded token passes the gate under make 4.3 (219/0, same log). This is not a proposed patch.
  - **The published evidence over-claims.** The round-2 REVIEW READY and the PR body state that every gate and the docs gates exit 0, citing `check_entity_shape.py` 166/0 and a local replica of the `docs-check` gate steps. That was the plain mode under the host make. The hosted step runs `--self-test` under make 4.3.
- **Authority:** AGENTS.md section 7: required tests and gates pass at the head. The lane assignment's gates include `check_entity_shape.py` and the docs gates. `docs-check` is a hosted required context.
- **Impact:** a required hosted context is red at the head, so the merge bar cannot be met. No product behaviour is affected. The consumer really is builder-written and untracked, as the classification intends. The inventory guard simply cannot read it under the runner's make.
- **Required outcome:** the "Entity shape gate" (`check_entity_shape.py --self-test`) passes under GNU make 4.3 and under the newer make, with the root suite's builder-written header still classified with its reason, and no other consumer weakened. The round's evidence states which make ran the gate.
- **Verification:** `scripts/make43_checks.sh <checkout> <make-4.3 dir>` reports `gate rc=0` for both makes. The hosted `docs-check` succeeds at the new head.

## Suggestions

- **R433-2-S1 (Tests).** `hdl/ieee1722/crf/KL_aaf_clock_meter.sv:155-158` now documents `max_dev_ns_o` as "saturating at 65535; a level, cleared by an era start". Neither clause is graded:
  - two reviewer probes survive all 446 meter checks: `max_dev_not_cleared_at_era_start` and `max_dev_no_saturation` (`receipts/meter_probes.log`, `scripts/meter_probes.py`);
  - M1 runs its offsets in non-decreasing |ppm| order (0, ±10.64, ±50, ±100), so a stale maximum carried across eras reads the same;
  - the field is a bench diagnostic that the design's test plan does not grade beyond "equals the meter's", so this is optional.
  - One option: follow a +100 ppm era with a 0 ppm era and require a maximum of about 0, and plant one deviation above 65,535 ns.
  - The two other probes in the same run are caught: a `tu` edge clearing the held lock, and a `tu` edge pulsing `disrupt_p`.
- **Retained, reasons accepted:**
  - **R433-1-S1** (the #386 settle band keyed on `follow_sel_r` rather than `mga_sel_w`): changing it is a design change to the merged settle table, with its own re-validation.
  - **R433-1-S2**, render T30 part: T30's INTERNAL window is the aligner's pull-in, and T31 holds the settled two-sided bound (`tb/verilator/milan_dp_render/sim_tdm8_render.cpp:3018-3040`). The `sim_aclk` part was taken; see below.

## Delta items judged

1. **Saved-state capture re-measure. Verified.**
   - **Census.**
     - The harness now takes each row's census from the generated shape, through `nvm_shape.closed_record_census` (`scripts/nvm_shape.py:251-261`, `tb/verilator/nvm_capture_cpu/soc.py:96-103,184`, `run.py:58-66`).
     - The gate uses the same helper (`scripts/check_nvm_capture.py:40,78-84,95-104`).
     - `soc.py` builds its donor base through `milan_soc.binding_base()`. The gate independently re-derives the census from the configs and binds the receipt to it.
   - **The TX-trace hold** (`sim_main.cpp:62-91,190,193`) changes only stdout ordering.
   - **Gate.** `check_nvm_capture.py` passes, and its four named mutations each exit 1 (`receipts/check_nvm_capture.log`).
   - **Receipt identity.** The `harness_sha256` entries equal the head's harness files. The receipt's `tree` `c28595df` is `a2f17342`'s tree. Between `a2f17342` and `d81198c2` only docs, the README and the receipt changed. Every arm's min and max recompute from its rows. Every row has `ok=1`, the census 13,210 / 164 (8x8) or 3,290 / 54 (1x1), and traffic counters consistent with its arm (`receipts/receipt_vs_docs.log`).
   - **Independent re-run.**
     - The README recipe was re-run for both 8x8 contract arms (50 MHz, aligned edges, 16 captures, traffic ON and OFF), offline, in a user and network namespace, with the receipt's environment and Verilator 5.052 (`receipts/capture_rerun_8x8-50-{on,off}.log`).
     - Every one of the 32 captures equals the receipt row exactly: `sys_cycles`, byte and record census, mismatches, and (ON) the request, response and read counters.
     - The harness's own grading exits 0, and its maxima are 13.86484 ms (ON) and 13.69390 ms (OFF).
     - The CPU netlist, instrumented firmware, BIOS and gPTP microcode hashes equal the receipt's (`receipts/capture_rerun_compare.log`, `receipts/capture_rerun_identities.log`).
     - The OFF arm, where the round-2 harness defect split a row, graded cleanly.
   - **Docs.**
     - Sections 17, 18 and 20 of `SAVED_STATE_SNAPSHOT_OWNERSHIP.md` and the harness README carry exactly the receipt's figures: the 8x8 maximum 13.86484 ms, ratio 3.5341x, margin 10.63516 ms; 1x1 3.96728 ms; the 100 MHz point 10.42973 ms; the six table rows; the commit, tree, firmware and pin lines.
     - `SAVED_STATE_FASTCONNECT.md` 4.2, 8.1 and the commit table equal `check_nvm_record_space.py`'s output: 3,336 and 13,256 B; 54 and 164 records; top IDs 0xA6 and 0xEA; 14 and 52 pages; 3,072.13504 and 3,268.48384 ms; 52,280 B free; 57,352 B (`receipts/check_nvm_record_space.log`). Each derived figure was recomputed by hand.
2. **Root suite under GNU make 4.3. Verified.**
   - Under a real make 4.3 with the inherited `MAKEFLAGS=w`, the round-1 Makefile puts `make[1]: Entering directory ...` into the schemata's `verilator` command line, and the head's does not (`receipts/make43_nested_repro.log`, `receipts/make43_checks_script_run.log`).
   - `make -C tb/verilator/milan_dp_mclk` under make 4.3 ran the clean legs (A 55/55, B 50/50, C 32/32) and the campaign: 31/31, all 16 mutants caught, 430 s. The campaign process carried `MAKEFLAGS=w MAKELEVEL=1` (`receipts/milan_dp_mclk_make43.log`).
   - Hosted Verilator shard 2/5 succeeded at the head.
3. **The ratchet answers. Accepted as a fabric-internal port change.**
   - `KL_aaf_clock_meter` lives in the parent's `hdl/ieee1722/crf` and is instantiated only in `milan_datapath` and the two test wrappers. No processor-boundary port changed, and the gitlinks are unchanged.
   - `AAFM_STAT` is composed as `{max_dev_ns_w, status_w}` (`milan_datapath.sv:5675-5705`): the same bits as round 1's `status_o`. The no-meter branch still ties it to zero.
   - The root CSR leg reads `AAFM_STAT 0x000b0007` equal to the meter, with a largest deviation of 11 ns against 11.25 ns expected.
   - OOC area is unchanged: 574 LUT (16 LUTRAM), 636 FF, 0 RAMB, 0 DSP (`receipts/ooc_meter_head.log`).
   - `check_port_contracts.py` passes (hdl 217 <= 217), and so does `measure_naming.py --check` (95 recorded). Neither budget changed in the delta. At `57f4b742` both failed exactly as R432-1 F3 reported (`receipts/static_gates.log`).
4. **The new failing tests. Planted and re-run.**
   - **Root:**
     - mutant 15 ("`tu` taken from the `tv` net") is caught at the `--tu` leg;
     - mutant 16 (a listener change keeping the lock) is caught at `--silent`;
     - leg A's `[TU]` row and leg B's `[SWITCH-TIMEOUT]` row pass clean.
   - **My round-1 probe** `plant_tu_from_tv.sh`, unchanged, now fails leg A on three `tu` checks; legs B and C still pass (`receipts/round1_probe_tu_from_tv_*.log`).
   - **Meter:**
     - `make` ran 446/446 cases, the servo with the meter 6/6, and the campaign 33/33 (32 mutants, the six new ones each killed by their named check: M12, M7 ×2, M6, M4, M1) (`receipts/meter_suite.log`);
     - R432-1's `reviewer_meter_probes.py`, run unmodified (sha256 prefix `8a33265dfe22`) from the public archive, gave 15 of 15 CAUGHT (`receipts/prior_r432_1_meter_probes_rerun.log`).
   - The new checks match the design:
     - lock per era event: a `tu` edge and the bind edge keep the lock, and a listener change and entry clear it with no pulse (`MEDIA_CLOCK_FOLLOWING.md:960-993`);
     - a gap before lock breaks the settle run;
     - zero channels is refused;
     - the restart lands in the step's PDU slot for M3 at positions 1 to 15 and M12 (b) at positions 1 to 14.
5. **Docs fixes, taken RESIDUE, retained suggestions.** These were checked at the head:
   - the FR_NFR status row and the FR-CLK-04 PICS AAF-5 qualifier;
   - REGISTER_MAP `:1837-1839`;
   - the `obj_aclk` row naming `milan_dp_mclk` mutant 3;
   - the design page's Implementation notes (the VERSION ruling, the area row pointing to `ooc.sh` and the STOP, the new `tu` row);
   - the TIME_SYNC W2 row;
   - the TESTING rows;
   - the milan_dp_mclk README (sixteen mutants, three legs).
   - `sim_aclk`'s INTERNAL check is now two-sided (`|ppm| < 5`), and its run measures +0.8002 ppm and passes (`receipts/milan_dp_aclk.log`).
   - The docs gates pass with the pinned Markdown environment: `docs_check`, `check_doc_style`, `gen_toc --check` and `--verify-anchors`, `check_em_dash --base cdf49d1a`, `check_doc_paths`, `git diff --check cdf49d1a HEAD`, and the lint ratchet (90 <= 90) (`receipts/static_gates.log`).
6. **The shipping image, from the author's receipts.**
   - The timing summary reads WNS +0.065 ns, WHS +0.036 ns, WPWS +0.264 ns, 0 failing endpoints, "All user specified timing constraints are met".
   - All four sign-off corners report "No timing paths found" for negative slack. Route status shows 106,333 of 106,333 nets routed with 0 errors.
   - Placed utilization: Slice 15,834 of 15,850 (99.90 %), LUT 80.52 %. The meter is placed at 483 LUT and 630 FF.
   - Vivado v2026.1. The reports are dated 2026-10-02 11:29 to 11:52, after the last RTL commit.
   - The zero critical warnings and the clean #607 refusal check rest on the author's statement plus the published hashes of `vivado.log` and `alinx_ax7101_timing.rpt`. Those two files are not archived (see limits).

## Per-lens results

All five lenses were applied to the delta at `d81198c2`.

```text
[R433] PASS Conformance - FR_NFR.md:156,239; MEDIA_CLOCK_FOLLOWING.md:960-993,1453-1466; sim_mclk.cpp row_tu_edge/row_switch_past_the_timeout; capture receipt vs 24.5 ms - tu edge per IEEE 1722-2016 4.4.4.7 (history restart, no request), one request per switch (4.4.4.3), lock per era event as designed, 8x8 capture maximum 13.86484 ms <= 24.5 ms reproduced bit-exactly; no processor-boundary port change
[R433] PASS RTL - KL_aaf_clock_meter.sv:104-163,376-382 and milan_datapath.sv:5672-5712 at d81198c2 - port split is a pure re-wiring: AAFM_STAT bits identical, no-meter tie-off intact, wrappers re-bound, OOC 574 LUT / 636 FF unchanged, gitlinks unchanged
[R433] PASS Robustness - meter M4 (0 channels), M6 (gap before lock), M7 (listener change, entry, tu edge, bind edge), root [SWITCH-TIMEOUT] (talker silent past the 100 ms timeout), milan_dp_mclk Makefile under make 4.3 with inherited MAKEFLAGS=w, capture harness OFF arm with the trace hold - each run at d81198c2 and passing; the round-1 failure reproduced first
[R433] MINOR Tests - scripts/shape_consumer_inventory.py:80-83 - R433-2-F1 (hosted Entity shape gate red under make 4.3); otherwise meter 446/6/33, root 31/31 under make 4.3, R432-1 probes 15/15, capture gate and mutations, aclk two-sided check all verified
[R433] MINOR Docs - PR #634 body "How to validate" / REVIEW READY 5951606845 gate claims - R433-2-F1 (claims every gate exits 0; the hosted docs-check is red); every round-2 doc figure otherwise matches its receipt
```

## Ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #629 and round-2 assignment; FR_NFR FR-CLK-03/04 row and FR-CLK-04; design :960-993 and Implementation notes; root `[TU]` and `[SWITCH-TIMEOUT]` rows; meter M7 rows; capture receipt against the 24.5 ms contract, re-measured bit-exactly; gitlinks and boundary | R433-2 | `d81198c2001756fd84c353d93c312c133c5af66b` |
| RTL | CLEAN | `KL_aaf_clock_meter.sv` ports and `max_dev_ns_o`/`status_o` assigns; `milan_datapath.sv:5672-5712` composition and tie-off; both test wrappers; OOC area at head | R433-2 | `d81198c2001756fd84c353d93c312c133c5af66b` |
| Robustness | CLEAN | meter M4, M6 and M7 era and lock events; root silent-past-timeout switch; nested make under 4.3 (failure reproduced at `57f4b742`, clean at head); capture OFF arm with the trace hold | R433-2 | `d81198c2001756fd84c353d93c312c133c5af66b` |
| Tests | UNCLEAN (R433-2-F1) | meter suite 446 + 6 + 33; root campaign 31/31 under make 4.3; R432-1 probes 15/15; round-1 tu probe; reviewer meter probes; capture gate and four mutations; aclk; hosted check runs; `check_entity_shape.py --self-test` under make 4.3 and 4.4.1 | R433-2 | `d81198c2001756fd84c353d93c312c133c5af66b` |
| Docs | UNCLEAN (R433-2-F1) | SAVED_STATE_SNAPSHOT_OWNERSHIP 17/18/20 and FASTCONNECT 4.2/8.1/commit table against receipts; harness README; FR_NFR; REGISTER_MAP; TIME_SYNC; TESTING; design Implementation notes; milan_dp and milan_dp_mclk READMEs; docs gates; PR body Round 2 and gate claims | R433-2 | `d81198c2001756fd84c353d93c312c133c5af66b` |

## Prior public review findings

These were read after the independent pass, then re-checked at `d81198c2`.

| Finding (original severity) | State at this head | Evidence |
|---|---|---|
| R433-1-F1 (MINOR) `tu` from the `tv` net unplanted | CLOSED | root mutant 15 caught; the round-1 probe fails leg A on 3 `tu` checks |
| R433-1-F2 (MAJOR) capture receipt for the old census | CLOSED | re-measured; gate rc 0; both 8x8 contract arms reproduced bit-exactly |
| R433-1-F3 (MINOR) FR_NFR status row | CLOSED | `FR_NFR.md:156` "implemented and graded in simulation (#629, PR #634); bench acceptance open" |
| R433-1-F4 (MINOR) REGISTER_MAP 0x8E0 to 0x8F4 | CLOSED | `REGISTER_MAP.md:1837-1839` maps `AAFM_STAT` and `AAFM_RATE`; 0x8E8 to 0x8F4 unmapped |
| R433-1-R1, R2, R3 (RESIDUE) | CLOSED | design `:1456`, `:1463`; `TIME_SYNC.md:203` |
| R433-1-S1, S2 (SUGGESTION) | S1 retained; S2 taken for `sim_aclk`, retained for T30 | reasons accepted, above |
| R432-1-F1 (MAJOR) capture receipt | CLOSED | as R433-1-F2 |
| R432-1-F2 (MAJOR) root suite under make 4.3 | CLOSED | reproduced at `57f4b742`, clean at head; 31/31 under make 4.3; hosted shard 2/5 success |
| R432-1-F3 (MINOR) port-contract and naming ratchets | CLOSED | both pass with budgets unchanged; both fail at `57f4b742` |
| R432-1-F4 (MINOR) `tu` from the `tv` net | CLOSED | as R433-1-F1 |
| R432-1-F5 (MINOR) five meter probes | CLOSED | their `reviewer_meter_probes.py` 15/15 CAUGHT; (b) also fails at the root (mutant 16) |
| R432-1-F6 (MINOR) nonexistent script in the `obj_aclk` row | CLOSED | `tb/verilator/milan_dp/README.md:74` names `milan_dp_mclk` mutant 3, which exists and is caught |
| R432-1-F7 (MINOR) FR register status | CLOSED | as R433-1-F3 |
| R432-1-R1, R2, R4 (RESIDUE) | CLOSED | in tree |
| R432-1-R3 (RESIDUE) PR body | CLOSED | Status reads "GREEN after round 2"; Known limitations cite the ruling |
| R432-1-S1 (SUGGESTION) | retained | as R433-1-S1 |
| R432-1-S2 (SUGGESTION) | taken | FR-CLK-04 qualified |

Nothing in the verdict or ledger changed after this reading. R433-2-F1 is new. It was latent at `57f4b742`, where the hosted step never ran.

## Real limits

- **Image not rebuilt.** No Vivado run was made. The timing, utilization and sign-off figures come from the author's published reports. The critical-warning count and the #607 refusal check rest on the author's statement and the published `vivado.log` hash, because that log is not archived.
- **Capture arms re-run.** Only the two 8x8 50 MHz contract arms were re-run, and they hold the published contract maximum. The 1x1 arms and the non-contract 100 MHz arms are checked by the gate, by internal consistency and against the docs, not by simulation.
- **One interrupted run.** The first `milan_dp_mclk` run under make 4.3 received a SIGTERM from outside the suite 2 min 19 s in, after its clean build. Its log is kept as `receipts/milan_dp_mclk_make43_attempt1_terminated.log`. The complete re-run reused that clean build, and built the schemata through the nested make 4.3 path that F2 concerned.
- **Banks not re-run.** The full banks were not re-run: all shards, `test_builder.py`, the full `milan_dp`, `milan_dp_render`, `mmcm_servo` and `csr` suites, and Yosys `run.sh`. The manager's banks cover them.
- **Hosted contexts.** At 12:31Z, hosted Verilator shard 1/5 was still in progress, and "Physical gPTP" was skipped, which means not executed. The manager owns hosted and act acceptance.
- **Clause texts.** No standards text was re-opened. The clauses were applied as cited in the design and the PR.
- **No physical evidence.** No bench, hardware or physical calibration was run.
- **Receipt paths.** In the receipts, the home-directory prefix is written as `$HOME`.

## Pending manager duties

- R433-2-F1: a fix, then hosted `docs-check` at the new head. Re-review is needed for Tests and Docs only.
- Hosted Verilator shard 1/5 to completion. The act replica.
- The current-dev candidate at the merge turn. Protocol-processor #141 lands first, then the parent pin bump.
- The author's out-of-scope items, to be filed if wanted:
  - `milan_dp_render` and `pp_shadow` derive source lists with the same unguarded nested `make`;
  - `tb/verilator/fw_service_budget/oracle.json` keeps the pre-#629 image sizes in a fixture that no gate binds.
- The later bench lane for AAF and CRF following.

## Clone integrity

Every probe ran in disposable copies under the packet's `scratch/`. The review clone was never edited. Checked at the end (`receipts/clone_integrity.txt`):

- HEAD is `d81198c2001756fd84c353d93c312c133c5af66b`, tree `4f0217ae46ef99d71a63bba26cee3da8fe827ebd`;
- `git status --porcelain --ignored` is empty;
- the worktree equals the index, and the index equals HEAD;
- every index mode and blob equals `git ls-tree -r HEAD`;
- the gitlinks equal the base's: `external` efeb541a (not initialised), `gptp-processor` 5dce647a, `protocol-processor` b2db3a97, `third_party/verilog-axis` 48ff7a7e. Each initialised submodule is clean.

## Receipts

Listed in `MANIFEST.sha256`. The scripts take a checkout path.

- `scripts/receipt_vs_docs.py`: recomputes each arm from its rows and checks every published figure.
- `scripts/compare_capture_rows.py`: compares a re-run with the receipt's rows.
- `scripts/meter_probes.py`: the reviewer meter probes.
- `scripts/make43_checks.sh`: the nested-make check and the entity shape gate under make 4.3 and the host make.
- `scripts/plant_tu_from_tv.sh`: the round-1 probe, unchanged.
- `receipts/*`: the raw outputs named above.

R433-2 FINISHED
